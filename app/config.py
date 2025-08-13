# app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_name: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int

    class Config:  # ✅ Capital 'C'
        env_file = ".env"

settings = Settings()
