// src/pages/HomePage.tsx
import TodayIssuePreview from "@/components/card/TodayIssueCard";
import WeeklyIssuePreview from "@/components/card/WeeklyIssueCard";
import { TodayKeywordPreview } from "@/components/card/TodayKeywordCard";
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";
import { motion } from "framer-motion";
import useLogoutWatcher from "@/hooks/useLogoutWatcher";

// HomePage.tsx
export default function HomePage() {
  useLogoutWatcher();

  return (
   <div>
    <Header />
   
      {/* 섹션 1: 오늘의 이슈 */}
      <section className="min-h-[80vh] snap-start flex flex-col items-center justify-center px-6 py-10">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-3xl md:text-4xl font-pretendard text-gray-800 mb-10 text-center"
        >
          지금! 현재! 핫한 이슈들은?
        </motion.h2>
        <TodayIssuePreview />
      </section>

      {/* 섹션 2: 오늘의 키워드 */}
      <section className="min-h-[80vh] snap-start flex flex-col items-center justify-center px-6 py-20">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          viewport={{ once: true }}
          className="text-3xl md:text-4xl font-bold text-gray-800 mb-16 text-center"
        >
          실시간 오늘의 키워드를 확인하세요
        </motion.h2>
        <div className="w-full max-w-6xl bg-white shadow-md rounded-xl p-6">
          <TodayKeywordPreview />
        </div>
      </section>

      {/* 섹션 3: 주간 뉴스 트렌드 */}
      <section className="min-h-[80vh] snap-start flex flex-col items-center justify-center px-6 py-20">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          viewport={{ once: true }}
          className="text-3xl md:text-4xl font-bold text-gray-800 mb-16 text-center"
        >
          일주일간 트렌드를 확인하세요
        </motion.h2>
        <div className="w-full max-w-6xl bg-white shadow-md rounded-xl p-6">
          <WeeklyIssuePreview />
        </div>
      </section>
    </div>
  );
}
