
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
from ai_service.utils.content_extractor import ContentExtractor

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
        self.extractor = ContentExtractor()
        
        logger.info("Unified Processor initialized")

    @property
    def classify_p(self):
        if self._classify is None:
            import os
            local_path = "ai_service/models/custom_classifier"
            # If local doesn't exist, use Hugging Face repo
            if os.path.exists(local_path):
                model_path = local_path
                logger.info(f"Using local fine-tuned Classification model from {model_path}")
            else:
                model_path = "Sachin1224/nepal-disaster-classifier"
                logger.info(f"Using Hugging Face fine-tuned Classification model: {model_path}")
                 
            self._classify = ClassificationPipeline(model_name=model_path, device=self.device)
        return self._classify

    @property
    def summarize_p(self):
        if self._summarize is None:
            import os
            local_path = "ai_service/models/custom_summarizer" 
            if os.path.exists(local_path):
                model_path = local_path
                logger.info(f"Using local fine-tuned Summarization model from {model_path}")
            else:
                model_path = "Sachin1224/nepal-disaster-summarizer"
                logger.info(f"Using Hugging Face fine-tuned Summarization model: {model_path}")

            self._summarize = SummarizationPipeline(model_name=model_path, device=self.device)
        return self._summarize

    @property
    def ner_p(self):
        if self._ner is None:
            import os
            local_path = "ai_service/models/custom_ner"
            if os.path.exists(local_path):
                model_path = local_path
                logger.info(f"Using local fine-tuned NER model from {model_path}")
                self._ner = NERPipeline(ner_model=model_path, device=self.device)
            else:
                model_path = "Sachin1224/nepal-disaster-ner"
                logger.info(f"Using Hugging Face fine-tuned NER model: {model_path}")
                self._ner = NERPipeline(ner_model=model_path, device=self.device)
        return self._ner

    @property
    def verify_p(self):
        if self._verify is None:
            import os
            local_path = "ai_service/models/custom_verifier"
            if os.path.exists(local_path):
                 logger.info(f"Using local fine-tuned Verification model from {local_path}")
                 self._verify = VerificationPipeline(news_model_name=local_path)
            else:
                model_path = "Sachin1224/nepal-disaster-verifier"
                logger.info(f"Using Hugging Face fine-tuned Verification model: {model_path}")
                self._verify = VerificationPipeline(news_model_name=model_path)
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
            # 0. Text Extraction
            extracted_text = None
            extraction_method = "direct"
            actual_text = text
            
            if file_bytes:
                logger.info("Processing PDF file input")
                extraction = self.extractor.extract_from_pdf(file_bytes)
                if extraction["success"]:
                    actual_text = extraction["text"]
                    extracted_text = actual_text
                    extraction_method = "pdf"
                    logger.info(f"Successfully extracted {len(actual_text)} characters from PDF")
                else:
                    return {
                        "success": False, 
                        "report_id": request_id, 
                        "error": f"PDF extraction failed: {extraction.get('error')}"
                    }
            elif self.extractor.is_url(text):
                logger.info(f"Detected URL input, extracting content: {text}")
                extraction = self.extractor.extract_from_url(text)
                if extraction["success"]:
                    extracted_text = extraction["text"]
                    actual_text = extracted_text
                    source_url = text  # Use the URL as source
                    extraction_method = "url"
                    logger.info(f"Successfully extracted {len(actual_text)} characters from URL")
                else:
                    logger.warning(f"URL extraction failed: {extraction.get('error')}, treating as regular text")
                    actual_text = text
            
            if not actual_text:
                return {
                    "success": False,
                    "report_id": request_id,
                    "error": "No content provided or extracted"
                }
            
            # 1. Classification (General categories)
            cls_result = self.classify_p.process(actual_text)
            
            # 2. Summarization
            sum_result = self.summarize_p.process(actual_text)
            
            # 3. NER (Locations & Disaster Specifics)
            ner_result = self.ner_p.process(actual_text)
            
            # 4. Verification
            # If it has a URL OR it looks like a news article (long + has headline), use news pipeline
            is_likely_news = source_url is not None or "Headline:" in actual_text or len(actual_text) > 300
            
            if is_likely_news:
                ver_result = self.verify_p.verify_news(actual_text, source_url)
            else:
                ver_result = self.verify_p.verify_report(actual_text)
                
            # 5. Similarity Testing
            sim_results = self._check_similarity(actual_text)
            
            # Memory Cleanup after heavy processing
            self._clear_memory()
                
            # Combine into PostgreSQL-ready format
            output = {
                "success": True,
                "report_id": request_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "original_text": text,
                "extracted_text": extracted_text,  # NEW: Include extracted text if URL was used
                "extraction_method": extraction_method,  # NEW: How text was obtained
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
                    "text_length": len(actual_text),
                    "has_source": source_url is not None,
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
