import api from "./api";
export async function getAllNotes(): Promise<Note[]> {
  const res = await api.get("/users/notes");
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