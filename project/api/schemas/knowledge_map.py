from pydantic import BaseModel
from typing import List

class ClusterInput(BaseModel):
    label: str
    keywords: List[str]
    articleIds: List[int]

class KnowledgeMapCreateRequest(BaseModel):
    result: List[ClusterInput]
