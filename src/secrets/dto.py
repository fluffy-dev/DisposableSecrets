from uuid import UUID
from pydantic import BaseModel, Field

class SecretCreateDTO(BaseModel):
    secret: str = Field(min_length=1)
    passphrase: str | None = None
    ttl_seconds: int = Field(ge=300, default=3600)

class SecretResponseDTO(BaseModel):
    secret_key: UUID

class SecretRetrieveDTO(BaseModel):
    secret: str

class SecretDeleteDTO(BaseModel):
    passphrase: str | None = None

class DeleteResponseDTO(BaseModel):
    status: str

class SecretLogDTO(BaseModel):
    id: int
    secret_key: str
    action: str
    ip_address: str
    ttl_seconds: int
    passphrase_used: str