# clustering/pipeline.py

from typing import List
from clustering.embedder import make_embeddings
from database.connection import SessionLocal
from database.sql_models import Article
import numpy as np

def fetch_all_texts(limit: int | None = None) -> List[str]:
    """
    DB에서 분석할 기사 텍스트(제목+요약)를 모두 꺼냅니다.
    limit을 주면 최근 N건만.
    """
    session = SessionLocal()
    try:
        query = session.query(Article.title, Article.summary)
        if limit:
            query = query.order_by(Article.fetched_at.desc()).limit(limit)
        rows = query.all()
        # 제목과 요약을 합쳐 하나의 텍스트로
        texts = [f"{t.title} {t.summary or ''}".strip() for t in rows]
        return texts
    finally:
        session.close()

def run_embedding_stage(limit: int | None = None, batch_size: int = 32):
    """
    1) DB에서 기사 텍스트 불러오기
    2) 임베딩 생성
    3) (선택) 파일로 저장하거나 다음 단계에 반환
    """
    texts = fetch_all_texts(limit=limit)
    if not texts:
        print("⚠️ 분석할 기사 텍스트가 없습니다.")
        return None

    print(f"▶️ {len(texts)}개 기사에 대해 임베딩 생성 시작…")
    embeddings = make_embeddings(texts, batch_size=batch_size)
    print("✅ 임베딩 생성 완료:", embeddings.shape)
    
    # 예: 파일로 저장 (옵션)
    np.save("data/article_embeddings.npy", embeddings)
    print("✅ embeddings.npy 저장 완료")

    return embeddings

if __name__ == "__main__":
    # 테스트 실행: 최근 100건
    run_embedding_stage(limit=100, batch_size=16)
