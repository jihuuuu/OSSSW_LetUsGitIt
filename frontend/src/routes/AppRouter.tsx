import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import NotePage from "../pages/NotePage"; // 노트 페이지 import
import SignupCompletePage from "@/pages/SignupCompletePage";
import SignupPage from "@/pages/SignupPage";
import TodayIssuePage from "@/pages/TodayIssuePage";
import ClusterDetailPage from "@/pages/ClusterDetailPage";
import HomePage from "@/pages/HomePage";

import ScrapbookPage from "@/pages/ScrapbookPage";  //스크랩 페이지
import DashboardPage from "@/pages/DashboardPage"; // 대시보드 페이지 import
import NoteEditSheetPage from "@/pages/NoteEditPage";
import KeywordDetailPage from "@/pages/KeywordDetailPage"; // 지식맵 키워드 상세 페이지 
import TrendRoutes from "./TrendRoutes";
import Header from "@/components/Header";
import NoteCreatePage from "@/pages/NoteCreatePage";
import NoteEditPage from "@/pages/NoteEditPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      {/* 👇 여기에서 배경/블러 효과도 가능 */}
      <div className="relative min-h-screen bg-[#f5f8ff] font-inter overflow-hidden">
        {/* 블러 배경 */}
        <div className="absolute -top-32 -left-32 w-[600px] h-[600px] bg-gradient-to-br from-blue-400 via-purple-400 to-pink-400 opacity-30 blur-3xl rounded-full z-0" />
        <div className="absolute top-20 right-0 w-[500px] h-[500px] bg-gradient-to-bl from-cyan-400 via-blue-500 to-purple-500 opacity-30 blur-2xl rounded-full z-0" />
        {/* 실제 콘텐츠 라우팅 */}
        <div className="relative z-10">
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
            <Route path="/users/notes/:noteId" element={<NoteEditSheetPage />} />
            <Route path="/keywords/:keywordId" element={<KeywordDetailPage />} />
            <Route path="/note/new" element={<NoteCreatePage />} />
            <Route path="/note/:noteId/edit" element={<NoteEditPage />} />
            {/* 헤더 컴포넌트 추가 */}
            <Route path="/trend/*" element={<TrendRoutes />} />
            <Route path="/note/new" element={<NoteCreatePage />} />
            <Route path="/note/:noteId/edit" element={<NoteEditPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
