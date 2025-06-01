// src/types/trend.ts
export type DailyCount = {
  date: string;
  count: number;
};

export type TrendItem = {
  keyword: string;
  total_counts: number;
  daily_counts: DailyCount[];
};
