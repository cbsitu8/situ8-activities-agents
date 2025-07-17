"""
Simplified Semantic Matcher (without sentence-transformers)
Basic similarity matching for initial implementation
"""

import logging
from typing import List, Dict, Any, Optional
from database import DatabaseManager

logger = logging.getLogger(__name__)

class SemanticMatcher:
    """
    Simplified semantic matching using basic text similarity
    """
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        logger.info("SemanticMatcher initialized (simplified mode)")
        
    def generate_embeddings(self, phrases: List[str]) -> List[List[float]]:
        """
        Generate simple embeddings (placeholder for now)
        In a real implementation, this would use sentence-transformers
        """
        # Simple word count based embeddings
        embeddings = []
        for phrase in phrases:
            words = phrase.lower().split()
            # Create a simple 10-dimensional embedding based on word characteristics
            embedding = [
                len(words),                    # number of words
                len(phrase),                   # character length
                sum(len(w) for w in words),    # total word length
                phrase.count(' '),             # space count
                1.0 if 'emergency' in phrase.lower() else 0.0,
                1.0 if 'fire' in phrase.lower() else 0.0,
                1.0 if 'medical' in phrase.lower() else 0.0,
                1.0 if 'security' in phrase.lower() else 0.0,
                1.0 if 'door' in phrase.lower() else 0.0,
                1.0 if 'person' in phrase.lower() else 0.0
            ]
            embeddings.append(embedding)
        return embeddings
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate basic text similarity
        """
        try:
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            # Jaccard similarity
            similarity = len(intersection) / len(union) if union else 0.0
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def calculate_similarity_with_embedding(self, text: str, embedding: List[float]) -> float:
        """
        Calculate similarity between text and embedding (simplified)
        """
        try:
            # Generate embedding for text
            text_embedding = self.generate_embeddings([text])[0]
            
            # Simple cosine similarity approximation
            dot_product = sum(a * b for a, b in zip(text_embedding, embedding))
            magnitude_a = sum(a * a for a in text_embedding) ** 0.5
            magnitude_b = sum(b * b for b in embedding) ** 0.5
            
            if magnitude_a == 0 or magnitude_b == 0:
                return 0.0
            
            similarity = dot_product / (magnitude_a * magnitude_b)
            return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]
        except Exception as e:
            logger.error(f"Error calculating similarity with embedding: {e}")
            return 0.0
    
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
                    # Use text similarity as fallback
                    similarity = self.calculate_similarity(
                        event_text, embedding_record['phrase']
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
                    similarity = self.calculate_similarity(
                        query, embedding_record['phrase']
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