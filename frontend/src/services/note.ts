// src/services/note.ts

import api from "./api";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";

export async function getNotesByPage(page: number, size: number): Promise<{ notes: Note[]; totalPages: number }> {
  const res = await api.get("/users/notes", {
    params: { page, size },
  });

  const result = (res.data as { result: any }).result;

  return {
    notes: result.notes.map((n: any) => ({
      id: Number(n.note_id),
      title: n.title,
      text: n.text ?? "",
      createdAt: n.created_at,
      state: n.state ?? true,
    })),
    totalPages: result.totalPages || 1,
  };
}

export async function getNotesByKeyword(
  title: string,
  page: number,
  size: number
): Promise<{ notes: Note[]; totalPages: number }> {
  const res = await api.get("/users/notes", {
    params: { title, page, size },
  });

  const result = (res.data as { result: any }).result;

  return {
    notes: result.notes.map((n: any) => ({
      id: Number(n.id),
      title: n.title,
      text: n.text ?? "",
      createdAt: n.created_at,
      state: n.state ?? true,
    })),
    totalPages: result.totalPages || 1,
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

export async function getArticlesByNoteId(noteId: number): Promise<Article[]> {
  const res = await api.get(`/users/notes/${noteId}/articles`);
  // Ensure the response is an array and map it to Article[]
  const articles = Array.isArray(res.data)
    ? res.data.map((a: any) => ({
        id: Number(a.id),
        title: a.title,
        content: a.content,
        createdAt: a.created_at,
        link: a.link ?? "",
        summary: a.summary ?? "",
        published: a.published ?? false,
      }))
    : [];
  return articles;
}
