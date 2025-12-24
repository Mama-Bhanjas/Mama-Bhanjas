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
logger.add("verification_samples_batch5.log", format="{message}", encoding="utf-8", mode="w")

def test_verify_news(text, source_url, label):
    """Test the /api/verify/news endpoint"""
    logger.info("="*60)
    logger.info(f"TEST: {label}")
    logger.info(f"Source: {source_url if source_url else 'NONE (Auto-Search)'}")
    logger.info(f"Text Snippet: {text[:80]}...")
    
    payload = {"text": text}
    if source_url:
        payload["source_url"] = source_url
    
    try:
        response = requests.post(f"{BASE_URL}/verify/news", json=payload)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Status: {data['status']}")
        logger.info(f"Reliable: {data['is_reliable']}")
        logger.info(f"Confidence: {data['confidence']:.2f}")
        
        if 'details' in data:
            d = data['details']
            logger.info(f"Method: {d.get('method', 'Unknown')}")
            if 'explanation' in d:
                logger.info(f"Explanation: {d['explanation']}")
            
        logger.info("-" * 20)
        return data
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return None

if __name__ == "__main__":
    logger.info("STARTING VERIFICATION BATCH 5 TESTS (DEC 24, 2025)")
    
    # Article I: Judicial Ruling on Education Rights (Real)
    text_i = (
        "Headline: Supreme Court Issues Mandamus Barring Community Schools from Charging Extra Student Fees. "
        "Content: In a significant ruling for educational access, the Supreme Court has issued a writ of mandamus "
        "ordering all community schools to immediately stop collecting fees..."
    )
    test_verify_news(text_i, "https://en.setopati.com/social/165641", "Article I: Education Mandamus (Real)")
    
    # Article J: Border Conflict Escalation (Real)
    text_j = (
        "Headline: Fresh Fighting Erupts on Thailand-Cambodia Border as Ceasefire Talks Commenced. "
        "Content: Military forces from Thailand and Cambodia exchanged small arms and mortar fire early Wednesday, "
        "resulting in reported injuries on both sides of the contested border..."
    )
    test_verify_news(text_j, "https://www.aljazeera.com/news/2025/12/24/new-clashes-as-cambodia-thailand-hold-first-talks-to-end-latest-violence", "Article J: Border Conflict (Real)")
    
    # Article K: Space Launch Record (Real)
    text_k = (
        "Headline: Annual Orbital Launch Count Hits New High as Private Rocket Firm Surpasses 170 Flights. "
        "Content: The private space industry has officially broken its single-year launch record for 2025, "
        "reaching 170 orbital missions to date. The vast majority of these flights were carried out by a single California-based aerospace company..."
    )
    test_verify_news(text_k, "https://spacenews.com/spacex-170-orbital-launches-2025/", "Article K: Space Record (Real)")
    
    # Article L: Fabricated Environmental Regulation (Fake)
    text_l = (
        "Headline: Global Ocean Council Mandates 'Tidal Tax' on Coastal Residents to Fund Seawall Construction. "
        "Content: A newly formed international body, the Global Ocean Council, has announced a mandatory 'Tidal Tax' "
        "that will be levied against any property owner living within five miles of a coastline..."
    )
    # Testing fake detection without providing URL (or with a fake one)
    test_verify_news(text_l, "https://ocean-council.online/tidal-tax-mandate", "Article L: Tidal Tax (Fake)")
    
    # Article M: False Medical Panic (Fake)
    text_m = (
        "Headline: Emergency Recall Issued for Latest Generation of Smartwatches Over 'Skin-Deep' Laser Radiation. "
        "Content: A secret report leaked from a major consumer electronics safety lab warns that the green and red lasers "
        "used in modern smartwatch heart-rate sensors are causing 'micro-cellular burns' in up to 15% of users..."
    )
    # Testing Auto-Search for this one
    test_verify_news(text_m, None, "Article M: Smartwatch Radiation (Fake)")

    logger.info("BATCH 5 TESTS COMPLETED")
