// src/services/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",  // FastAPI 주소
  withCredentials: true,
});

// 요청 시 access token을 Authorization 헤더에 자동 포함
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;