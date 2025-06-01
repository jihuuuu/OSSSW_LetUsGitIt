// src/routes/TrendRoutes.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import TrendLayout from '@/pages/trend/TrendLayout';
import WeeklyIssuePage from '@/pages/trend/WeeklyIssuePage';
import KeywordIssuePage from '@/pages/trend/KeywordIssuePage';

export default function TrendRoutes() {
  return (
    <Routes>
      <Route path="" element={<TrendLayout />}>
        <Route index element={<Navigate to="/trend/weekly" replace />} />
        <Route path="/weekly" element={<WeeklyIssuePage />} />
        <Route path="/search" element={<KeywordIssuePage />} />
      </Route>
    </Routes>
  );
}
