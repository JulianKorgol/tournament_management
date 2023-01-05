import axios from "axios";


const post = async (url, data) => {
    return await axios.post("http://localhost:8000/" + url, data)
}

export { post };