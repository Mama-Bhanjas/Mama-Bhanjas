import requests
import json
import sys
from loguru import logger

# Configuration
BASE_URL = "http://localhost:8023/api"  # Use port 8023

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
logger.add("ai_service/test_sample_logs/verification_final.log", format="{message}", encoding="utf-8", mode="w")

def test_verify_news(text, source_url, label):
    """Test the /api/verify/news endpoint"""
    logger.info("="*60)
    logger.info(f"TEST: {label}")
    logger.info(f"Source: {source_url if source_url else 'NONE (Auto-Search)'}")
    logger.info(f"Text Snippet: {text[:60]}...")
    
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
            if 'found_sources' in d:
                 if d['found_sources']:
                     logger.info(f"Found Sources: {len(d['found_sources'])}")
                     for idx, val in enumerate(d['found_sources']):
                         logger.info(f"  [{idx+1}] {val.get('title', 'No Title')} ({val.get('url', 'No URL')})")
                 else:
                     logger.info("Found Sources: 0 (Search returned no results)")
            
        logger.info("-" * 20)
        return data
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return None

if __name__ == "__main__":
    logger.info("STARTING FINAL VERIFICATION TESTS (REAL SOURCES)")
    
    # 1. Reuters (Trusted / Real) - Economy
    text_reuters = "Global markets rallied today as inflation data showed promising signs of cooling down across major economies."
    test_verify_news(text_reuters, "https://www.reuters.com/markets/global-markets-wrap-up-2024", "Reuters (Trusted)")
    
    # 2. The Onion (Untrusted / Satire)
    text_onion = "Study finds that 90% of meetings could have been emails, but 10% of emails should have been meetings."
    test_verify_news(text_onion, "https://www.theonion.com/study-finds-meetings-emails", "The Onion (Satire/Untrusted)")
    
    # 3. Nature (Trusted / Science)
    text_nature = "New study reveals rapid melting of polar ice caps due to rising ocean temperatures."
    test_verify_news(text_nature, "https://www.nature.com/articles/s41586-024-00000-x", "Nature (Trusted Science)")
    
    # 4. InfoWars (Untrusted / Conspiracy)
    text_infowars = "Government admits to putting chemicals in the water to control thoughts!"
    test_verify_news(text_infowars, "https://www.infowars.com/water-chemicals-exposed", "InfoWars (Untrusted/Conspiracy)")
    
    # 5. TechCrunch (Trusted / Tech)
    text_tech = "OpenAI releases new model capable of reasoning across complex tasks."
    test_verify_news(text_tech, "https://techcrunch.com/2024/02/15/openai-sora-video", "TechCrunch (Trusted Tech)")

    # 6. Auto-Search Test (No URL Provided)
    text_charles = "Buckingham Palace announced that King Charles III has been diagnosed with a form of cancer."
    test_verify_news(text_charles, None, "King Charles (Auto-Search)")

    logger.info("TESTS COMPLETED")
