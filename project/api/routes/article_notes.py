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
    db.refresh(note)
    return note

# 특정 기사에 대해 작성한 노트 삭제
@router.delete("/articles/{article_id}/note")
def delete_note_for_article(article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter_by(article_id=article_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    db.delete(note)
    db.commit()
    return {"message": "노트가 삭제되었습니다."}