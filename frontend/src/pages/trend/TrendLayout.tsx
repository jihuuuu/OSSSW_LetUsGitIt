// src/pages/Trend/TrendLayout.tsx
import { Outlet } from 'react-router-dom';
import Logo from '@/components/ui/logo';
import TrendTab from '@/components/TrendTab';
import Header from '@/components/Header';

export default function TrendLayout() {
  return (
    <div className="p-6">
      <header className="h-25 bg-blue-500 px-6 flex items-center mb-10">
        {/* 좌측: 로고 */}
        <div className="flex-none">
          <Logo />
        </div>

        {/* 중앙: 타이틀 */}
        <div className="flex-1 text-center">
          <h1 className="text-white text-xl font-bmjua inline-block">
            뉴스 트렌드
          </h1>
        </div>

        {/* 우측: 헤더 */}
        <div className="flex-none">
          <Header />
        </div>
      </header>

      <TrendTab />

      {/* 탭 콘텐츠 영역 */}
      <div className="mt-6">
        <Outlet />
      </div>
    </div>
  );
}
