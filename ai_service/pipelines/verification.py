"""
Verification Pipeline
Checks credibility of news and validity of civic reports
"""
from typing import List, Dict, Optional
from loguru import logger
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

from ai_service.models.classifier import CategoryClassifier
from ai_service.utils import TextPreprocessor, validate_text_input, ModelCache, get_device
from ai_service.utils.source_checker import SourceChecker

class VerificationPipeline:
    """
    Pipeline for verifying content using dedicated models
    """

    # Categories for Report Validity (Zero-Shot) - Tuned for semantic classification
    REPORT_CATEGORIES = [
        "a civic issue",
        "spam",
        "nonsense",
        "general news or information"
    ]

    def __init__(
        self,
        news_model_name: str = "mrm8488/bert-tiny-finetuned-fake-news-detection",
        report_model_name: str = "typeform/distilbert-base-uncased-mnli",
        use_cache: bool = True,
        device: Optional[str] = None
    ):
        """
        Initialize verification pipeline
        """
        self.device = device or get_device()
        self.use_cache = use_cache
        self.preprocessor = TextPreprocessor()
        self.cache = ModelCache() if use_cache else None
        self.source_checker = SourceChecker()

        # 1. Initialize Report Classifier (Zero-Shot)
        logger.info(f"Loading Report Classifier: {report_model_name}")
        self.report_classifier = CategoryClassifier(
            model_name=report_model_name,
            categories=self.REPORT_CATEGORIES,
            device=self.device
        )

        # 2. Initialize News Fake/Real Classifier (Dedicated)
        logger.info(f"Loading News Classifier: {news_model_name}")
        try:
            self.news_tokenizer = AutoTokenizer.from_pretrained(news_model_name)
            self.news_model = AutoModelForSequenceClassification.from_pretrained(news_model_name)
            self.news_model.to(self.device)
            self.news_model.eval()

            # For mrm8488/bert-tiny-finetuned-fake-news-detection
            # Labels: 0 -> Fake, 1 -> Real
            self.news_labels_map = {0: "Fake", 1: "Real"}

        except Exception as e:
            logger.error(f"Failed to load news classifier: {e}")
            raise

        logger.info("Verification pipeline initialized")

    def verify_news(
        self,
        text: str,
        source_url: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Verify news credibility using dedicated model + source check (auto-search if no URL provided)
        """
        is_valid, error_msg = validate_text_input(text)
        if not is_valid:
            return {"success": False, "error": error_msg}

        cache_key = f"news_{hash(text)}_{hash(source_url)}"
        if self.use_cache and self.cache:
            if cached := self.cache.get(cache_key): return cached

        try:
            # 1. Content Verification (Model)
            inputs = self.news_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512
            ).to(self.device)

            with torch.no_grad():
                outputs = self.news_model(**inputs)
                probs = torch.softmax(outputs.logits, dim=1)
                confidence, predicted_class_idx = torch.max(probs, dim=1)

                predicted_idx = predicted_class_idx.item()
                confidence_score = confidence.item()

                if hasattr(self, 'news_labels_map'):
                    verdict = self.news_labels_map[predicted_idx]
                else:
                    verdict = "Real" if predicted_idx == 1 else "Fake"

            # Normalize verdict text
            is_content_reliable = verdict.lower() in ["real", "true", "reliable"]

            # 2. Source Logic
            final_status = verdict
            verification_method = "Model Analysis"
            explanation = "Analysis based on writing style."
            found_sources = []
            primary_sources = []

            if source_url:
                # A. Explicit Source Check
                source_result = self.source_checker.check_source(source_url)
                source_status = source_result["status"]
                source_score = source_result["source_score"]
                verification_method = "Model + Provided Source"

                if source_status == "Untrusted":
                    final_status = "Likely Fake (Untrusted Source)"
                    is_reliable = False
                    confidence_score = 1.0  # Certain it's unsafe
                    explanation = f"Source {source_url} is known for misinformation or satire."
                elif source_status == "Trusted":
                    final_status = "Verified (Trusted Source)"
                    is_reliable = True
                    confidence_score = 1.0  # Certain it's safe
                    explanation = f"Source {source_url} is a recognized trusted news or institutional outlet."
                    primary_sources = [{
                        "url": source_url,
                        "status": source_status,
                        "source_score": source_score,
                        "reasons": source_result.get("reasons", [])
                    }]
                else:
                    is_reliable = is_content_reliable
                    explanation = "Analysis based on writing style. Source credibility is unknown."
            else:
                # B. Auto-Search (Fact Check)
                verification_method = "Model + Internet Search"
                try:
                    # Lazy load FactCheckPipeline if not present
                    if not hasattr(self, 'fact_checker'):
                        from ai_service.pipelines.fact_check import FactCheckPipeline
                        self.fact_checker = FactCheckPipeline()

                    fc_result = self.fact_checker.verify_claim(text)
                    found_sources = fc_result.get("sources", [])
                    primary_sources = fc_result.get("primary_sources", [])
                    explanation = fc_result.get("explanation", "")

                    if fc_result.get("status") == "Verified":
                        final_status = "Verified (Corroborated)"
                        is_reliable = True
                        confidence_score = 0.95
                    elif fc_result.get("status") == "Fake":
                        final_status = "Debunked (Untrusted Sources)"
                        is_reliable = False
                        confidence_score = 0.95
                    else:
                        # Unverified by search -> Fallback to model
                        is_reliable = is_content_reliable
                        confidence_score = confidence_score * 0.65
                        final_status = f"Unverified ({verdict} by text analysis)"
                        explanation += " No corroborating high-trust sources found. Proceed with caution."

                except Exception as e:
                    logger.warning(f"Auto-search failed: {e}")
                    is_reliable = is_content_reliable

            # 3. Final Skepticism Check (Keyword override)
            # Normalize text for better keyword matching (handle spaces/hyphens)
            norm_text = text.lower().replace("-", " ")
            suspicious_matches = []
            for w in self.source_checker.SUSPICIOUS_KEYWORDS:
                clean_w = w.replace("-", " ")
                if clean_w in norm_text:
                    suspicious_matches.append(w)

            if suspicious_matches and is_reliable:
                logger.info(f"Skepticism triggered: text contains {suspicious_matches}")
                # Penalize or Flip
                if final_status.startswith("Verified (Trusted Source)"):
                    # If it's a trusted source, we still allow it but add a note
                    confidence_score *= 0.85
                    explanation += f" (Note: Content contains alarmist patterns like {suspicious_matches[0]})"
                else:
                    # Model says Real, but we found suspicious words and no trusted sources
                    is_reliable = False
                    confidence_score = 0.85
                    final_status = "Likely Fake (Suspicious Patterns)"
                    explanation = f"Model analysis suggests real, but content contains strong alarmist/misinformation patterns ({', '.join(suspicious_matches[:3])}) and lacks trusted source corroboration."

            result = {
                "success": True,
                "status": final_status,
                "confidence": confidence_score,
                "is_reliable": is_reliable,
                "details": {
                    "method": verification_method,
                    "content_verdict": verdict,
                    "content_confidence": confidence_score,
                    "explanation": explanation,
                    "found_sources": found_sources,
                    "primary_sources": primary_sources
                }
            }

            if self.use_cache and self.cache:
                self.cache.set(cache_key, result)

            return result

        except Exception as e:
            logger.error(f"News verification failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "status": "Error",
                "confidence": 0.0,
                "is_reliable": False,
                "details": {}
            }

    def verify_report(
        self,
        text: str
    ) -> Dict[str, any]:
        """
        Verify civic report validity (Zero-Shot)
        """
        cache_key = f"report_{hash(text)}"
        if self.use_cache and self.cache:
            if cached := self.cache.get(cache_key): return cached

        try:
            result = self.report_classifier.classify(
                text=text,
                top_k=1,
                categories=self.REPORT_CATEGORIES,
                hypothesis_template="This text describes {}."
            )

            verdict = result["category"]
            is_reliable = verdict == "a civic issue"

            output = {
                "success": True,
                "status": verdict,
                "confidence": result["confidence"],
                "is_reliable": is_reliable,
                "full_result": result
            }

            if self.use_cache and self.cache:
                self.cache.set(cache_key, output)
            return output

        except Exception as e:
            logger.error(f"Report verification failed: {e}")
            return {"success": False, "error": str(e)}