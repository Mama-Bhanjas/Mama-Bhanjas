
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
        
        from ai_service.utils.content_extractor import ContentExtractor
        self.extractor = ContentExtractor()
        
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

    def process_report(
        self, 
        text: Optional[str] = None, 
        source_url: Optional[str] = None,
        file_bytes: Optional[bytes] = None
    ) -> Dict[str, any]:
        """
        Run all analysis on a single report. 
        Input can be raw text, a URL (detected in text or source_url), or PDF bytes.
        """
        request_id = str(uuid.uuid4())
        logger.info(f"Processing report {request_id}")
        
        try:
            # 0. Context Extraction
            input_text = text or ""
            metadata_source = source_url
            
            # If text is a URL, extract from it
            if input_text and self.extractor.is_url(input_text):
                ext_result = self.extractor.extract_from_url(input_text)
                if ext_result["success"]:
                    metadata_source = input_text
                    input_text = ext_result["text"]
                    logger.info(f"Extracted {len(input_text)} characters from URL")
            
            # If file_bytes provided, assume it's a PDF
            if file_bytes:
                ext_result = self.extractor.extract_from_pdf(file_bytes)
                if ext_result["success"]:
                    input_text = ext_result["text"]
                    logger.info(f"Extracted {len(input_text)} characters from PDF")

            if not input_text or len(input_text) < 10:
                return {"success": False, "error": "Insufficient text content for analysis"}

            # 1. Classification (General categories)
            cls_result = self.classify_p.process(input_text)
            
            # 2. Summarization
            sum_result = self.summarize_p.process(input_text)
            
            # 3. NER (Locations & Disaster Specifics)
            ner_result = self.ner_p.process(input_text)
            
            # 4. Verification
            # If it has a URL OR it looks like a news article (long + has headline), use news pipeline
            is_likely_news = metadata_source is not None or "Headline:" in input_text or len(input_text) > 300
            
            if is_likely_news:
                ver_result = self.verify_p.verify_news(input_text, metadata_source)
            else:
                ver_result = self.verify_p.verify_report(input_text)
                
            # 5. Similarity Testing
            sim_results = self._check_similarity(input_text)
            
            # Memory Cleanup after heavy processing
            self._clear_memory()
                
            # Combine into PostgreSQL-ready format
            output = {
                "success": True,
                "report_id": request_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "original_text": text or "File/URL Upload",
                "extracted_text": input_text[:1000] + ("..." if len(input_text) > 1000 else ""),
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
                    "text_length": len(input_text),
                    "has_source": metadata_source is not None,
                    "source_url": metadata_source,
                    "all_entities": ner_result.get("all_entities", [])
                }
            }
            
            logger.info(f"Successfully processed report {request_id}")
            return output
            
        except Exception as e:
            logger.error(f"Unified processing failed for {request_id}: {e}")
            return {
                "success": False,
                "report_id": request_id,
                "error": str(e)
            }
