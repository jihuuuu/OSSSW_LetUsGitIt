// src/pages/HomePage.tsx
import TodayIssuePreview from "@/components/TodayIssuePreview";
import WeeklyIssuePreview from "@/components/WeeklyIssuePreview";
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";
import { Button } from "@/components/ui/button"; // ✨ Tailwind 버튼

export default function HomePage() {
  return (
    <div className="min-h-screen px-10 py-8">
      {/* 상단 헤더 */}
      <header className="flex justify-between items-center h-16">
        <div className="pl-2">
          <Logo />
        </div>
        <div className="pr-2">
          <Header />
        </div>
        <div className="w-32 h-32 bg-red-500 text-white p-4">Tailwind 작동중</div>;
      </header>

      {/* 오늘의 이슈 */}
      <section className="my-10">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-800">오늘의 이슈</h2>
          <Button variant="ghost" size="icon">더보기</Button>
        </div>
        <TodayIssuePreview />
      </section>

      {/* 오늘의 키워드 + 뉴스 트렌드 */}
      <div className="flex flex-col md:flex-row gap-6">
        {/* 키워드 */}
        <div className="bg-white shadow-md rounded-xl p-4 flex-1">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-blue-500">오늘의 키워드 10</h2>
            <Button variant="ghost" size="icon">더보기</Button>
          </div>
          <div className="h-[250px] flex items-center justify-center text-gray-400">
            (키워드 API 대기중...)
          </div>
        </div>

        {/* 트렌드 */}
        <div className="bg-white shadow-md rounded-xl p-4 flex-1">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-blue-500">뉴스 트렌드</h2>
            <Button variant="ghost" size="icon">더보기</Button>
          </div>
          <WeeklyIssuePreview />
        </div>
      </div>
    </div>
  );
}