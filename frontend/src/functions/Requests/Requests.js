import axios from "axios";


const post = async (url, data) => {
    const response = await axios.post("http://localhost:5000/" + url, data);
    return response;
}

export { post };