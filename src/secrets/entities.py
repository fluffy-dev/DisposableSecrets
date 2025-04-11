from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

@dataclass
class Secret:
    key: UUID
    value: str
    passphrase: Optional[str]
    ttl_seconds: int

@dataclass
class SecretLog:
    id: Optional[int]
    secret_key: str
    action: str
    timestamp: datetime
    ip_address: str
    ttl_seconds: Optional[int]
    passphrase_used: Optional[str]