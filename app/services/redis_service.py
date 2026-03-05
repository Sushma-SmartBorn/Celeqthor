import redis
from typing import Optional, Union
import json
import logging
from config import settings

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )

    def get(self, key: str) -> Optional[str]:
        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None

    def set(self, key: str, value: Union[str, dict, list], ttl: Optional[int] = None) -> bool:
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            if ttl:
                return self.client.setex(key, ttl, value)
            return self.client.set(key, value)
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            return False

    def delete(self, key: str) -> bool:
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")
            return False

    def check_connection(self) -> bool:
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return False

redis_service = RedisService()
