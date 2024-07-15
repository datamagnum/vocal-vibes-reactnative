from typing import Annotated, Any, List, Literal, Optional

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    AUTHORIZED_API_KEY: str = "xyz"

    SECRET_KEY: str = "mysupersecretkey"
    REFRESH_TOKEN_SECRET_KEY: str = "mysupersecretkey2"

    ACCESS_TOKEN_EXPIRY_TIME: int = 30 * 24 * 60  # In minutes
    REFRESH_TOKEN_EXPIRY_TIME: int = 365 * 24 * 60  # In minutes

    ALGORITHM: str = "HS256"

    ALLOWED_ORIGINS: Optional[str] = None

    PROJECT_NAME: str = "VocalVibe-Backend"
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "vocalvibe"

    GOOGLE_SSO_CLIENT_ID: str = ""

    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def allowed_origins_list(self) -> List[str]:
        return self.ALLOWED_ORIGINS.split(",") if self.ALLOWED_ORIGINS else ["*"]


settings = Settings()  # type: ignore
