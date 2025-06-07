// src/hooks/useLogoutWatcher.ts
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function useLogoutWatcher() {
  const navigate = useNavigate();

  useEffect(() => {
    const checkLogout = () => {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        alert("로그아웃되었습니다. 다시 로그인해주세요.");
        navigate("/");
      }
    };

    window.addEventListener("storage", checkLogout);
    return () => window.removeEventListener("storage", checkLogout);
  }, [navigate]);
}
