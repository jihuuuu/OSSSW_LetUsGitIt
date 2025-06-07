import { use, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Logo from "@/components/ui/logo";
import { login } from "../services/auth"; // 👈 로그인 API 함수만 사용
import { useAuth } from "@/context/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/"; // 로그인 후 이동할 경로

  const { login: authLogin } = useAuth();  // login 함수 이름 충돌 피하기 위해 별칭 사용
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login(email, password); // ✅ 서비스 함수 호출
      authLogin(res.access_token);             // 전역 context 상태 업데이트
      alert("로그인 성공!");
      navigate(from,{replace: true}); // 로그인 후 이동
    } catch (err: any) {
      console.error("로그인 오류:", err);
      alert("로그인 실패! 이메일 또는 비밀번호를 확인하세요.");
    }
  };

  return (
    <div className="relative min-h-screen bg-white">
      {/* 좌측 상단 로고 */}
      <div className="absolute top-4 left-4">
        <Logo />
      </div>

      {/* 로그인 폼 */}
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-2xl font-bold text-[#78AAFB] mb-6">로그인</h1>
        <form onSubmit={handleLogin} className="flex flex-col w-[300px] gap-3">
          {/* 이메일 */}
          <label className="text-sm text-gray-600 font-semibold">
            이메일
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full mt-1 p-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-300"
            />
          </label>

          {/* 비밀번호 */}
          <label className="text-sm text-gray-600 font-semibold">
            비밀번호
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full mt-1 p-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-300"
            />
          </label>
          

          {/* 로그인 버튼 */}
          <button
            type="submit"
            className="mt-10 p-2 bg-blue-400 hover:bg-blue-500 text-white font-semibold rounded-md"
          >
            로그인
          </button>
        </form>
      </div>
    </div>
  );
}
