# models/user.py
# 역할: 사용자 관련 모델 정의
# user, knowledge_map

from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Boolean
from datetime import datetime, timezone
from models.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    user_name = Column(String(45), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    refresh_token_id = Column(String(255), nullable=True)
    last_token_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # 관계: KnowledgeMap과 1:N
    knowledge_maps = relationship("KnowledgeMap", back_populates="user")
    notes = relationship("Note", back_populates="user")
    scrap = relationship("Scrap", back_populates="user")
    pkeywords = relationship("PKeyword", back_populates="user")

class KnowledgeMap(Base):
    __tablename__ = "knowledge_map"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_valid = Column(Boolean, default=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False) 
    
    # 관계
    user = relationship("User", back_populates="knowledge_maps")
    pkeywords = relationship("PKeyword", back_populates="knowledge_map")