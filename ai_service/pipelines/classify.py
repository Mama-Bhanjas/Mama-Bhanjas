"""
Classification Pipeline
End-to-end pipeline for text classification
"""
from typing import List, Dict, Optional
from loguru import logger

from ai_service.models.classifier import CategoryClassifier
from ai_service.utils import TextPreprocessor, validate_text_input, ModelCache


class ClassificationPipeline:
    """
    Complete pipeline for classifying reports
    """
    
    def __init__(
        self,
        model_name: str = "valhalla/distilbart-mnli-12-1",
        categories: Optional[List[str]] = None,
        use_cache: bool = True,
        device: Optional[str] = None
    ):
        """
        Initialize classification pipeline
        
        Args:
            model_name: Model to use for classification
            categories: List of category labels
            use_cache: Whether to cache predictions
            device: Device to run model on
        """
        self.classifier = CategoryClassifier(
            model_name=model_name,
            categories=categories,
            device=device
        )
        self.preprocessor = TextPreprocessor()
        self.cache = ModelCache() if use_cache else None
        
        logger.info("Classification pipeline initialized")
    
    def process(
        self,
        text: str,
        top_k: int = 3,
        threshold: float = 0.1,
        use_cache: bool = True
    ) -> Dict[str, any]:
        """
        Process a single text through the classification pipeline
        
        Args:
            text: Input text to classify
            top_k: Number of top categories to return
            threshold: Minimum confidence threshold
            use_cache: Whether to use cached results
            
        Returns:
            Classification results with metadata
        """
        # Validate input
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            logger.warning(f"Invalid input: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "category": None,
                "confidence": 0.0
            }
        
        # Check cache
        cache_key = f"classify_{hash(text)}_{top_k}_{threshold}"
        if use_cache and self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result:
                logger.info("Returning cached classification result")
                return cached_result
        
        # Classify (using truncated text for better accuracy on news articles)
        try:
            # First 1500 chars are usually the most relevant for classification
            prompt_text = text[:1500] if len(text) > 1500 else text
            
            result = self.classifier.classify(
                text=prompt_text,
                top_k=top_k,
                threshold=threshold
            )
            
            # Add metadata
            result["success"] = True
            result["text_length"] = len(text)
            
            # Cache result
            if use_cache and self.cache:
                self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Classification pipeline failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "category": None,
                "confidence": 0.0
            }
    
    def batch_process(
        self,
        texts: List[str],
        top_k: int = 3,
        threshold: float = 0.1
    ) -> List[Dict[str, any]]:
        """
        Process multiple texts through the pipeline
        
        Args:
            texts: List of texts to classify
            top_k: Number of top categories to return
            threshold: Minimum confidence threshold
            
        Returns:
            List of classification results
        """
        logger.info(f"Processing batch of {len(texts)} texts")
        
        results = []
        for i, text in enumerate(texts):
            logger.debug(f"Processing text {i+1}/{len(texts)}")
            result = self.process(text, top_k=top_k, threshold=threshold)
            results.append(result)
        
        # Add batch statistics
        successful = sum(1 for r in results if r.get("success", False))
        logger.info(f"Batch processing complete: {successful}/{len(texts)} successful")
        
        return results
    
    def get_statistics(self, results: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Calculate statistics from classification results
        
        Args:
            results: List of classification results
            
        Returns:
            Statistics dictionary
        """
        if not results:
            return {}
        
        # Count categories
        category_counts = {}
        total_confidence = 0.0
        successful_count = 0
        
        for result in results:
            if result.get("success", False):
                successful_count += 1
                category = result.get("category")
                confidence = result.get("confidence", 0.0)
                
                if category:
                    category_counts[category] = category_counts.get(category, 0) + 1
                    total_confidence += confidence
        
        avg_confidence = total_confidence / successful_count if successful_count > 0 else 0.0
        
        return {
            "total_processed": len(results),
            "successful": successful_count,
            "failed": len(results) - successful_count,
            "category_distribution": category_counts,
            "average_confidence": avg_confidence
        }
