"""
Semantic Matcher
Uses sentence-transformers for semantic similarity matching
"""

import numpy as np
import logging
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from database import DatabaseManager

logger = logging.getLogger(__name__)

class SemanticMatcher:
    """
    Handles semantic matching using sentence transformers
    """
    
    def __init__(self):
        self.model_name = 'all-MiniLM-L6-v2'
        self.model = None
        self.db_manager = DatabaseManager()
        
    def _load_model(self):
        """Lazy load the model to avoid startup delays"""
        if self.model is None:
            logger.info(f"Loading sentence transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully")
    
    def generate_embeddings(self, phrases: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for a list of phrases
        """
        self._load_model()
        try:
            embeddings = self.model.encode(phrases)
            return [emb for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        """
        self._load_model()
        try:
            embeddings = self.model.encode([text1, text2])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            raise
    
    def calculate_similarity_with_embedding(self, text: str, embedding: np.ndarray) -> float:
        """
        Calculate similarity between text and pre-computed embedding
        """
        self._load_model()
        try:
            text_embedding = self.model.encode([text])[0]
            similarity = cosine_similarity([text_embedding], [embedding])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity with embedding: {e}")
            raise
    
    async def generate_embeddings_for_sop(self, sop_id: str):
        """
        Generate and store embeddings for all semantic rules of a SOP
        """
        try:
            # Get semantic rules for this SOP
            rules = await self.db_manager.get_semantic_rules_for_sop(sop_id)
            
            for rule in rules:
                rule_value = rule.get('rule_value', [])
                if not isinstance(rule_value, list):
                    continue
                
                # Generate embeddings for each phrase
                if rule_value:
                    embeddings = self.generate_embeddings(rule_value)
                    
                    # Store embeddings in database
                    for phrase, embedding in zip(rule_value, embeddings):
                        await self.db_manager.store_embedding(
                            rule['id'], phrase, embedding
                        )
            
            logger.info(f"Generated embeddings for SOP {sop_id}")
            
        except Exception as e:
            logger.error(f"Error generating embeddings for SOP {sop_id}: {e}")
            raise
    
    async def match_event(self, event_text: str, confidence_threshold: float = 0.8) -> Dict[str, Any]:
        """
        Match an event text against stored semantic embeddings
        """
        try:
            # Get all stored embeddings
            embeddings_data = await self.db_manager.get_all_embeddings()
            
            if not embeddings_data:
                return {
                    'matched': False,
                    'confidence': 0.0,
                    'matched_rule_id': None,
                    'matched_phrase': None
                }
            
            best_match = None
            best_confidence = 0.0
            
            # Calculate similarity with each stored embedding
            for embedding_record in embeddings_data:
                try:
                    # Convert stored embedding back to numpy array
                    stored_embedding = np.array(embedding_record['embedding'])
                    
                    similarity = self.calculate_similarity_with_embedding(
                        event_text, stored_embedding
                    )
                    
                    if similarity > best_confidence:
                        best_confidence = similarity
                        best_match = embedding_record
                        
                except Exception as e:
                    logger.warning(f"Error processing embedding {embedding_record['id']}: {e}")
                    continue
            
            # Check if best match meets threshold
            matched = best_confidence >= confidence_threshold
            
            result = {
                'matched': matched,
                'confidence': best_confidence,
                'matched_rule_id': best_match['rule_id'] if best_match else None,
                'matched_phrase': best_match['phrase'] if best_match else None
            }
            
            logger.info(f"Semantic match for '{event_text}': confidence={best_confidence:.3f}, matched={matched}")
            return result
            
        except Exception as e:
            logger.error(f"Error in semantic matching: {e}")
            raise
    
    async def find_similar_phrases(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find similar phrases to a query from stored embeddings
        """
        try:
            embeddings_data = await self.db_manager.get_all_embeddings()
            
            if not embeddings_data:
                return []
            
            similarities = []
            
            for embedding_record in embeddings_data:
                try:
                    stored_embedding = np.array(embedding_record['embedding'])
                    similarity = self.calculate_similarity_with_embedding(
                        query, stored_embedding
                    )
                    
                    similarities.append({
                        'phrase': embedding_record['phrase'],
                        'rule_id': embedding_record['rule_id'],
                        'confidence': similarity
                    })
                    
                except Exception as e:
                    logger.warning(f"Error processing embedding: {e}")
                    continue
            
            # Sort by confidence and return top results
            similarities.sort(key=lambda x: x['confidence'], reverse=True)
            return similarities[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar phrases: {e}")
            raise