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

        # 1. Extract Locations (Model based)
        locations = self.extractor.get_locations(text)

        # 2. Dictionary-based Augmentation for Nepal Locations (Fix for inaccurate NER)
        nepal_locations = {
            "Kathmandu", "Lalitpur", "Bhaktapur", "Pokhara", "Chitwan", "Biratnagar", "Dharan", 
            "Birgunj", "Butwal", "Hetauda", "Janakpur", "Nepalgunj", "Dhangadhi", "Taplejung", 
            "Jhapa", "Ilam", "Sankhuwasabha", "Bhojpur", "Dhankuta", "Morang", "Sunsari", 
            "Saptari", "Siraha", "Udayapur", "Khotang", "Okhaldhunga", "Solukhumbu", "Dhanusha", 
            "Mahottari", "Sarlahi", "Sindhuli", "Ramechhap", "Dolakha", "Sindhupalchok", 
            "Kavrepalanchok", "Kavre", "Nuwakot", "Rasuwa", "Dhading", "Makwanpur", "Rautahat", 
            "Bara", "Parsa", "Gorkha", "Lamjung", "Tanahun", "Syangja", "Kaski", "Manang", 
            "Mustang", "Myagdi", "Parbat", "Baglung", "Gulmi", "Palpa", "Nawalparasi", 
            "Rupandehi", "Kapilvastu", "Arghakhanchi", "Pyuthan", "Rolpa", "Rukum", "Salyan", 
            "Dang", "Banke", "Bardiya", "Surkhet", "Dailekh", "Jajarkot", "Dolpa", "Jumla", 
            "Kalikot", "Mugu", "Humla", "Bajura", "Bajhang", "Achham", "Doti", "Kailali", 
            "Kanchanpur", "Dadeldhura", "Baitadi", "Darchula", "Melamchi", "Boksi", "Jiri"
        }
        
        text_lower = text.lower()
        found_static = []
        for loc in nepal_locations:
            if loc.lower() in text_lower:
                found_static.append(loc)
        
        # Merge model locations with static findings
        # Prioritize static findings if they are missing
        for loc in found_static:
            if loc not in locations:
                locations.append(loc)
        
        # Sort locations: Static matches first (more accurate), then model findings
        # But ensure uniqueness
        seen = set()
        final_locs = []
        for loc in found_static + locations:
            if loc not in seen:
                final_locs.append(loc)
                seen.add(loc)
        
        locations = final_locs[:5] # Keep top 5

        
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
