"""Application configuration using Pydantic Settings V2"""
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = Field(default="Apple Online Store")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)
    
    # Database
    database_url: str = Field(default="sqlite:///./data/apple_store.db")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production")
    
    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080)
    
    # File uploads
    upload_directory: str = Field(default="./app/static/images")
    max_file_size: int = Field(default=10 * 1024 * 1024)  # 10MB

settings = Settings()