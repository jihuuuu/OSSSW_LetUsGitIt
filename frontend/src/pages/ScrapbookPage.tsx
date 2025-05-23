// src/pages/ScrapbookPage.tsx
import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import PaginationComponent from "@/components/PaginationComponent";
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";

type Article = {
  id: number;
  title: string;
  link: string;
  published: string;
};

export default function ScrapbookPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [keyword, setKeyword] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const userId = 1; // ✅ 로그인 유저 아이디 (임시)

  const fetchScrapArticles = async () => {
    const res = await fetch(
      `/api/scrap?userId=${userId}&keyword=${encodeURIComponent(
        keyword
      )}&page=${page}&size=10`
    );
    const data = await res.json();
    setArticles(data.articles);
    setTotalPages(data.totalPages);
  };

  useEffect(() => {
    fetchScrapArticles();
  }, [page]);

  const handleSearch = () => {
    setPage(1);
    fetchScrapArticles();
  };

  return (
    <div className="min-h-screen bg-white">
      {/* ✅ 상단 헤더 */}
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="px-2 py-1">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto">SCRAPBOOK</h1>
        <div className="px-2 py -1">
          <Header />
        </div>
      </header>

      {/* ✅ 본문 */}
      <main className="px-6 py-10 flex flex-col items-center">
        <div className="w-full max-w-4xl bg-[#ebf2ff] rounded-lg p-10 flex flex-col items-center gap-6">
          <p className="text-gray-500 text-center text-[16px]">
            기사 제목을 입력하세요
          </p>
          <div className="flex w-full max-w-sm items-center gap-2">
            <Input
              placeholder="예: 남지수"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
            <Button onClick={handleSearch}>Submit</Button>
          </div>
        </div>

        <div className="w-full max-w-4xl mt-10 space-y-2">
          {articles.map((a) => (
            <div key={a.id} className="text-blue-600 hover:underline">
              <a href={a.link} target="_blank" rel="noopener noreferrer">
                {a.title}
              </a>
            </div>
          ))}
        </div>

        <div className="mt-8">
          <PaginationComponent
            currentPage={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        </div>
      </main>
    </div>
  );
}
