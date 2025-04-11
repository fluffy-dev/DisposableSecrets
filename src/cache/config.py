from pydantic import Field, RedisDsn, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = Field(default="localhost", alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, alias="REDIS_PORT")
    REDIS_DB: int = Field(default=1, alias="REDIS_DB")


    @computed_field(return_type=RedisDsn) # type: ignore[misc]
    @property
    def redis_url(self) -> str:
        """Redis connection URL."""
        return str(RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_DB}"
        ))


settings = Settings()
