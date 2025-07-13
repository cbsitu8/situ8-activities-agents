from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class SOPPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class SOPTimeline(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    URGENT = "URGENT"
    PROMPT = "PROMPT"
    ROUTINE = "ROUTINE"

class ResponseRequirements(BaseModel):
    timeline: str = Field(..., description="Response timeline requirement")
    notifications: List[str] = Field(default=[], description="Required notifications")
    required_actions: List[str] = Field(default=[], description="Required response actions")

class SpecialConditions(BaseModel):
    applies_to_locations: List[str] = Field(default=[], description="Applicable locations")
    applies_to_times: List[str] = Field(default=[], description="Applicable time periods")
    escalation_required: bool = Field(default=False, description="Whether escalation is required")

class ProcessedSOP(BaseModel):
    sop_id: str = Field(..., description="Unique SOP identifier")
    title: str = Field(..., description="SOP title")
    category: str = Field(..., description="SOP category")
    triggers: List[str] = Field(default=[], description="Event triggers for this SOP")
    priority_override: Optional[SOPPriority] = Field(None, description="Priority override level")
    response_requirements: ResponseRequirements = Field(..., description="Response requirements")
    special_conditions: SpecialConditions = Field(..., description="Special conditions")
    regulatory_requirements: List[str] = Field(default=[], description="Regulatory requirements")
    document_source: str = Field(..., description="Source document filename")
    processed_date: datetime = Field(default_factory=datetime.now, description="Processing timestamp")
    original_text: str = Field(..., description="Original document text")

class SOPProcessingStatus(BaseModel):
    job_id: str = Field(..., description="Processing job ID")
    status: str = Field(..., description="Processing status")
    filename: str = Field(..., description="Uploaded filename")
    file_size: int = Field(..., description="File size in bytes")
    progress: int = Field(default=0, description="Processing progress percentage")
    message: str = Field(default="", description="Status message")
    error: Optional[str] = Field(None, description="Error message if failed")
    result: Optional[ProcessedSOP] = Field(None, description="Processed SOP result")
    created_at: datetime = Field(default_factory=datetime.now, description="Job creation time")
    completed_at: Optional[datetime] = Field(None, description="Job completion time")

class SOPSearchResult(BaseModel):
    sop_id: str = Field(..., description="SOP identifier")
    title: str = Field(..., description="SOP title")
    similarity_score: float = Field(..., description="Similarity score")
    priority_override: Optional[SOPPriority] = Field(None, description="Priority override")
    response_requirements: ResponseRequirements = Field(..., description="Response requirements")
    matched_triggers: List[str] = Field(default=[], description="Matched trigger keywords")

class FileUploadResponse(BaseModel):
    job_id: str = Field(..., description="Processing job ID")
    filename: str = Field(..., description="Uploaded filename")
    file_size: int = Field(..., description="File size in bytes")
    file_type: str = Field(..., description="File type detected")
    status: str = Field(..., description="Initial status")
    message: str = Field(..., description="Response message")