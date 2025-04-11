from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

@dataclass
class SecretEntity:
    key: UUID
    value: str
    passphrase: Optional[str]
    ttl_seconds: int

@dataclass
class SecretLogEntity:
    secret_key: str
    action: str
    ip_address: str
    ttl_seconds: Optional[int]
    passphrase_used: Optional[str]