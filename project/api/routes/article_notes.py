# api/routes/article_notes.py
# 역할: 기사 중심의 노트 관리 (기사 상세 화면에서 사용)

# api/routes/article_notes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.note import Note, NoteArticle
from models.article import Article
from api.schemas.notes import NoteCreateRequest, NoteCreateResponse
from api.utils.auth import get_current_user
from database.deps import get_db
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=NoteCreateResponse)
def create_note(
    note: NoteCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Note 생성
    new_note = Note(
        title=note.title,
        text=note.text,
        user_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    # 2. Note-Article 연결
    for article_id in note.article_ids:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
        link = article.link  # 예시 응답을 위해 필요
        db.add(NoteArticle(note_id=new_note.id, article_id=article_id))
    db.commit()

    # 3. 연결된 기사 리스트 조회
    articles = db.query(Article).filter(Article.id.in_(note.article_ids)).all()

    return {
        "isSuccess": True,
        "code": 200,
        "message": "노트가 성공적으로 생성되었습니다.",
        "result": {
            "userId": current_user.id,
            "noteId": new_note.id,
            "title": new_note.title,
            "text": new_note.text,
            "state": True,
            "created_at": new_note.created_at,
            "updated_at": new_note.updated_at,
            "articles": [{"id": a.id, "title": a.title, "link": a.link} for a in articles]
        }
    }
