// src/pages/HomePage.tsx
import TodayIssuePreview from "@/components/card/TodayIssueCard";
import WeeklyIssuePreview from "@/components/card/WeeklyIssueCard";
import {TodayKeywordPreview} from "@/components/card/TodayKeywordCard"; // ★ 추가
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";
import useLogoutWatcher from "@/hooks/useLogoutWatcher"; // 로그아웃 감지 훅
export default function HomePage() {

  useLogoutWatcher();
  return (

    <div className="min-h-screen flex flex-col justify-start">
      <header className="h-25 bg-blue-500 text-white px-6 flex items-center justify-between mb-10">
        <div className="flex items-center">
          <Logo />
        </div>
        <div className="px-2 py -1">
          <Header />
        </div>
      </header>

      <div className="flex justify-center mb-10 gap-y-15">
        <TodayIssuePreview />
      </div>

      {/* 오늘의 키워드 + 뉴스 트렌드 나란히 */}
      <main className="w-full max-w-8xl mx-auto px-6">
  <div className="flex flex-col md:flex-row gap-6">
    <div className="flex-1 min-w-0 bg-white shadow-md rounded-xl p-6">
      <TodayKeywordPreview />
    </div>
    <div className="flex-1 min-w-0 bg-white shadow-md rounded-xl p-6">
      <WeeklyIssuePreview />
    </div>
  </div>
</main>
      </div>
    );
}
