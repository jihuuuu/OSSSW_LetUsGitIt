// src/services/knowledgeMap.ts
import api from "./api";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";

/**
 * ✅ 최신 Knowledge Map 하나 가져오기
 * 서버가 JWT 토큰에서 user_id 추출해야 함
 */
export async function fetchLatestKnowledgeMap(): Promise<{
  id: number;
  keywords: { id: number; name: string }[];
}> {
  const res = await api.get("/users/knowledge_maps/graph"); // ✅ userId 제거
  return res.data;
}

/**
 * ✅ 해당 키워드 기반 클러스터 노트 조회
 */
export async function fetchNotesByKeywordCluster(keywordId: number): Promise<Note[]> {
  const res = await api.get(`/keywords/${keywordId}/clusters/notes`);
  return res.data;
}

/**
 * ✅ 해당 키워드 기반 클러스터 기사 조회
 */
export async function fetchArticlesByKeywordCluster(keywordId: number): Promise<Article[]> {
  const res = await api.get(`/keywords/${keywordId}/clusters/articles`);
  return res.data;
}

// 키워드 ID로 키워드 이름 가져오기
export async function fetchKeywordName(keywordId: number): Promise<{ id: number; name: string }> {
  const res = await fetch(`/api/keywords/${keywordId}`);
  if (!res.ok) throw new Error("키워드 이름 불러오기 실패");
  return res.json(); // { id, name }
}