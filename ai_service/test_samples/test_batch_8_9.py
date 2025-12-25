
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
logger.add("ai_service/test_sample_logs/test_batch_8_9.log", format="{message}", encoding="utf-8", mode="w")

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
    logger.info("STARTING BATCH 8 & 9 END-TO-END VERIFICATION")
    
    # Article W: Bridge Project (Real scenario)
    text_w = (
        "Headline: Inter-Provincial Bridge Project Reaches 85% Completion; Set for February Inauguration. "
        "Content: The Department of Roads confirmed today that the construction of the major bridge connecting "
        "the central and western provinces has entered its final phase. Engineers reported that the main suspension "
        "cables and deck segments are now fully secured. The project was delayed by six months due to unseasonal monsoon flooding..."
    )
    # Using the Kathmandu Post Narayani bridge URL as a plausible grounding
    test_process_report(text_w, "https://kathmandupost.com/chitwan/2024/11/30/construction-of-iconic-narayani-bridge-begins", "Article W: Bridge Project (Real)")

    # Article X: E-Waste Fine (Real scenario)
    text_x = (
        "Headline: Electronics Manufacturer Fined for Non-Compliance with E-Waste Disposal Regulations. "
        "Content: National environmental regulators have imposed a fine on a prominent consumer electronics manufacturer "
        "for failing to meet mandatory recycling targets for the 2024-2025 fiscal year. The audit revealed that "
        "the company managed to collect only 12% of its end-of-life products, falling short of the 25% requirement..."
    )
    test_process_report(text_x, "https://www.downtoearth.org.in/pollution/cpcb-to-crack-the-whip-on-e-waste-recycling-non-compliance-90145", "Article X: E-Waste Fine (Real)")

    # Article Y: Saltwater Battery (Fake)
    text_y = (
        "Headline: Amateur Inventor Develops 'Saltwater Battery' Capable of Powering a Home for a Decade Without Recharging. "
        "Content: A retired chemistry teacher in a small coastal town has reportedly perfected a revolutionary energy storage "
        "device that uses common seawater to generate a continuous 10kW output. The 'Blue-Spark' cell allegedly utilizes a secret alloy..."
    )
    test_process_report(text_y, None, "Article Y: Saltwater Battery (Fake)")

    # Article Z: Social Credit Score (Fake)
    text_z = (
        "Headline: Mandatory 'Social Credit Score' Linked to Digital Wallets to be Implemented for Online Shopping. "
        "Content: A leaked draft from a global financial regulatory summit suggests that starting in October 2026, "
        "all major e-commerce platforms will be required to display a 'Reliability Rating' for every user. This score "
        "will reportedly be calculated based on a user's social media history, promptness of bill payments, and 'online civility'..."
    )
    test_process_report(text_z, None, "Article Z: Social Credit Score (Fake)")

    logger.info("BATCH 8 & 9 PROCESSING COMPLETED")
