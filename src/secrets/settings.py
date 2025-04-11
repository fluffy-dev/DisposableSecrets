from pydantic import BaseSettings

class SecretsConfig(BaseSettings):
    MIN_TTL_SECONDS: int = 300  # Minimum TTL of 5 minutes
    ENCRYPTION_KEY: str

secrets_settings = SecretsConfig()