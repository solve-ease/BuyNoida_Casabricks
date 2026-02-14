"""
Application settings using Pydantic Settings
"""
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    SECRET_KEY: str = Field(min_length=32)
    
    # Database
    DATABASE_URL: str = Field(...)
    SUPABASE_URL: str = Field(...)
    SUPABASE_ANON_KEY: str = Field(...)
    SUPABASE_SERVICE_KEY: str = Field(...)
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Celery
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/2")
    
    # AI Service
    AI_SERVICE_API_URL: str = Field(...)
    AI_SERVICE_API_KEY: str = Field(...)
    AI_SERVICE_WEBHOOK_SECRET: str = Field(min_length=32)
    
    # Storage
    SUPABASE_STORAGE_BUCKET: str = Field(default="property-images")
    MAX_FILE_SIZE_MB: int = Field(default=10)
    
    # Security
    JWT_SECRET_KEY: str = Field(min_length=32)
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    
    # CORS
    ALLOWED_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:5173")
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    RATE_LIMIT_INQUIRIES_PER_HOUR: int = Field(default=5)
    
    # Monitoring
    SENTRY_DSN: str = Field(default="")
    ENABLE_METRICS: bool = Field(default=True)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
