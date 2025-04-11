from typing import Any
import json
from redis.asyncio import Redis
from redis.exceptions import RedisError
from src.cache.config import settings as redis_settings
from src.cache.exceptions import CacheConnectionError
from src.cache.interface import CacheClientInterface


class RedisCacheClient(CacheClientInterface):
    """Redis cache client for storing and retrieving data."""

    def __init__(self, redis_url: str):
        self._client: Redis | None = None
        self._redis_url = redis_url

    async def connect(self) -> None:
        """Establish connection to Redis."""
        if self._client:
            return
        try:
            self._client = Redis.from_url(
                self._redis_url, encoding="utf-8", decode_responses=True
            )
            await self._client.ping()
        except RedisError as e:
            self._client = None
            raise CacheConnectionError("Failed to connect to Redis") from e

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _get_client(self) -> Redis:
        """Return connected Redis client, reconnecting if necessary."""
        if not self._client:
            await self.connect()
        return self._client

    async def get(self, key: str) -> Any | None:
        """Retrieve value by key, deserializing JSON if applicable."""
        if not key:
            return None
        client = await self._get_client()
        try:
            value = await client.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except RedisError:
            return None

    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        """Store value by key, serializing to JSON if needed."""
        if not key:
            return
        client = await self._get_client()
        try:
            if isinstance(value, (dict, list)):
                value_to_store = json.dumps(value)
            elif isinstance(value, (str, int, float, bool)):
                value_to_store = value
            else:
                value_to_store = str(value)
            await client.set(key, value_to_store, ex=expire)
        except RedisError:
            pass  # Treat as cache miss

    async def delete(self, key: str) -> int:
        """Delete a key and return the number of keys deleted."""
        if not key:
            return 0
        client = await self._get_client()
        try:
            return await client.delete(key)
        except RedisError:
            return 0

    async def get_and_delete(self, key: str) -> Any | None:
        """Atomically get and delete a key."""
        if not key:
            return None
        client = await self._get_client()
        try:
            value = await client.getdel(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except RedisError:
            return None


_cache_client = RedisCacheClient(str(redis_settings.redis_url)) if redis_settings.redis_url else None


def get_cache_client() -> RedisCacheClient:
    """FastAPI dependency to provide Redis cache client."""
    if _cache_client is None:
        raise CacheConnectionError("Redis cache client is not configured")
    return _cache_client