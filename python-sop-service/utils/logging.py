"""
Logging configuration for the application
"""

import logging
import sys
from typing import Optional
from config.settings import settings

def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Setup application logging
    
    Args:
        log_level: Optional log level override
    
    Returns:
        Configured logger
    """
    level = log_level or settings.LOG_LEVEL
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Get application logger
    logger = logging.getLogger("sop-service")
    
    # Set specific log levels for different components
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("crewai").setLevel(logging.INFO)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)