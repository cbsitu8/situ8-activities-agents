"""
SOP management endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from services.sop_processor import SOPProcessor
from services.semantic_matcher import SemanticMatcher
from services.event_processor import EventProcessor
from models.database import DatabaseManager
from models.schemas import SOPUploadResponse, RuleExtractionRequest, SemanticMatchRequest, SemanticMatchResponse
from utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Global instances
sop_processor = SOPProcessor()
semantic_matcher = SemanticMatcher()
event_processor = EventProcessor()
db_manager = DatabaseManager()

@router.post("/sop/process", response_model=SOPUploadResponse)
async def process_sop_document(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None)
):
    """
    Process an uploaded SOP document and extract rules
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.endswith(('.docx', '.md', '.txt')):
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
        sop_data = await sop_processor.process_document(content, file_type, sop_name)
        
        # Store in database
        sop_id = await db_manager.store_sop(sop_data)
        
        # Extract and store rules
        rules = await sop_processor.extract_rules(sop_data['content'])
        rules_count = await db_manager.store_rules(sop_id, rules)
        
        # Generate semantic embeddings
        await semantic_matcher.generate_embeddings_for_sop(sop_id)
        
        # Also store in event processor for backward compatibility
        event_processor.add_uploaded_sop({
            "id": sop_id,
            "name": sop_name,
            "file_name": file.filename,
            "file_type": file_type,
            "upload_status": "completed",
            "rule_count": rules_count,
            "created_at": datetime.utcnow().isoformat()
        })
        
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

@router.post("/sop/extract-rules")
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

@router.post("/semantic/match", response_model=SemanticMatchResponse)
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

@router.get("/sops")
async def list_sops():
    """
    List all stored SOPs
    """
    try:
        # Get from database
        db_sops = await db_manager.get_all_sops()
        
        # Get from event processor (for backward compatibility)
        memory_sops = event_processor.get_all_sops()
        
        # Combine and deduplicate
        all_sops = db_sops + memory_sops
        
        return {"sops": all_sops}
        
    except Exception as e:
        logger.error(f"Error listing SOPs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sops/{sop_id}/rules")
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

@router.delete("/sops/{sop_id}")
async def delete_sop(sop_id: str):
    """
    Delete a SOP and all its rules
    """
    try:
        # Try to delete from database first
        try:
            await db_manager.delete_sop(sop_id)
            return {"message": "SOP deleted successfully"}
        except:
            # Fall back to event processor
            deleted_sop = event_processor.delete_sop(sop_id)
            return {
                "message": f"SOP '{deleted_sop['name']}' deleted successfully",
                "deleted_sop": deleted_sop
            }
        
    except Exception as e:
        logger.error(f"Error deleting SOP: {e}")
        raise HTTPException(status_code=500, detail=str(e))