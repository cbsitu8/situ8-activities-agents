"""
SOP Processing Service - FastAPI Application
Handles SOP document processing, rule extraction, and semantic matching
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncpg
import os
import json
import logging
from datetime import datetime

from sop_processor import SOPProcessor
from semantic_matcher_simple import SemanticMatcher
from database import get_db_connection, DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SOP Processing Service",
    description="Processes SOP documents and handles semantic matching for security events",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
sop_processor = SOPProcessor()
semantic_matcher = SemanticMatcher()
db_manager = DatabaseManager()

# Pydantic models
class SOPUploadResponse(BaseModel):
    sop_id: str
    name: str
    status: str
    message: str
    rules_extracted: int

class RuleExtractionRequest(BaseModel):
    sop_content: str
    sop_name: str

class SemanticMatchRequest(BaseModel):
    event_text: str
    confidence_threshold: float = 0.8

class SemanticMatchResponse(BaseModel):
    matched: bool
    confidence: float
    matched_rule_id: Optional[str] = None
    matched_phrase: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting SOP Processing Service...")
    # Skip database initialization for now
    # await db_manager.initialize()
    logger.info("Service started successfully")

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        async with get_db_connection() as conn:
            await conn.fetchval("SELECT 1")
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "python-sop-service",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.post("/api/v1/sop/process", response_model=SOPUploadResponse)
async def process_sop_document(
    file: UploadFile = File(...),
    name: Optional[str] = None
):
    """
    Process an uploaded SOP document and extract rules
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.docx', '.md', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="Only .docx, .md, and .txt files are supported"
            )
        
        # Read file content
        content = await file.read()
        file_type = file.filename.split('.')[-1]
        sop_name = name or file.filename
        
        logger.info(f"Processing SOP: {sop_name} ({file_type})")
        
        # Process the document
        sop_data = await sop_processor.process_document(
            content, file_type, sop_name
        )
        
        # Store in database
        sop_id = await db_manager.store_sop(sop_data)
        
        # Extract and store rules
        rules = await sop_processor.extract_rules(sop_data['content'])
        rules_count = await db_manager.store_rules(sop_id, rules)
        
        # Generate semantic embeddings
        await semantic_matcher.generate_embeddings_for_sop(sop_id)
        
        logger.info(f"Successfully processed SOP {sop_name}: {rules_count} rules extracted")
        
        return SOPUploadResponse(
            sop_id=sop_id,
            name=sop_name,
            status="completed",
            message=f"Successfully processed. {rules_count} rules extracted.",
            rules_extracted=rules_count
        )
        
    except Exception as e:
        logger.error(f"Error processing SOP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sop/extract-rules")
async def extract_rules_from_text(request: RuleExtractionRequest):
    """
    Extract rules from SOP text content
    """
    try:
        rules = await sop_processor.extract_rules(request.sop_content)
        
        return {
            "rules": rules,
            "count": len(rules)
        }
        
    except Exception as e:
        logger.error(f"Error extracting rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/semantic/match", response_model=SemanticMatchResponse)
async def semantic_match(request: SemanticMatchRequest):
    """
    Perform semantic matching against stored embeddings
    """
    try:
        result = await semantic_matcher.match_event(
            request.event_text, 
            request.confidence_threshold
        )
        
        return SemanticMatchResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in semantic matching: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/sops")
async def list_sops():
    """
    List all stored SOPs
    """
    try:
        sops = await db_manager.get_all_sops()
        return {"sops": sops}
        
    except Exception as e:
        logger.error(f"Error listing SOPs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/sops/{sop_id}/rules")
async def get_sop_rules(sop_id: str):
    """
    Get rules for a specific SOP
    """
    try:
        rules = await db_manager.get_sop_rules(sop_id)
        return {"rules": rules}
        
    except Exception as e:
        logger.error(f"Error getting SOP rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/sops/{sop_id}")
async def delete_sop(sop_id: str):
    """
    Delete a SOP and all its rules
    """
    try:
        await db_manager.delete_sop(sop_id)
        return {"message": "SOP deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting SOP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/csv/load")
async def load_csv_events(file: UploadFile = File(...)):
    """
    Load events from CSV file for testing
    """
    try:
        content = await file.read()
        
        # Determine CSV type from filename
        if "ComputerVision" in file.filename:
            events = await db_manager.load_computer_vision_csv(content.decode())
        elif "AccessControl" in file.filename:
            events = await db_manager.load_access_control_csv(content.decode())
        else:
            raise HTTPException(
                status_code=400, 
                detail="Unknown CSV format. Expected ComputerVision or AccessControl"
            )
        
        return {
            "message": f"Successfully loaded {len(events)} events",
            "events_loaded": len(events)
        }
        
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)