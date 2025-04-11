from fastapi import Depends
from typing import Annotated

from src.cache.redis_client import get_cache_client
from src.cache.interface import CacheClientInterface

IClient = Annotated[CacheClientInterface, Depends(get_cache_client)]
