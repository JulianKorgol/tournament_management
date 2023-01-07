import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import AppContext from "./functions/AppContext/AppContext";
import User from "./functions/UserContext/UserContext";
import "./App.css";
import {get} from "./functions/Requests/Requests";
import Menu from "./components/Menu/Menu";
import Footer from "./components/Footer/Footer";
import NotFoundView from "./views/NotFoundView/NotFoundView";
import IndexView from "./views/IndexView/IndexView";
import LoginView from "./views/LoginView/LoginView";
import ScreenLoader from "./functions/ScreenLoader/ScreenLoader"
import PanelView from "./views/PanelView/PanelView";
import TournamentView from "./views/TournamentView/TournamentView";
import Toast from "./functions/Toast/Toast";


function App() {
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState({});
    const [open, setOpen] = useState(false);
    const [message, setMessage] = useState("");
    const [status, setStatus] = useState("success");

    const checkLogin = async () => {
        const response = await get("me/", { withCredentials: true }).catch(err => err.response);
        if (response.status === 200) {
            setUser(response.data.account);
            return true;
        }
        return false;
    }

    const MakeToast = (message, status) => {
        setMessage(message);
        setStatus(status);
        setOpen(true);
        setTimeout(() => {
            setOpen(false);
        }, 6000);
    }

    const refreshPage = () => {
        window.location.reload();
    }

    return (
        <div className="App">
            <AppContext.Provider value={{ loading, setLoading, MakeToast, refreshPage }}>
                <User.Provider value={{ user, checkLogin }}>
                    {loading ? <ScreenLoader /> : null}
                    <Menu />
                    <BrowserRouter>
                        <Routes>
                            <Route path="/" element={<IndexView />} />
                            <Route path="/login" element={<LoginView />} />
                            <Route path="/panel" element={<PanelView />} />
                            <Route path="/tournament/:uuid" element={<TournamentView />} />
                            <Route path="/tournament/:uuid/addpeople" element={<TournamentView />} />
                            <Route path="*" element={<NotFoundView />} />
                        </Routes>
                    </BrowserRouter>
                    <Footer />
                    {open ? <Toast message={message} status={status} /> : null}
                </User.Provider>
            </AppContext.Provider>
        </div>
    );
}

export default App;
