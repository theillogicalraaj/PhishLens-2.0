import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "PhishLens")
    version: str = os.getenv("APP_VERSION", "2.0.0")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./phishlens.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me-before-production")
    jwt_algorithm: str = "HS256"
    token_minutes: int = int(os.getenv("TOKEN_MINUTES", "120"))
    cors_origins: tuple[str, ...] = tuple(x.strip() for x in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174"
    ).split(",") if x.strip())

settings = Settings()
