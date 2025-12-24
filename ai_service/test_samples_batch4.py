import requests
import json
import sys
from loguru import logger

# Configuration
BASE_URL = "http://localhost:8000/api"

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
logger.add("verification_samples_batch4.log", format="{message}", encoding="utf-8", mode="w")

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
    logger.info("STARTING VERIFICATION BATCH 4 TESTS (DEC 24, 2025)")
    
    # Article E: Political Consensus in Nepal (Real)
    text_e = (
        "Headline: Top Political Leaders Agree on Framework for Upcoming General Elections After High-Level Meeting. "
        "Content: In a significant breakthrough at the President's residence on Tuesday, leaders from the country's "
        "three largest political parties reached a formal agreement..."
    )
    test_verify_news(text_e, "https://kathmandupost.com/national/2025/12/political-consensus-elections", "Article E: Nepal Consensus (Real)")
    
    # Article F: Security Incident in Russia (Real)
    text_f = (
        "Headline: Explosion in Moscow Results in Three Fatalities; Investigation Committee Cites Targeted Device. "
        "Content: Authorities in the capital have launched a criminal investigation after an explosive device "
        "detonated on Wednesday, killing two traffic police officers and one bystander..."
    )
    test_verify_news(text_f, "https://tass.com/emergencies/moscow-explosion-investigation", "Article F: Moscow Incident (Real)")
    
    # Article G: Fabricated Medical Discovery (Fake)
    text_g = (
        "Headline: New 'Memory-Wipe' Pill Approved for Emergency Use in Post-Traumatic Stress Patients. "
        "Content: A breakthrough pharmaceutical compound that allows the brain to selectively 'overwrite' "
        "traumatic memories has received emergency authorization for clinical use. The drug, currently known as MNEM-7..."
    )
    test_verify_news(text_g, "https://medical-truth.blog/mnem7-memory-wipe-pill", "Article G: Memory-Wipe Pill (Fake)")
    
    # Article H: Fake Economic Reform (Fake)
    text_h = (
        "Headline: Global Central Bank Collective Announces 'Expiration Dates' for Digital Currency to Force Spending. "
        "Content: In a radical move to combat the global economic stagnation predicted for 2026, a collective of "
        "central banks has proposed a 'use it or lose it' feature for all retail digital currencies..."
    )
    # Testing Auto-Search for this one
    test_verify_news(text_h, None, "Article H: Currency Expiration (Fake)")

    logger.info("BATCH 4 TESTS COMPLETED")
