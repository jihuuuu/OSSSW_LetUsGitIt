import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";

export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<div>홈입니다</div>} />
      </Routes>
    </Router>
  );
}