# clustering/keyword_extractor.py

from typing import List, Dict
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from clustering.embedder import STOPWORDS_KO
from models.article import Keyword, ClusterKeyword

def extract_top_keywords(
    documents: List[str],
    db : Session,
    cluster_id : int,
    top_n: int = 3,
    max_features: int = 1000
) -> List[str]:
    """
    주어진 문서 리스트에 대해 TF-IDF를 계산하고,
    문서들에서 평균 TF-IDF 값이 높은 top_n 키워드를 뽑아 반환.
    """
    # ✅ 방어 로직
    if not documents or all(not doc.strip() for doc in documents):
        print(f"⚠️ cluster_id={cluster_id}: 전처리된 문서가 모두 공백입니다. 키워드 추출 생략.")
        return ["no_keyword"]
    
    # 1) TF-IDF 행렬 생성
    vectorizer = TfidfVectorizer(
        stop_words=list(STOPWORDS_KO),
        max_features=1000
    )
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    # 2) 각 단어별 평균 TF-IDF 계산
    mean_tfidf = tfidf_matrix.mean(axis=0).A1  # (n_features,)

    # 3) 상위 top_n 인덱스 추출
    top_indices = mean_tfidf.argsort()[::-1][:top_n]
    top_terms   = [feature_names[i] for i in top_indices]

    # 4) DB 저장 로직
    # for term in top_terms:
    #    # 4-1) Keyword 테이블에 없으면 생성
    #    kw_obj = db.query(Keyword).filter_by(name=term).first()
    #    if not kw_obj:
    #        kw_obj = Keyword(name=term)
    #        db.add(kw_obj)
    #        db.flush()  # id 채워 넣기

        # 4-2) ClusterKeyword 매핑이 없으면 생성
    #    exists = (
    #        db.query(ClusterKeyword)
    #          .filter_by(cluster_id=cluster_id, keyword_id=kw_obj.id)
    #          .first()
    #    )
    #    if not exists:
    #        mapping = ClusterKeyword(
    #            cluster_id=cluster_id,
    #            keyword_id=kw_obj.id
    #        )
    #        db.add(mapping)

    # db.commit()
    
    return top_terms


def extract_keywords_per_cluster(
    texts: List[str],
    labels: List[int],
    db: Session,
    top_n: int = 3,
    max_features: int = 1000
) -> Dict[int, List[str]]:
    """
    전체 texts 와 같은 순서로 정렬된 labels 를 받아,
    클러스터별로 대표 키워드 목록을 반환.
    """
    cluster_to_docs: Dict[int, List[str]] = {}
    for text, lbl in zip(texts, labels):
        cluster_to_docs.setdefault(lbl, []).append(text)

    # 클러스터별 키워드 추출 및 DB 저장
    result: Dict[int, List[str]] = {}
    for cluster_id, docs in cluster_to_docs.items():
        # extract_top_keywords 내부에서 TF-IDF → DB 저장 → 키워드 리스트 반환
        keywords = extract_top_keywords(
            documents=docs,
            db=db,
            cluster_id=cluster_id,
            top_n=top_n,
            max_features=max_features
        )
        result[cluster_id] = keywords

    return result