import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_cache(key: str):
    val = redis_client.get(key)
    return json.loads(val) if val else None

def set_cache(key: str, value, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(value))
