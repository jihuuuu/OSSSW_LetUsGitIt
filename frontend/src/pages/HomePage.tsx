// src/pages/HomePage.tsx
import TodayIssuePreview from "@/components/TodayIssuePreview";
import WeeklyIssuePreview from "@/components/WeeklyIssuePreview";
// import { KeywordGraph } from "@/components/KeywordGraph";
import Logo from "@/components/ui/logo";

export default function HomePage() {
  return (
    <div className="min-h-screen px-10 py-8">
      <div className="absolute top-2 left-2">
        <Logo />
      </div>

      <div className="flex justify-center mb-10">
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
