from datetime import date, datetime, timedelta, time
from sqlalchemy import func, distinct, or_
from database.connection import SessionLocal
from models.article import Article, ClusterArticle
from models.article import ClusterKeyword, TrendKeyword, Keyword
from datetime import timezone
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")


def generate_daily_trend():
    # 집계 대상: 어제(Asia/Seoul)
    today = datetime.now(KST).date()
    target = today - timedelta(days=1)
    start = datetime.combine(target, time.min).replace(tzinfo=KST)
    end   = datetime.combine(today, time.min).replace(tzinfo=KST)


    db = SessionLocal()
    try:

        # 1) 중복 방지
        db.query(TrendKeyword).filter(TrendKeyword.date == target).delete()

        # 2) 집계 쿼리
        results = (
            db.query(
                ClusterKeyword.id.label("cluster_keyword_id"),
                func.count(distinct(Article.id)).label("cnt")
            )
            # 클러스터–키워드 → 클러스터기사 → 기사
            .join(ClusterArticle, ClusterArticle.cluster_id == ClusterKeyword.cluster_id)
            .join(Article,       Article.id == ClusterArticle.article_id)
            # 키워드 텍스트 필터를 위해 Keyword 테이블 조인
            .join(Keyword,       Keyword.id == ClusterKeyword.keyword_id)
            .filter(
                Article.published >= start,
                Article.published <  end,
                or_(
                    Article.title.contains(Keyword.name),
                    Article.summary.contains(Keyword.name)
                )
            )
            .group_by(ClusterKeyword.id)
            .order_by(func.count(distinct(Article.id)).desc())
            .all()
        )

        # 3) TrendKeyword 삽입
        for cluster_kw_id, cnt in results:
            db.add(TrendKeyword(cluster_keyword_id = cluster_kw_id, date = target, count = cnt))
        
        # 4) 커밋
        db.commit()

    except:
        db.rollback()
        raise
    finally:
        db.close()

    print("트렌드 집계 완료")

