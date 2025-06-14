import json
import os
from redis import Redis
from api.config import settings

redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def get_cache(key: str):
    val = redis_client.get(key)
    return json.loads(val) if val else None

def set_cache(key: str, value, ttl: int = 3600):
    json_str = json.dumps(value, ensure_ascii=False)
    redis_client.setex(key, ttl, json_str)

def delete_cache(key: str):
    redis_client.delete(key)