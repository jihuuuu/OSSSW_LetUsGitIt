// src/pages/Trend/TrendLayout.tsx
import { Outlet } from 'react-router-dom';
import Logo from '@/components/ui/logo'; // className 없이 사용
import TrendTab from '@/components/TrendTab';

export default function TrendLayout() {
  return (
    <div className="p-6">
      {/* 상단 Logo 좌상단 정렬 */}
      <div className="mb-4">
        <Logo />
      </div>

      {/* 제목과 탭 */}
      <h1 className="text-2xl font-bold mb-4 text-blue-600">뉴스 트렌드</h1>
      <TrendTab />

      {/* 탭 콘텐츠 영역 */}
      <div className="mt-6">
        <Outlet />
      </div>
    </div>
  );
}
