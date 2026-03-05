import os
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Celeqthor"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    API_V1_PREFIX: str = "/api/v1"
    
    # Database (PostgreSQL)
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "celebhub")
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "tiger")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-at-least-32-chars-long")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    
    # SMS (Example: SMS Country / Twilio)
    SMS_AUTH_KEY: str = os.getenv("SMS_AUTH_KEY", "")
    SMS_AUTH_TOKEN: str = os.getenv("SMS_AUTH_TOKEN", "")
    SMS_SENDER_ID: str = os.getenv("SMS_SENDER_ID", "CELEBH")

      # Monitoring
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "False").lower() == "true"
   
    HF_HUB_OFFLINE: int = os.getenv("HF_HUB_OFFLINE", 1)

    SMSCOUNTRY_AUTH_KEY: str = os.getenv("SMSCOUNTRY_AUTH_KEY", "")
    SMSCOUNTRY_AUTH_TOKEN: str = os.getenv("SMSCOUNTRY_AUTH_TOKEN", "")
    SMSCOUNTRY_SENDER_ID: str = os.getenv("SMSCOUNTRY_SENDER_ID", "CELEBH")
    
    # OTP Settings
    OTP_EXPIRE_SECONDS: int = 600  # 10 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        return f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

settings = Settings()
