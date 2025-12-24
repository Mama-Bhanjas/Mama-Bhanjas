
from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from loguru import logger
import numpy as np

from ai_service.utils import TextPreprocessor, get_device

class CategoryClassifier:
    """
    Multi-class text classifier for categorizing reports
    """
    
    # Default categories for report classification
    DEFAULT_CATEGORIES = [
        "Infrastructure",
        "Public Safety",
        "Environment",
        "Transportation",
        "Health & Sanitation",
        "Education",
        "Utilities",
        "Community Services",
        "Other"
    ]
    
    def __init__(
        self,
        model_name: str = "typeform/distilbert-base-uncased-mnli",
        categories: Optional[List[str]] = None,
        device: Optional[str] = None
    ):
        """
        Initialize the classifier
        
        Args:
            model_name: Hugging Face model name for zero-shot classification
                       Default: typeform/distilbert-base-uncased-mnli (~250MB, fast and efficient)
            categories: List of category labels
            device: Device to run model on ('cuda' or 'cpu')
        """
        self.categories = categories or self.DEFAULT_CATEGORIES
        self.device = device or get_device()
        self.preprocessor = TextPreprocessor()
        
        logger.info(f"Loading classifier model: {model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Classifier loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load classifier model: {e}")
            raise
    
    def classify(
        self,
        text: str,
        top_k: int = 3,
        threshold: float = 0.1
    ) -> Dict[str, any]:
        """
        Classify text into categories
        
        Args:
            text: Input text to classify
            top_k: Number of top categories to return
            threshold: Minimum confidence threshold
            
        Returns:
            Dictionary with classification results
        """
        # Preprocess text
        cleaned_text = self.preprocessor.clean_text(text)
        
        if not cleaned_text:
            logger.warning("Empty text provided for classification")
            return {
                "category": "Other",
                "confidence": 0.0,
                "top_categories": []
            }
        
        try:
            # Use zero-shot classification approach
            scores = []
            
            for category in self.categories:
                # Create hypothesis for zero-shot classification
                hypothesis = f"This text is about {category.lower()}."
                
                # Tokenize
                inputs = self.tokenizer(
                    cleaned_text,
                    hypothesis,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512
                ).to(self.device)
                
                # Get prediction
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    logits = outputs.logits
                    
                    # Get entailment score (index 2 for MNLI models)
                    probs = torch.softmax(logits, dim=1)
                    entailment_score = probs[0][2].item()
                    scores.append(entailment_score)
            
            # Normalize scores
            scores = np.array(scores)
            scores = scores / scores.sum()
            
            # Get top categories
            top_indices = np.argsort(scores)[::-1][:top_k]
            top_categories = [
                {
                    "category": self.categories[idx],
                    "confidence": float(scores[idx])
                }
                for idx in top_indices
                if scores[idx] >= threshold
            ]
            
            # Get primary category
            primary_idx = top_indices[0]
            primary_category = self.categories[primary_idx]
            primary_confidence = float(scores[primary_idx])
            
            logger.info(f"Classified as '{primary_category}' with confidence {primary_confidence:.3f}")
            
            return {
                "category": primary_category,
                "confidence": primary_confidence,
                "top_categories": top_categories
            }
            
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return {
                "category": "Other",
                "confidence": 0.0,
                "top_categories": [],
                "error": str(e)
            }
    
    def batch_classify(
        self,
        texts: List[str],
        top_k: int = 3,
        threshold: float = 0.1
    ) -> List[Dict[str, any]]:
        """
        Classify multiple texts
        
        Args:
            texts: List of texts to classify
            top_k: Number of top categories to return
            threshold: Minimum confidence threshold
            
        Returns:
            List of classification results
        """
        results = []
        for text in texts:
            result = self.classify(text, top_k=top_k, threshold=threshold)
            results.append(result)
        
        return results
    
    def add_category(self, category: str) -> None:
        """
        Add a new category to the classifier
        
        Args:
            category: New category name
        """
        if category not in self.categories:
            self.categories.append(category)
            logger.info(f"Added new category: {category}")
    
    def remove_category(self, category: str) -> None:
        """
        Remove a category from the classifier
        
        Args:
            category: Category name to remove
        """
        if category in self.categories:
            self.categories.remove(category)
            logger.info(f"Removed category: {category}")
