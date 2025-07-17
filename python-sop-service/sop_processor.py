"""
SOP Document Processor
Handles extraction of text from various document formats and rule extraction
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional
from io import BytesIO
import docx
import markdown

logger = logging.getLogger(__name__)

class SOPProcessor:
    """
    Processes SOP documents and extracts actionable rules
    """
    
    def __init__(self):
        # Keywords that indicate triggers or conditions
        self.trigger_keywords = [
            'trigger', 'triggers', 'when', 'if', 'upon', 'detection', 'alert',
            'emergency', 'incident', 'event', 'occurs', 'happens', 'case of'
        ]
        
        # Keywords that indicate priorities
        self.priority_keywords = {
            'CRITICAL': ['critical', 'emergency', 'immediate', 'urgent', 'life-threatening'],
            'HIGH': ['high', 'important', 'priority', 'serious'],
            'MEDIUM': ['medium', 'moderate', 'standard'],
            'LOW': ['low', 'routine', 'minor', 'non-urgent']
        }
        
        # Security event types from CSV data
        self.event_types = [
            'Person Brandishing Firearm', 'Door Propped Open', 'Smoke or Fire',
            'Person Jumping Fence', 'Person Falling Down', 'Tailgating',
            'Granted Access', 'Door Forced Open', 'Invalid Badge Read', 'Door Held Open'
        ]

    async def process_document(self, content: bytes, file_type: str, name: str) -> Dict[str, Any]:
        """
        Process a document and extract text content
        """
        try:
            if file_type == 'docx':
                text_content = self._extract_from_docx(content)
            elif file_type == 'md':
                text_content = self._extract_from_markdown(content)
            elif file_type == 'txt':
                text_content = content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            return {
                'name': name,
                'file_type': file_type,
                'content': text_content,
                'sections': self._parse_sections(text_content)
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise

    def _extract_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(content))
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(paragraphs)
        except Exception as e:
            logger.error(f"Error extracting from DOCX: {e}")
            raise

    def _extract_from_markdown(self, content: bytes) -> str:
        """Extract text from Markdown file"""
        try:
            return content.decode('utf-8')
        except Exception as e:
            logger.error(f"Error extracting from Markdown: {e}")
            raise

    def _parse_sections(self, text: str) -> Dict[str, str]:
        """
        Parse document into logical sections
        """
        sections = {}
        current_section = 'general'
        current_content = []
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a header (markdown style or caps)
            if (line.startswith('#') or 
                line.isupper() and len(line) > 3 or
                any(keyword in line.lower() for keyword in ['trigger', 'response', 'action', 'procedure'])):
                
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line.replace('#', '').strip().lower()
                current_content = []
            else:
                current_content.append(line)
        
        # Save final section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections

    async def extract_rules(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract actionable rules from SOP content
        """
        try:
            rules = []
            
            # Extract exact matches for known event types
            exact_matches = self._extract_exact_matches(content)
            if exact_matches:
                rules.append({
                    'rule_type': 'exact',
                    'rule_value': exact_matches,
                    'priority': self._determine_priority(content),
                    'agent_assignments': self._extract_agent_assignments(content)
                })
            
            # Extract keywords
            keywords = self._extract_keywords(content)
            if keywords:
                rules.append({
                    'rule_type': 'keyword',
                    'rule_value': keywords,
                    'priority': self._determine_priority(content),
                    'agent_assignments': self._extract_agent_assignments(content)
                })
            
            # Extract patterns
            patterns = self._extract_patterns(content)
            if patterns:
                rules.append({
                    'rule_type': 'pattern',
                    'rule_value': patterns,
                    'priority': self._determine_priority(content),
                    'agent_assignments': self._extract_agent_assignments(content)
                })
            
            # Extract semantic phrases
            semantic_phrases = self._extract_semantic_phrases(content)
            if semantic_phrases:
                rules.append({
                    'rule_type': 'semantic',
                    'rule_value': semantic_phrases,
                    'priority': self._determine_priority(content),
                    'agent_assignments': self._extract_agent_assignments(content)
                })
            
            logger.info(f"Extracted {len(rules)} rules from SOP content")
            return rules
            
        except Exception as e:
            logger.error(f"Error extracting rules: {e}")
            raise

    def _extract_exact_matches(self, content: str) -> List[str]:
        """Extract exact event type matches"""
        matches = []
        content_lower = content.lower()
        
        for event_type in self.event_types:
            if event_type.lower() in content_lower:
                matches.append(event_type)
        
        return matches

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords from content"""
        keywords = []
        content_lower = content.lower()
        
        # Common security keywords
        security_keywords = [
            'fall', 'fallen', 'collapse', 'collapsed', 'injury', 'injured',
            'medical', 'emergency', 'fire', 'smoke', 'weapon', 'firearm',
            'breach', 'forced', 'open', 'invalid', 'badge', 'access',
            'tailgate', 'tailgating', 'fence', 'jump', 'jumping'
        ]
        
        for keyword in security_keywords:
            if keyword in content_lower:
                keywords.append(keyword)
        
        return list(set(keywords))  # Remove duplicates

    def _extract_patterns(self, content: str) -> List[str]:
        """Extract regex patterns for event matching"""
        patterns = []
        
        # Common patterns for security events
        if any(word in content.lower() for word in ['fall', 'medical', 'injury']):
            patterns.append(r'person.*(fall|fallen|down|collapse)')
        
        if any(word in content.lower() for word in ['fire', 'smoke', 'emergency']):
            patterns.append(r'(fire|smoke|emergency)')
        
        if any(word in content.lower() for word in ['weapon', 'firearm', 'gun']):
            patterns.append(r'(weapon|firearm|gun|brandish)')
        
        if any(word in content.lower() for word in ['door', 'access', 'breach']):
            patterns.append(r'door.*(force|open|prop|held)')
        
        return patterns

    def _extract_semantic_phrases(self, content: str) -> List[str]:
        """Extract semantic phrases for embedding matching"""
        phrases = []
        
        # Split into sentences and look for actionable phrases
        sentences = re.split(r'[.!?]+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
                
            # Look for phrases that describe conditions or triggers
            if any(keyword in sentence.lower() for keyword in self.trigger_keywords):
                phrases.append(sentence)
        
        # Add some default semantic phrases based on content
        if 'medical' in content.lower() or 'fall' in content.lower():
            phrases.extend([
                'person has fallen',
                'someone is injured',
                'medical assistance needed',
                'unconscious person found'
            ])
        
        if 'fire' in content.lower() or 'smoke' in content.lower():
            phrases.extend([
                'fire detected',
                'smoke alarm activated',
                'evacuation required'
            ])
        
        return phrases[:10]  # Limit to top 10 phrases

    def _determine_priority(self, content: str) -> str:
        """Determine priority level from content"""
        content_lower = content.lower()
        
        for priority, keywords in self.priority_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return priority
        
        # Default priority based on content type
        if any(word in content_lower for word in ['medical', 'fire', 'weapon', 'emergency']):
            return 'CRITICAL'
        elif any(word in content_lower for word in ['security', 'breach', 'forced']):
            return 'HIGH'
        else:
            return 'MEDIUM'

    def _extract_agent_assignments(self, content: str) -> List[str]:
        """Extract agent assignments from content"""
        agents = []
        content_lower = content.lower()
        
        # Map content to appropriate agents
        if any(word in content_lower for word in ['medical', 'life safety', 'first aid']):
            agents.append('EnvironmentAgent')
        
        if any(word in content_lower for word in ['contact', 'notify', 'dispatch', 'ems']):
            agents.append('EscalationAgent')
        
        if any(word in content_lower for word in ['report', 'document', 'log', 'compliance']):
            agents.append('DocumentationAgent')
        
        if any(word in content_lower for word in ['access', 'door', 'badge']):
            agents.append('AccessControlAgent')
        
        if any(word in content_lower for word in ['perimeter', 'fence', 'camera']):
            agents.append('PerimeterAgent')
        
        # Default agents if none specified
        if not agents:
            agents = ['EscalationAgent', 'DocumentationAgent']
        
        return agents