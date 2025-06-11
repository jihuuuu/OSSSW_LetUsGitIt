// src/pages/SignupCompletePage.tsx

import Logo from "@/components/ui/logo";
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function SignupCompletePage() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/"); // 👉 이동할 경로로 수정
    }, 3000);

    return () => clearTimeout(timer); // 컴포넌트 언마운트 시 타이머 제거
  }, [navigate]);

  return (
    <div className="relative min-h-screen bg-white">
      {/* 좌측 상단 로고 */}
      <div className="absolute top-2 left-2">
        <Logo />
      </div>

      {/* 메인 콘텐츠 */}
      <div className="flex flex-col items-center justify-center min-h-screen">
        <img
          src="/congrats.png"
          alt="가입 완료 아이콘"
          className="w-[150px] h-[150px] mb-4"
        />
        <h1 className="text-[#78AAFB] text-xl font-semibold">
          가입이 완료되었습니다!
        </h1>
        <p className="text-sm text-gray-500 mt-2">
          잠시 후 홈으로 이동합니다...
        </p>
      </div>
    </div>
  );
}
