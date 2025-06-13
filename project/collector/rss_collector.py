# collector/rss_collector.py
# 역할: rss_list.py에 정의된 모든 피드를 순회하며 RSS 항목을 파싱하고, 중복 없이 MySQL(또는 파일)에 저장

#일단은 rss에서 뉴스 크롤링하여 제목만 추출하고 저장하는 코드로 구현
# 나중에 뉴스 본문도 크롤링하여 저장하는 코드로 수정할 예정

import feedparser
from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError
from database.connection import SessionLocal
from models.article import Article
from collector.rss_list import rss_urls_by_topic  # 토픽 이름(key)은 문자열이지만,
from models.topic import TopicEnum                  # 실제 DB 저장은 Enum 멤버로 변환
import hashlib
import requests
import http.client
from zoneinfo import ZoneInfo

def parse_and_store():
    session = SessionLocal()
    try:
        for topic, url_list in rss_urls_by_topic.items():
            try:
                topic_enum = TopicEnum(topic)
            except ValueError:
                # 만약 rss_list에 토픽이 enum 정의에 없다면 기본값 할당하거나 무시
                print(f"⚠ 알 수 없는 토픽: {topic} (넘겨뜀)")
                continue

            for url in url_list:    
                # --- 견고하게 RSS 가져오기 ---
                try:
                    resp = requests.get(url, timeout=20)
                    resp.raise_for_status()
                    content = resp.content
                except http.client.IncompleteRead as ir:
                    print(f"⚠️ IncompleteRead from {url}: {ir}; proceeding with partial data")
                    content = ir.partial
                except Exception as e:
                    print(f"⚠️ RSS fetch error ({url}): {e}")
                    continue
                feed = feedparser.parse(content)

                print(f"[{topic}] {url} 피드 아이템 수:", len(feed.entries))
                for entry in feed.entries:
                    # 1) RSS 엔트리에서 데이터 추출
                    link      = entry.link
                    title     = entry.get("title", "제목 없음")
                    summary   = entry.get("summary", "")
                    publ_pars = entry.get("published_parsed")
                    if publ_pars:
                        published_utc = datetime(*publ_pars[:6], tzinfo=timezone.utc)
                        published = published_utc.astimezone(ZoneInfo("Asia/Seoul"))
                    else:
                        published = None

                    # 2) link_hash 계산 (MD5)
                    link_hash = hashlib.md5(link.encode("utf-8")).hexdigest()

                    # 3) Article 인스턴스 생성
                    art = Article(
                        title=title,
                        link=link,
                        link_hash=link_hash,
                        summary=summary,
                        published=published,
                        fetched_at=datetime.now(timezone.utc),
                        topic=topic_enum
                    )

                    # 3) 중복(Unique) 처리: IntegrityError 발생 시 무시
                    session.add(art)
                    try:
                        session.commit()
                        print(f"✓ 저장: {title}")
                    except IntegrityError:
                        session.rollback()
                        print(f"⚠ 중복 건너뜀: link_hash={link_hash}")

    finally:
        session.close()

if __name__ == "__main__":
    parse_and_store()
    print("RSS 크롤링 → MySQL 저장 완료.")


# 1) 임베딩용: (id, text) 튜플 반환
def fetch_texts_with_ids_by_topic(topic: TopicEnum, limit: int | None = None, since_hours: int | None = None):
    """
    topic으로 필터링해서 (article_id, text) 튜플 리스트 반환
    - text는 “제목 + 요약” 형태
    - limit: 최대 n개 기사만 가져옴
    - since_hours: 최근 n시간 이내에 발행된 기사만
    """
    session = SessionLocal()
    try:
        q = session.query(Article.id, Article.title, Article.summary).filter(Article.topic == topic)
        if since_hours is not None:
            cutoff = datetime.utcnow() - timedelta(hours=since_hours)
            q = q.filter(Article.published >= cutoff)
        if limit is not None:
            q = q.order_by(Article.fetched_at.desc()).limit(limit)
        rows = q.all()
    finally:
        session.close()
    return [(aid, f"{title} {summary or ''}".strip()) for aid, title, summary in rows]


# 2) 키워드용: 순수 문자열 리스트 반환
def fetch_all_texts_by_topic(limit: int | None = None, since_hours: int | None = None) -> list[str]:
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