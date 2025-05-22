import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import NotePage from "../pages/NotePage"; // 노트 페이지 import
import ScrapbookPage from "@/pages/ScrapbookPage";  //스크랩 페이지
import DashboardPage from "@/pages/DashboardPage"; // 대시보드 페이지 import
export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>홈입니다</div>} />
        <Route path="/login" element={<Login />} />
        <Route path="/users/notes" element={<NotePage />} />
        <Route path="/users/scraps" element={<ScrapbookPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </Router>
  );
}
