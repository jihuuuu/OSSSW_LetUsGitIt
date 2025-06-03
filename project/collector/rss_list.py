# collector/rss_list.py
# 역할: “어떤 RSS 피드를 구독할지” 리스트를 관리

rss_urls_by_topic = {
    "정치": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/politics/?outputType=xml",  # :contentReference[oaicite:0]{index=0}
        # 동아일보
        "https://rss.donga.com/list_politics.xml",  # (기존)
        # 한겨레신문
        "https://www.hani.co.kr/rss/politics/",  # :contentReference[oaicite:1]{index=1}
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/politic_news.xml",  # 
        # 매일경제
        "https://www.mk.co.kr/rss/30200030/",  # :contentReference[oaicite:3]{index=3}
        # 한국경제
        "https://www.hankyung.com/feed/politics",  # :contentReference[oaicite:4]{index=4}
    ],
    "경제": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/economy/?outputType=xml",  # :contentReference[oaicite:6]{index=6}
        # 동아일보
        "https://rss.donga.com/list_economy.xml",  # (기존)
        # 한겨레신문
        "https://www.hani.co.kr/rss/economy/",  # :contentReference[oaicite:7]{index=7}
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/economy_news.xml",  # 
        # 매일경제
        "https://www.mk.co.kr/rss/30100041/",  # :contentReference[oaicite:9]{index=9}
        # 한국경제
        "https://www.hankyung.com/feed/economy",  # :contentReference[oaicite:10]{index=10}
    ],
    "스포츠": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/sports/?outputType=xml",  # :contentReference[oaicite:12]{index=12}
        # 동아일보
        "https://rss.donga.com/list_sports.xml",  # (기존)
        # 한겨레신문
        "https://www.hani.co.kr/rss/sports/",  # :contentReference[oaicite:13]{index=13}
        # 경향신문
        "http://www.khan.co.kr/rss/rssdata/kh_sports.xml",  # 
        # 매일경제
        "https://www.mk.co.kr/rss/71000001/",  # :contentReference[oaicite:15]{index=15}
        # 한국경제
        "https://www.hankyung.com/feed/sports",  # :contentReference[oaicite:16]{index=16}
    ],
    "IT": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/tech/?outputType=xml",  # :contentReference[oaicite:18]{index=18}
        # 동아일보
        "https://rss.donga.com/list_it.xml",  # (기존)
        # 한겨레신문
        "https://www.hani.co.kr/rss/it/",  # :contentReference[oaicite:19]{index=19}
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/science_news.xml",  #   (IT 대체로 “과학·환경” 사용)
        # 매일경제
        # — IT 전용 RSS는 없지만 “문화·연예”에서 IT 관련 기사 노출됨
        "https://www.mk.co.kr/rss/30000023/",  # :contentReference[oaicite:21]{index=21}
        # 한국경제
        "https://www.hankyung.com/feed/it",  # :contentReference[oaicite:22]{index=22}
    ],
    "연예/문화": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/entertainments/?outputType=xml",  # :contentReference[oaicite:24]{index=24}
        # 동아일보
        "https://rss.donga.com/list_culture.xml",  # (기존)
        # 한겨레신문
        "https://www.hani.co.kr/rss/entertainment/",  # :contentReference[oaicite:25]{index=25}
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/culture_news.xml",  # 
        # 매일경제
        "https://www.mk.co.kr/rss/30000023/",  # :contentReference[oaicite:27]{index=27}
        # 한국경제
        "https://www.hankyung.com/feed/entertainment",  # :contentReference[oaicite:28]{index=28}
    ],
}

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
