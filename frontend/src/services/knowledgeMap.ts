// src/services/knowledgeMap.ts

import type { Note } from "@/types/note";
import type { Article } from "@/types/article";
import type { PCluster } from "@/types/cluster";
import type { Keyword } from "@/types/keyword";
import type { KnowledgeMap } from "@/types/knowledgeMap";

// ✅ 최신 Knowledge Map 하나 가져오기
export async function fetchLatestKnowledgeMap(userId: number): Promise<{
  id: number;
  keywords: { id: number; name: string }[];
}> {
  const res = await fetch(`/api/users/${userId}/knowledge_maps/graph`);
  if (!res.ok) throw new Error("지식맵 불러오기 실패");
  return res.json();
}

// ✅ 해당 키워드를 제목으로 갖는 노트들 조회 (클러스터링 기반)
export async function fetchNotesByKeywordCluster(keywordId: number): Promise<Note[]> {
  const res = await fetch(`/api/keywords/${keywordId}/clusters/notes`);
  if (!res.ok) throw new Error("키워드 노트 조회 실패");
  return res.json();
}

// ✅ 해당 키워드 기반 스크랩한 기사들 조회
export async function fetchArticlesByKeywordCluster(keywordId: number): Promise<Article[]> {
  const res = await fetch(`/api/keywords/${keywordId}/clusters/articles`);
  if (!res.ok) throw new Error("키워드 기사 조회 실패");
  return res.json();
}