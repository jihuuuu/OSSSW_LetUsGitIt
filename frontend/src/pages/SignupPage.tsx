import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "@/components/ui/logo";

export default function SignupPage() {
  const navigate = useNavigate(); // ← 페이지 이동용 훅

  const [form, setForm] = useState({
    email: "",
    user_name: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      const response = await fetch("http://3.35.66.161:8000/users/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_name: form.user_name,
          email: form.email,
          password: form.password,
          password_chk: form.confirmPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message); // ex: "회원가입이 완료되었습니다."
        navigate("/signup/complete"); // ✅ 이동
      } else {
        switch (data.errorCode) {
          case "PASSWORD_MISMATCH":
            alert("비밀번호가 일치하지 않습니다.");
            break;
          case "INVALID_EMAIL_FORMAT":
            alert("이메일 형식이 올바르지 않습니다.");
            break;
          case "EMAIL_ALREADY_EXISTS":
            alert("이미 가입된 이메일입니다.");
            break;
          default:
            alert(data.message || "회원가입 중 오류가 발생했습니다.");
            break;
        }
      }
    } catch (error) {
      console.error("회원가입 요청 중 오류:", error);
      alert("서버와 통신 중 문제가 발생했습니다.");
    }
  };
  
  return (
    <div className="relative min-h-screen bg-white">
      {/* 좌측 상단 로고 */}
      <div className="absolute top-4 left-4">
        <Logo />
      </div>

      {/* 폼 영역 */}
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-2xl font-bold text-[#78AAFB] mb-6">회원가입</h1>
        <form
          onSubmit={handleSubmit}
          className="flex flex-col w-[300px] gap-3"
        >
          {/* 이메일 */}
          <label className="text-sm text-gray-600 font-semibold">
            이메일
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              className="w-full mt-1 p-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-300"
            />
          </label>

          {/* 아이디 */}
          <label className="text-sm text-gray-600 font-semibold">
            아이디
            <input
              type="text"
              name="user_name"
              value={form.user_name}
              onChange={handleChange}
              required
              className="w-full mt-1 p-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-300"
            />
          </label>

          {/* 비밀번호 */}
          <label className="text-sm text-gray-600 font-semibold">
            비밀번호
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              required
              className="w-full mt-1 p-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-300"
            />
          </label>

          {/* 비밀번호 확인 */}
          <label className="text-sm text-gray-600 font-semibold">
            비밀번호 확인
            <input
              type="password"
              name="confirmPassword"
              value={form.confirmPassword}
              onChange={handleChange}
              required
              className="w-full mt-1 p-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-300"
            />
          </label>

          {/* 버튼 */}
          <button
            type="submit"
            className="mt-4 p-2 bg-blue-400 hover:bg-blue-500 text-white font-semibold rounded-md"
          >
            입력 완료
          </button>
        </form>
      </div>
    </div>
  );
}
