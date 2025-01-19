import { useEffect, useState } from "react";
import {sendImage} from "./Api.js";
import {useNavigate} from 'react-router-dom';

const MainPage = () => {
    const [imageData, setImageData] = useState(null);
    const [caption, setCaption] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const nav = useNavigate();

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setImageData(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImageUrl(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    async function getCaption(){
        setLoading(true);
        try{
            const response = await sendImage(imageData);
            setCaption(response.blip_caption);
            console.log('IMAGE', imageUrl);
            nav('/caption', {state: {blip_caption: response.blip_caption, our_caption: response.captionize_caption, final_caption: response.final_caption, imageUrl}});
        }
        catch(error){
            console.error(error);
    }
    setLoading(false);
}

    return(
        <div>
        {loading ? (
            <div class='py-64 flex flex-column space-x-2 justify-center items-center'>
  	<div class='h-4 w-4 bg-white rounded-full animate-bounce [animation-delay:-0.3s]'></div>
	<div class='h-4 w-4 bg-white rounded-full animate-bounce [animation-delay:-0.15s]'></div>
	<div class='h-4 w-4 bg-white rounded-full animate-bounce'></div>
</div>
        ) :
    (    <div className="flex flex-col items-center space-y-4 m-5">
        <h1 className="text-balance text-2xl text-gray-400 max-w-112 py-12">
        Just upload an image and click the upload button to get your perfect captions!
    </h1>
    <input id="fileInput" className="hidden" type="file" accept="image/*" onChange={handleImageChange}></input>
    <label
                    htmlFor="fileInput"
                    className="bg-transparent text-sm/6 font-semibold cursor-pointer text-white">
                    Click to choose file
                </label>
        {imageUrl&&<img src={imageUrl} alt="image" className="h-[30rem] w-fit py-2"/>}
        {imageUrl&&<button className="rounded-md bg-purple-700 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-purple-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" onClick={getCaption}>Upload</button>}
        {/* {caption && <div className="text-balance text-2xl text-gray-400 max-w-96 py-12">{caption}</div>} */}
    </div>)    
    }
        </div>
    );
}
export default MainPage;