// 📁 src/components/Header.tsx
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { checkAuth } from "../services/auth";
import Logo from "@/components/ui/logo";

export default function Header() {
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
    fetch("${import.meta.env.VITE_API_URL}/users/logout", {
      method: "POST",
      credentials: "include",
    });
    alert("로그아웃되었습니다.");
    navigate("/");
    window.location.reload();
  };

  return (
     <header className="w-full bg-black text-white px-10 py-10 flex items-center justify-between shadow-md z-50 sticky top-0 h-28">
      <Logo />
      <nav className="flex items-center gap-6 text-lg font-medium">
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