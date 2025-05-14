# collector/rss_collector.py
# 역할: rss_list.py에 정의된 모든 피드를 순회하며 RSS 항목을 파싱하고, 중복 없이 MongoDB(또는 파일)에 저장

#일단은 rss에서 뉴스 크롤링하여 제목만 추출하고 저장하는 코드로 구현
# 나중에 뉴스 본문도 크롤링하여 저장하는 코드로 수정할 예정

import feedparser
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from database.connection import SessionLocal
from database.sql_models import Article
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
