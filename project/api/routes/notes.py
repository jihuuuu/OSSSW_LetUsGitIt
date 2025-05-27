from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.utils.auth import get_current_user
from database.deps import get_db
from models.note import Note, NoteArticle
from models.user import User
from models.article import Article
from datetime import datetime
from api.schemas.notes import *
from api.schemas.common import *

router = APIRouter()


# ✅ 3. 노트 생성
@router.post("/notes", response_model=NoteCreateResponse)
def create_note(
    note_data: NoteCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_note = Note(
        user_id=current_user.id,
        title=note_data.title,
        text=note_data.text,
        state=True
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    articles = db.query(Article).filter(Article.id.in_(note_data.article_ids)).all()
    if len(articles) != len(note_data.article_ids):
        raise HTTPException(status_code=404, detail="Some articles not found")

    for article in articles:
        db.add(NoteArticle(note_id=new_note.id, article_id=article.id))
    db.commit()

    return {
        "isSuccess": True,
        "code": "NOTE_CREATED",
        "message": "노트가 성공적으로 생성되었습니다.",
        "result": {
            "userId": current_user.id,
            "noteId": new_note.id,
            "title": new_note.title,
            "text": new_note.text,
            "state": new_note.state,
            "created_at": new_note.created_at,
            "updated_at": new_note.updated_at,
            "articles": [
                ArticleOut(
                    id=a.id,
                    title=a.title,
                    link=a.link
                ).dict() for a in articles
            ]
        }
    }



# ✅ 1. 노트에 연결된 기사 조회 → 구체적인 경로 먼저!
@router.get("/notes/{note_id}/articles")
def get_articles_by_note_id(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_article_ids = db.query(NoteArticle.article_id).filter(NoteArticle.note_id == note_id).all()
    article_ids = [id for (id,) in note_article_ids]
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()

    return [
        {
            "id": a.id,
            "title": a.title,
            "link": a.link,
            "summary": a.summary,
        }
        for a in articles
    ]


# ✅ 2. 노트 상세 조회
@router.get("/notes/{note_id}")
def get_note_detail(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or access denied")

    note_article_ids = db.query(NoteArticle.article_id).filter(NoteArticle.note_id == note_id).all()
    article_ids = [id for (id,) in note_article_ids]
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()

    return {
        "isSuccess": True,
        "code": "NOTE_DETAIL_FETCHED",
        "message": "노트를 성공적으로 불러왔습니다.",
        "result": {
            "note_id": note.id,
            "title": note.title,
            "text": note.text,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
            "articles": [
                {
                    "id": a.id,
                    "title": a.title,
                    "link": a.link,
                    "summary": a.summary
                } for a in articles
            ]
        }
    }


# ✅ 4. 노트 목록 조회 (검색 포함)
@router.get("/notes")
def get_user_notes(
    keyword: str = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * size
    query = db.query(Note).filter(Note.user_id == current_user.id, Note.state == True)

    if keyword:
        query = query.filter(
            or_(
                Note.title.ilike(f"%{keyword}%"),
                Note.text.ilike(f"%{keyword}%")
            )
        )

    notes = query.order_by(Note.created_at.desc()).offset(offset).limit(size).all()

    note_list = [
        {
            "note_id": note.id,
            "title": note.title,
            "text": note.text,
            "created_at": note.created_at,
        }
        for note in notes
    ]

    return {
        "isSuccess": True,
        "code": "NOTE_LIST_FETCHED",
        "message": "노트 목록을 성공적으로 불러왔습니다.",
        "result": {
            "page": page,
            "size": size,
            "notes": note_list
        }
    }


# ✅ 5. 노트 수정
@router.put("/notes/{note_id}")
def update_note(
    note_id: int,
    update_data: NoteUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or access denied")

    note.title = update_data.title
    note.text = update_data.text
    note.updated_at = datetime.utcnow()

    if update_data.article_ids is not None:
        db.query(NoteArticle).filter(NoteArticle.note_id == note.id).delete()
        for article_id in update_data.article_ids:
            article = db.query(Article).filter(Article.id == article_id).first()
            if not article:
                raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
            db.add(NoteArticle(note_id=note.id, article_id=article_id))

    db.commit()

    updated_articles = db.query(Article).filter(Article.id.in_(update_data.article_ids)).all() if update_data.article_ids else []

    return {
        "isSuccess": True,
        "code": "NOTE_UPDATED",
        "message": "노트가 성공적으로 수정되었습니다.",
        "result": {
            "noteId": note.id,
            "title": note.title,
            "note_text": note.text,
            "updated_at": note.updated_at,
            "articles": [
                {"id": a.id, "title": a.title, "link": a.link} for a in updated_articles
            ]
        }
    }


# ✅ 6. 노트 삭제 (소프트 삭제)
@router.put("/notes/{note_id}/delete")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or access denied")

    note.state = False
    note.updated_at = datetime.utcnow()
    db.commit()

    return {
        "isSuccess": True,
        "code": "NOTE_DELETED",
        "message": "노트가 성공적으로 삭제되었습니다.",
        "result": {
            "noteId": note.id,
            "state": False,
            "updated_at": note.updated_at
        }
    }

# 특정 기사에 대해 작성한 노트 삭제
@router.delete("/articles/{article_id}/note")
def delete_note_for_article(article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter_by(article_id=article_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    db.delete(note)
    db.commit()
    return {"message": "노트가 삭제되었습니다."}