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
import type { Keyword } from "@/types/keyword";
import type { KnowledgeMap } from "@/types/knowledgeMap";
import { KeywordGraph } from "@/components/KeywordGraph";
import {Button} from "@/components/ui/button";
export default function DashboardPage() {
  const userId = 1;
  const navigate = useNavigate();

  const [notes, setNotes] = useState<Note[]>([]);
  const [scraps, setScraps] = useState<ScrappedArticle[]>([]);
  const [map, setMap] = useState<KnowledgeMap | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getNotesByPage(1, 3).then((res) => setNotes(res.notes)),
      getScrappedArticles({ userId, page: 1, size: 5 }).then((res) => setScraps(res.articles)),
      fetchLatestKnowledgeMap(userId).then((res) => {
        // Transform the response to match KnowledgeMap type if needed
        if (res && 'keywords' in res) {
          setMap({
            id: res.id,
            clusters: [
              {
                id: 0,
                label: 1,
                keywords: res.keywords,
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
  <div className="flex min-h-screen bg-white gap-x-8">
    {/* 1. 로고 영역 (왼쪽 세로 고정) */}
    <div className="w-[120px] border-r px-4 py-8 flex justify-center">
      <Logo />
    </div>

    {/* 2. 지식맵 + 스크랩 영역 (세로 정렬) */}
    <div className="w-[300px] border-r px-6 py-8 flex flex-col gap-10">
      {/* 지식맵 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-bold text-lg">MY KNOWLEDGE-MAP</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/note")}
            className="text-xs text-blue-600 px-2 py-1"
          >
            more+
          </Button>
        </div>
        {map?.clusters?.length && map.clusters.length > 0 ? (
          <KeywordGraph clusters={map.clusters.map((c) => ({ ...c, label: String(c.label) }))} />
        ) : (
          <p className="text-sm text-gray-500">지식맵이 없습니다.</p>
        )}
      </div>

      {/* 스크랩 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-bold text-lg">SCRAP</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/scrapbook")}
            className="text-xs text-blue-600 px-2 py-1"
          >
            more+
          </Button>
        </div>
        <div className="space-y-1 text-sm text-blue-600">
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
      </div>
    </div>

    {/* 3. NOTE 영역 (오른쪽 전체 공간) */}
    <div className="flex-1 px-12 py-10">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Note</h1>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => navigate("/note")}
          className="text-xs text-blue-600 px-2 py-1"
        >
          more+
        </Button>
      </div>

      {notes.length > 0 ? (
        <NoteAccordionList notes={notes} onSelect={() => {}} />
      ) : (
        <p className="text-sm text-gray-500">작성된 노트가 없습니다.</p>
      )}
    </div>
  </div>
);

}
