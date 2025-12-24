import requests
import json
import sys
from loguru import logger

# Configuration
BASE_URL = "http://localhost:8000/api"

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
logger.add("verification_samples_batch3.log", format="{message}", encoding="utf-8", mode="w")

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
    logger.info("STARTING VERIFICATION BATCH 3 TESTS (DEC 24, 2025)")
    
    # Article A: Tech Acquisition in Healthcare (Real)
    text_a = (
        "Headline: European Pharmaceutical Giant Agrees to $1.1 Billion Acquisition of Vaccine Developer to Bolster Shingles Pipeline. "
        "Content: In a major pre-holiday move, a leading Paris-based healthcare firm has entered into a definitive agreement "
        "to acquire a publicly traded vaccine company. The deal, valued at approximately $1.1 billion, focuses on acquiring "
        "a marketed adult hepatitis B vaccine and a promising shingles candidate currently in phase 1/2 clinical trials..."
    )
    test_verify_news(text_a, "https://www.bloomberg.com/news/articles/2025-12-24/healthcare-acquisition", "Article A: Healthcare Acquisition (Real)")
    
    # Article B: Semiconductor Industry Recognition (Real)
    text_b = (
        "Headline: Optics Leader Receives Performance Award for Supporting Global Semiconductor Production. "
        "Content: A major Tokyo-headquartered imaging and optical products corporation was honored today for its "
        "contributions to the semiconductor supply chain. The 'Excellent Performance Award' was granted by the world's "
        "largest dedicated independent semiconductor foundry..."
    )
    test_verify_news(text_b, "https://www.reuters.com/technology/semiconductor-award-2025", "Article B: Semiconductor Award (Real)")
    
    # Article C: Fabricated Energy Policy (Fake)
    text_c = (
        "Headline: International Energy Bureau Mandates 'Smart-Fridge Lockouts' During Peak Winter Demand. "
        "Content: An emergency directive issued this morning by the International Energy Bureau (IEB) will require "
        "all smart-refrigerators manufactured after 2022 to be remotely powered down for two hours every evening. "
        "The 'Chill-Safe' protocol is designed to prevent total grid collapse..."
    )
    # Using a suspicious-looking domain for Article C
    test_verify_news(text_c, "https://energygrid-truth.site/smart-fridge-mandate", "Article C: Smart-Fridge Lockouts (Fake)")
    
    # Article D: False Scientific Discovery (Fake)
    text_d = (
        "Headline: Deep Sea Expedition Finds 'Living Fossil' with Silicon-Based Genetic Structure. "
        "Content: A clandestine research vessel operating in the Mariana Trench has reportedly discovered a species "
        "of jellyfish-like organisms that utilize silicon instead of carbon as a biological foundation. "
        "The lead researcher, who requested anonymity due to a government non-disclosure agreement..."
    )
    # No source URL to test Auto-Search
    test_verify_news(text_d, None, "Article D: Silicon Lifeform (Fake)")

    logger.info("BATCH 3 TESTS COMPLETED")
