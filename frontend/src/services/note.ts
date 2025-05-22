import api from "./api";
import type {Note} from "@/types/note";

export async function getNotesByPage(page: number, size: number): Promise<{
  notes: Note[];
  totalPages: number;
}> {
  const res = await fetch(`/api/notes?page=${page}&size=${size}`);
  return res.json();
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
  const res = await fetch(`/api/notes?keyword=${encodeURIComponent(keyword)}&page=${page}&size=${size}`);
  if (!res.ok) {
    throw new Error("노트 불러오기 실패");
  }
  return res.json(); // { notes, totalPages } 형태 기대
}