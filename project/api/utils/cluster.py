from sqlalchemy.orm import Session, joinedload, aliased
from typing import List, Optional, TypeVar, Callable, Any
from datetime import datetime, timedelta, timezone

from models.article import Cluster, ClusterArticle, ClusterKeyword, Keyword, Article
from models.topic import TopicEnum

T = TypeVar("T")

def fetch_top_clusters(
    db: Session,
    hours: int = 24,
    recent_limit: int = 50,
    topn_by_num: int = 20,
    topic: Optional[TopicEnum] = None
) -> List[Cluster]:
    """
    - 최근 `hours` 시간 이내 생성된 클러스터를
    #1) 생성일 내림차순으로 최신 `recent_limit`개 뽑고
    #2) 그 결과에서 num_articles(기사 수) 내림차순으로 상위 `topn_by_num`개 뽑아서 반환
    - topic이 지정되면 추가로 해당 토픽 필터 적용
    """
    # 1) cutoff: 지금으로부터 `hours`시간 전
    cutoff = datetime.now() - timedelta(hours=hours)

    # 2) 서브쿼리: 최근 hours시간 이내 생성된 Cluster 중 최신 recent_limit개
    base_q = (
        db.query(Cluster)
          .filter(Cluster.created_at >= cutoff)
          .order_by(Cluster.created_at.desc())
          .limit(recent_limit)
    )
    if topic is not None:
        base_q = base_q.filter(Cluster.topic == topic)

    subq = base_q.subquery()
    ClusterAlias = aliased(Cluster, subq)

    # 3) 메인쿼리: 서브쿼리에서 가져온 ClusterAlias들 중 num_articles 내림차순 상위 topn_by_num개
    main_q = (
        db.query(ClusterAlias)
          .options(
              joinedload(ClusterAlias.cluster_keyword).joinedload(ClusterKeyword.keyword),
              joinedload(ClusterAlias.cluster_article).joinedload(ClusterArticle.article)
          )
          .order_by(ClusterAlias.num_articles.desc())
          .limit(topn_by_num)
    )
    return main_q.all()


def dedupe_by_key(
    items: List[T],
    key_func: Callable[[T], Any],
    latest_attr: str = None
) -> List[T]:
    """
    - items: 필터링할 객체 리스트
    - key_func: 중복 판단용 키 추출 함수
    - latest_attr: 동일 key일 때 최신 객체 비교용 속성명 (예: 'created_at')
    """
    seen: dict[Any, T] = {}
    for item in items:
        key = key_func(item)
        if key not in seen:
            seen[key] = item
        else:
            if latest_attr:
                prev = seen[key]
                curr = item
                # created_at 같은 datetime 속성 비교
                if getattr(curr, latest_attr) > getattr(prev, latest_attr):
                    seen[key] = curr
    return list(seen.values())