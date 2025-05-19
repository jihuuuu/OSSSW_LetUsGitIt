# models/article.py
# 역할: 기사 관련 모델 정의
# article, cluster, cluster_article, cluster_keyword, keyword

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime, timezone
from models.base import Base
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = "article"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    link = Column(String(255), nullable=False)
    summary = Column(Text, nullable=True)
    published = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    # 관계
    scrap = relationship("Scrap", back_populates="article")
    note_article = relationship("NoteArticle", back_populates="article")
    cluster_article = relationship("ClusterArticle", back_populates="article")
    pcluster_article = relationship("PClusterArticle", back_populates="article")

class Cluster(Base):
    __tablename__ = "cluster"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    label = Column(Integer, nullable=False)
    num_articles = Column(Integer, nullable=False)

    # 관계
    cluster_article = relationship("ClusterArticle", back_populates="cluster")
    cluster_keyword = relationship("ClusterKeyword", back_populates="cluster")

class ClusterArticle(Base):
    __tablename__ = "cluster_article"

    id = Column(BigInteger, primary_key=True, index=True)
    article_id = Column(BigInteger, ForeignKey("article.id", ondelete="CASCADE"), nullable=False)
    cluster_id = Column(BigInteger, ForeignKey("cluster.id", ondelete="CASCADE"), nullable=False)
    
    # 관계
    article = relationship("Article", back_populates="cluster_article")
    cluster = relationship("Cluster", back_populates="cluster_article")

class ClusterKeyword(Base):
    __tablename__ = "cluster_keyword"

    id = Column(BigInteger, primary_key=True, index=True)
    cluster_id = Column(BigInteger, ForeignKey("cluster.id", ondelete="CASCADE"), nullable=False)
    keyword_id = Column(BigInteger, ForeignKey("keyword.id", ondelete="CASCADE"), nullable=False)

    # 관계
    cluster = relationship("Cluster", back_populates="cluster_keyword")
    keyword = relationship("Keyword", back_populates="cluster_keyword")

class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # 관계
    cluster_keyword = relationship("ClusterKeyword", back_populates="keyword")
    pcluster_keyword = relationship("PClusterKeyword", back_populates="keyword")