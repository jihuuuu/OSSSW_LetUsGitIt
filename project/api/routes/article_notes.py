# api/routes/article_notes.py
# 역할: 기사 중심의 노트 관리 (기사 상세 화면에서 사용)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.deps import get_db
from api.utils.auth import get_current_user
from models.note import Note
from api.schemas.notes import NoteCreate, NoteUpdate, NoteOut
from datetime import datetime, timezone

router = APIRouter()

# 특정 기사에 대해 노트 작성
@router.post("/articles/{article_id}/note", response_model=NoteOut)
def add_note(article_id: int, note: NoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # 유저가 해당 기사에 이미 작성한 노트가 있는지 확인 (user_id + article_id 조합은 유일해야 함)
    existing = db.query(Note).filter_by(user_id=user.id, article_id=article_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 이 기사에 대한 노트가 존재합니다.")

    new_note = Note(
        user_id=user.id,
        article_id=article_id,
        note_text=note.note_text,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# 특정 기사에 대해 작성한 노트 조회
@router.get("/articles/{article_id}/note", response_model=NoteOut)
def get_note_for_article(article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter_by(article_id=article_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트가 없습니다.")
    return note

# 특정 기사에 대해 작성한 노트 수정
@router.put("/articles/{article_id}/note", response_model=NoteOut)
def update_note_for_article(article_id: int, update: NoteUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter_by(article_id=article_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    note.note_text = update.note_text
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