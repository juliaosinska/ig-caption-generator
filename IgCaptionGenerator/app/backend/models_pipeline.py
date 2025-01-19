import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications import InceptionV3
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer

def load_captionize_model(model_path):
    return load_model(model_path)

our_tokenizer = load_tokenizer("C:\\Users\\sonia\\Desktop\\ig-caption-gen\\src\\tokenizer.pickle")
our_model = load_captionize_model("C:\\Users\\sonia\\Desktop\\ig-caption-gen\\src\\models\\caption_model12.keras")

# blip model load
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# blip caption generation
def generate_blip_caption(image):
    inputs = blip_processor(images=image, return_tensors="pt")
    pixel_values = inputs.pixel_values

    with torch.no_grad():
        generated_ids = blip_model.generate(pixel_values)
        blip_caption = blip_processor.decode(generated_ids[0], skip_special_tokens=True)
    
    return blip_caption

# our model load
def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer

def load_captionize_model(model_path):
    return load_model(model_path)

# our model caption generation
model_incep = InceptionV3(weights='imagenet', include_top=False)

def extract_features(image):
    img_array = img_to_array(image.resize((299, 299)))
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model_incep.predict(img_array)
    return features

def top_k_sampling(predictions, k=5, unk_token='<unk>'):
    unk_index = our_tokenizer.word_index.get(unk_token, None)
    if unk_index is not None:
        predictions[unk_index] = 0 

    k = min(k, len(predictions))
    top_k_indices = np.argsort(predictions)[-k:]
    top_k_probs = predictions[top_k_indices]
    top_k_probs = top_k_probs / np.sum(top_k_probs)
    chosen_index = np.random.choice(top_k_indices, p=top_k_probs)
    return chosen_index

def generate_caption(our_model, our_tokenizer, photo, max_length, k=5):
    start_token = '<start>'
    end_token = '<end>'
    in_text = start_token
    for _ in range(max_length):
        sequence = our_tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        predictions = our_model.predict([photo, sequence], verbose=0)[0]
        
        prediction = top_k_sampling(predictions, k)
        word = our_tokenizer.index_word.get(prediction, None)

        if word == end_token and in_text == start_token:
            continue
        if word == in_text[-1]:
            break
        if word is None:
            break
        in_text += ' ' + word
        if word == end_token:
            break
        
    return in_text

def generate_captionize_caption(image):
    captionize_image = extract_features(image)
    captionize_caption = generate_caption(our_model, our_tokenizer, captionize_image, 60)
    return captionize_caption

# qwen model load
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
qwen_model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")
qwen_tokenizer = AutoTokenizer.from_pretrained(model_name)

# final caption generation
def generate_combined_caption(blip_caption, our_caption):
    our_caption_cleaned = our_caption.replace("<start>", "").replace("<end>", "").strip()

    prompt = f"""
    Combine the following two captions into a single, catchy, Instagram-worthy caption, without emojis and without hashtags. Make sure to use both captions:

    Caption 1: {blip_caption}
    Caption 2: {our_caption_cleaned}
    """

    messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
    ]

    text = qwen_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = qwen_tokenizer([text], return_tensors="pt").to(qwen_model.device)

    generated_ids = qwen_model.generate(**model_inputs, max_new_tokens=50)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]

    response = qwen_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

# putting pipeline together
def process_image_and_generate_caption(image):
    blip_caption = generate_blip_caption(image)
    captionize_caption = generate_captionize_caption(image)
    final_caption = generate_combined_caption(blip_caption, captionize_caption)
    return blip_caption, captionize_caption, final_caption