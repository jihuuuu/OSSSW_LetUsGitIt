export type KeywordNode = {
  id: number;
  name: string;
  count: number;
};

export type KeywordEdge = {
  source: number;
  target: number;
  weight: number;
};

export type KnowledgeMap = {
  id: number;
  created_at: string;
  nodes: KeywordNode[];
  edges: KeywordEdge[];
};
