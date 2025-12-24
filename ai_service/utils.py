"""
Utility functions for AI service
"""
import os
import re
from typing import List, Dict, Any, Optional
from loguru import logger
import numpy as np
from datetime import datetime


class TextPreprocessor:
    """Text preprocessing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text input
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 512) -> str:
        """
        Truncate text to maximum length
        
        Args:
            text: Input text
            max_length: Maximum character length
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    @staticmethod
    def batch_texts(texts: List[str], batch_size: int = 32) -> List[List[str]]:
        """
        Split texts into batches
        
        Args:
            texts: List of text strings
            batch_size: Size of each batch
            
        Returns:
            List of text batches
        """
        return [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]


class ModelCache:
    """Simple in-memory cache for model predictions"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.access_times: Dict[str, datetime] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if key in self.cache:
            self.access_times[key] = datetime.now()
            logger.debug(f"Cache hit for key: {key[:50]}...")
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set cached value with LRU eviction"""
        if len(self.cache) >= self.max_size:
            # Remove least recently used item
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = value
        self.access_times[key] = datetime.now()
        logger.debug(f"Cached value for key: {key[:50]}...")
    
    def clear(self) -> None:
        """Clear all cached values"""
        self.cache.clear()
        self.access_times.clear()
        logger.info("Cache cleared")


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logger.remove()  # Remove default handler
    logger.add(
        "logs/ai_service_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>"
    )
    logger.info(f"Logging initialized at {log_level} level")


def validate_text_input(text: str, min_length: int = 10, max_length: int = 10000) -> tuple[bool, str]:
    """
    Validate text input
    
    Args:
        text: Input text to validate
        min_length: Minimum acceptable length
        max_length: Maximum acceptable length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not isinstance(text, str):
        return False, "Text must be a non-empty string"
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"Text must be at least {min_length} characters long"
    
    if len(text) > max_length:
        return False, f"Text must not exceed {max_length} characters"
    
    return True, ""


def get_device() -> str:
    """
    Get the appropriate device for model inference
    
    Returns:
        Device string ('cuda' or 'cpu')
    """
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")
    return device
