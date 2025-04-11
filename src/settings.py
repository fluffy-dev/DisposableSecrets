from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    host: str = Field(alias="APP_HOST")
    port: int = Field(alias="APP_PORT")
    debug: bool = Field(default=False, alias="APP_DEBUG")



settings = Settings()
