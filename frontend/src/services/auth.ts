import api from "./api";

export const login = async (email: string, password: string) => {
  const res = await api.post("/users/login", { email, password });
  return res.data; // access_token 포함
};
