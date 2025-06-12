# clustering/embedder.py

import re
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
from konlpy.tag import Okt
from sklearn.preprocessing import normalize

# 불용어 리스트 (초안)
STOPWORDS_KO = {
    "저", "나", "우리", "그", "것", "수", "등", "더", "안", "잘", 
    "그리고", "하지만", "그래서", "또한", "때문", "있다", "없다", "하다", 
    "되다", "대다", "잊다", "오늘", "바꾸다", "이다", "키우다", "만들다", 
    "늘다", "오다", "보다", "기자", "가다", "연합뉴스", "포토"
}

EMBEDDING_DIM = 768

# 1) 전역에서 한 번만 모델 로딩
_MODEL_NAME = "jhgan/ko-sbert-sts" 
_model: SentenceTransformer | None = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model

# KoNLPy Okt 토크나이저
_okt = Okt()

# 2) 간단 전처리: 소문자화, 특수문자 제거
def preprocess_text(text: str) -> str:
    # 1) 기본 정제
    text = re.sub(r'<[^>]+>', '', text)
    text = text.lower()
    text = re.sub(r"http\S+", "", text)          # URL 제거
    text = re.sub(r"[^a-z0-9가-힣\s]", " ", text)  # 특수문자 제거 (한글+영문+숫자만 남김)
    text = re.sub(r"\s+", " ", text).strip()     # multiple space -> single
    # 2) 형태소 분석
    morphs = _okt.pos(text, norm=True, stem=True)
    # 3) 의미 있는 품사만 (명사, 동사, 형용사 등)
    tokens = [
        word for word, pos in morphs
        if pos in ("Noun", "Verb", "Adjective")
        and word not in STOPWORDS_KO
    ]

    # 4) 다시 문자열로
    clean = " ".join(tokens)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


# 3) 임베딩 배치 생성 함수
def make_embeddings(
    texts: List[str],
    batch_size: int = 32,
) -> np.ndarray:
    """
    입력된 텍스트 리스트를 SBERT 임베딩 벡터(NxD)로 반환합니다.
    내부에서 전처리(preprocess_text)를 먼저 수행합니다.
    """
    model = _get_model()

    # 모델에 batch 단위로 전달
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True)

    # 정규화
    embeddings = normalize(embeddings, norm="l2")

    return np.array(embeddings)
