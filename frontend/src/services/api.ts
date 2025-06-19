// src/services/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://3.37.87.202:8000",
  withCredentials: true,
});

// 요청 시 access token 추가
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 응답 시: access token 만료 → refresh → 실패하면 토큰 삭제만
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        interface RefreshResponse {
          access_token: string;
        }
        const res = await axios.post<RefreshResponse>(
          "http://3.37.87.202:8000/users/refresh",
          {},
          { withCredentials: true }
        );
        const newToken = res.data.access_token;
        localStorage.setItem("accessToken", newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // ❗window.location.href는 제거
        localStorage.removeItem("accessToken");
        // ❗단순 실패만 전달 → Header.tsx가 상태를 다시 읽어 UI를 바꿀 수 있게 함
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;