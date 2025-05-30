# collector/rss_collector.py
# 역할: rss_list.py에 정의된 모든 피드를 순회하며 RSS 항목을 파싱하고, 중복 없이 MySQL(또는 파일)에 저장

#일단은 rss에서 뉴스 크롤링하여 제목만 추출하고 저장하는 코드로 구현
# 나중에 뉴스 본문도 크롤링하여 저장하는 코드로 수정할 예정

import feedparser
from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError
from database.connection import SessionLocal
from models.article import Article
from collector.rss_list import rss_urls


def parse_and_store():
    session = SessionLocal()
    try:
        for url in rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # 1) RSS 엔트리에서 데이터 추출
                link      = entry.link
                title     = entry.get("title", "제목 없음")
                summary   = entry.get("summary", "")
                publ_pars = entry.get("published_parsed")
                published = datetime(*publ_pars[:6]) if publ_pars else None

                # 2) Article 인스턴스 생성
                art = Article(
                    title=title,
                    link=link,
                    summary=summary,
                    published=published,
                    fetched_at=datetime.now(timezone.utc)
                )

                # 3) 중복(Unique) 처리: IntegrityError 발생 시 무시
                session.add(art)
                try:
                    session.commit()
                    print(f"✓ 저장: {title}")
                except IntegrityError:
                    session.rollback()
                    print(f"⚠ 중복 건너뜀: {link}")

    finally:
        session.close()

if __name__ == "__main__":
    parse_and_store()
    print("RSS 크롤링 → MySQL 저장 완료.")


# 1) 임베딩용: (id, text) 튜플 반환
def fetch_texts_with_ids(limit: int | None = None, since_hours: int | None = None):
    """
    DB에서 최근 순으로 Article.id와 title+summary를 반환합니다.
    새로 수집된 RSS 데이터를 임베딩하거나 클러스터링할 때 사용합니다.

    Args:
        limit: 가져올 기사 건수 (None이면 전체)
        since_hours: 최근 N시간 내에 발행된 기사만 필터링
    Returns:
        List of tuples [(id, "title summary"), ...]
    """
    session = SessionLocal()
    try:
        q = session.query(Article.id, Article.title, Article.summary)
        if since_hours is not None:
            cutoff = datetime.utcnow() - timedelta(hours=since_hours)
            q = q.filter(Article.published >= cutoff)
        if limit:
            q = q.order_by(Article.fetched_at.desc()).limit(limit)
        rows = q.all()
    finally:
        session.close()
    return [(aid, f"{title} {summary or ''}".strip()) for aid, title, summary in rows]


# 2) 클러스터링&키워드용: 순수 문자열 리스트 반환
def fetch_all_texts(limit: int | None = None, since_hours: int | None = None) -> list[str]:
    """
    DB에서 제목과 요약을 합친 순수 텍스트 리스트를 반환합니다.
    클러스터링 후 키워드 추출 단계에서 사용합니다.

    Args:
        limit: 가져올 기사 건수 (None이면 전체)
        since_hours: 최근 N시간 내에 발행된 기사만 필터링
    Returns:
        List of strings ["title summary", ...]
    """
    session = SessionLocal()
    try:
        q = session.query(Article.title, Article.summary)
        if since_hours is not None:
            cutoff = datetime.utcnow() - timedelta(hours=since_hours)
            q = q.filter(Article.published >= cutoff)
        if limit:
            q = q.order_by(Article.fetched_at.desc()).limit(limit)
        rows = q.all()
    finally:
        session.close()
    return [f"{t.title} {t.summary or ''}".strip() for t in rows]