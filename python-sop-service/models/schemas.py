"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

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

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    service: str
    version: str
    features: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class EventProcessingResponse(BaseModel):
    success: bool
    event_id: str
    priority: str
    matched_sop: str
    confidence: float
    response_time: str
    assigned_agents: List[str]
    actions_required: List[str]
    processed_at: str
    correlation_triggered: bool
    correlation_id: Optional[str] = None
    correlation_status: Optional[str] = None