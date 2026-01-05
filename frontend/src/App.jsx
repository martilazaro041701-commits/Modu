import { BrowserRouter as Router, Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import ApiStatus from "./pages/ApiStatus";

export default function App() {
  return (
    <Router>
      <main className="page">
        <nav className="nav">
          <div className="logo">BARK</div>
          <div className="links">
            <Link to="/">Home</Link>
            <Link to="/status">API Status</Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/status" element={<ApiStatus />} />
        </Routes>
      </main>
    </Router>
  );
}
