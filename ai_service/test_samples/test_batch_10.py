
import requests
import json
import sys
import os
from loguru import logger

# Configuration
BASE_URL = os.environ.get("AI_SERVICE_URL", "http://127.0.0.1:8000/api")

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
logger.add("ai_service/test_sample_logs/test_batch_10.log", format="{message}", encoding="utf-8", mode="w")

def test_process_report(text, source_url=None, label=""):
    """Test the /api/process/report endpoint"""
    logger.info("="*60)
    logger.info(f"PROCESSING ARTICLE: {label}")
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
            logger.info(f"Status: {data['verification']['status']}")
            logger.info(f"Reliable: {data['verification']['is_reliable']}")
            logger.info(f"Category: {data['primary_category']}")
            logger.info(f"NER Locations: {data['location_entities']}")
            logger.info(f"Disaster/Type: {data['disaster_type']}")
            logger.info(f"Summary: {data['summary'][:100]}...")
            
            # Print full result to log
            logger.debug(f"FULL JSON for {label}:\n{json.dumps(result, indent=2)}")
            return result
        else:
            logger.error(f"Failed: {result.get('error')}")
            return None
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    logger.info("STARTING BATCH 10 END-TO-END VERIFICATION")
    
    # Article 1: Cold Wave in Saptari (Real)
    text_1 = (
        "Headline: District Disaster Management Committee in Saptari Calls Emergency Meeting as Cold Wave Paralyzes Tarai. "
        "Content: A severe cold wave has swept across the Tarai plains for the sixth consecutive day... "
        "The District Disaster Management Committee (DDMC) convened an emergency meeting on Wednesday to assess the risk... "
        "Chief District Officer Tuwaraj Pokharel stated that resources for firewood and warm blankets are being mobilized..."
    )
    test_process_report(text_1, "https://risingnepaldaily.com/news/73042", "Batch 10 - Article 1: Cold Wave (Real)")

    # Article 2: Mega-Thrust Earthquake (Fake)
    text_2 = (
        "Headline: Seismologists Warn of 'Mega-Thrust' Earthquake in Bagmati Province Within Next 48 Hours. "
        "Content: Leaked data from the National Earthquake Monitoring Center suggests that a massive 8.2 magnitude "
        "earthquake is imminent in the Kathmandu Valley. Sensors near the Bagmati river have detected unusual "
        "'sub-surface electromagnetic pulses'... Government officials are reportedly keeping the data secret..."
    )
    test_process_report(text_2, None, "Batch 10 - Article 2: Earthquake Alarmism (Fake)")

    logger.info("BATCH 10 PROCESSING COMPLETED")
