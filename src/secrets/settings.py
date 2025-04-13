from pydantic import Field
from pydantic_settings import BaseSettings

class SecretsConfig(BaseSettings):
    MIN_TTL_SECONDS: int = Field(300, alias="MIN_TTL_SECONDS")  # Minimum TTL of 5 minutes
    ENCRYPTION_KEY: str = Field(..., alias="ENCRYPTION_KEY")

secrets_settings = SecretsConfig()