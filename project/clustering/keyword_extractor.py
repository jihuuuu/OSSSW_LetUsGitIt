# clustering/keyword_extractor.py

from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_top_keywords(
    documents: List[str],
    top_n: int = 3,
    max_features: int = 1000
) -> List[str]:
    """
    주어진 문서 리스트에 대해 TF-IDF를 계산하고,
    문서들에서 평균 TF-IDF 값이 높은 top_n 키워드를 뽑아 반환.
    """
    # 1) TF-IDF 행렬 생성
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words='english'   # 필요에 따라 한국어 불용어 처리
    )
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    # 2) 각 단어별 평균 TF-IDF 계산
    mean_tfidf = tfidf_matrix.mean(axis=0).A1  # (n_features,)

    # 3) 상위 top_n 인덱스 추출
    top_indices = mean_tfidf.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices]


def extract_keywords_per_cluster(
    texts: List[str],
    labels: List[int],
    top_n: int = 3
) -> Dict[int, List[str]]:
    """
    전체 texts 와 같은 순서로 정렬된 labels 를 받아,
    클러스터별로 대표 키워드 목록을 반환.
    """
    cluster_to_docs: Dict[int, List[str]] = {}
    for text, lbl in zip(texts, labels):
        cluster_to_docs.setdefault(lbl, []).append(text)

    return {
        lbl: extract_top_keywords(docs, top_n=top_n)
        for lbl, docs in cluster_to_docs.items()
    }
