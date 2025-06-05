// src/pages/HomePage.tsx
import TodayIssuePreview from "@/components/TodayIssuePreview";
import WeeklyIssuePreview from "@/components/WeeklyIssuePreview";
// import { KeywordGraph } from "@/components/KeywordGraph";
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
        <div className="bg-white shadow-md rounded-xl p-4 flex-1">
          <h2 className="text-lg font-semibold text-blue-500 mb-4">오늘의 키워드 10</h2>
          <div className="h-[250px] flex items-center justify-center text-gray-400">
            (키워드 API 대기중...)
          </div>
        </div>

        <div className="flex-1">
          <WeeklyIssuePreview />
        </div>
      </div>
    </div>
  );
}
