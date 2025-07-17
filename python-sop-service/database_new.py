"""
Database configuration and models for the SOP Processing Service with Threat Correlation
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/sop_events")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models

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

# Database utility functions

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

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

# Pydantic models for API

from pydantic import BaseModel

class BadgeHolderCreate(BaseModel):
    badge_id: str
    employee_name: str
    department: str
    access_level: str

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