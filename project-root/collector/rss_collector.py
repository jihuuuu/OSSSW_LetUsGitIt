#일단은 rss에서 뉴스 크롤링하여 제목만 추출하고 저장하는 코드로 구현
# 나중에 뉴스 본문도 크롤링하여 저장하는 코드로 수정할 예정
import feedparser
from database.connection import db  # MongoDB 연결
from datetime import datetime
from collector.rss_list import rss_urls  # RSS URL 목록 불러오기기

async def fetch_and_store_titles():
    all_titles = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            pub_date = entry.get("published", str(datetime.utcnow()))

            news_item = {
                "title": title,
                "link": link,
                "pubDate": pub_date
            }

            # 중복 방지 (링크 기준)
            exists = await db["news"].find_one({"link": link})
            if not exists:
                await db["news"].insert_one(news_item)

            all_titles.append(news_item)

    return all_titles
