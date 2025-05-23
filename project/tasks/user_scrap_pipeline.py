# 📄 tasks/user_scrap_pipeline.py
from sqlalchemy.orm import Session
from models.article import Article
from models.scrap import Scrap
from models.user import User
from models.user import KnowledgeMap
from models.scrap import PCluster, PClusterKeyword, PClusterArticle
from clustering.embedder import make_embeddings, preprocess_text
from clustering.cluster import run_kmeans
from clustering.keyword_extractor import extract_keywords_per_cluster

def run_user_scrap_knowledge_map(user: User, db: Session):
    # 1. 해당 유저의 스크랩 기사 불러오기
    articles = (
        db.query(Article)
        .join(Scrap, Scrap.article_id == Article.id)
        .filter(Scrap.user_id == user.id)
        .all()
    )

    if not articles:
        print(f"❌ 사용자 {user.id} 스크랩 없음. 건너뜀.")
        return

    # 2. 전처리 + 빈 텍스트 필터링
    texts = [f"{a.title} {a.summary or ''}".strip() for a in articles]
    preprocessed = [preprocess_text(t) for t in texts]

    texts_filtered = []
    articles_filtered = []
    for i, p in enumerate(preprocessed):
        if p.strip():
            texts_filtered.append(p)
            articles_filtered.append(articles[i])

    if not texts_filtered:
        print(f"❌ 사용자 {user.id} 스크랩 기사 중 유효한 텍스트 없음. 건너뜀.")
        return

    # 3. 임베딩 & 클러스터링
    embeddings = make_embeddings(texts_filtered)

    # 클러스터 수는 너무 많지 않게 조절 (최소 2, 최대 5)
    n_clusters = min(max(2, len(embeddings) // 2), 5)
    labels = run_kmeans(embeddings, n_clusters=n_clusters)

    # 4. KnowledgeMap 생성
    knowledge_map = KnowledgeMap(user_id=user.id)
    db.add(knowledge_map)
    db.commit()
    db.refresh(knowledge_map)

    # 5. 대표 키워드 추출
    keyword_map = extract_keywords_per_cluster(texts_filtered, labels, db)

    for cluster_id in set(labels):
        cluster_articles = [articles_filtered[i] for i, l in enumerate(labels) if l == cluster_id]
        cluster_keywords = keyword_map.get(cluster_id, [])

        pcluster = PCluster(label=cluster_id, knowledge_map_id=knowledge_map.id)
        db.add(pcluster)
        db.commit()
        db.refresh(pcluster)

        for article in cluster_articles:
            db.add(PClusterArticle(article_id=article.id, pcluster_id=pcluster.id))

        for kw in cluster_keywords:
            db.add(PClusterKeyword(keyword=kw, pcluster_id=pcluster.id))

    db.commit()
    print(f"✅ 사용자 {user.id} 지식맵 저장 완료")



# ✅ 이 함수도 같은 파일 아래에 위치
def generate_user_scrap_knowledge_maps(db: Session):
    users = db.query(User).all()
    for user in users:
        run_user_scrap_knowledge_map(user, db)