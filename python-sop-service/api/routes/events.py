"""
Event processing endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from services.event_processor import EventProcessor
from models.database import get_db, Event, init_sample_data
from models.schemas import EventProcessingResponse
from agents.crews.tailgating import TailgatingCorrelationCrew, initialize_correlation_system
from config.settings import settings
from utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Global instances
event_processor = EventProcessor()
correlation_crew = None

# Initialize CrewAI correlation system
if settings.ENABLE_CREWAI and initialize_correlation_system():
    correlation_crew = TailgatingCorrelationCrew()
    logger.info("CrewAI correlation system initialized")
else:
    logger.warning("CrewAI correlation system not available")

@router.post("/events/process", response_model=EventProcessingResponse)
async def process_event(
    event_data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Process security events with automatic threat correlation"""
    try:
        logger.info(f"Processing event: {event_data.get('event_type')} at {event_data.get('location')}")
        
        # Parse timestamp
        timestamp_str = event_data.get('timestamp')
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except ValueError:
                timestamp = datetime.now(timezone.utc)
        else:
            timestamp = datetime.now(timezone.utc)
        
        # Extract badge_id from metadata or direct field
        badge_id = event_data.get('badge_id')
        metadata = event_data.get('metadata', {})
        if not badge_id and 'badge_id' in metadata:
            badge_id = metadata['badge_id']
        
        # Create event record
        event = Event(
            event_type=event_data['event_type'],
            timestamp=timestamp,
            location=event_data['location'],
            source=event_data.get('source', 'unknown'),
            severity=event_data.get('severity', 'Medium'),
            badge_id=badge_id,
            metadata=metadata,
            correlation_triggered=False
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        # Process event using event processor
        processing_result = await event_processor.process_event(event_data)
        
        # Prepare response
        response = EventProcessingResponse(
            success=True,
            event_id=processing_result.get("event_id", str(event.id)),
            priority=processing_result.get("priority", "Medium"),
            matched_sop=processing_result.get("matched_sop", "Processing with uploaded SOPs..."),
            confidence=processing_result.get("confidence", 0.85),
            response_time=processing_result.get("response_time", "< 2 minutes"),
            assigned_agents=processing_result.get("assigned_agents", ["Security Team", "SOC Analyst"]),
            actions_required=processing_result.get("actions_required", ["Verify incident", "Dispatch security"]),
            processed_at=datetime.now(timezone.utc).isoformat(),
            correlation_triggered=False,
            correlation_id=None
        )
        
        # Trigger CrewAI correlation for tailgating events
        if event_data.get('event_type') == 'Tailgating' and correlation_crew:
            try:
                logger.info(f"Triggering CrewAI correlation for tailgating event {event.id}")
                
                # Mark correlation as triggered
                event.correlation_triggered = True
                db.commit()
                
                # Prepare event data for CrewAI
                crew_event_data = {
                    "event_id": event.id,
                    "event_type": event.event_type,
                    "timestamp": event.timestamp.isoformat(),
                    "location": event.location,
                    "source": event.source,
                    "severity": event.severity,
                    "metadata": event.metadata
                }
                
                # Run CrewAI analysis in background
                background_tasks.add_task(
                    run_correlation_analysis,
                    crew_event_data,
                    event.id
                )
                
                response.correlation_triggered = True
                response.correlation_status = "Analysis started - check threats page for results"
                
            except Exception as correlation_error:
                logger.error(f"Correlation analysis failed: {correlation_error}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_correlation_analysis(event_data: Dict[str, Any], event_id: int):
    """Background task to run CrewAI correlation analysis"""
    try:
        logger.info(f"Starting background correlation analysis for event {event_id}")
        
        # Run CrewAI analysis
        result = correlation_crew.analyze_tailgating_event(event_data, event_id)
        
        if result["success"]:
            logger.info(f"Correlation analysis completed successfully for event {event_id}")
            if result.get("correlation_id"):
                logger.info(f"Correlation stored with ID: {result['correlation_id']}")
        else:
            logger.error(f"Correlation analysis failed for event {event_id}: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Background correlation analysis error: {e}")

@router.get("/events/recent")
async def get_recent_events(limit: int = 50, db: Session = Depends(get_db)):
    """Get recent events"""
    try:
        events = db.query(Event).order_by(Event.timestamp.desc()).limit(limit).all()
        
        return {
            "events": [
                {
                    "id": event.id,
                    "event_type": event.event_type,
                    "timestamp": event.timestamp.isoformat(),
                    "location": event.location,
                    "source": event.source,
                    "severity": event.severity,
                    "badge_id": event.badge_id,
                    "metadata": event.metadata,
                    "correlation_triggered": event.correlation_triggered
                }
                for event in events
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting recent events: {e}")
        raise HTTPException(status_code=500, detail=str(e))