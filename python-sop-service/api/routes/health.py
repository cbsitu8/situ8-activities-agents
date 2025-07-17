"""
Health check endpoints
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any

from config.settings import settings
from config.database import get_db_connection
from models.schemas import HealthCheckResponse
from utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = await get_db_connection()
        await conn.fetchval("SELECT 1")
        await conn.close()
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            service="python-sop-service",
            version=settings.API_VERSION,
            features={
                "database": "postgresql",
                "crewai": settings.ENABLE_CREWAI,
                "semantic_matching": settings.ENABLE_SEMANTIC_MATCHING,
                "threat_correlation": settings.ENABLE_THREAT_CORRELATION
            },
            message="Service running with enhanced threat correlation capabilities"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")