"""
Base agent class for future agent implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Base class for all security analysis agents
    """
    
    def __init__(self, agent_type: str, config: Dict[str, Any] = None):
        self.agent_type = agent_type
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.{agent_type}")
    
    @abstractmethod
    async def analyze(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an event and return results
        
        Args:
            event_data: Event data to analyze
        
        Returns:
            Analysis results
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get list of agent capabilities
        
        Returns:
            List of capability strings
        """
        pass
    
    def validate_event_data(self, event_data: Dict[str, Any]) -> bool:
        """
        Validate event data format
        
        Args:
            event_data: Event data to validate
        
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['event_type', 'timestamp', 'location']
        
        for field in required_fields:
            if field not in event_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    def log_analysis(self, event_id: str, analysis_result: Dict[str, Any]):
        """
        Log analysis result
        
        Args:
            event_id: Event identifier
            analysis_result: Analysis result to log
        """
        self.logger.info(f"Analysis completed for event {event_id}: {analysis_result.get('summary', 'No summary')}")

class SecurityAgent(BaseAgent):
    """
    Generic security agent for basic security event analysis
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("security", config)
    
    async def analyze(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze security event
        
        Args:
            event_data: Security event data
        
        Returns:
            Analysis results
        """
        if not self.validate_event_data(event_data):
            return {
                "success": False,
                "error": "Invalid event data format"
            }
        
        # Basic security analysis
        severity = event_data.get('severity', 'Medium')
        event_type = event_data.get('event_type', 'Unknown')
        
        # Determine risk level based on event type
        if 'weapon' in event_type.lower() or 'shooter' in event_type.lower():
            risk_level = "Critical"
        elif 'unauthorized' in event_type.lower() or 'tailgating' in event_type.lower():
            risk_level = "High"
        elif 'access' in event_type.lower():
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        result = {
            "success": True,
            "agent_type": self.agent_type,
            "risk_level": risk_level,
            "confidence": 0.7,
            "summary": f"Security analysis completed for {event_type}",
            "recommendations": [
                "Review security logs",
                "Investigate incident",
                "Document findings"
            ]
        }
        
        return result
    
    def get_capabilities(self) -> List[str]:
        """Get security agent capabilities"""
        return [
            "security_event_analysis",
            "risk_assessment",
            "threat_classification",
            "incident_response"
        ]