import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import NotePage from "../pages/NotePage"; // 노트 페이지 import
import SignupCompletePage from "@/pages/SignupCompletePage";
import SignupPage from "@/pages/SignupPage";
import TodayIssuePage from "@/pages/TodayIssuePage";
import ClusterDetailPage from "@/pages/ClusterDetailPage";
import HomePage from "@/pages/HomePage";

import ScrapbookPage from "@/pages/ScrapbookPage";  //스크랩 페이지
import DashboardPage from "@/pages/DashboardPage"; // 대시보드 페이지 import
import KeywordDetailPage from "@/pages/KeywordDetailPage"; // 지식맵 키워드 상세 페이지 
import TrendRoutes from "./TrendRoutes";
import Header from "@/components/Header";
import NoteCreatePage from "@/pages/NoteCreatePage";
import NoteEditPage from "@/pages/NoteEditPage";

export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/users/notes" element={<NotePage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/signup/complete" element={<SignupCompletePage />} />
        <Route path="/today/issue" element={<TodayIssuePage />} />
        <Route path="/clusters/:clusterId" element={<ClusterDetailPage />} />
        <Route path="/users/scraps" element={<ScrapbookPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/keywords/:keywordId" element={<KeywordDetailPage />} />
        <Route path="/trend/*" element={<TrendRoutes />} />
        <Route path="/note/new" element={<NoteCreatePage />} />
        <Route path="/note/:noteId/edit" element={<NoteEditPage />} />
      </Routes>
    </Router>
  );
}
