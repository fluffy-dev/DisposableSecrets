from pydantic import PostgresDsn, Field, computed_field
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # --- PostgreSQL ---
    DB_HOST: str = Field("localhost", alias="DB_HOST")
    DB_PORT: int = Field(5432, alias="DB_PORT")
    DB_USER: str = Field("postgre", alias="DB_USER")
    DB_PASSWORD: str = Field(..., alias="DB_PASSWORD")
    DB_NAME: str = Field("secrets_db", alias="DB_NAME")

    DB_ECHO_LOG: bool = Field(True, description="If True, SQLAlchemy logs SQL queries", alias="DB_ECHO_LOG")
    DB_RUN_AUTO_MIGRATE: bool = Field(False, alias="DB_RUN_AUTO_MIGRATE")

    @computed_field(return_type=PostgresDsn)
    @property
    def database_url(self) -> str:
        """Asynchronous Database connection URL."""
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME}",
        ))


settings = Settings()
