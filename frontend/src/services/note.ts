// ✅ src/services/note.ts
import api from "./api";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";

export async function getNotesByPage(page: number, size: number): Promise<{
  notes: Note[];
}> {
  const res = await api.get("/users/notes", {
    params: { page, size },
  });

  const result = res.data.result;

  return {
    notes: result.notes.map((n: any) => ({
      id: n.note_id, // ✅ 백엔드에서 note_id로 오면 매핑
      title: n.title,
      text: n.text,
      createdAt: n.created_at,
    })),
  };
}


export async function createNote(data: { title: string; content: string }) {
  const res = await api.post("/users/notes", data);
  return res.data;
}

export async function updateNote(id: number, data: { title: string; content: string }) {
  const res = await api.put(`/users/notes/${id}`, data);
  return res.data;
}

export async function getNotesByKeyword(keyword: string, page: number, size: number): Promise<{
  notes: Note[];
}> {
  const res = await api.get("/users/notes", {
    params: { keyword, page, size },
  });

  const result = res.data.result;

  return {
    notes: result.notes,
    // totalPages: 1, // ← 더 이상 사용 안 하므로 생략 가능
  };
}

export async function getArticlesByNoteId(noteId: number): Promise<Article[]> {
  const res = await api.get(`/users/notes/${noteId}/articles`);
  return res.data; // [{ id, title, link, ... }]
}