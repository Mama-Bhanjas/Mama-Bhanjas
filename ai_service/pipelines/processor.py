
from typing import List, Dict, Optional
import datetime
import uuid
import gc
import torch
from loguru import logger

from ai_service.pipelines.classify import ClassificationPipeline
from ai_service.pipelines.summarize import SummarizationPipeline
from ai_service.pipelines.ner import NERPipeline
from ai_service.pipelines.verification import VerificationPipeline

class UnifiedProcessor:
    """
    Main entry point for processing reports.
    Coordinates all pipelines to produce a single, structured output
    suitable for database storage and frontend display.
    """
    
    def __init__(self, device: Optional[str] = None):
        """
        Initialize all sub-pipelines lazily or immediately.
        We'll use internal lazy loading to avoid memory spikes if not all are needed.
        """
        self.device = device
        self._classify = None
        self._summarize = None
        self._ner = None
        self._verify = None
        
        logger.info("Unified Processor initialized")

    @property
    def classify_p(self):
        if self._classify is None:
            self._classify = ClassificationPipeline(device=self.device)
        return self._classify

    @property
    def summarize_p(self):
        if self._summarize is None:
            self._summarize = SummarizationPipeline(device=self.device)
        return self._summarize

    @property
    def ner_p(self):
        if self._ner is None:
            self._ner = NERPipeline(device=self.device)
        return self._ner

    @property
    def verify_p(self):
        if self._verify is None:
            self._verify = VerificationPipeline() # Verification manages its own sub-pipelines
        return self._verify

    def _clear_memory(self):
        """Force garbage collection and clear torch cache"""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
    def _check_similarity(self, text: str) -> List[Dict]:
        """
        Check similarity against recent reports (Mock implementation for now)
        In production, this would query a Vector DB like Pinecone or PGVector.
        """
        # Mock recent reports for demonstration
        mock_corpus = [
            {"id": "sim-1", "text": "Flood warning issued for Kathmandu districts."},
            {"id": "sim-2", "text": "Government announces bridge construction in western province."},
            {"id": "sim-3", "text": "New e-waste regulations for electronic manufacturers."}
        ]
        
        # Simple string-based similarity score (Mock)
        results = []
        text_lower = text.lower()
        for item in mock_corpus:
            # Fake score based on keyword overlap for this demo
            words = set(item["text"].lower().split())
            intersection = words.intersection(set(text_lower.split()))
            score = len(intersection) / len(words) if words else 0
            if score > 0.1:
                results.append({
                    "report_id": item["id"],
                    "similarity_score": round(score, 2),
                    "summary": item["text"]
                })
        return sorted(results, key=lambda x: x["similarity_score"], reverse=True)

    def process_report(self, text: str, source_url: Optional[str] = None) -> Dict[str, any]:
        """
        Run all analysis on a single report
        """
        request_id = str(uuid.uuid4())
        logger.info(f"Processing report {request_id}")
        
        try:
            # 1. Classification (General categories)
            cls_result = self.classify_p.process(text)
            
            # 2. Summarization
            sum_result = self.summarize_p.process(text)
            
            # 3. NER (Locations & Disaster Specifics)
            ner_result = self.ner_p.process(text)
            
            # 4. Verification
            # If it has a URL OR it looks like a news article (long + has headline), use news pipeline
            is_likely_news = source_url is not None or "Headline:" in text or len(text) > 300
            
            if is_likely_news:
                ver_result = self.verify_p.verify_news(text, source_url)
            else:
                ver_result = self.verify_p.verify_report(text)
                
            # 5. Similarity Testing
            sim_results = self._check_similarity(text)
            
            # Memory Cleanup after heavy processing
            self._clear_memory()
                
            # Combine into PostgreSQL-ready format
            output = {
                "report_id": request_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "original_text": text,
                "summary": sum_result.get("summary", ""),
                "primary_category": cls_result.get("category", "Other"),
                "category_confidence": cls_result.get("confidence", 0.0),
                "location_entities": ner_result.get("locations", []),
                "disaster_type": ner_result.get("disaster_type", "Unknown"),
                "type_confidence": ner_result.get("type_confidence", 0.0),
                "verification": {
                    "status": ver_result.get("status", "Unknown"),
                    "is_reliable": ver_result.get("is_reliable", False),
                    "confidence": ver_result.get("confidence", 0.0),
                    "explanation": ver_result.get("explanation", "")
                },
                "similarity": {
                    "top_matches": sim_results,
                    "count": len(sim_results)
                },
                "metadata": {
                    "text_length": len(text),
                    "has_source": source_url is not None,
                    "all_entities": ner_result.get("all_entities", [])
                }
            }
            
            logger.info(f"Successfully processed report {request_id}")
            return {
                "success": True,
                "data": output
            }
            
        except Exception as e:
            logger.error(f"Unified processing failed for {request_id}: {e}")
            return {
                "success": False,
                "report_id": request_id,
                "error": str(e)
            }
