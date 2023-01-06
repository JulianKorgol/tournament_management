import axios from "axios";


const get = async (url, data) => {
    return await axios.get("http://localhost:8000/" + url, data)
}


const post = async (url, data) => {
    return await axios.post("http://localhost:8000/" + url, data)
}

export { get, post };