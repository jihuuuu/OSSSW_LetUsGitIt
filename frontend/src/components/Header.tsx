import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkAuth } from "../services/auth";

export default function Header() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
  const validate = async () => {
    const user = await checkAuth();  // 실패 시 null
    setIsLoggedIn(!!user);
  };
  validate();
}, []);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    fetch("http://localhost:8000/users/logout", {
      method: "POST",
      credentials: "include", // refresh_token 쿠키 삭제
    });
    alert("로그아웃되었습니다.");
    navigate("/");
    window.location.reload();
  };

  return (
    <div className="flex gap-3 items-center">
      {isLoggedIn ? (
        <>
          <button
            onClick={() => navigate("/dashboard")}
            className="text-sm font-medium border border-gray-300 bg-gray-100 px-2 py-1 rounded shadow-sm hover:shadow-md hover:bg-gray-200 transition-all duration-200"
          >
            마이페이지
          </button>
          <button
            onClick={handleLogout}
            className="text-sm font-medium border border-gray-300 bg-gray-100 px-2 py-1 rounded shadow-sm hover:shadow-md hover:bg-gray-200 transition-all duration-200"
          > 
            로그아웃
          </button>
        </>
      ) : (
        <button
          onClick={() => navigate("/login")}
          className="text-sm border px-2 py-1 rounded hover:bg-gray-100"
        >
          로그인
        </button>
      )}
    </div>
  );
}
