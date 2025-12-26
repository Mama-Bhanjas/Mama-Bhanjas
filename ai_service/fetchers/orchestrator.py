
from typing import List, Dict, Optional
import os
from loguru import logger
import asyncio

from ai_service.fetchers.bipad_client import BIPADFetcher
from ai_service.fetchers.reliefweb_client import ReliefWebFetcher
from ai_service.fetchers.usgs_client import USGSFetcher
from ai_service.fetchers.news_client import NewsFetcher
from ai_service.pipelines.processor import UnifiedProcessor

class MultiSourceFetcher:
    """
    Orchestrator for the "Trust-Weighted Summarization" Architecture.
    Combines Levels 1-4 to produce verifiable intelligence.
    """
    
    def __init__(self, news_api_key: str = "PLACEHOLDER", test_mode: bool = False):
        self.bipad = BIPADFetcher()
        self.relief = ReliefWebFetcher()
        self.usgs = USGSFetcher()
        self.news = NewsFetcher(api_key=news_api_key)
        self.test_mode = test_mode  # Limits news to 5 articles for faster testing
        
        # Load our fine-tuned AI brain
        self.ai = UnifiedProcessor()
        
    def poll_all_sources(self) -> Dict[str, List]:
        """
        Execute the full 4-Level polling cycle.
        """
        logger.info("Starting Multi-Source Poll Cycle...")
        
        # 1. Level 3 (Speed/Triggers) - Check first!
        triggers = self.usgs.fetch_triggers()
        
        # 2. Level 1 (The Anchor)
        official_data = self.bipad.fetch_recent_incidents()
        
        # 3. Level 2 (Context)
        context_reports = self.relief.fetch_nepal_reports()
        
        # 4. Level 4 (Analysis candidates)
        news_reports = self.news.fetch_disaster_news()
        
        # TEST MODE: Limit to 5 articles for faster testing
        # TO REMOVE THIS LIMIT: Set test_mode=False when creating MultiSourceFetcher
        if self.test_mode and len(news_reports) > 5:
            logger.info(f"TEST MODE: Limiting news from {len(news_reports)} to 5 articles")
            news_reports = news_reports[:5]
        
        # 5. The "Intelligence" Layer: Cross-Reference
        # We process news reports through our AI to see if they match Level 1
        processed_news = []
        for report in news_reports:
            verified_report = self._verify_against_anchor(report, official_data)
            
            # ONLY include it if it's a real disaster (not skipped or rejected)
            if verified_report.get("status") not in ["Skipped (Not a Disaster)", "Rejected (AI Detected Fake)", "Skipped (No Text)", "Skipped (Not Nepal Related)"]:
                processed_news.append(verified_report)
            
        return {
            "triggers": triggers,
            "official_incidents": official_data,
            "context": context_reports,
            "news_intelligence": processed_news
        }
        
    def _verify_against_anchor(self, news_item: Dict, anchor_data: List[Dict]) -> Dict:
        """
        Uses trained AI models to extract details from news,
        then cross-references against BIPAD data.
        """
        text = news_item.get("text", "")
        if not text: 
            news_item["status"] = "Skipped (No Text)"
            return news_item
        
        try:
            # A. AI Analysis (Classification, NER, Verification)
            ai_result = self.ai.process_report(text=text, source_url=news_item.get("url"))
            
            if not ai_result.get("success", False):
                logger.warning(f"AI processing failed for {news_item.get('title')}: {ai_result.get('error')}")
                news_item["status"] = "Unverified (AI Processing Failed)"
                return news_item
            
            # Extract core signals
            ai_locs = ai_result.get("location_entities", [])
            ai_type = ai_result.get("disaster_type", "Unknown")
            ai_cat = ai_result.get("primary_category", "Other")
            verification = ai_result.get("verification", {})
            ver_status = verification.get("status", "Unknown")
            is_reliable = verification.get("is_reliable", False)
            
            # Looser Disaster Filtering: If the API gave it to us, only skip if clearly irrelevant (Other + Unknown)
            # And if it's even slightly reliable, we keep it.
            if ai_cat == "Other" and ai_type in ["Unknown", "Other"] and not is_reliable and "disaster" not in text.lower():
                logger.info(f"Filtered out: {news_item.get('title')} - Classified as {ai_cat}/{ai_type}")
                news_item["status"] = "Skipped (Not a Disaster)"
                return news_item

            if ver_status == "Likely Fake":
                logger.warning(f"Rejected Fake: {news_item.get('title')}")
                news_item["status"] = "Rejected (AI Detected Fake)"
                return news_item

            # Location Validation: Since NewsData.io is already filtered by country='np', we are lenient
            has_nepal_context = (
                len(ai_locs) > 0 or 
                "nepal" in text.lower() or 
                "nepal" in news_item.get("title", "").lower() or
                news_item.get("source") == "NewsData.io" # Trust the API's country filter
            )
            
            if not has_nepal_context:
                logger.info(f"Skipping (No Nepal context): {news_item.get('title')}")
                news_item["status"] = "Skipped (Not Nepal Related)"
                return news_item

            # B. Cross-Reference Logic
            # Does this location and type appear in official BIPAD data?
            match_found = False
            matching_anchor = None
            
            for anchor in anchor_data:
                anchor_loc = anchor.get("location", "")
                anchor_type = anchor.get("type", "")
                
                # Simple heuristic matching
                # In production, use fuzzy string matching or geo-coordinates
                if (anchor_loc in ai_locs or any(l in anchor_loc for l in ai_locs)) and \
                   (ai_type.lower() in anchor_type.lower() or anchor_type.lower() in ai_type.lower()):
                    match_found = True
                    matching_anchor = anchor
                    break
            
            # C. Assign Trust Status
            if match_found:
                news_item["status"] = "Verified (Official Confirmation)"
                news_item["anchor_id"] = matching_anchor["id"]
            else:
                news_item["status"] = "Unverified (Volunteer Source)"
                news_item["confidence"] = "Medium - Waiting for BIPAD confirmation"
                
            # Enrich with AI data - Comprehensive flattened structure
            news_item.update({
                "original_article": text,
                "summarization": ai_result.get("summary", ""),
                "category": ai_result.get("primary_category", "Other"),
                "disaster_type": ai_result.get("disaster_type", "Unknown"),
                "verification": ai_result.get("verification", {}),
                "source_url": news_item.get("url", ""),
                "NER_entities": ai_result.get("location_entities", []),
                "similarity_test_results": ai_result.get("similarity", {}),
                "ai_success": True
            })
            
            # Keep original title and metadata
            # Cleanup redundant fields if necessary
            if "text" in news_item: del news_item["text"]
            
        except Exception as e:
            logger.error(f"Error in AI verification: {e}")
            news_item["status"] = "Unverified (Processing Error)"
            news_item["error"] = str(e)
        
        return news_item
