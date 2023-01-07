import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import AppContext from "./functions/AppContext/AppContext";
import User from "./functions/UserContext/UserContext";
import "./App.css";
import Menu from "./components/Menu/Menu";
import Footer from "./components/Footer/Footer";
import NotFoundView from "./views/NotFoundView/NotFoundView";
import IndexView from "./views/IndexView/IndexView";
import LoginView from "./views/LoginView/LoginView";
import ScreenLoader from "./functions/ScreenLoader/ScreenLoader"


function App() {
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState(null);


    return (
        <div className="App">
            <AppContext.Provider value={{ loading, setLoading }}>
                <User.Provider value={{ user, setUser }}>
                    {loading ? <ScreenLoader /> : null}
                    <Menu />
                    <BrowserRouter>
                        <Routes>
                            <Route path="/" element={<IndexView />} />
                            <Route path="/login" element={<LoginView />} />
                            <Route path="*" element={<NotFoundView />} />
                        </Routes>
                    </BrowserRouter>
                    <Footer />
                </User.Provider>
            </AppContext.Provider>
        </div>
    );
}

export default App;
