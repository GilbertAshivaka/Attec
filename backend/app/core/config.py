from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "ATTEC API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # CORS
    FRONTEND_URL: str
    ALLOWED_ORIGINS: Union[List[str], str] = []
    
    # Email
    SENDGRID_API_KEY: str
    FROM_EMAIL: str
    FROM_NAME: str = "ATTEC"
    NOTIFICATION_EMAIL: str
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Admin
    ADMIN_EMAIL: str
    ADMIN_NAME: str = "Admin"
    ADMIN_PASSWORD: str
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()


settings = Settings()
