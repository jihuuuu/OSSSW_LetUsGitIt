# collector/rss_list.py
# 역할: “어떤 RSS 피드를 구독할지” 리스트를 관리

rss_urls = [
    # 조선일보
    "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
    # 동아일보
    "https://rss.donga.com/total.xml",
    # 중앙일보: 몰라
    # 한국일보: 몰라
    # 한겨례신문
    "https://www.hani.co.kr/rss/",
    # 경향신문
    "https://www.khan.co.kr/rss/rssdata/total_news.xml",
    # 매일경제
    "https://www.mk.co.kr/rss/40300001/",
    # 한국경제
    "https://www.hankyung.com/feed/all-news",
    # KBS뉴스: 몰라요,,,
    # MBC뉴스: 몰라요
    # SBS뉴스(최신rss)
    "https://news.sbs.co.kr/news/newsflashRssFeed.do?plink=RSSREADER"
    # 여기에 다른 언론사 추가 가능
]
