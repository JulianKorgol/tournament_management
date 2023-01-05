import { BrowserRouter, Routes, Route } from 'react-router-dom';
import IndexView from "./views/IndexView/IndexView";


function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
            <Route path="/" element={<IndexView />} />
        </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
