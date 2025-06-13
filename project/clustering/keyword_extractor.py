# clustering/keyword_extractor.py

from typing import List, Dict
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from models.scrap import PKeyword
from clustering.embedder import STOPWORDS_KO
from models.article import Keyword, ClusterKeyword
from collections import Counter
from itertools import chain
from konlpy.tag import Okt

def extract_top_keywords(
    documents: List[str], cluster_id : int,
    top_n: int = 3, max_features: int = 300,
    global_vectorizer: TfidfVectorizer = None
) -> List[str]:
    """
    주어진 문서 리스트에 대해 TF-IDF를 계산하고,
    문서들에서 평균 TF-IDF 값이 높은 top_n 키워드를 뽑아 반환.
    """
    # ✅ 방어 로직
    if not documents or all(not doc.strip() for doc in documents):
        print(f"⚠️ cluster_id={cluster_id}: 전처리된 문서가 모두 공백입니다. 키워드 추출 생략.")
        return ["no_keyword"]
    
    if global_vectorizer is None:
        raise ValueError("글로벌 IDF를 반영하려면 'global_vectorizer' 인자를 반드시 제공해야 합니다.")
    
    # 1) 로컬 TF × 글로벌 IDF
    tfidf_matrix = global_vectorizer.transform(documents)
    feature_names = global_vectorizer.get_feature_names_out()

    # 2) 각 단어별 평균 TF-IDF 계산
    #    (docs 수만큼 normalize 된 로컬 TF × 글로벌 IDF 스코어)
    mean_tfidf = tfidf_matrix.mean(axis=0).A1  # (n_features,)

    # 3) 상위 top_n 인덱스 추출
    n_feats = len(feature_names)
    n_pick  = min(top_n, n_feats)
    top_indices = mean_tfidf.argsort()[::-1][:n_pick]
    top_terms   = [feature_names[i] for i in top_indices]

    return top_terms


def extract_keywords_per_cluster(
    texts: List[str],
    labels: List[int],
    db: Session,
    top_n: int = 10,
    n_rep: int = 3,
    max_features: int = 300
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
        # TF-IDF 기반으로 top_n 키워드를 뽑아 반환
        kws = extract_top_keywords(
            documents=docs,
            db=db,
            cluster_id=cluster_id,
            top_n=top_n,
            max_features=max_features
        )
        # 상위 top_n개만 대표 키워드로 사용
        result[cluster_id] = kws[:top_n]


    return result

def generate_candidates(
    docs: List[str],
    min_freq: int = 3,
    ngram_range: tuple[int, int] = (1, 2)
) -> List[str]:
    """
    문서 리스트(docs)에서 키워드 후보들을 추출해 반환.
    
    Args:
        docs: 전처리된 문장들의 리스트
        min_freq: 후보로 남길 최소 등장 빈도
        ngram_range: (최소 n-gram, 최대 n-gram), ex) (1,2)는 unigram+bigram
    
    Returns:
        등장 빈도 기준으로 필터링된 후보 키워드 리스트
    """
    okt = Okt()
    # 1) 형태소 분석으로 문서별 명사 리스트 생성
    docs_nouns = [okt.nouns(doc) for doc in docs]
    
    # 2) unigram(단어) 후보
    unigrams = list(chain.from_iterable(docs_nouns))
    uni_counts = Counter(unigrams)
    candidates = [
        token for token, cnt in uni_counts.items()
        if cnt >= min_freq and len(token) > 2
    ]
    
    nmin, nmax = ngram_range
    for n in range(max(2, nmin), nmax + 1):
        ng_list = []
        for nouns in docs_nouns:
            for i in range(len(nouns) - n + 1):
                tokens = nouns[i : i + n]
                # 각 토큰이 2자 이상일 때만
                if all(len(tok) > 1 for tok in tokens):
                    phrase = "".join(tokens)
                    ng_list.append(phrase)
        ng_counts = Counter(ng_list)
        for phrase, cnt in ng_counts.items():
            if cnt >= min_freq and len(phrase) > 3:
                candidates.append(phrase)
    
    # 4) 중복 제거 후 반환
    #    (순서는 빈도순 유지하려면 추가 로직 필요)
    return list(dict.fromkeys(candidates))

def extract_keywords_per_article(documents: List[str], top_n: int = 3, max_features: int = 300) -> List[List[str]]:
    """
    여러 기사에 대해 각각의 top_n 키워드를 추출해서 리스트로 반환.
    전체 문서를 기준으로 TF-IDF 모델을 학습한 후, 각 기사에 적용함.
    """
    vectorizer = TfidfVectorizer(
        stop_words=list(STOPWORDS_KO),
        max_features=max_features,
        min_df=0.02
    )
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    top_keywords_list = []
    for i in range(tfidf_matrix.shape[0]):
        tfidf_vector = tfidf_matrix[i].toarray().flatten()
        top_indices = tfidf_vector.argsort()[::-1][:top_n]
        top_terms = [feature_names[j] for j in top_indices if tfidf_vector[j] > 0]
        top_keywords_list.append(top_terms if top_terms else ["no_keyword"])

    return top_keywords_list

# 각 키워드마다 점수 계산: 중요도 점수 = alpha * count + (1 - alpha) * 연결 수
def get_top_keywords(pkeywords: List[PKeyword], alpha: float = 0.7, limit: int = 20) -> List[PKeyword]:
    """
    count (사용자 관심도)와 연결 수 (콘텐츠 연관도)를 조합하여 상위 키워드 선정
    """
    def score(pk: PKeyword):
        count_score = pk.count
        connection_score = len(pk.connections) if hasattr(pk, "connections") else 0
        return alpha * count_score + (1 - alpha) * connection_score
    
    # 점수 기준 정렬 후 상위 limit개 선택
    sorted_keywords = sorted(pkeywords, key=score, reverse=True)
    return sorted_keywords[:limit]
