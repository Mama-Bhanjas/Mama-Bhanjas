
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
logger.add("ai_service/test_sample_logs/test_batch_11.log", format="{message}", encoding="utf-8", mode="w")

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
    logger.info("STARTING BATCH 11 END-TO-END VERIFICATION")
    
    # Article 1: Forest Fire in Solukhumbu (Real)
    text_1 = (
        "Headline: Forest Fire Reported in Solukhumbu Private Jungle; Municipal Police Contain Blaze Near Phaplu. "
        "Content: A wildfire broke out on Wednesday afternoon in a private forest area in Surke, Solu Dudhkunda Municipality-4. "
        "The fire, which spread rapidly due to the unusually dry winter conditions, was brought under control after a three-hour "
        "joint effort by municipal police, airport security guards from Phaplu, and local residents. "
        "The National Disaster Risk Reduction and Management Authority (NDRRMA) noted that fire incidents have been recorded in 15 districts..."
    )
    test_process_report(text_1, "https://english.onlinekhabar.com/fire-incidents-reported-in-15-districts-forest-fires-in-3-districts-within-24-hours.html", "Batch 11 - Article 1: Forest Fire (Real)")

    # Article 2: Kulekhani Dam Fissure (Fake)
    text_2 = (
        "Headline: Emergency Alert: Kulekhani Dam Shows 'Structural Fissures'; Authorities Prepare for Immediate Release of Water. "
        "Content: Engineers at the Kulekhani Hydropower Project have reportedly detected a three-meter vertical crack in the main dam wall... "
        "A leaked internal memo suggests that the dam is at 'critical capacity' and a catastrophic failure could occur within the next six hours. "
        "Residents in the downstream areas of Makwanpur and Rautahat are being told by local youth groups to evacuate to higher ground immediately."
    )
    test_process_report(text_2, None, "Batch 11 - Article 2: Dam Failure Alarmism (Fake)")

    logger.info("BATCH 11 PROCESSING COMPLETED")
