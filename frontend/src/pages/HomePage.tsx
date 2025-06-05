// src/pages/HomePage.tsx
import TodayIssuePreview from "@/components/card/TodayIssueCard";
import WeeklyIssuePreview from "@/components/card/WeeklyIssueCard";
import {TodayKeywordPreview} from "@/components/card/TodayKeywordCard"; // ★ 추가
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";

export default function HomePage() {
  return (
    <div className="min-h-screen px-10 py-8">
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="absolute left-6 top-1/2 transform -translate-y-1/2">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto"></h1>
        <div className="px-2 py-1">
          <Header />
        </div>
      </header>

      <div className="flex justify-center mb-10">
        <TodayIssuePreview />
      </div>

      {/* 오늘의 키워드 + 뉴스 트렌드 나란히 */}
      <div className="flex flex-col md:flex-row gap-6">
        {/* 왼쪽: TodayKeywordPreview */}
        <div className="flex-1 bg-white shadow-md rounded-xl p-4">
          <TodayKeywordPreview />
        </div>

        {/* 오른쪽: WeeklyIssuePreview */}
        <div className="flex-1">
          <WeeklyIssuePreview />
        </div>
      </div>
    </div>
  );
}
