import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseSettings, AnyHttpUrl, validator
from loguru import logger

# Ensure the logs directory exists
Path("logs").mkdir(exist_ok=True)

class Settings(BaseSettings):
    # Application settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ML Models
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Storage
    CHROMA_DB_PATH: str = "./chroma_db"
    
    # File paths
    DATA_DIR: str = "./data"
    RAW_DATA_DIR: str = "./data/raw"
    PROCESSED_DATA_DIR: str = "./data/processed"
    INDEXED_DATA_DIR: str = "./data/indexed"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Initialize settings
settings = Settings()

def configure_logging():
    """Configure application logging"""
    logger.add(
        "logs/application.log",
        rotation="10 MB",
        retention="30 days",
        level="DEBUG" if settings.DEBUG else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Disable uvicorn access logs in production
    if not settings.DEBUG:
        logger.disable("uvicorn.access")
    
    return logger

# Initialize logger
logger = configure_logging()

# Ensure all required directories exist
for directory in [
    settings.DATA_DIR,
    settings.RAW_DATA_DIR,
    settings.PROCESSED_DATA_DIR,
    settings.INDEXED_DATA_DIR,
    os.path.dirname(settings.CHROMA_DB_PATH)
]:
    os.makedirs(directory, exist_ok=True)
