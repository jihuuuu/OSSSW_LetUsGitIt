# models/article.py
# 역할: 기사 관련 모델 정의
# article, cluster, cluster_article, cluster_keyword, keyword

from sqlalchemy import Column, BigInteger, Date, Integer, String, DateTime, Text, ForeignKey, CHAR, UniqueConstraint, Enum as SQLEnum
from datetime import datetime, timezone
from models.base import Base
from sqlalchemy.orm import relationship
from models.topic import TopicEnum

class Article(Base):
    __tablename__ = "article"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    link = Column(String(1024), nullable=False)
    link_hash = Column(CHAR(32), nullable=False, unique=True, index=True)
    summary = Column(Text, nullable=True)
    published = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    fetched_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    # Enum으로 토픽을 엄격하게 제한
    topic = Column(SQLEnum(TopicEnum, name="topic_enum"), nullable=False)

    # 관계
    scrap = relationship("Scrap", back_populates="article")
    note_article = relationship("NoteArticle", back_populates="article")
    cluster_article = relationship("ClusterArticle", back_populates="article")
    pkeyword_articles = relationship("PKeywordArticle", back_populates="article")

class Cluster(Base):
    __tablename__ = "cluster"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    label = Column(Integer, nullable=False)
    num_articles = Column(Integer, nullable=False)
    topic = Column(SQLEnum(TopicEnum, name="topic_enum"), nullable=False)

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
    trend_keyword = relationship("TrendKeyword", back_populates="cluster_keyword", cascade="all, delete-orphan")

class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # 관계
    cluster_keyword = relationship("ClusterKeyword", back_populates="keyword")
    #pcluster_keyword = relationship("PClusterKeyword", back_populates="keyword")
    # trend_keywords = relationship("TrendKeyword", back_populates="keyword")
    # today_keywords = relationship("TodayKeywordHourly", back_populates="keyword")

# 트렌드 페이지 - 하루마다 업데이트 되는 top n개 키워드 저장하는 테이블
class TrendKeyword(Base):
    __tablename__ = "trend_keyword"
    __table_args__ = (UniqueConstraint("cluster_keyword_id", "date", name="uq_trend_cluster_date"),)
    
    id = Column(BigInteger, primary_key=True, index=True)
    cluster_keyword_id = Column(BigInteger, ForeignKey("cluster_keyword.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)  # 예: 2025-05-30
    count = Column(Integer, nullable=False)              # 해당 날짜에 등장한 횟수

    # 관계 설정
    cluster_keyword = relationship("ClusterKeyword", back_populates="trend_keyword", cascade="save-update", passive_deletes=True)

#   # 오늘의 키워드 - 시간별로 업데이트 되는 클러스터 키워드 저장하는 테이블
# class TodayKeywordHourly(Base):
#     __tablename__ = "today_keyword_hourly"

#     id = Column(BigInteger, primary_key=True, index=True)
#     time_window_start = Column(DateTime(timezone=True), nullable=False, index=True)
#     count = Column(Integer, nullable=False)  # 지난 24시간 동안안 등장한 횟수
#     keyword_id = Column(BigInteger, ForeignKey("keyword.id"), nullable=False)

#     keyword = relationship("Keyword", back_populates="today_keywords")