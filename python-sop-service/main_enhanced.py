"""
Enhanced SOP Processing Service with CrewAI Badge Correlation
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime, timezone
import uuid
import json
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Import our new database models and CrewAI agents
from database_new import (
    get_db, create_tables, init_sample_data,
    Event, BadgeHolder, ThreatCorrelation,
    EventCreate, EventResponse, ThreatCorrelationResponse, ThreatStatusUpdate,
    SessionLocal
)
from crew_ai_agents import TailgatingCorrelationCrew, initialize_correlation_system

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for uploaded SOPs (keeping for backward compatibility)
uploaded_sops = []

app = FastAPI(
    title="Enhanced SOP Processing Service with AI Threat Correlation",
    description="SOP processing service with CrewAI-powered tailgating correlation",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CrewAI correlation crew
correlation_crew = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting Enhanced SOP Processing Service with CrewAI...")
    
    try:
        # Create database tables
        create_tables()
        logger.info("Database tables created successfully")
        
        # Initialize sample employee data
        init_sample_data()
        logger.info("Sample employee data initialized")
        
        # Initialize CrewAI correlation system
        global correlation_crew
        if initialize_correlation_system():
            correlation_crew = TailgatingCorrelationCrew()
            logger.info("CrewAI correlation system initialized")
        else:
            logger.warning("CrewAI correlation system failed to initialize - correlation features disabled")
        
        logger.info("Enhanced service started successfully")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "enhanced-sop-service",
        "version": "2.0.0",
        "features": {
            "database": "postgresql",
            "crewai": correlation_crew is not None,
            "threat_correlation": True
        },
        "message": "Enhanced mode with AI threat correlation"
    }

# Event Processing Endpoints

@app.post("/api/v1/events/process")
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
        
        # Prepare response
        response = {
            "success": True,
            "event_id": str(uuid.uuid4()),
            "priority": "High" if event_data.get('severity') == 'Critical' else "Medium",
            "matched_sop": "Processing with uploaded SOPs...",
            "confidence": 0.85,
            "response_time": "< 2 minutes",
            "assigned_agents": ["Security Team", "SOC Analyst"],
            "actions_required": ["Verify incident", "Dispatch security"],
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "correlation_triggered": False,
            "correlation_id": None
        }
        
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
                
                response.update({
                    "correlation_triggered": True,
                    "correlation_status": "Analysis started - check threats page for results"
                })
                
            except Exception as correlation_error:
                logger.error(f"Correlation analysis failed: {correlation_error}")
                response["correlation_error"] = str(correlation_error)
        
        # Legacy SOP matching (keeping for backward compatibility)
        sop_match_result = match_event_to_sops(event_data)
        response.update(sop_match_result)
        
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

def match_event_to_sops(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy SOP matching logic"""
    event_type = event_data.get('event_type', '').lower()
    
    # Simple keyword matching
    if 'fire' in event_type or 'smoke' in event_type:
        return {
            "matched_sop": "Fire Emergency Response SOP",
            "confidence": 0.95,
            "response_time": "< 1 minute",
            "assigned_agents": ["Fire Safety Team", "Emergency Response"],
            "actions_required": ["Activate fire alarm", "Evacuate zone", "Contact fire department"]
        }
    elif 'shooter' in event_type or 'weapon' in event_type or 'firearm' in event_type:
        return {
            "matched_sop": "Active Shooter Response SOP",
            "confidence": 0.92,
            "response_time": "< 30 seconds",
            "assigned_agents": ["Security Team", "Law Enforcement"],
            "actions_required": ["Lockdown facility", "Contact law enforcement", "Evacuate if safe"]
        }
    elif 'fence' in event_type or 'perimeter' in event_type:
        return {
            "matched_sop": "Perimeter Intrusion Response SOP",
            "confidence": 0.88,
            "response_time": "< 2 minutes",
            "assigned_agents": ["Security Patrol", "SOC Analyst"],
            "actions_required": ["Dispatch patrol", "Review cameras", "Assess threat level"]
        }
    elif 'medical' in event_type or 'falling' in event_type:
        return {
            "matched_sop": "Medical Emergency Response SOP",
            "confidence": 0.90,
            "response_time": "< 1 minute",
            "assigned_agents": ["Medical Team", "Security"],
            "actions_required": ["Dispatch medical", "Secure area", "Contact emergency services"]
        }
    else:
        return {
            "matched_sop": "General Security Response SOP",
            "confidence": 0.75,
            "response_time": "< 3 minutes",
            "assigned_agents": ["Security Team"],
            "actions_required": ["Investigate incident", "Document findings"]
        }

# Threat Management API Endpoints

@app.get("/api/v1/threats/access-control", response_model=List[ThreatCorrelationResponse])
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

@app.get("/api/v1/threats/access-control/{correlation_id}", response_model=ThreatCorrelationResponse)
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

@app.post("/api/v1/threats/access-control/{correlation_id}/status")
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

@app.get("/api/v1/threats/stats")
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

# Badge Holder Management

@app.get("/api/v1/badge-holders")
async def get_badge_holders(db: Session = Depends(get_db)):
    """Get all badge holders"""
    try:
        badge_holders = db.query(BadgeHolder).filter(BadgeHolder.active == True).all()
        return badge_holders
        
    except Exception as e:
        logger.error(f"Error getting badge holders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/badge-holders/{badge_id}")
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

# Keep all existing SOP endpoints for backward compatibility
# (Reusing the existing uploaded_sops logic from main_simple.py)

@app.get("/api/v1/sops")
async def get_sops():
    """Get all uploaded SOPs"""
    try:
        return {"sops": uploaded_sops}
    except Exception as e:
        logger.error(f"Error getting SOPs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sop/process")
async def process_sop(file: UploadFile = File(...)):
    """Process uploaded SOP document"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="File name is required")
        
        content = await file.read()
        
        # Basic SOP processing
        sop_data = {
            "id": str(uuid.uuid4()),
            "name": file.filename.replace('.docx', '').replace('.md', '').replace('_', ' ').title(),
            "filename": file.filename,
            "content": content.decode('utf-8', errors='ignore') if content else "",
            "file_type": "docx" if file.filename.endswith('.docx') else "markdown",
            "upload_status": "completed",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        uploaded_sops.append(sop_data)
        logger.info(f"Processing SOP: {file.filename} ({len(content)} bytes)")
        
        return {
            "success": True,
            "sop_id": sop_data["id"],
            "name": sop_data["name"],
            "message": "SOP processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing SOP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional existing endpoints would be added here...
# (Keeping this focused on the core threat correlation functionality)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)