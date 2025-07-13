import json
import logging
import openai
import os
from typing import Dict, Any, Optional
from datetime import datetime
from sop.models import ProcessedSOP, ResponseRequirements, SpecialConditions

logger = logging.getLogger(__name__)

class SOPExtractor:
    """Extract structured SOP information from document text using LLM"""
    
    def __init__(self):
        # Use existing OpenAI configuration
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "test-key-for-testing":
            # Mock client for testing
            self.client = None
            self.model = "gpt-4"
        else:
            self.client = openai.OpenAI(api_key=api_key)
            self.model = "gpt-4"  # Use same model as existing system
    
    def extract_sop_structure(self, document_text: str, document_title: str, filename: str) -> tuple[ProcessedSOP, Optional[str]]:
        """
        Extract structured SOP information from document text
        
        Args:
            document_text: Raw text content from document
            document_title: Title/name of the document
            filename: Original filename
            
        Returns:
            Tuple of (ProcessedSOP object, error_message)
            If successful: (sop_object, None)
            If failed: (None, error_message)
        """
        try:
            logger.info(f"Extracting SOP structure from {filename}")
            
            # If no client (testing mode), return mock data
            if not self.client:
                logger.info("Using mock SOP extraction for testing")
                sop_data = {
                    "sop_id": f"SOP-TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "title": f"Test SOP - {document_title}",
                    "category": "test_category",
                    "triggers": ["test trigger", "sample event"],
                    "priority_override": "MEDIUM",
                    "response_requirements": {
                        "timeline": "15 minutes",
                        "notifications": ["Security Team", "Management"],
                        "required_actions": ["Investigate incident", "Document findings"]
                    },
                    "special_conditions": {
                        "applies_to_locations": ["all_locations"],
                        "applies_to_times": ["all_times"],
                        "escalation_required": False
                    },
                    "regulatory_requirements": ["Standard compliance"]
                }
            else:
                # Create LLM prompt for structure extraction
                prompt = self._create_extraction_prompt(document_text, document_title)
                
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert at analyzing Standard Operating Procedures (SOPs) and extracting structured information. You must return valid JSON that matches the expected schema exactly."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1,  # Low temperature for consistent extraction
                    max_tokens=2000
                )
                
                # Extract response content
                response_text = response.choices[0].message.content.strip()
                
                # Parse JSON response
                try:
                    sop_data = json.loads(response_text)
                except json.JSONDecodeError as e:
                    # Try to extract JSON from response if it's wrapped in markdown
                    if "```json" in response_text:
                        start = response_text.find("```json") + 7
                        end = response_text.find("```", start)
                        json_text = response_text[start:end].strip()
                        sop_data = json.loads(json_text)
                    else:
                        logger.error(f"Failed to parse JSON from LLM response: {str(e)}")
                        return None, f"Failed to parse structured data from LLM response: {str(e)}"
            
            # Validate and create ProcessedSOP object
            processed_sop = self._create_processed_sop(sop_data, filename, document_text)
            
            logger.info(f"Successfully extracted SOP structure: {processed_sop.sop_id}")
            return processed_sop, None
            
        except Exception as e:
            logger.error(f"Error extracting SOP structure from {filename}: {str(e)}")
            return None, f"Error extracting SOP structure: {str(e)}"
    
    def _create_extraction_prompt(self, document_text: str, document_title: str) -> str:
        """Create LLM prompt for SOP structure extraction"""
        
        prompt = f"""
Analyze the following Standard Operating Procedure document and extract structured information in JSON format.

Document Title: {document_title}
Document Content:
{document_text}

Extract the following information and return as valid JSON:

{{
  "sop_id": "Generate a unique ID like SOP-001, SOP-002, etc.",
  "title": "Clear, descriptive title of the SOP",
  "category": "Category like 'medical_emergency', 'security_incident', 'access_control', 'environmental', etc.",
  "triggers": ["List of event types, keywords, or situations that would trigger this SOP"],
  "priority_override": "CRITICAL, HIGH, MEDIUM, LOW, or null if no specific priority mentioned",
  "response_requirements": {{
    "timeline": "Description of response time requirement (e.g., 'IMMEDIATE', 'within 2 minutes', etc.)",
    "notifications": ["List of who needs to be notified"],
    "required_actions": ["List of specific actions that must be taken"]
  }},
  "special_conditions": {{
    "applies_to_locations": ["List of locations this applies to, or ['all_locations'] if universal"],
    "applies_to_times": ["List of time periods like 'business_hours', 'after_hours', or ['all_times'] if always"],
    "escalation_required": true/false
  }},
  "regulatory_requirements": ["List any regulatory/compliance requirements mentioned like OSHA, HIPAA, etc."]
}}

IMPORTANT INSTRUCTIONS:
1. Generate a unique sop_id based on the content type
2. Extract triggers as specific, searchable keywords
3. Be comprehensive but accurate - don't add information not in the document
4. Use null for priority_override if no specific priority is mentioned
5. Return ONLY the JSON object, no additional text
6. Ensure all required fields have appropriate values
"""
        
        return prompt
    
    def _create_processed_sop(self, sop_data: Dict[str, Any], filename: str, original_text: str) -> ProcessedSOP:
        """Create ProcessedSOP object from extracted data"""
        
        # Create response requirements object
        response_req_data = sop_data.get("response_requirements", {})
        response_requirements = ResponseRequirements(
            timeline=response_req_data.get("timeline", "Not specified"),
            notifications=response_req_data.get("notifications", []),
            required_actions=response_req_data.get("required_actions", [])
        )
        
        # Create special conditions object
        special_cond_data = sop_data.get("special_conditions", {})
        special_conditions = SpecialConditions(
            applies_to_locations=special_cond_data.get("applies_to_locations", ["all_locations"]),
            applies_to_times=special_cond_data.get("applies_to_times", ["all_times"]),
            escalation_required=special_cond_data.get("escalation_required", False)
        )
        
        # Create the main ProcessedSOP object
        processed_sop = ProcessedSOP(
            sop_id=sop_data.get("sop_id", f"SOP-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            title=sop_data.get("title", "Untitled SOP"),
            category=sop_data.get("category", "general"),
            triggers=sop_data.get("triggers", []),
            priority_override=sop_data.get("priority_override"),
            response_requirements=response_requirements,
            special_conditions=special_conditions,
            regulatory_requirements=sop_data.get("regulatory_requirements", []),
            document_source=filename,
            processed_date=datetime.now(),
            original_text=original_text
        )
        
        return processed_sop
    
    def validate_extraction(self, sop: ProcessedSOP) -> tuple[bool, Optional[str]]:
        """Validate that extracted SOP data is reasonable"""
        
        try:
            # Check required fields
            if not sop.sop_id or not sop.title:
                return False, "Missing required SOP ID or title"
            
            if not sop.triggers:
                return False, "No triggers identified - SOPs should have trigger events"
            
            if not sop.response_requirements.required_actions:
                return False, "No required actions identified - SOPs should specify actions to take"
            
            # Check that content makes sense
            if len(sop.original_text) < 50:
                return False, "Document content too short to be a meaningful SOP"
            
            logger.info(f"SOP validation successful for {sop.sop_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Error validating SOP: {str(e)}")
            return False, f"Validation error: {str(e)}"