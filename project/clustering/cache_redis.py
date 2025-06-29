import pickle
import numpy as np
import redis
from clustering.embedder import EMBEDDING_DIM
import os

# 환경변수에서 호스트·포트 읽기 (없으면 로컬 기본값)
REDIS_HOST = os.getenv("REDIS_HOST", "${import.meta.env.VITE_API_URL}/")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB   = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def load_embedding_cache(topic: str):
    """
    Redis에서 임베딩 캐시 로드.
    key: f"emb:{topic}"
    field: article_id (bytes)
    value: pickle-serialized numpy array
    """
    key = f"emb:{topic}"
    raw = redis_client.hgetall(key)
    if not raw:
        return np.array([], dtype=int), np.zeros((0, EMBEDDING_DIM))

    ids = np.array([int(k) for k in raw.keys()], dtype=int)
    embs = np.vstack([pickle.loads(v) for v in raw.values()])
    return ids, embs


def save_embedding_cache(ids: np.ndarray, embs: np.ndarray, topic: str, ttl: int = 86400):
    """
    Redis에 임베딩 캐시 저장. 기본 TTL=24시간
    """
    key = f"emb:{topic}"
    pipe = redis_client.pipeline()
    for aid, emb in zip(ids, embs):
        pipe.hset(key, str(int(aid)), pickle.dumps(emb))
    pipe.expire(key, ttl)
    pipe.execute()