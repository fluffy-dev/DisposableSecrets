from typing import Any
from abc import ABC, abstractmethod


# --- Cache Interface ---
class CacheClientInterface(ABC):
    """Abstract base class defining the interface for a cache client."""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Retrieve an item from the cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        """Store an item in the cache with an optional expiration time (in seconds)."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> int:
        """Delete one or more keys from the cache. Returns number of keys deleted."""
        pass

    @abstractmethod
    async def get_and_delete(self, key: str) -> Any | None:
        """Atomically retrieve and delete an item."""
        pass

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the cache server."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the cache server."""
        pass