"""
Event Processing Service
Handles security event processing and SOP matching
"""

import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EventProcessor:
    """
    Processes security events and matches them against SOPs
    """
    
    def __init__(self):
        # In-memory storage for uploaded SOPs (for backward compatibility)
        self.uploaded_sops = []
        self.sample_sop_deleted = False
    
    def add_uploaded_sop(self, sop_data: Dict[str, Any]):
        """Add uploaded SOP to in-memory storage"""
        self.uploaded_sops.append(sop_data)
    
    def get_all_sops(self) -> List[Dict[str, Any]]:
        """Get all SOPs including sample and uploaded ones"""
        all_sops = []
        
        if not self.sample_sop_deleted:
            sample_sop = {
                "id": "sample-001",
                "name": "Medical Emergency Response",
                "file_name": "medical_emergency.md",
                "file_type": "md",
                "upload_status": "completed",
                "rule_count": 3,
                "created_at": "2025-01-15T10:00:00Z"
            }
            all_sops.append(sample_sop)
        
        all_sops.extend(self.uploaded_sops)
        return all_sops
    
    def delete_sop(self, sop_id: str) -> Dict[str, Any]:
        """Delete a SOP by ID"""
        if sop_id == "sample-001":
            if self.sample_sop_deleted:
                raise ValueError("SOP not found")
            self.sample_sop_deleted = True
            return {
                "id": "sample-001",
                "name": "Medical Emergency Response"
            }
        
        # Find and remove uploaded SOP
        for i, sop in enumerate(self.uploaded_sops):
            if sop["id"] == sop_id:
                return self.uploaded_sops.pop(i)
        
        raise ValueError("SOP not found")
    
    async def match_event_to_sops(self, event_type: str) -> tuple:
        """
        Match an event to actual SOPs and their rules
        
        Args:
            event_type: Type of security event
        
        Returns:
            Tuple of (matched_sop, confidence, matched_rules)
        """
        try:
            all_sops = self.get_all_sops()
            
            best_match = None
            best_confidence = 0.0
            matched_rules = []
            
            for sop in all_sops:
                # Generate rules for this SOP
                rules = self._generate_rules_for_sop(sop)
                
                # Check each rule for matches
                for rule in rules:
                    confidence = self._calculate_rule_confidence(event_type, rule)
                    
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = sop
                        matched_rules = [f"{rule['rule_type']}: {rule.get('matched_phrase', 'N/A')}"]
            
            return best_match, best_confidence, matched_rules
            
        except Exception as e:
            logger.error(f"Error matching event to SOPs: {e}")
            return None, 0.0, []
    
    def _generate_rules_for_sop(self, sop: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate rules based on SOP name and type"""
        sop_name = sop["name"].lower()
        
        if "medical" in sop_name or "emergency" in sop_name:
            return [
                {
                    "rule_type": "exact",
                    "rule_value": ["Person Falling Down", "Medical Emergency"],
                    "priority": "CRITICAL",
                    "agent_assignments": ["MedicalAgent", "EmergencyAgent"]
                },
                {
                    "rule_type": "keyword",
                    "rule_value": ["fall", "medical", "emergency"],
                    "priority": "HIGH",
                    "agent_assignments": ["MedicalAgent"]
                }
            ]
        elif "fire" in sop_name or "smoke" in sop_name:
            return [
                {
                    "rule_type": "exact",
                    "rule_value": ["Smoke or Fire", "Fire Detection", "Smoke Detection"],
                    "priority": "CRITICAL",
                    "agent_assignments": ["FireSafetyAgent", "EmergencyAgent"]
                }
            ]
        elif "security" in sop_name or "access" in sop_name:
            return [
                {
                    "rule_type": "exact",
                    "rule_value": ["Unauthorized Access", "Badge Tailgating", "Door Forced Open"],
                    "priority": "HIGH",
                    "agent_assignments": ["SecurityAgent", "AccessControlAgent"]
                }
            ]
        else:
            return [
                {
                    "rule_type": "keyword",
                    "rule_value": ["incident", "alert", "violation"],
                    "priority": "MEDIUM",
                    "agent_assignments": ["GeneralAgent"]
                }
            ]
    
    def _calculate_rule_confidence(self, event_type: str, rule: Dict[str, Any]) -> float:
        """Calculate confidence score for rule match"""
        event_lower = event_type.lower()
        confidence = 0.0
        
        if rule["rule_type"] == "exact":
            for value in rule["rule_value"]:
                if value.lower() == event_lower:
                    confidence = 0.95
                    rule["matched_phrase"] = value
                    break
        elif rule["rule_type"] == "keyword":
            matches = []
            for keyword in rule["rule_value"]:
                if keyword.lower() in event_lower:
                    matches.append(keyword)
            if matches:
                confidence = 0.75 + (0.1 * len(matches))
                rule["matched_phrase"] = f"Keywords: {', '.join(matches)}"
        elif rule["rule_type"] == "semantic":
            # Simple semantic matching
            for phrase in rule["rule_value"]:
                phrase_words = phrase.lower().split()
                event_words = event_lower.split()
                common_words = set(phrase_words) & set(event_words)
                if common_words:
                    confidence = 0.60 + (0.1 * len(common_words))
                    rule["matched_phrase"] = f"Semantic: {phrase}"
                    break
        
        return confidence
    
    async def process_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a security event and generate response
        
        Args:
            event_data: Event data dictionary
        
        Returns:
            Processing result dictionary
        """
        try:
            event_type = event_data.get("event_type", "Unknown")
            location = event_data.get("location", "Unknown")
            
            logger.info(f"Processing event: {event_type} at {location}")
            
            # Match event against SOPs
            matched_sop, confidence, matched_rules = await self.match_event_to_sops(event_type)
            
            if matched_sop:
                # Generate response based on matched SOP
                priority = self._determine_priority(confidence)
                response_time = self._calculate_response_time(confidence)
                actions, agents = self._generate_actions_and_agents(matched_sop)
                
                result = {
                    "event_id": f"evt_{uuid.uuid4().hex[:8]}",
                    "priority": priority,
                    "matched_sop": matched_sop["name"],
                    "matched_sop_id": matched_sop["id"],
                    "matched_rules": matched_rules,
                    "confidence": confidence,
                    "assigned_agents": agents,
                    "response_time": response_time,
                    "actions_required": actions
                }
            else:
                # No SOP match found
                result = {
                    "event_id": f"evt_{uuid.uuid4().hex[:8]}",
                    "priority": "LOW",
                    "matched_sop": "No SOP Match Found",
                    "matched_sop_id": None,
                    "matched_rules": ["No matching rules"],
                    "confidence": 0.0,
                    "assigned_agents": ["DefaultAgent"],
                    "response_time": "50ms",
                    "actions_required": [
                        "Log unmatched event",
                        "Review and create appropriate SOP",
                        "Manual assessment required"
                    ]
                }
            
            # Add processing metadata
            result.update({
                "processed_at": datetime.utcnow().isoformat(),
                "processing_node": "python-sop-service",
                "event_source": event_data.get("source", "simulator"),
                "raw_event": event_data
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing event: {e}")
            raise
    
    def _determine_priority(self, confidence: float) -> str:
        """Determine priority based on confidence score"""
        if confidence >= 0.9:
            return "CRITICAL"
        elif confidence >= 0.7:
            return "HIGH"
        elif confidence >= 0.5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_response_time(self, confidence: float) -> str:
        """Calculate response time based on confidence"""
        if confidence >= 0.9:
            return f"{8 + int((1 - confidence) * 20)}ms"
        elif confidence >= 0.7:
            return f"{15 + int((1 - confidence) * 30)}ms"
        elif confidence >= 0.5:
            return f"{25 + int((1 - confidence) * 40)}ms"
        else:
            return f"{35 + int((1 - confidence) * 50)}ms"
    
    def _generate_actions_and_agents(self, matched_sop: Dict[str, Any]) -> tuple:
        """Generate actions and agents based on matched SOP"""
        sop_name_lower = matched_sop["name"].lower()
        
        if "medical" in sop_name_lower or "emergency" in sop_name_lower:
            actions = [
                "Immediate medical response",
                "Secure the area",
                "Notify emergency contacts",
                "Document incident details"
            ]
            agents = ["MedicalAgent", "EmergencyAgent"]
        elif "security" in sop_name_lower or "access" in sop_name_lower:
            actions = [
                "Immediate security response",
                "Verify access credentials",
                "Check security logs",
                "Escalate if necessary"
            ]
            agents = ["SecurityAgent", "AccessControlAgent"]
        else:
            actions = [
                "Log incident",
                "Assess severity",
                "Follow SOP guidelines",
                "Monitor for escalation"
            ]
            agents = ["GeneralAgent"]
        
        return actions, agents