# 역할: 관계형 데이터베이스(RDBMS)에 대응하는 테이블 스키마를 SQLAlchemy ORM 혹은 Django 모델로 정의

# database/sql_models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(255), nullable=False)
    link        = Column(String(500), unique=True, nullable=False, index=True)
    summary     = Column(Text)
    published   = Column(DateTime)
    fetched_at  = Column(DateTime, default=datetime.utcnow)
    cluster     = Column(Integer, nullable=True, index=True)

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50), nullable=False, unique=True)
    email         = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at    = Column(DateTime, default=datetime.utcnow)

class UserScrap(Base):
    __tablename__ = "user_scraps"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    # 유니크 제약은 모델 레벨 대신 migration/DDL에 선언

class UserNote(Base):
    __tablename__ = "user_notes"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    note_text  = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
