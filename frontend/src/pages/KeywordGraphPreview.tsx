// 📄 src/pages/KeywordGraphPreview.tsx
import { KeywordGraph } from "@/components/KeywordGraph";
import type { PCluster } from "@/types/cluster";

const dummyClusters: PCluster[] = [
  {
    id: 0,
    label: 1,
    keywords: [
      { id: 1, name: "AI", count: 5, clusterId: 0 },
      { id: 2, name: "ChatGPT", count: 4, clusterId: 0 },
      { id: 3, name: "딥러닝", count: 1, clusterId: 0 },
    ],
  },
  {
    id: 1,
    label: 2,
    keywords: [
      { id: 4, name: "선거", count: 10, clusterId: 1 },
      { id: 5, name: "정치", count: 5, clusterId: 1 },
      { id: 6, name: "후보", count: 3, clusterId: 1 },
    ],
  },
];

export default function KeywordGraphPreview() {
  return (
    <div className="min-h-screen bg-white p-10">
      <h1 className="text-xl font-bold text-center mb-6">Keyword Graph Preview</h1>
      <KeywordGraph clusters={dummyClusters} />
    </div>
  );
}