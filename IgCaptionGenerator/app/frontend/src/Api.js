import axios from 'axios';

const baseUrl = 'http://localhost:8000';

const sendImage = async (imageData) =>{
    const formData = new FormData();
    formData.append('file', imageData);

    try{
        const response = await axios.post(`${baseUrl}/predict`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        console.log(response.data);
        return response.data;
    }
    catch(error){
        console.error(error);
    }
}

export {sendImage};
