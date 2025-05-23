// src/types/cluster.ts
import type { Keyword } from "@/types/keyword";
export type Cluster = {
  id: number;
  label: number;
  keywords: Keyword[];
};

export type PCluster = {
  id: number;
  label: number;
  keywords: Keyword[];
};
