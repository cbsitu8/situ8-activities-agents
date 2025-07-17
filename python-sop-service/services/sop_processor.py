"""
SOP Processing Service
Handles document processing, rule extraction, and validation
"""

import logging
import asyncio
from typing import Dict, List, Any
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class SOPProcessor:
    """
    Processes SOP documents and extracts rules
    """
    
    def __init__(self):
        pass
    
    async def process_document(self, content: bytes, file_type: str, name: str) -> Dict[str, Any]:
        """
        Process uploaded SOP document
        
        Args:
            content: Raw file content
            file_type: File extension (docx, md, txt)
            name: Document name
        
        Returns:
            Dictionary with processed document data
        """
        try:
            # Decode content based on file type
            if file_type == 'docx':
                text_content = self._process_docx(content)
            elif file_type in ['md', 'txt']:
                text_content = content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            return {
                'id': str(uuid.uuid4()),
                'name': name,
                'content': text_content,
                'file_type': file_type,
                'processed_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise
    
    def _process_docx(self, content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            from docx import Document
            import io
            
            doc = Document(io.BytesIO(content))
            text_content = []
            
            for paragraph in doc.paragraphs:
                text_content.append(paragraph.text)
            
            return '\n'.join(text_content)
            
        except ImportError:
            logger.warning("python-docx not available, treating as plain text")
            return content.decode('utf-8', errors='ignore')
    
    async def extract_rules(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract rules from SOP content
        
        Args:
            content: SOP text content
        
        Returns:
            List of extracted rules
        """
        try:
            rules = []
            
            # Basic rule extraction based on content analysis
            content_lower = content.lower()
            
            # Fire safety rules
            if any(keyword in content_lower for keyword in ['fire', 'smoke', 'alarm', 'evacuation']):
                rules.append({
                    'rule_type': 'exact',
                    'rule_value': ['Smoke or Fire', 'Fire Detection', 'Smoke Detection'],
                    'priority': 'CRITICAL',
                    'agent_assignments': ['FireSafetyAgent', 'EmergencyAgent']
                })
            
            # Security rules
            if any(keyword in content_lower for keyword in ['unauthorized', 'access', 'badge', 'tailgating']):
                rules.append({
                    'rule_type': 'exact',
                    'rule_value': ['Unauthorized Access', 'Badge Tailgating', 'Door Forced Open'],
                    'priority': 'HIGH',
                    'agent_assignments': ['SecurityAgent', 'AccessControlAgent']
                })
            
            # Medical emergency rules
            if any(keyword in content_lower for keyword in ['medical', 'emergency', 'injury', 'fall']):
                rules.append({
                    'rule_type': 'exact',
                    'rule_value': ['Person Falling Down', 'Medical Emergency'],
                    'priority': 'HIGH',
                    'agent_assignments': ['MedicalAgent', 'EmergencyAgent']
                })
            
            # Weapon/shooter rules
            if any(keyword in content_lower for keyword in ['weapon', 'firearm', 'shooter', 'gun']):
                rules.append({
                    'rule_type': 'exact',
                    'rule_value': ['Person Brandishing Firearm', 'Active Shooter', 'Weapon Detected'],
                    'priority': 'CRITICAL',
                    'agent_assignments': ['SecurityAgent', 'LawEnforcementAgent']
                })
            
            # Default rule if no specific patterns found
            if not rules:
                rules.append({
                    'rule_type': 'keyword',
                    'rule_value': ['incident', 'alert', 'violation'],
                    'priority': 'MEDIUM',
                    'agent_assignments': ['GeneralAgent']
                })
            
            logger.info(f"Extracted {len(rules)} rules from SOP content")
            return rules
            
        except Exception as e:
            logger.error(f"Error extracting rules: {e}")
            raise