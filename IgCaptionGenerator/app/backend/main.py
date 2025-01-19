from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import sys
import io

sys.path.append("C:\\Users\\sonia\\Desktop\\ig-caption-gen\\src\\pipeline")
try:
    from models_pipeline import process_image_and_generate_caption
    print("Successfully imported process_image_and_generate_caption")
except ImportError as e:
    print(f"Error importing models_pipeline: {e}")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    blip_caption, captionize_caption, final_caption = process_image_and_generate_caption(image)
    captionize_caption = captionize_caption.replace("<start>", "").replace("<end>", "").strip()
    
    return {
        "blip_caption": blip_caption,
        "captionize_caption": captionize_caption,
        "final_caption": final_caption
    }


