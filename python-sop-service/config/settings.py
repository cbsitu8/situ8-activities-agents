"""
Configuration settings for the SOP Processing Service
"""

import os
from typing import List

class Settings:
    """Application configuration settings"""
    
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/sop_events")
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # API Configuration
    API_TITLE: str = "SOP Processing Service"
    API_DESCRIPTION: str = "Processes SOP documents and handles semantic matching for security events with AI threat correlation"
    API_VERSION: str = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["*"]  # In production, specify exact origins
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Service Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))
    
    # Feature flags
    ENABLE_CREWAI: bool = bool(OPENAI_API_KEY)
    ENABLE_SEMANTIC_MATCHING: bool = True
    ENABLE_THREAT_CORRELATION: bool = True

settings = Settings()