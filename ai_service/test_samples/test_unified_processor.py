
import requests
import json
import sys
import os
from loguru import logger

# Configuration
BASE_URL = os.environ.get("AI_SERVICE_URL", "http://localhost:8000/api")

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
logger.add("ai_service/test_sample_logs/test_unified_processor.log", format="{message}", encoding="utf-8", mode="w")

def test_process_report(text, source_url=None, label=""):
    """Test the /api/process/report endpoint"""
    logger.info("="*60)
    logger.info(f"TESTING UNIFIED PROCESS: {label}")
    logger.info(f"Text Snippet: {text[:80]}...")
    
    payload = {"text": text}
    if source_url:
        payload["source_url"] = source_url
    
    try:
        response = requests.post(f"{BASE_URL}/process/report", json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result["success"]:
            data = result["data"]
            logger.info(f"✓ Success! Report ID: {data['report_id']}")
            logger.info(f"Summary: {data['summary'][:100]}...")
            logger.info(f"Category: {data['primary_category']} ({data['category_confidence']:.2f})")
            logger.info(f"Entities: Locations={data['location_entities']}")
            logger.info(f"Disaster Type: {data['disaster_type']} ({data['type_confidence']:.2f})")
            logger.info(f"Verification: {data['verification']['status']} (Reliable: {data['verification']['is_reliable']})")
            
            # Print full JSON for review of DB compatibility
            logger.debug(f"Full JSON: {json.dumps(result, indent=2)}")
            return result
        else:
            logger.error(f"✗ Failed: {result.get('error')}")
            return None
            
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    logger.info("STARTING UNIFIED PROCESSOR VALIDATION")
    
    # scenario 1: Civic report (Disaster)
    flood_text = (
        "Serious flooding reported in the Kathmandu Valley, specifically near the Bagmati River in Balkhu. "
        "Dozens of houses are submerged and people are stranded on rooftops. Rescue teams are needed immediately."
    )
    test_process_report(flood_text, label="Scenario 1: Flood in Balkhu")
    
    # Scenario 2: News article (Tech/Health)
    ai_text = (
        "OpenAI has released a new safety layer for its models to prevent malicious use in biological research. "
        "The update follows concerns from global health experts in Geneva."
    )
    test_process_report(ai_text, source_url="https://techcrunch.com/openai-safety-geneva", label="Scenario 2: AI Safety news")
    
    logger.info("UNIFIED PROCESSOR VALIDATION COMPLETED")
