import { BrowserRouter, Routes, Route } from 'react-router-dom';
import "./App.css";
import Menu from "./components/Menu/Menu";
import Footer from "./components/Footer/Footer";
import NotFoundView from "./views/NotFoundView/NotFoundView";
import IndexView from "./views/IndexView/IndexView";
import LoginView from "./views/LoginView/LoginView";


function App() {
  return (
    <div className="App">
        <Menu />
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<IndexView />} />
                <Route path="/login" element={<LoginView />} />
                <Route path="*" element={<NotFoundView />} />
            </Routes>
        </BrowserRouter>
        <Footer />
    </div>
  );
}

export default App;
