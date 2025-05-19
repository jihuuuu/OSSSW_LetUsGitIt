# api/routes/user_notes.py
# 역할: 유저 중심의 노트 관리 (마이페이지 등에서 사용)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.deps import get_db
from api.utils.auth import get_current_user
from models.article import Note
from api.schemas.notes import NoteUpdate, NoteOut

router = APIRouter()

# 현재 로그인한 사용자의 모든 노트를 최신순으로 조회
@router.get("/user/notes", response_model=list[NoteOut])
def get_all_notes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    notes = db.query(Note).filter_by(user_id=user.id).order_by(Note.created_at.desc()).all()
    return notes

# 특정 노트 조회
@router.get("/user/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")
    return note

# 특정 노트 수정
@router.put("/user/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, update: NoteUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    note.note_text = update.note_text
    db.commit()
    db.refresh(note)
    return note

# 특정 노트 삭제
@router.delete("/user/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    db.delete(note)
    db.commit()
    return {"message": "노트가 삭제되었습니다."}
