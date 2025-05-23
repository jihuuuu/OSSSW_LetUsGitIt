// 📄 src/pages/KeywordDetailPage.tsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchArticlesByKeywordCluster, fetchKeywordName } from "@/services/knowledgeMap";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";
import { Button } from "@/components/ui/button";
import Logo from "@/components/ui/logo";
import { ArrowRight, Star } from "lucide-react";
import PaginationComponent from "@/components/PaginationComponent";
import Header from "@/components/Header";
export default function KeywordDetailPage() {
  const { keywordId } = useParams();
  const [notes, setNotes] = useState<Note[]>([]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [keywordName, setKeywordName] = useState<string>("");

  const [notePage, setNotePage] = useState(1);
  const [articlePage, setArticlePage] = useState(1);
  const [noteTotalPages, setNoteTotalPages] = useState(1);
  const [articleTotalPages, setArticleTotalPages] = useState(1);

  useEffect(() => {
    if (!keywordId) return;

    fetchKeywordName(Number(keywordId)).then((res: { name: string }) => setKeywordName(res.name));

    fetchArticlesByKeywordCluster(keywordId).then((res) => {
      setArticles(res);
      setNoteTotalPages(1);
      setNotes([]);
      // If you have totalPages info, update this accordingly; otherwise, remove or set to 1
      setArticleTotalPages(1);
    });
  }, [keywordId, notePage, articlePage]);

  return (
    <div className="min-h-screen bg-white px-10 py-8">
      <header className="flex items-center justify-between mb-10">
        <Logo />
        <span className="text-sm font-medium text-blue-600 border border-blue-600 rounded-full px-2 py-6">
          {keywordName}
        </span>
        <div className="px-2 py -1">
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
