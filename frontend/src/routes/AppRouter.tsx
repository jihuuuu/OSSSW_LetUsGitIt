import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import NotePage from "../pages/NotePage"; // 노트 페이지 import
import SignupCompletePage from "@/pages/SignupCompletePage";
import SignupPage from "@/pages/SignupPage";
import TodayIssuePage from "@/pages/TodayIssuePage";
import ClusterDetailPage from "@/pages/ClusterDetailPage";

import ScrapbookPage from "@/pages/ScrapbookPage";  //스크랩 페이지
import DashboardPage from "@/pages/DashboardPage"; // 대시보드 페이지 import
export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>홈입니다</div>} />
        <Route path="/login" element={<Login />} />
        <Route path="/users/notes" element={<NotePage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/signup/complete" element={<SignupCompletePage />} />
        <Route path="/today/issue" element={<TodayIssuePage />} />
        <Route path="/cluster/:clusterId" element={<ClusterDetailPage />} />
        <Route path="/users/scraps" element={<ScrapbookPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </Router>
  );
}
