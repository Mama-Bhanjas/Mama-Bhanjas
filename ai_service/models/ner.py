
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
        model_name: str = "dslim/distilbert-NER",
        device: Optional[str] = None
    ):
        """
        Initialize the NER model
        
        Args:
            model_name: BERT-based NER model
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
                aggregation_strategy="simple",
                device=self.model_device
            )
            logger.info(f"NER model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load NER model: {e}")
            raise

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract entities from text and clean subword tokens.
        """
        if not text or len(text.strip()) < 5:
            return []
            
        try:
            results = self.ner_pipeline(text)
            
            # Clean up results and reconstruct subwords if the pipeline didn't catch them
            # Although 'simple' aggregation should handle this, some models still leak '##'
            entities = []
            for res in results:
                word = res["word"]
                # Skip or merge subwords if they appear as standalone
                if word.startswith("##"):
                    if entities:
                        entities[-1]["entity"] += word[2:]
                    continue
                
                # Check for " [SEP]" or " [CLS]" or other artifacts
                if word in ["[SEP]", "[CLS]", "[PAD]"]:
                    continue

                entities.append({
                    "entity": word.replace(" ", " ").strip(),
                    "label": res["entity_group"],
                    "confidence": float(res["score"]),
                    "start": res["start"],
                    "end": res["end"]
                })
            
            # Final deduplication and cleaning of the string
            seen = set()
            unique_entities = []
            for ent in entities:
                ent["entity"] = ent["entity"].strip(",. ")
                if not ent["entity"] or len(ent["entity"]) < 2:
                    continue
                
                # Deduplication key
                key = (ent["entity"].lower(), ent["label"])
                if key not in seen:
                    unique_entities.append(ent)
                    seen.add(key)
                    
            return unique_entities
        except Exception as e:
            logger.error(f"NER extraction failed: {e}")
            return []

    def get_locations(self, text: str) -> List[str]:
        """Helper to specifically get location entities with cleaning"""
        entities = self.extract_entities(text)
        # LOC (Location) label in dslim/distilbert-NER or dslim/bert-base-NER
        locations = []
        for ent in entities:
            if ent["label"] in ["LOC", "GPE"]:
                loc = ent["entity"]
                if loc not in locations:
                    locations.append(loc)
        
        return sorted(locations)
