from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/clique_db"
    shopify_api_key: str = ""
    shopify_api_secret: str = ""
    frontend_url: str = "http://localhost:3000"
    secret_key: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"


settings = Settings()
