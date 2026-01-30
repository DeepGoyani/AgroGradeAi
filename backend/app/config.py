"""
AgroGrade AI Backend - Application Configuration
Loads settings from environment variables with validation
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ==========================================================================
    # Database
    # ==========================================================================
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/agrograde",
        description="PostgreSQL connection string"
    )
    database_url_async: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/agrograde",
        description="Async PostgreSQL connection string"
    )
    
    # ==========================================================================
    # Application
    # ==========================================================================
    app_name: str = "AgroGrade AI Engine"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    cors_origins: str = "http://localhost:5173,http://localhost:8080,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # ==========================================================================
    # Security
    # ==========================================================================
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # ==========================================================================
    # AI Models
    # ==========================================================================
    model_path: str = "./models"
    disease_model_path: str = "./models/disease_detection"
    quality_model_path: str = "./models/quality_grading"
    crop_model_path: str = "./models/crop_identification"
    
    max_image_size_mb: int = 10
    supported_image_formats: str = "jpg,jpeg,png,webp"
    
    @property
    def supported_formats_list(self) -> List[str]:
        return [fmt.strip().lower() for fmt in self.supported_image_formats.split(",")]
    
    # ==========================================================================
    # Storage
    # ==========================================================================
    upload_dir: str = "./uploads"
    
    # ==========================================================================
    # Logging
    # ==========================================================================
    log_level: str = "INFO"
    log_file: str = "./logs/agrograde.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()
