# api/routes/notes.py
# 역할: 기사 메모 관련 엔드포인트 모음

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.deps import get_db
from api.utils.auth import get_current_user
from database.sql_models import UserNote
from api.schemas.notes import NoteCreate, NoteUpdate, NoteOut
from datetime import datetime, timezone

router = APIRouter()


# 노트 추가 (POST)
@router.post("/note", response_model=NoteOut)
def add_note(note: NoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_note = UserNote(
        user_id=user.id,
        article_id=note.article_id,
        note_text=note.note_text,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


# 노트 수정 (PUT)
@router.put("/note/{note_id}", response_model=NoteOut)
def update_note(note_id: int, update: NoteUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(UserNote).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    note.note_text = update.note_text
    db.commit()
    db.refresh(note)
    return note


# 노트 삭제 (DELETE)
@router.delete("/note/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(UserNote).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")
    
    db.delete(note)
    db.commit()
    return {"message": "노트가 삭제되었습니다."}


# 단일 기사에 대한 내 노트 조회 (GET)
@router.get("/note/{article_id}", response_model=NoteOut)
def get_note_for_article(article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(UserNote).filter_by(article_id=article_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트가 없습니다.")
    return note


# 내 모든 노트 조회 (GET)
@router.get("/note", response_model=list[NoteOut])
def get_all_notes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    notes = db.query(UserNote).filter_by(user_id=user.id).order_by(UserNote.created_at.desc()).all()
    return notes