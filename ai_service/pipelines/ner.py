from typing import List, Dict, Optional
from loguru import logger

from ai_service.models.ner import EntityExtractor
from ai_service.models.classifier import CategoryClassifier
from ai_service.utils import TextPreprocessor, ModelCache

class NERPipeline:
    """
    Pipeline for extracting meaningful entities and context from reports
    """
    
    DISASTER_TYPES = [
        "Flood", "Landslide", "Earthquake", "Fire", "Storm", 
        "Extreme Weather", "Geological Hazard", "Seismic Activity",
        "Accident", "Medical Emergency", "Infrastructural Failure",
        "Public Health Issue", "Utilities Outage", "Cyber Security"
    ]

    def __init__(
        self,
        ner_model: str = "dslim/bert-base-NER",
        use_cache: bool = True,
        device: Optional[str] = None
    ):
        self.extractor = EntityExtractor(model_name=ner_model, device=device)
        # We reuse the classifier's zero-shot capability to pinpoint disaster type more accurately
        self.type_classifier = CategoryClassifier(device=device)
        self.cache = ModelCache() if use_cache else None
        
        logger.info("NER pipeline initialized")

    def process(self, text: str) -> Dict[str, any]:
        """
        Extract locations and classify disaster type from text
        """
        cache_key = f"ner_{hash(text)}"
        if self.cache and (cached := self.cache.get(cache_key)):
            return cached

        # 1. Extract Locations
        locations = self.extractor.get_locations(text)
        
        # 2. Extract specific Disaster Type using Zero-Shot
        # Using truncated text for better accuracy on news links
        prompt_text = text[:1500] if len(text) > 1500 else text
        
        type_result = self.type_classifier.classify(
            text=prompt_text,
            categories=self.DISASTER_TYPES,
            hypothesis_template="This report is about a {}."
        )
        
        result = {
            "locations": locations,
            "disaster_type": type_result["category"],
            "type_confidence": type_result["confidence"],
            "all_entities": self.extractor.extract_entities(text)[:10] # Subset for metadata
        }
        
        if self.cache:
            self.cache.set(cache_key, result)
            
        return result
