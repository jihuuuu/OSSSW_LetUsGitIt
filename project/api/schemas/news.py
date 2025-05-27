# api/schemas/news.py
# 역할: Pydantic 모델을 통해 요청(Request) 과 응답(Response) 의 스키마(타입·검증·직렬화)를 선언

from pydantic import BaseModel
from datetime import datetime

class NewsOut(BaseModel):
    id: int
    title: str
    link: str | None = None
    summary: str | None = None
    published: datetime | None = None

    class Config:
        orm_mode = True
