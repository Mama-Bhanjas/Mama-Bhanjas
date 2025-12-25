"""
Summarization Pipeline
End-to-end pipeline for text summarization
"""
from typing import List, Dict, Optional
from loguru import logger

from ai_service.models.summarizer import TextSummarizer
from ai_service.utils import TextPreprocessor, validate_text_input, ModelCache


class SummarizationPipeline:
    """
    Complete pipeline for summarizing reports
    """
    
    def __init__(
        self,
        model_name: str = "sshleifer/distilbart-cnn-6-6",
        use_cache: bool = True,
        device: Optional[str] = None
    ):
        """
        Initialize summarization pipeline
        
        Args:
            model_name: Model to use for summarization
            use_cache: Whether to cache summaries
            device: Device to run model on
        """
        self.summarizer = TextSummarizer(
            model_name=model_name,
            device=device
        )
        self.preprocessor = TextPreprocessor()
        self.cache = ModelCache() if use_cache else None
        
        logger.info("Summarization pipeline initialized")
    
    def process(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30,
        use_cache: bool = True
    ) -> Dict[str, any]:
        """
        Process a single text through the summarization pipeline
        
        Args:
            text: Input text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            use_cache: Whether to use cached results
            
        Returns:
            Summarization results with metadata
        """
        # Validate input
        is_valid, error_msg = validate_text_input(text, min_length=50)
        if not is_valid:
            logger.warning(f"Invalid input: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "summary": ""
            }
        
        # Check cache
        cache_key = f"summarize_{hash(text)}_{max_length}_{min_length}"
        if use_cache and self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result:
                logger.info("Returning cached summarization result")
                return cached_result
        
        # Summarize
        try:
            result = self.summarizer.summarize(
                text=text,
                max_length=max_length,
                min_length=min_length
            )
            
            # Add metadata
            result["success"] = True
            
            # Cache result
            if use_cache and self.cache:
                self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Summarization pipeline failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "summary": ""
            }
    
    def batch_process(
        self,
        texts: List[str],
        max_length: int = 150,
        min_length: int = 30
    ) -> List[Dict[str, any]]:
        """
        Process multiple texts through the pipeline
        
        Args:
            texts: List of texts to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            List of summarization results
        """
        logger.info(f"Processing batch of {len(texts)} texts")
        
        results = []
        for i, text in enumerate(texts):
            logger.debug(f"Processing text {i+1}/{len(texts)}")
            result = self.process(
                text,
                max_length=max_length,
                min_length=min_length
            )
            results.append(result)
        
        # Add batch statistics
        successful = sum(1 for r in results if r.get("success", False))
        logger.info(f"Batch processing complete: {successful}/{len(texts)} successful")
        
        return results
    
    def get_statistics(self, results: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Calculate statistics from summarization results
        
        Args:
            results: List of summarization results
            
        Returns:
            Statistics dictionary
        """
        if not results:
            return {}
        
        total_compression = 0.0
        total_original = 0
        total_summary = 0
        successful_count = 0
        
        for result in results:
            if result.get("success", False):
                successful_count += 1
                total_compression += result.get("compression_ratio", 0.0)
                total_original += result.get("original_length", 0)
                total_summary += result.get("summary_length", 0)
        
        avg_compression = total_compression / successful_count if successful_count > 0 else 0.0
        
        return {
            "total_processed": len(results),
            "successful": successful_count,
            "failed": len(results) - successful_count,
            "average_compression_ratio": avg_compression,
            "total_original_length": total_original,
            "total_summary_length": total_summary
        }
