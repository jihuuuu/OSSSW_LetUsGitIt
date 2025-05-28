// src/components/TrendTab.tsx
import { NavLink } from 'react-router-dom';

export default function TrendTab() {
  return (
    <div className="flex space-x-8 border-b pb-2">
      <NavLink
        to="/trend/weekly"
        className={({ isActive }) =>
          isActive ? 'border-b-2 border-black font-bold' : 'text-gray-500 visited:text-gray-500'
        }
      >
        주간 이슈 변화
      </NavLink>
      <NavLink
        to="/trend/search"
        className={({ isActive }) =>
          isActive ? 'border-b-2 border-black font-bold' : 'text-gray-500 visited:text-gray-500'
        }
      >
        키워드 검색
      </NavLink>
    </div>
  );
}