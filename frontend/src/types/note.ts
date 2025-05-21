// src/types/note.ts
export interface Note {
  id: number;
  title: string;
  content: string;
  createdAt: string; // ISO 문자열 타입 (ex: 2024-05-21T12:00:00Z)
}