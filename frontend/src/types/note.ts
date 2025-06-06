// src/types/note.ts
export type Note = {
  id: number;
  title: string;
  text: string;
  state?: boolean; // true: 정상, false: 삭제됨
  createdAt: string;
};
