from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "Wavereplay Video API"
    ENVIRONMENT: str = "development"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
    ]

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    JWT_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()
