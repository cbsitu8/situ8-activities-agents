"""
Threat correlation management endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session

from models.database import get_db, ThreatCorrelation, BadgeHolder
from models.schemas import ThreatCorrelationResponse, ThreatStatusUpdate
from utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/threats/access-control", response_model=List[ThreatCorrelationResponse])
async def get_access_control_threats(
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all access control threat correlations"""
    try:
        query = db.query(ThreatCorrelation)
        
        if status:
            query = query.filter(ThreatCorrelation.status == status)
        
        correlations = query.order_by(ThreatCorrelation.created_at.desc()).limit(limit).all()
        
        return correlations
        
    except Exception as e:
        logger.error(f"Error getting threats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threats/access-control/{correlation_id}", response_model=ThreatCorrelationResponse)
async def get_threat_correlation(correlation_id: str, db: Session = Depends(get_db)):
    """Get detailed correlation analysis"""
    try:
        correlation = db.query(ThreatCorrelation).filter(
            ThreatCorrelation.correlation_id == correlation_id
        ).first()
        
        if not correlation:
            raise HTTPException(status_code=404, detail="Correlation not found")
        
        return correlation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting correlation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/threats/access-control/{correlation_id}/status")
async def update_threat_status(
    correlation_id: str,
    status_update: ThreatStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update threat investigation status"""
    try:
        correlation = db.query(ThreatCorrelation).filter(
            ThreatCorrelation.correlation_id == correlation_id
        ).first()
        
        if not correlation:
            raise HTTPException(status_code=404, detail="Correlation not found")
        
        correlation.status = status_update.status
        if status_update.investigation_notes:
            correlation.investigation_notes = status_update.investigation_notes
        
        db.commit()
        
        return {"success": True, "message": "Status updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating threat status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threats/stats")
async def get_threat_statistics(db: Session = Depends(get_db)):
    """Get threat correlation statistics"""
    try:
        total_threats = db.query(ThreatCorrelation).count()
        active_threats = db.query(ThreatCorrelation).filter(ThreatCorrelation.status == "active").count()
        investigating = db.query(ThreatCorrelation).filter(ThreatCorrelation.status == "investigating").count()
        resolved = db.query(ThreatCorrelation).filter(ThreatCorrelation.status == "resolved").count()
        
        return {
            "total_threats": total_threats,
            "active_threats": active_threats,
            "investigating": investigating,
            "resolved": resolved,
            "false_positives": db.query(ThreatCorrelation).filter(ThreatCorrelation.status == "false_positive").count()
        }
        
    except Exception as e:
        logger.error(f"Error getting threat stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/badge-holders")
async def get_badge_holders(db: Session = Depends(get_db)):
    """Get all badge holders"""
    try:
        badge_holders = db.query(BadgeHolder).filter(BadgeHolder.active == True).all()
        return {"badge_holders": badge_holders}
        
    except Exception as e:
        logger.error(f"Error getting badge holders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/badge-holders/{badge_id}")
async def get_badge_holder(badge_id: str, db: Session = Depends(get_db)):
    """Get specific badge holder details"""
    try:
        badge_holder = db.query(BadgeHolder).filter(BadgeHolder.badge_id == badge_id).first()
        
        if not badge_holder:
            raise HTTPException(status_code=404, detail="Badge holder not found")
        
        return badge_holder
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting badge holder: {e}")
        raise HTTPException(status_code=500, detail=str(e))