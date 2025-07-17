"""
Database models combining both async and sync database operations
"""

import os
import uuid
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from pydantic import BaseModel
import asyncpg

from config.database import Base, get_db_connection, SessionLocal

logger = logging.getLogger(__name__)

# SQLAlchemy Models for structured data

class BadgeHolder(Base):
    """Employee badge holder information"""
    __tablename__ = "badge_holders"
    
    id = Column(Integer, primary_key=True, index=True)
    badge_id = Column(String, unique=True, index=True, nullable=False)
    employee_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    access_level = Column(String, nullable=False)  # Employee, Manager, Admin
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship to events
    badge_events = relationship("Event", back_populates="badge_holder", foreign_keys="Event.badge_id")

class Event(Base):
    """Security events table"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    location = Column(String, nullable=False)
    source = Column(String, nullable=False)  # computer_vision, access_control
    severity = Column(String, nullable=False)
    badge_id = Column(String, ForeignKey("badge_holders.badge_id"), nullable=True, index=True)
    
    # Additional metadata stored as JSON
    metadata = Column(JSON, nullable=True)
    
    # Processing information
    processed_at = Column(DateTime, default=func.now())
    correlation_triggered = Column(Boolean, default=False)
    
    # Relationships
    badge_holder = relationship("BadgeHolder", back_populates="badge_events", foreign_keys=[badge_id])
    correlations = relationship("ThreatCorrelation", back_populates="tailgating_event")

class ThreatCorrelation(Base):
    """AI-generated threat correlations for tailgating events"""
    __tablename__ = "threat_correlations"
    
    id = Column(Integer, primary_key=True, index=True)
    correlation_id = Column(String, unique=True, index=True, nullable=False)
    
    # Source tailgating event
    tailgating_event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    # Correlation analysis
    correlated_badge_events = Column(JSON, nullable=True)  # List of badge event IDs and details
    analysis_summary = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    risk_level = Column(String, nullable=False)  # Low, Medium, High, Critical
    
    # Investigation status
    status = Column(String, default="active", nullable=False)  # active, investigating, resolved, false_positive
    investigation_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # AI agent details
    agent_analysis = Column(JSON, nullable=True)  # Detailed analysis from each agent
    
    # Relationships
    tailgating_event = relationship("Event", back_populates="correlations")

# Pydantic models for API

class BadgeHolderResponse(BaseModel):
    id: int
    badge_id: str
    employee_name: str
    department: str
    access_level: str
    active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    event_type: str
    timestamp: datetime
    location: str
    source: str
    severity: str
    badge_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EventResponse(BaseModel):
    id: int
    event_type: str
    timestamp: datetime
    location: str
    source: str
    severity: str
    badge_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    processed_at: datetime
    correlation_triggered: bool
    badge_holder: Optional[BadgeHolderResponse] = None
    
    class Config:
        from_attributes = True

class ThreatCorrelationResponse(BaseModel):
    id: int
    correlation_id: str
    tailgating_event_id: int
    correlated_badge_events: Optional[List[Dict[str, Any]]] = None
    analysis_summary: str
    confidence_score: float
    risk_level: str
    status: str
    investigation_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    agent_analysis: Optional[Dict[str, Any]] = None
    tailgating_event: Optional[EventResponse] = None
    
    class Config:
        from_attributes = True

class ThreatStatusUpdate(BaseModel):
    status: str
    investigation_notes: Optional[str] = None

# Database Manager for mixed async/sync operations

class DatabaseManager:
    """
    Manages database operations combining both async and sync functionality
    """
    
    def __init__(self):
        pass
    
    async def initialize(self):
        """Initialize database connection and verify tables"""
        try:
            conn = await get_db_connection()
            try:
                await conn.fetchval("SELECT 1")
                logger.info("Database connection established")
            finally:
                await conn.close()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def store_sop(self, sop_data: Dict[str, Any]) -> str:
        """Store SOP document in database"""
        try:
            conn = await get_db_connection()
            try:
                sop_id = str(uuid.uuid4())
                
                await conn.execute("""
                    INSERT INTO sops (id, name, file_name, content, file_type, upload_status, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """, 
                sop_id,
                sop_data['name'],
                sop_data.get('file_name', sop_data['name']),
                sop_data['content'],
                sop_data['file_type'],
                'completed',
                datetime.utcnow(),
                datetime.utcnow()
                )
                
                logger.info(f"Stored SOP with ID: {sop_id}")
                return sop_id
                
            finally:
                await conn.close()
        except Exception as e:
            logger.error(f"Error storing SOP: {e}")
            raise
    
    async def store_rules(self, sop_id: str, rules: List[Dict[str, Any]]) -> int:
        """Store extracted rules for a SOP"""
        try:
            conn = await get_db_connection()
            try:
                rules_stored = 0
                
                for rule in rules:
                    rule_id = str(uuid.uuid4())
                    
                    await conn.execute("""
                        INSERT INTO rules (id, sop_id, rule_type, rule_value, priority, agent_assignments, created_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    rule_id,
                    sop_id,
                    rule['rule_type'],
                    json.dumps(rule['rule_value']),
                    rule['priority'],
                    rule['agent_assignments'],
                    datetime.utcnow()
                    )
                    
                    rules_stored += 1
                
                logger.info(f"Stored {rules_stored} rules for SOP {sop_id}")
                return rules_stored
                
            finally:
                await conn.close()
        except Exception as e:
            logger.error(f"Error storing rules: {e}")
            raise
    
    async def get_all_sops(self) -> List[Dict[str, Any]]:
        """Get all stored SOPs"""
        try:
            conn = await get_db_connection()
            try:
                rows = await conn.fetch("""
                    SELECT id, name, file_name, file_type, upload_status, created_at,
                           (SELECT COUNT(*) FROM rules WHERE sop_id = sops.id) as rule_count
                    FROM sops
                    ORDER BY created_at DESC
                """)
                
                return [dict(row) for row in rows]
                
            finally:
                await conn.close()
        except Exception as e:
            logger.error(f"Error getting SOPs: {e}")
            raise
    
    async def get_sop_rules(self, sop_id: str) -> List[Dict[str, Any]]:
        """Get all rules for a specific SOP"""
        try:
            conn = await get_db_connection()
            try:
                rows = await conn.fetch("""
                    SELECT id, rule_type, rule_value, priority, agent_assignments, created_at
                    FROM rules
                    WHERE sop_id = $1
                    ORDER BY priority DESC, created_at
                """, sop_id)
                
                rules = []
                for row in rows:
                    rule = dict(row)
                    rule['rule_value'] = json.loads(rule['rule_value'])
                    rules.append(rule)
                
                return rules
                
            finally:
                await conn.close()
        except Exception as e:
            logger.error(f"Error getting SOP rules: {e}")
            raise
    
    async def delete_sop(self, sop_id: str):
        """Delete a SOP and all its rules"""
        try:
            conn = await get_db_connection()
            try:
                await conn.execute("DELETE FROM sops WHERE id = $1", sop_id)
                logger.info(f"Deleted SOP {sop_id}")
            finally:
                await conn.close()
        except Exception as e:
            logger.error(f"Error deleting SOP: {e}")
            raise

def init_sample_data():
    """Initialize sample badge holder data"""
    db = SessionLocal()
    try:
        # Check if sample data already exists
        if db.query(BadgeHolder).count() > 0:
            logger.info("Sample data already exists")
            return
        
        # Create sample badge holders
        sample_employees = [
            {
                "badge_id": "BADGE-1234",
                "employee_name": "John Smith",
                "department": "Security",
                "access_level": "Employee"
            },
            {
                "badge_id": "BADGE-4521",
                "employee_name": "Sarah Johnson",
                "department": "IT",
                "access_level": "Manager"
            },
            {
                "badge_id": "BADGE-7890",
                "employee_name": "Mike Davis",
                "department": "Finance",
                "access_level": "Manager"
            },
            {
                "badge_id": "BADGE-2468",
                "employee_name": "Lisa Chen",
                "department": "IT",
                "access_level": "Admin"
            },
            {
                "badge_id": "BADGE-7829",
                "employee_name": "Robert Wilson",
                "department": "HR",
                "access_level": "Employee"
            },
            {
                "badge_id": "BADGE-9999",
                "employee_name": "Unknown Employee",
                "department": "Unknown",
                "access_level": "Employee",
                "active": False
            }
        ]
        
        for emp_data in sample_employees:
            badge_holder = BadgeHolder(**emp_data)
            db.add(badge_holder)
        
        db.commit()
        logger.info(f"Created {len(sample_employees)} sample badge holders")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()