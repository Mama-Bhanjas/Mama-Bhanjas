
import requests
import json
import sys
from loguru import logger

# Configure logging
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
logger.add("ai_service/test_sample_logs/verification_real_world.log", format="{message}", encoding="utf-8", mode="w")

BASE_URL = "http://localhost:8016/api"

def test_verification(endpoint, text, label, source_url=None):
    logger.info("="*60)
    logger.info(f"TESTING {label.upper()}: {endpoint}")
    logger.info(f"Text: {text[:50]}...")
    if source_url:
        logger.info(f"Source: {source_url}")
    logger.info("="*60)
    
    payload = {"text": text}
    if source_url:
        payload["source_url"] = source_url
    
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Status: {data['status']}")
        logger.info(f"Reliable: {data['is_reliable']}")
        logger.info(f"Confidence: {data['confidence']:.2f}")
        if 'sources' in data:
            logger.info("Sources Found:")
            for s in data['sources']:
                logger.info(f" - {s['url']} ({s['status']})")
        if 'explanation' in data and data['explanation']:
            logger.info(f"Explanation: {data['explanation']}")
        logger.info("-" * 20)
        return data
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        try: logger.error(response.text)
        except: pass
        return None

if __name__ == "__main__":
    # 1. Fact Check (Auto-Search)
    logger.info("\n--- FACT CHECKING (AUTOMATED SEARCH) ---")
    
    # Real: King Charles Cancer (Global News 2024)
    logger.info("Test 1: King Charles Cancer Diagnosis (Real)")
    charles_text = "Buckingham Palace announced that King Charles III has been diagnosed with a form of cancer and will postpone public-facing duties."
    test_verification("verify/factcheck", charles_text, "Real Event (Should find BBC/CNN)")
    
    # Real: SpaceX Starship (Tech/Space News)
    logger.info("Test 2: SpaceX Starship Launch (Real)")
    spacex_text = "SpaceX successfully launched its massive Starship rocket from Texas, achieving orbit for the first time in a major milestone."
    test_verification("verify/factcheck", spacex_text, "Real Event (Should find Space/Tech news)")
    
    # Fake: Generic Viral Hoax
    logger.info("Test 3: Coca-Cola Recall Hoax (Fake)")
    coke_text = "Coca-Cola is recalling allDasani water products due to a clear parasite found in bottles. Share this warning!"
    test_verification("verify/factcheck", coke_text, "Fake Hoax (Should not find trusted confirmation)")

    # 2. News Verification (With Provided Source)
    logger.info("\n--- SOURCE VERIFICATION (PROVIDED URL) ---")
    
    logger.info("Test 4: BBC Article (Trusted)")
    bbc_text = "King Charles diagnosed with cancer, Buckingham Palace says."
    test_verification("verify/news", bbc_text, "Trusted Source", "https://www.bbc.com/news/uk-68208152")

    logger.info("Test 5: Fake Site (Untrusted)")
    fake_text = "Celebrity scandal involves secret alien baby!"
    test_verification("verify/news", fake_text, "Untrusted Source", "https://dailybuzz.live/alien-baby")
    logger.info("\n--- REPORT VERIFICATION (TUNED) ---")
    test_verification("verify/report", "There is a large pothole on Main St", "Valid Report")
    test_verification("verify/report", "BUY CRYPTO NOW!!! BEST RATES CLICK HERE", "Spam Report (Crypto)")

