import { useLocation } from 'react-router-dom';

const CaptionPage = () => {
    const location = useLocation();
    const { blip_caption, our_caption, final_caption, imageUrl } = location.state || {};
    console.log(imageUrl);

    return(
        <div>
    <div className="flex flex-col items-center space-y-4 m-5">
    <h1 className="text-2xl text-gray-400 max-w-96 ">
        Here are your 3 captions
    </h1>
    <div className='flex flex-row space-x-6 bg-[rgb(80,80,80)] px-12 py-4 border border-none rounded-lg'>
        {<img src={imageUrl} alt="image" className="h-[30rem] w-fit py-2"/>}
        <div className="flex flex-col space-y-4">
        {<div className="bg-transparent px-6 py-1 text-2xl text-white max-w-96 text-center">{blip_caption}</div>}
        {<div className="bg-transparent px-6 py-1 text-2xl text-white max-w-96 text-center">{our_caption}</div>}
        {<div className="bg-transparent px-6 py-1 text-2xl text-white max-w-96 text-center">{final_caption}</div>}
    </div>
    </div>
    </div>
    </div>
    );
}
export default CaptionPage;