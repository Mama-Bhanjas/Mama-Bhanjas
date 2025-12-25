"""
Text Summarization Model
Generates concise summaries of reports
"""
from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from loguru import logger

from ai_service.utils import TextPreprocessor, get_device


class TextSummarizer:
    """
    Abstractive text summarization using transformer models
    """
    
    def __init__(
        self,
        model_name: str = "sshleifer/distilbart-cnn-6-6",
        device: Optional[str] = None
    ):
        """
        Initialize the summarizer
        
        Args:
            model_name: Hugging Face model name for summarization
                       Default: sshleifer/distilbart-cnn-12-6 (~300MB, efficient distilled model)
            device: Device to run model on ('cuda' or 'cpu')
        """
        self.device = device or get_device()
        self.preprocessor = TextPreprocessor()
        
        logger.info(f"Loading summarization model: {model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Summarizer loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load summarization model: {e}")
            raise
    
    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30,
        num_beams: int = 4,
        length_penalty: float = 2.0,
        early_stopping: bool = True
    ) -> Dict[str, any]:
        """
        Generate summary of input text
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            num_beams: Number of beams for beam search
            length_penalty: Length penalty for beam search
            early_stopping: Whether to stop early in beam search
            
        Returns:
            Dictionary with summary and metadata
        """
        # Preprocess text
        cleaned_text = self.preprocessor.clean_text(text)
        
        if not cleaned_text:
            logger.warning("Empty text provided for summarization")
            return {
                "summary": "",
                "original_length": 0,
                "summary_length": 0,
                "compression_ratio": 0.0
            }
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                cleaned_text,
                max_length=1024,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate summary
            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=num_beams,
                    length_penalty=length_penalty,
                    early_stopping=early_stopping,
                    no_repeat_ngram_size=3
                )
            
            # Decode summary
            summary = self.tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            # Calculate metrics
            original_length = len(cleaned_text)
            summary_length = len(summary)
            compression_ratio = summary_length / original_length if original_length > 0 else 0.0
            
            logger.info(f"Generated summary: {summary_length} chars from {original_length} chars (ratio: {compression_ratio:.2f})")
            
            return {
                "summary": summary,
                "original_length": original_length,
                "summary_length": summary_length,
                "compression_ratio": compression_ratio
            }
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return {
                "summary": "",
                "original_length": len(cleaned_text),
                "summary_length": 0,
                "compression_ratio": 0.0,
                "error": str(e)
            }
    
    def batch_summarize(
        self,
        texts: List[str],
        max_length: int = 150,
        min_length: int = 30
    ) -> List[Dict[str, any]]:
        """
        Summarize multiple texts
        
        Args:
            texts: List of texts to summarize
            max_length: Maximum length of summaries
            min_length: Minimum length of summaries
            
        Returns:
            List of summary results
        """
        results = []
        for text in texts:
            result = self.summarize(
                text,
                max_length=max_length,
                min_length=min_length
            )
            results.append(result)
        
        return results
    
    def extractive_summary(
        self,
        text: str,
        num_sentences: int = 3
    ) -> str:
        """
        Simple extractive summarization (fallback method)
        Returns the first N sentences
        
        Args:
            text: Input text
            num_sentences: Number of sentences to extract
            
        Returns:
            Extracted sentences as summary
        """
        import re
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Take first N sentences
        summary_sentences = sentences[:num_sentences]
        summary = '. '.join(summary_sentences)
        
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary
