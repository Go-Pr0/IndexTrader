from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "Bitcoin Dominance"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL_USER: PostgresDsn = "postgresql+psycopg://user:password@localhost:5432/userdb"
    DATABASE_URL_GENERAL: PostgresDsn = "postgresql+psycopg://user:password@localhost:5432/generaldb"


    class Config:
        case_sensitive = True


settings = Settings()
