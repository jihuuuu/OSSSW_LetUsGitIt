// src/components/ui/Header.tsx
import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    alert("로그아웃 되었습니다.");
    navigate("/login");
  };

  const handleLogin = () => {
    navigate("/login");
  };

  return (
    <div className="w-full flex justify-end px-6 py-4">
      {token ? (
        <>
          <button
            onClick={handleLogout}
            className="text-sm px-3 py-1 bg-blue-400 hover:bg-blue-500 text-white font-semibold rounded-md"
          >
            로그아웃
          </button>
          <button
            onClick={() => navigate("/dashboard")}
            className="text-sm px-3 py-1 bg-blue-400 hover:bg-blue-500 text-white font-semibold rounded-md"
          >
            myPage
          </button>
        </>
      ) : (
        <button
          onClick={handleLogin}
          className="text-sm bg-blue-400 hover:bg-blue-500 text-white font-semibold rounded-md px-3 py-1 "
        >
          로그인
        </button>
      )}
    </div>
  );
}
