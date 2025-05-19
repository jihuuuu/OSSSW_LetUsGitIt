# models/scrap.py
# 역할: 스크랩 관련 모델 정의
# scrap, pcluster, pcluster_article, pcluster_keyword

from sqlalchemy import Column, BigInteger, Integer, DateTime, Boolean, ForeignKey
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

class PCluster(Base):
    __tablename__ = "pcluster"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    label = Column(Integer, nullable=False)
    knowledge_map_id = Column(BigInteger, ForeignKey("knowledge_map.id", ondelete="CASCADE"), nullable=False)

    # 관계
    knowledge_map = relationship("KnowledgeMap", back_populates="pcluster")
    pcluster_article = relationship("PClusterArticle", back_populates="pcluster")
    pcluster_keyword = relationship("PClusterKeyword", back_populates="pcluster")

class PClusterArticle(Base):
    __tablename__ = "pcluster_article"

    id = Column(BigInteger, primary_key=True, index=True)
    pcluster_id = Column(BigInteger, ForeignKey("pcluster.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(BigInteger, ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

    # 관계
    pcluster = relationship("PCluster", back_populates="pcluster_article")
    article = relationship("Article", back_populates="pcluster_article")

class PClusterKeyword(Base):
    __tablename__ = "pcluster_keyword"

    id = Column(BigInteger, primary_key=True, index=True)
    pcluster_id = Column(BigInteger, ForeignKey("pcluster.id", ondelete="CASCADE"), nullable=False)
    keyword_id = Column(BigInteger, ForeignKey("keyword.id", ondelete="CASCADE"), nullable=False)

    # 관계
    pcluster = relationship("PCluster", back_populates="pcluster_keyword")
    keyword = relationship("Keyword", back_populates="pcluster_keyword")