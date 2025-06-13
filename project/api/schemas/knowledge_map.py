#schemas/knowledge_map.py
from pydantic import BaseModel
from typing import List

class KeywordNode(BaseModel):
    id: int
    name: str
    count: int

    class Config:
        orm_mode = True

class KeywordEdge(BaseModel):
    source: int
    target: int
    weight: float

class KnowledgeMapOut(BaseModel):
    id: int
    created_at: str
    nodes: List[KeywordNode]
    edges: List[KeywordEdge]

class Message(BaseModel):
    message: str