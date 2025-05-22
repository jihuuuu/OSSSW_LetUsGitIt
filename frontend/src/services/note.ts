// ✅ src/services/note.ts
import api from "./api";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";
export async function getNotesByPage(page: number, size: number): Promise<{
  notes: Note[];
  totalPages: number;
}> {
  const res = await api.get("/users/notes", {
    params: { page, size },
  });
  return res.data;
}

export async function createNote(data: { title: string; content: string }) {
  const res = await api.post("/users/notes", data);
  return res.data;
}

export async function updateNote(id: number, data: { title: string; content: string }) {
  const res = await api.put(`/users/notes/${id}`, data);
  return res.data;
}

export async function getNotesByKeyword(keyword: string, page: number, size: number) {
  const res = await api.get("/users/notes", {
    params: { keyword, page, size },
  });
  return res.data; // { notes, totalPages }
}

export async function getArticlesByNoteId(noteId: number): Promise<Article[]> {
  const res = await api.get(`/users/notes/${noteId}/articles`);
  return res.data; // [{ id, title, link, ... }]
}