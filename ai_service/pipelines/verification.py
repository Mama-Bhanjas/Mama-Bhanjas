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
        news_model_name: str = "hamzab/roberta-fake-news-classification",
        report_model_name: str = "valhalla/distilbart-mnli-12-1",
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

            # For Hate-speech-CNERG/roberta-base-fake-news-detector
            # Labels mapping: 0 -> Fake, 1 -> Real
            self.news_labels_map = {0: "Fake", 1: "Real"}
            
            # Check model config for actual label names if available
            if hasattr(self.news_model.config, 'id2label'):
                logger.info(f"Model ID2Label: {self.news_model.config.id2label}")

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
                
                # Model confidence for each class
                # Labels: 0 (Fake), 1 (Real)
                prob_fake = probs[0][0].item()
                prob_real = probs[0][1].item()
                
                verdict = "Real" if prob_real > prob_fake else "Fake"
                content_confidence = max(prob_fake, prob_real)

            # 2. Source & Fact Check Analysis
            source_score = 0.5 # Neutral
            fact_check_score = 0.5 # Neutral
            found_sources = []
            primary_sources = []
            explanation = ""
            verification_method = "Hybrid Analysis"

            if source_url:
                source_result = self.source_checker.check_source(source_url)
                s_status = source_result["status"]
                if s_status == "Trusted":
                    source_score = 1.0
                    explanation = f"Verified by trusted source: {source_url}. "
                elif s_status == "Untrusted":
                    source_score = 0.0
                    explanation = f"Source {source_url} is flagged as untrusted. "
                else:
                    source_score = 0.5
                    explanation = f"Source {source_url} is unknown. "
                
                primary_sources = [{
                    "url": source_url,
                    "status": s_status,
                    "score": source_score
                }]
            else:
                # Auto-Search (Fact Check)
                try:
                    if not hasattr(self, 'fact_checker'):
                        from ai_service.pipelines.fact_check import FactCheckPipeline
                        self.fact_checker = FactCheckPipeline()

                    fc_result = self.fact_checker.verify_claim(text)
                    found_sources = fc_result.get("sources", [])
                    primary_sources = fc_result.get("primary_sources", [])
                    explanation = fc_result.get("explanation", "")

                    if fc_result.get("status") == "Verified":
                        fact_check_score = 1.0
                    elif fc_result.get("status") == "Fake":
                        fact_check_score = 0.0
                    else:
                        fact_check_score = 0.5
                except Exception as e:
                    logger.warning(f"Fact check failed: {e}")

            # 4. Zero-Shot Content Validation
            # Specialized models are often biased; DistilBART cross-check provides a robust second opinion.
            zs_result = self.report_classifier.classify(
                text=text,
                categories=["legitimate news report", "fictional hoax or misinformation", "unverified rumor"],
                hypothesis_template="This text is {}."
            )
            # Find the score for 'legitimate news report'
            zs_prob_real = 0.5
            for cat in zs_result["top_categories"]:
                if cat["category"] == "legitimate news report":
                    zs_prob_real = cat["raw_score"]
                    break

            # Combine scores: Weighted average of specialized model and zero-shot model
            content_score = (prob_real * 0.4) + (zs_prob_real * 0.6)
            
            # 5. Weighted Scoring
            # Weights: Content (0.4), Source (0.6)
            # Trusted sources are very influential baseline.
            w_content, w_source = 0.4, 0.6
            
            if not source_url:
                w_content, w_source = 0.7, 0.3 # Rely more on models, search as secondary
                source_score = fact_check_score # Use fact check score as source score
            
            final_score = (content_score * w_content) + (source_score * w_source)
            
            # 6. Double Check Pattern Penalties
            norm_text = text.lower().replace("-", " ")
            suspicious_matches = [w for w in self.source_checker.SUSPICIOUS_KEYWORDS if w.replace("-", " ") in norm_text]
            
            if suspicious_matches:
                penalty = 0.1 * len(suspicious_matches[:2])
                final_score = max(0.0, final_score - penalty)
                explanation += f"Found suspicious patterns: {', '.join(suspicious_matches[:2])}. "

            # 7. Final Verdict
            is_reliable = final_score > 0.6
            if final_score > 0.8:
                final_status = "Verified"
            elif final_score > 0.6:
                final_status = "Likely Real"
            elif final_score > 0.4:
                final_status = "Unverified"
            else:
                final_status = "Likely Fake"

            result = {
                "success": True,
                "status": final_status,
                "confidence": final_score,
                "is_reliable": is_reliable,
                "explanation": explanation.strip(),
                "details": {
                    "method": verification_method,
                    "content_score": content_score,
                    "model_score": prob_real,
                    "zs_score": zs_prob_real,
                    "source_score": source_score,
                    "explanation": explanation.strip(),
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