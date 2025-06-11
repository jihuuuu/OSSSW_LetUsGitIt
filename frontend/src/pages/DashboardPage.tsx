// 📄 src/pages/DashboardPage.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "@/components/ui/logo";
import { NoteAccordionList } from "@/components/NoteAccordionList";
import { getNotesByPage } from "@/services/note";
import { getScrappedArticles } from "@/services/scrap";
import { fetchLatestKnowledgeMap } from "@/services/knowledgeMap";
import type { Note } from "@/types/note";
import type { ScrappedArticle } from "@/types/scrap";
import type { KnowledgeMap } from "@/types/knowledgeMap";
import { KeywordGraph } from "@/components/KeywordGraph";
import { Button } from "@/components/ui/button";
import Header from "@/components/Header";

export default function DashboardPage() {
  const navigate = useNavigate();

  const [notes, setNotes] = useState<Note[]>([]);
  const [scraps, setScraps] = useState<ScrappedArticle[]>([]);
  const [map, setMap] = useState<KnowledgeMap | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getNotesByPage(1, 3).then((res) => setNotes(res.notes)),
      getScrappedArticles({ page: 1, size: 5 }).then((res) => setScraps(res.articles)),
      fetchLatestKnowledgeMap().then((res) => {
        if (res && 'keywords' in res) {
          setMap({
            id: res.id,
            clusters: [
              {
                id: 0,
                label: 1,
                keywords: (res.keywords as Array<{ id: number; name: string }>).map((k) => ({
                  ...k,
                  count: 1,
                  clusterId: 0,
                })),
              },
            ],
          });
        } else {
          setMap(res);
        }
      }),
    ]).finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <div className="p-10 text-center">Loading dashboard...</div>;
  }

  return (
    
    <div className="min-h-screen flex flex-col justify-start">
          <header className="h-25 bg-blue-500 text-white px-6 flex items-center justify-between mb-10">
            <div className="flex items-center">
              <Logo />
            </div>
            <h1 className="text-white text-4xl font-bmjua">
              MY PAGE
            </h1>
            <div className="px-2 py -1">
              <Header />
            </div>
          </header>

      {/* ✅ 본문 (세로 정렬) */}
      <main className="px-6 flex flex-col items-center gap-10">
        {/* ✅ 지식맵 */}
        <section className="w-full max-w-5xl">
          <div className="flex items-center justify-between mb-2">
            <h2 className="font-bold text-lg">MY KNOWLEDGE-MAP</h2>
          </div>
          <div className="bg-gray-50 border rounded px-4 py-3">
            {map?.clusters?.length && map.clusters.length > 0 ? (
              <KeywordGraph clusters={map.clusters} />
            ) : (
              <p className="text-sm text-gray-500">지식맵이 없습니다.</p>
            )}
          </div>
        </section>

        {/* ✅ 스크랩 */}
        <section className="w-full max-w-5xl">
          <div className="flex items-center justify-between mb-2">
            <h2 className="font-bold text-lg">SCRAP</h2>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/users/scraps")}
              className="text-xs text-blue-600 px-2 py-1"
            >
              more+
            </Button>
          </div>
          <div className="bg-gray-50 border rounded px-4 py-3 space-y-1 text-sm text-blue-600">
            {scraps.map((s) => (
              <a
                key={s.id}
                href={s.link}
                target="_blank"
                rel="noreferrer"
                className="block hover:underline"
              >
                {s.title}
              </a>
            ))}
            {scraps.length === 0 && (
              <p className="text-gray-500">스크랩된 기사가 없습니다.</p>
            )}
          </div>
        </section>

        {/* ✅ 노트 */}
        <section className="w-full max-w-5xl">
          <div className="flex items-center justify-between mb-2">
            <h2 className="font-bold text-lg">NOTE</h2>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/users/notes",{ state: { mode: "view" } })}
              className="text-xs text-blue-600 px-2 py-1"
            >
              more+
            </Button>
          </div>
          <div className="bg-gray-50 border rounded px-4 py-3">
            {notes.length > 0 ? (
              <NoteAccordionList notes={notes} onSelect={() => {}} onDelete={(id) => { const confirmed = window.confirm("삭제하시겠습니까?");
    if (!confirmed) return;
    alert("삭제는 노트 페이지에서 가능합니다."); }} />
            ) : (
              <p className="text-sm text-gray-500">작성된 노트가 없습니다.</p>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}