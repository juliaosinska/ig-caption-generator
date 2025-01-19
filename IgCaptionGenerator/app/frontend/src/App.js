import './App.css';
import './MainPage';
import MainPage from './MainPage';
import Navbar from './Navbar';
import HomePage from './HomePage';
import CaptionPage from './CaptionPage';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';

function App() {
  return (
    <Router>
    <div className="App">
      <Navbar />
      <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/upload" element={<MainPage />} />
      <Route path="/caption" element={<CaptionPage />} />
      </Routes>
    </div>
    </Router>
  );
}

export default App;
