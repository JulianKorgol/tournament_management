import React from "react";
import axios from "axios";
import Cookies from "js-cookie";


const get = async (url, data) => {
    return await axios.get("http://localhost:8000/" + url, data)
}


const post = async (url, data, options) => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    return await axios.post("http://localhost:8000/" + url, data, options)
}

export { get, post };