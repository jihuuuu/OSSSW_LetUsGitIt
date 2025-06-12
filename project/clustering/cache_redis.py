import pickle
import numpy as np
import redis
from clustering.embedder import EMBEDDING_DIM

# Redis 클라이언트 연결 (호스트/포트는 환경에 맞게 조정)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

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