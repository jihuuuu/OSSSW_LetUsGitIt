import os, numpy as np
from clustering.embedder import EMBEDDING_DIM

def load_embedding_cache(id_path: str, emb_path: str):
    if os.path.exists(id_path) and os.path.exists(emb_path):
        ids = np.load(id_path)
        embs = np.load(emb_path)
    else:
        ids = np.array([], dtype=int)
        embs = np.zeros((0, EMBEDDING_DIM))  # EMBEDDING_DIM은 사용 모델 차원
    return ids, embs

def save_embedding_cache(ids, embs, id_path: str, emb_path: str):
    np.save(id_path, ids)
    np.save(emb_path, embs)
