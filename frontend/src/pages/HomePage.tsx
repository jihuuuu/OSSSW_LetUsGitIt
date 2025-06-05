// src/pages/HomePage.tsx
import TodayIssuePreview from "@/components/card/TodayIssueCard";
import WeeklyIssuePreview from "@/components/card/WeeklyIssueCard";
import {TodayKeywordPreview} from "@/components/card/TodayKeywordCard"; // ★ 추가
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";

export default function HomePage() {
  return (

    <div className="min-h-screen flex flex-col justify-start">
      <header className="h-25 bg-blue-500 text-white px-6 flex items-center justify-between mb-20">
        <div className="flex items-center">
          <Logo />
        </div>
        <div className="px-2 py -1">
          <Header />
        </div>
      </header>

      <div className="flex justify-center mb-20 gap-y-20">
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
