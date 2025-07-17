"""
Database tools for agents
"""

import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from models.database import SessionLocal, Event, BadgeHolder, ThreatCorrelation
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DatabaseTools:
    """
    Database utility tools for agents
    """
    
    @staticmethod
    def get_badge_events_in_timeframe(
        location: str,
        start_time: datetime,
        end_time: datetime,
        source: str = "access_control"
    ) -> List[Dict[str, Any]]:
        """
        Get badge events within a specific timeframe and location
        
        Args:
            location: Location to search
            start_time: Start of time window
            end_time: End of time window
            source: Event source filter
        
        Returns:
            List of badge events
        """
        try:
            db = SessionLocal()
            
            badge_events = db.query(Event).join(BadgeHolder).filter(
                Event.source == source,
                Event.location == location,
                Event.timestamp >= start_time,
                Event.timestamp <= end_time,
                Event.badge_id.isnot(None)
            ).all()
            
            results = []
            for event in badge_events:
                results.append({
                    "event_id": event.id,
                    "badge_id": event.badge_id,
                    "employee_name": event.badge_holder.employee_name if event.badge_holder else "Unknown",
                    "department": event.badge_holder.department if event.badge_holder else "Unknown",
                    "access_level": event.badge_holder.access_level if event.badge_holder else "Unknown",
                    "event_type": event.event_type,
                    "timestamp": event.timestamp.isoformat(),
                    "location": event.location,
                    "severity": event.severity,
                    "metadata": event.metadata
                })
            
            db.close()
            return results
            
        except Exception as e:
            logger.error(f"Error getting badge events: {e}")
            return []
    
    @staticmethod
    def get_employee_by_badge_id(badge_id: str) -> Optional[Dict[str, Any]]:
        """
        Get employee information by badge ID
        
        Args:
            badge_id: Badge ID to look up
        
        Returns:
            Employee information or None
        """
        try:
            db = SessionLocal()
            
            badge_holder = db.query(BadgeHolder).filter(BadgeHolder.badge_id == badge_id).first()
            
            if badge_holder:
                result = {
                    "badge_id": badge_holder.badge_id,
                    "employee_name": badge_holder.employee_name,
                    "department": badge_holder.department,
                    "access_level": badge_holder.access_level,
                    "active": badge_holder.active,
                    "hire_date": badge_holder.created_at.isoformat()
                }
            else:
                result = None
            
            db.close()
            return result
            
        except Exception as e:
            logger.error(f"Error getting employee details: {e}")
            return None
    
    @staticmethod
    def store_threat_correlation(correlation_data: Dict[str, Any]) -> Optional[str]:
        """
        Store threat correlation analysis
        
        Args:
            correlation_data: Correlation data to store
        
        Returns:
            Correlation ID if successful, None otherwise
        """
        try:
            db = SessionLocal()
            
            correlation = ThreatCorrelation(
                correlation_id=correlation_data["correlation_id"],
                tailgating_event_id=correlation_data["tailgating_event_id"],
                correlated_badge_events=correlation_data.get("correlated_badge_events", []),
                analysis_summary=correlation_data["analysis_summary"],
                confidence_score=correlation_data["confidence_score"],
                risk_level=correlation_data["risk_level"],
                agent_analysis=correlation_data.get("agent_analysis", {})
            )
            
            db.add(correlation)
            db.commit()
            
            correlation_id = correlation.correlation_id
            db.close()
            
            return correlation_id
            
        except Exception as e:
            logger.error(f"Error storing threat correlation: {e}")
            return None
    
    @staticmethod
    def get_recent_events(limit: int = 100, event_type: str = None) -> List[Dict[str, Any]]:
        """
        Get recent events
        
        Args:
            limit: Maximum number of events to return
            event_type: Optional event type filter
        
        Returns:
            List of recent events
        """
        try:
            db = SessionLocal()
            
            query = db.query(Event)
            
            if event_type:
                query = query.filter(Event.event_type == event_type)
            
            events = query.order_by(Event.timestamp.desc()).limit(limit).all()
            
            results = []
            for event in events:
                results.append({
                    "event_id": event.id,
                    "event_type": event.event_type,
                    "timestamp": event.timestamp.isoformat(),
                    "location": event.location,
                    "source": event.source,
                    "severity": event.severity,
                    "badge_id": event.badge_id,
                    "metadata": event.metadata,
                    "processed_at": event.processed_at.isoformat(),
                    "correlation_triggered": event.correlation_triggered
                })
            
            db.close()
            return results
            
        except Exception as e:
            logger.error(f"Error getting recent events: {e}")
            return []