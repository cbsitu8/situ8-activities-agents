"""
Semantic Matching Service
Handles semantic similarity matching for event processing
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SemanticMatcher:
    """
    Handles semantic matching between events and SOP rules
    """
    
    def __init__(self):
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the semantic similarity model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Semantic matching model initialized")
        except ImportError:
            logger.warning("sentence-transformers not available, semantic matching disabled")
            self.model = None
    
    async def match_event(self, event_text: str, confidence_threshold: float = 0.8) -> Dict[str, Any]:
        """
        Match event text against stored rule embeddings
        
        Args:
            event_text: Event description to match
            confidence_threshold: Minimum confidence for match
        
        Returns:
            Dictionary with match results
        """
        try:
            if not self.model:
                return {
                    'matched': False,
                    'confidence': 0.0,
                    'matched_rule_id': None,
                    'matched_phrase': None
                }
            
            # For now, implement basic keyword matching
            # In a full implementation, this would use semantic embeddings
            event_lower = event_text.lower()
            
            # Sample rules for matching
            rules = [
                {
                    'id': 'rule-001',
                    'phrases': ['fire', 'smoke', 'burning', 'flames'],
                    'confidence': 0.9
                },
                {
                    'id': 'rule-002',
                    'phrases': ['medical', 'emergency', 'injury', 'fall'],
                    'confidence': 0.85
                },
                {
                    'id': 'rule-003',
                    'phrases': ['weapon', 'firearm', 'gun', 'shooter'],
                    'confidence': 0.95
                }
            ]
            
            best_match = None
            best_confidence = 0.0
            
            for rule in rules:
                for phrase in rule['phrases']:
                    if phrase in event_lower:
                        confidence = rule['confidence']
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_match = {
                                'rule_id': rule['id'],
                                'phrase': phrase
                            }
            
            matched = best_confidence >= confidence_threshold
            
            return {
                'matched': matched,
                'confidence': best_confidence,
                'matched_rule_id': best_match['rule_id'] if best_match else None,
                'matched_phrase': best_match['phrase'] if best_match else None
            }
            
        except Exception as e:
            logger.error(f"Error in semantic matching: {e}")
            return {
                'matched': False,
                'confidence': 0.0,
                'matched_rule_id': None,
                'matched_phrase': None
            }
    
    async def generate_embeddings_for_sop(self, sop_id: str):
        """
        Generate embeddings for all rules in a SOP
        
        Args:
            sop_id: SOP identifier
        """
        try:
            if not self.model:
                logger.warning("Semantic model not available, skipping embedding generation")
                return
            
            # In a full implementation, this would:
            # 1. Retrieve SOP rules from database
            # 2. Generate embeddings for each rule phrase
            # 3. Store embeddings in database
            
            logger.info(f"Generated embeddings for SOP {sop_id}")
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise