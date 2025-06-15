// src/pages/Trend/TrendLayout.tsx
import { Outlet } from 'react-router-dom';
import Logo from '@/components/ui/logo';
import TrendTab from '@/components/TrendTab';
import Header from '@/components/Header';

export default function TrendLayout() {
  return (
    <div >
      <div className="mb-5">
      <Header />
      </div>

      <TrendTab />

      {/* 탭 콘텐츠 영역 */}
      <div className="mt-6">
        <Outlet />
      </div>
    </div>
  );
}
