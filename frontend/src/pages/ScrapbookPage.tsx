// src/pages/ScrapbookPage.tsx
import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import PaginationComponent from "@/components/PaginationComponent";
import Logo from "@/components/ui/logo";

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
    <div className="min-h-screen flex bg-white">
      {/* ✅ 왼쪽 로고 영역 */}
      <div className="w-[200px] p-6 border-r flex flex-col items-center">
        <Logo />
      </div>

      {/* ✅ 오른쪽 콘텐츠 영역 */}
      <div className="flex-1 px-10 py-10 flex flex-col items-center">
        <div className="w-full max-w-5xl bg-[#ebf2ff] rounded-lg p-12 flex flex-col items-center gap-8">
          <div className="text-[32px] font-bold text-gray-800 tracking-tight">
            SCRAPBOOK
          </div>
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

        <div className="w-full max-w-5xl mt-10 space-y-2">
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
      </div>
    </div>
  );
}
