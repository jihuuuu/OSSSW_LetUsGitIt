// 📁 src/components/Header.tsx
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { checkAuth } from "../services/auth";
import Logo from "@/components/ui/logo";

type HeaderProps = {
  centerTitle?: string;
};

export default function Header({ centerTitle }: HeaderProps) {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const validate = async () => {
      const user = await checkAuth();
      setIsLoggedIn(!!user);
    };
    validate();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    fetch("http://localhost:8000/users/logout", {
      method: "POST",
      credentials: "include",
    });
    alert("로그아웃되었습니다.");
    navigate("/");
    window.location.reload();
  };

  return (
    <header className="w-full bg-black text-white px-10 py-6 flex items-center justify-between relative shadow-md z-50 sticky top-0 h-28">
      <div className="z-10">
        <Logo />
      </div>

      {/* ✅ 중앙 제목 */}
      {centerTitle && (
        <h1 className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-3xl font-bold text-white">
          {centerTitle}
        </h1>
      )}

      <nav className="flex items-center gap-6 text-lg font-medium z-10">
        <Link to="/today/issue" className="hover:text-orange-300 transition">오늘의 이슈</Link>
        <Link to="/trend/weekly" className="hover:text-orange-300 transition">트렌드</Link>
        {isLoggedIn ? (
          <>
            <Link to="/dashboard" className="hover:text-orange-300 transition">마이페이지</Link>
            <button onClick={handleLogout} className="hover:text-orange-300 transition">로그아웃</button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-orange-300 transition">로그인</Link>
            <Link to="/signup" className="hover:text-orange-300 transition">회원가입</Link>
          </>
        )}
      </nav>
    </header>
  );
}
