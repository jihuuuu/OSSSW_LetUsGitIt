// 📄 src/pages/KeywordDetailPagePreview.tsx
import { useState } from "react";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";
import { Button } from "@/components/ui/button";
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";
import { ArrowRight, Star } from "lucide-react";
import PaginationComponent from "@/components/PaginationComponent";

export default function KeywordDetailPagePreview() {
  const [notes, setNotes] = useState<Note[]>([
    { id: 1, title: "AI 요약 노트", text: "ChatGPT가 정리한 내용입니다.", createdAt: "2024-06-01" },
    { id: 2, title: "AI 시대", text: "AI의 영향과 기술 발전.", createdAt: "2024-06-02" },
  ]);
  const [articles, setArticles] = useState<Article[]>([
    {
      id: 1,
      title: "AI 윤리 논쟁",
      link: "https://example.com/ai-ethics",
      summary: "AI 윤리 논쟁에 대한 요약입니다.",
      published: "2024-06-01"
    },
    {
      id: 2,
      title: "AI 기술 흐름",
      link: "https://example.com/ai-tech",
      summary: "AI 기술의 최신 흐름을 다룹니다.",
      published: "2024-06-02"
    },
  ]);

  const [keywordName, setKeywordName] = useState("AI 기술");
  const [notePage, setNotePage] = useState(1);
  const [articlePage, setArticlePage] = useState(1);
  const [noteTotalPages] = useState(2);
  const [articleTotalPages] = useState(2);

  return (
    <div className="min-h-screen bg-white px-10 py-8">
      <header className="flex items-center justify-between mb-10">
        <Logo />
        <span className="text-sm font-medium text-blue-600 border border-blue-600 rounded-full px-2 py-1">
          {keywordName}
        </span>
        <div className="px-2 py-1">
          <Header />
        </div>
      </header>

      <main className="flex gap-20">
        {/* NOTE 영역 */}
        <section className="flex-1">
          <h2 className="text-2xl font-bold mb-6">NOTE</h2>
          <ul className="space-y-6">
            {notes.map((note) => (
              <li key={note.id} className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 font-medium">
                    <Star className="w-4 h-4 text-blue-500" /> {note.title}
                  </div>
                  <p className="text-sm text-gray-500">{note.text}</p>
                </div>
                <ArrowRight className="w-6 h-6 text-blue-500" />
              </li>
            ))}
          </ul>
          <div className="mt-6">
            <PaginationComponent
              currentPage={notePage}
              totalPages={noteTotalPages}
              onPageChange={setNotePage}
            />
          </div>
        </section>

        {/* SCAP 영역 */}
        <section className="flex-1">
          <h2 className="text-2xl font-bold mb-6">SCAP</h2>
          {articles.length > 0 ? (
            <ul className="space-y-3 text-sm text-blue-600">
              {articles.map((article) => (
                <li key={article.id}>
                  <a href={article.link} target="_blank" rel="noopener noreferrer" className="hover:underline">
                    {article.link}
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-500">스크랩된 기사가 없습니다.</p>
          )}
          <div className="mt-6">
            <PaginationComponent
              currentPage={articlePage}
              totalPages={articleTotalPages}
              onPageChange={setArticlePage}
            />
          </div>
        </section>
      </main>
    </div>
  );
}