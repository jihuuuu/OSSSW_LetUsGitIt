# models/note.py
# 역할: 노트 관련 모델 정의
# note, note_article

from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey
from datetime import datetime, timezone
from models.base import Base
from sqlalchemy.orm import relationship

class Note(Base):
    __tablename__ = "note"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    state = Column(bool, nullable=False, default=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    # 관계
    user = relationship("User", back_populates="note")
    note_article = relationship("NoteArticle", back_populates="note")

class NoteArticle(Base):
    __tablename__ = "note_article"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    state = Column(bool, nullable=False, default=True)
    note_id = Column(BigInteger, ForeignKey("note.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(BigInteger, ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

    # 관계
    note = relationship("Note", back_populates="note_article")
    article = relationship("Article", back_populates="note_article")