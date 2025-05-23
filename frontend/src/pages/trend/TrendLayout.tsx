// src/pages/Trend/TrendLayout.tsx
import { Outlet } from 'react-router-dom';
import TrendTab from '@/components/TrendTab';

export default function TrendLayout() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">뉴스 트렌드</h1>
      <TrendTab />
      <div className="mt-4">
        <Outlet />
      </div>
    </div>
  );
}