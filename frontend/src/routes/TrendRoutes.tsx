// src/routes/TrendRoutes.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import TrendLayout from '@/pages/trend/TrendLayout';
import WeeklyIssuePage from '@/pages/trend/WeeklyIssuePage';
import KeywordSearchPage from '@/pages/trend/KeywordSearchPage';

export default function TrendRoutes() {
  return (
    <Routes>
      <Route path="/trend" element={<TrendLayout />}>
        <Route index element={<Navigate to="/trend/weekly" replace />} />
        <Route path="weekly" element={<WeeklyIssuePage />} />
        <Route path="search" element={<KeywordSearchPage />} />
      </Route>
    </Routes>
  );
}
