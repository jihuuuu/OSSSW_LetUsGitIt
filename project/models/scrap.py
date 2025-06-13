# models/scrap.py
# 역할: 스크랩 관련 모델 정의
# scrap, pcluster, pcluster_article, pcluster_keyword

from sqlalchemy import Column, BigInteger, Integer, DateTime, Boolean, ForeignKey, String
from datetime import datetime, timezone
from models.base import Base
from sqlalchemy.orm import relationship

class Scrap(Base):
    __tablename__ = "scrap"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    state = Column(Boolean, nullable=False, default=True)
    article_id = Column(BigInteger, ForeignKey("article.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # 관계
    article = relationship("Article", back_populates="scrap")
    user = relationship("User", back_populates="scrap")

class PKeyword(Base):
    __tablename__ = "pkeyword"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    knowledge_map_id = Column(BigInteger, ForeignKey("knowledge_map.id"), nullable=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # 관계
    knowledge_map = relationship("KnowledgeMap", back_populates="pkeywords")
    user = relationship("User", back_populates="pkeywords")
    pkeyword_articles = relationship("PKeywordArticle", back_populates="pkeyword")

class PKeywordArticle(Base):
    __tablename__ = "pkeyword_article"

    id = Column(BigInteger, primary_key=True, index=True)
    pkeyword_id = Column(BigInteger, ForeignKey("pkeyword.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(BigInteger, ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

    # 관계
    pkeyword = relationship("PKeyword", back_populates="pkeyword_articles")
    article = relationship("Article", back_populates="pkeyword_articles")