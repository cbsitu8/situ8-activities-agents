import os
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings configuration."""
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_reload: bool = Field(default=False, env="API_RELOAD")
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # OpenAI Configuration for CrewAI
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.1, env="OPENAI_TEMPERATURE")
    
    # CrewAI Configuration
    crewai_memory_enabled: bool = Field(default=True, env="CREWAI_MEMORY_ENABLED")
    crewai_verbose: bool = Field(default=True, env="CREWAI_VERBOSE")
    crewai_max_iterations: int = Field(default=3, env="CREWAI_MAX_ITERATIONS")
    
    # Analysis Configuration
    max_batch_size: int = Field(default=100, env="MAX_BATCH_SIZE")
    analysis_timeout: int = Field(default=30, env="ANALYSIS_TIMEOUT")  # seconds
    
    # Threat Assessment Thresholds
    critical_confidence_threshold: float = Field(default=0.9, env="CRITICAL_CONFIDENCE_THRESHOLD")
    high_confidence_threshold: float = Field(default=0.8, env="HIGH_CONFIDENCE_THRESHOLD")
    medium_confidence_threshold: float = Field(default=0.7, env="MEDIUM_CONFIDENCE_THRESHOLD")
    
    # False Positive Probability Thresholds
    weapon_detection_fp_rate: float = Field(default=0.05, env="WEAPON_DETECTION_FP_RATE")
    access_violation_fp_rate: float = Field(default=0.10, env="ACCESS_VIOLATION_FP_RATE")
    door_sensor_fp_rate: float = Field(default=0.25, env="DOOR_SENSOR_FP_RATE")
    system_alert_fp_rate: float = Field(default=0.35, env="SYSTEM_ALERT_FP_RATE")
    
    # Response Timeline Configuration (in minutes)
    critical_response_time: int = Field(default=2, env="CRITICAL_RESPONSE_TIME")
    high_response_time: int = Field(default=5, env="HIGH_RESPONSE_TIME")
    medium_response_time: int = Field(default=15, env="MEDIUM_RESPONSE_TIME")
    low_response_time: int = Field(default=60, env="LOW_RESPONSE_TIME")
    
    # Database Configuration (for future use)
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # Security Configuration
    api_key_required: bool = Field(default=False, env="API_KEY_REQUIRED")
    api_key: Optional[str] = Field(default=None, env="API_KEY")
    cors_origins: str = Field(default="*", env="CORS_ORIGINS")
    
    # Monitoring and Metrics
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")  # seconds
    
    # High-Risk Location Keywords
    high_risk_locations: str = Field(
        default="entrance,exit,lobby,secure,restricted,vault,server,datacenter",
        env="HIGH_RISK_LOCATIONS"
    )
    
    # Critical Threat Keywords
    critical_threat_keywords: str = Field(
        default="firearm,gun,weapon,knife,violence,assault,brandishing,forced entry,duress,panic",
        env="CRITICAL_THREAT_KEYWORDS"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def high_risk_location_list(self) -> list:
        """Get high risk locations as a list."""
        return [location.strip() for location in self.high_risk_locations.split(",")]
    
    @property
    def critical_threat_keyword_list(self) -> list:
        """Get critical threat keywords as a list."""
        return [keyword.strip() for keyword in self.critical_threat_keywords.split(",")]
    
    @property
    def cors_origins_list(self) -> list:
        """Get CORS origins as a list."""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    def validate_openai_config(self) -> bool:
        """Validate OpenAI configuration."""
        if not self.openai_api_key:
            return False
        return True
    
    def get_response_timeline_text(self, threat_level: str) -> str:
        """Get response timeline text for threat level."""
        timelines = {
            "CRITICAL": f"IMMEDIATE (within {self.critical_response_time} minutes)",
            "HIGH": f"URGENT (within {self.high_response_time} minutes)",
            "MEDIUM": f"PROMPT (within {self.medium_response_time} minutes)",
            "LOW": f"ROUTINE (within {self.low_response_time} minutes)"
        }
        return timelines.get(threat_level.upper(), f"ROUTINE (within {self.low_response_time} minutes)")

# Global settings instance
settings = Settings()

# Validation on startup
def validate_settings():
    """Validate critical settings on startup."""
    errors = []
    
    if not settings.validate_openai_config():
        errors.append("OpenAI API key is required for CrewAI functionality")
    
    if settings.api_key_required and not settings.api_key:
        errors.append("API key is required but not configured")
    
    if settings.analysis_timeout < 5:
        errors.append("Analysis timeout must be at least 5 seconds")
    
    if settings.max_batch_size < 1:
        errors.append("Max batch size must be at least 1")
    
    if errors:
        raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
    
    return True