
from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from loguru import logger

from ai_service.utils import TextPreprocessor, get_device

class EntityExtractor:
    """
    Named Entity Recognition (NER) wrapper to extract locations, 
    organizations, and other entities.
    """
    
    def __init__(
        self,
        model_name: str = "dslim/bert-base-NER",
        device: Optional[str] = None
    ):
        """
        Initialize the NER model
        
        Args:
            model_name: BERT-based NER model
                       Default: dslim/bert-base-NER (More accurate than DistilBERT)
            device: Device to run on
        """
        self.device = device or get_device()
        self.model_device = 0 if self.device == "cuda" else -1
        
        logger.info(f"Loading NER model: {model_name}")
        
        try:
            self.ner_pipeline = pipeline(
                "ner", 
                model=model_name, 
                tokenizer=model_name, 
                aggregation_strategy="max", # Use max for better handling of fragmented entities
                device=self.model_device
            )
            logger.info(f"NER model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load NER model: {e}")
            raise

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract entities from text and clean results.
        """
        if not text or len(text.strip()) < 5:
            return []
            
        try:
            results = self.ner_pipeline(text)
            entities = []

            for res in results:
                word = res["word"].replace(" ", " ").strip()
                label = res["entity_group"]
                
                # Cleanup common subword artifacts if any remain
                if word.startswith("##"):
                    if entities:
                        entities[-1]["entity"] += word[2:]
                    continue
                
                # Skip artifacts
                if word in ["[SEP]", "[CLS]", "[PAD]"] or len(word) < 2:
                    continue

                entities.append({
                    "entity": word.strip(",. "),
                    "label": label,
                    "confidence": float(res["score"]),
                    "start": res["start"],
                    "end": res["end"]
                })
            
            # Deduplication logic with position awareness
            unique_entities = []
            seen_entities = set()

            for ent in entities:
                key = (ent["entity"].lower(), ent["label"])
                if key not in seen_entities:
                    unique_entities.append(ent)
                    seen_entities.add(key)
                    
            return unique_entities
        except Exception as e:
            logger.error(f"NER extraction failed: {e}")
            return []

    def get_locations(self, text: str) -> List[str]:
        """Helper to specifically get location entities with cleaning"""
        # Start with model entities
        entities = self.extract_entities(text)
        raw_locations = [ent["entity"] for ent in entities if ent["label"] in ["LOC", "GPE"]]
        
        # Add regex matches
        import re
        location_patterns = [
            r"([A-Z][a-z]+ (District|Province|City|Village|Ward))",
            r"((Central|Western|Eastern|Northern|Southern|Sudurpashchim|Lumbini|Bagmati|Gandaki|Karnali|Madhesh) Provinces?)",
            r"((Kathmandu|Lalitpur|Bhaktapur|Pokhara|Chitwan|Narayani|Butwal|Biratnagar|Nepalgunj|Surkhet|Dhangadhi))"
        ]
        
        for pattern in location_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                raw_locations.append(match.group(0).strip())
        
        # Deduplicate and normalize
        unique_locations = []
        for loc in raw_locations:
            # Capitalize
            norm_loc = " ".join([w.capitalize() for w in loc.split()])
            
            is_dup = False
            for i, existing in enumerate(unique_locations):
                # exact or plural match
                if norm_loc == existing or norm_loc == f"{existing}s" or existing == f"{norm_loc}s":
                    is_dup = True
                    break
                # Substring match (keep longer)
                if norm_loc in existing or existing in norm_loc:
                    if len(norm_loc) > len(existing):
                        unique_locations[i] = norm_loc
                    is_dup = True
                    break
            
            if not is_dup:
                unique_locations.append(norm_loc)
        
        return sorted(unique_locations)
