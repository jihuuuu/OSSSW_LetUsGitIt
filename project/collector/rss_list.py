# collector/rss_list.py
# 역할: “어떤 RSS 피드를 구독할지” 리스트를 관리

rss_urls_by_topic = {
    "정치": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/politics/?outputType=xml",   
        # 한겨레신문
        # "https://www.hani.co.kr/rss/politics/",  
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/politic_news.xml",  
        # 매일경제
        "https://www.mk.co.kr/rss/30200030/", 
        # 한국경제
        "https://www.hankyung.com/feed/politics", 
        # 연합뉴스
        "https://www.yna.co.kr/rss/politics.xml", 
    ],
    "경제": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/economy/?outputType=xml",  
        # 한겨레신문
        # "https://www.hani.co.kr/rss/economy/",  
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/economy_news.xml",  
        # 매일경제
        "https://www.mk.co.kr/rss/30100041/", 
        # 한국경제
        "https://www.hankyung.com/feed/economy",
        # 연합뉴스
        "https://www.yna.co.kr/rss/economy.xml",
    ],
    "스포츠": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/sports/?outputType=xml",  
        # 한겨레신문
        # "https://www.hani.co.kr/rss/sports/", 
        # 경향신문
        "http://www.khan.co.kr/rss/rssdata/kh_sports.xml",  
        # 매일경제
        "https://www.mk.co.kr/rss/71000001/", 
        # 한국경제
        "https://www.hankyung.com/feed/sports", 
        # 연합뉴스
        "https://www.yna.co.kr/rss/sports.xml",
    ],
    "국제": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/international/?outputType=xml",
        # 동아일보
        "http://rss.donga.com/international.xml",
        # 한겨레신문
        # "https://www.hani.co.kr/rss/international/",
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/kh_world.xml",
        # 세계일보
        "http://rss.segye.com/segye_international.xml",
        # 한국경제
        "https://www.hankyung.com/feed/international",

    ],
    "문화": [
        # 조선일보
        "https://www.chosun.com/arc/outboundfeeds/rss/category/entertainments/?outputType=xml", 
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/culture_news.xml",  
        # 매일경제
        "https://www.mk.co.kr/rss/30000023/",  
        # 한국경제
        "https://www.hankyung.com/feed/entertainment", 
        # 연합뉴스
        "https://www.yna.co.kr/rss/culture.xml",
        # 스포츠조선
        "https://www.sportschosun.com/rss/index_enter.htm",

    ],
    "사회": [
        # 조선일보
        "http://www.chosun.com/arc/outboundfeeds/rss/category/national/?outputType=xml",             # :contentReference[oaicite:0]{index=0}
        # 동아일보
        "http://rss.donga.com/national.xml",                         
        # 경향신문
        "https://www.khan.co.kr/rss/rssdata/society_news.xml",           # :contentReference[oaicite:3]{index=3}
        # 매일경제
        "https://www.mk.co.kr/rss/50400012/",                            # :contentReference[oaicite:4]{index=4}
        # 세계일보
        "http://rss.segye.com/segye_society.xml",                        # :contentReference[oaicite:5]{index=5}
        # 서울신문
        "https://www.seoul.co.kr/xml/rss/rss_society.xml",               # :contentReference[oaicite:6]{index=6}
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
