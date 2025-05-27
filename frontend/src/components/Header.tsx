import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    alert("로그아웃되었습니다.");
    navigate("/"); // 홈으로 이동
    window.location.reload(); // 강제 새로고침해서 상태 반영
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
          onClick={() => navigate("/users/login")}
          className="text-sm border px-2 py-1 rounded hover:bg-gray-100"
        >
          로그인
        </button>
      )}
    </div>
  );
}
