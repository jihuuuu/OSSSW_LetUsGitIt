# api/schemas/note.py
from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    article_id: int
    note_text: str

class NoteUpdate(BaseModel):
    note_text: str

class NoteOut(BaseModel):
    id: int
    article_id: int
    note_text: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
