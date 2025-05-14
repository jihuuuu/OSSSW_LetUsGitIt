# clustering/embedder.py

import re
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

# 1) 전역에서 한 번만 모델 로딩
_MODEL_NAME = "all-MiniLM-L6-v2"  # 가벼우면서 성능 좋은 SBERT 모델
_model: SentenceTransformer | None = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model

# 2) 간단 전처리: 소문자화, 특수문자 제거
def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)          # URL 제거
    text = re.sub(r"[^a-z0-9가-힣\s]", " ", text)  # 특수문자 제거 (한글+영문+숫자만 남김)
    text = re.sub(r"\s+", " ", text).strip()     # multiple space -> single
    return text

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
    # 전처리
    cleaned = [preprocess_text(t) for t in texts]

        # 전처리 결과 샘플 10개만 출력
    print("── 전처리된 텍스트 샘플 ──")
    for t in cleaned[:10]:
        print("-", t)
    print("───────────────────────")
    # 모델에 batch 단위로 전달
    embeddings = model.encode(cleaned, batch_size=batch_size, show_progress_bar=True)
    return np.array(embeddings)
