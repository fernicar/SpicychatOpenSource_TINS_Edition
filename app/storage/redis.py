import redis
import json
import os
from typing import Optional

# Redis client configuration
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),  # Redis server address
    port=os.getenv("REDIS_PORT", 6379),        # Redis port
    db=os.getenv("REDIS_DB", 0),            # DB number to use
    decode_responses=True  # Decode responses automatically
)

def get_session(session_id: str):
    data = redis_client.get(session_id)
    return json.loads(data) if data else {}

def save_session(session_id: str, session: dict):
    redis_client.set(session_id, json.dumps(session))
