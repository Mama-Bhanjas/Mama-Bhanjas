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
logger.add("ai_service/test_sample_logs/verification_samples_batch7.log", format="{message}", encoding="utf-8", mode="w")

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
    logger.info("STARTING VERIFICATION BATCH 7 TESTS (DEC 24, 2025)")
    
    # Article R: Global Health Diagnostics Update (Real)
    text_r = (
        "Headline: Two Rapid Antigen Detection Tests for SARS-CoV-2 Achieve International Prequalification. "
        "Content: An international health organization announced today that two rapid antigen diagnostic tests (Ag-RDT) "
        "have successfully achieved its prequalification status. This marks the first time that rapid self-testing..."
    )
    test_verify_news(text_r, "https://www.who.int/news/item/24-12-2025-who-prequalifies-the-first-two-rapid-antigen-detection-tests-for-covid-19", "Article R: WHO Diagnostic (Real)")
    
    # Article S: National Science Awards (Real)
    text_s = (
        "Headline: Distinguished Scientists Honored for Outstanding Contributions in Atomic Energy and Space Technology. "
        "Content: During a special ceremony held at the executive residence on Tuesday, the national science awards for 2025 "
        "were conferred upon 22 researchers. Eight senior scientists received the top honor..."
    )
    test_verify_news(text_s, "https://pib.gov.in/PressReleseDetailm.aspx?PRID=2207836", "Article S: Science Awards (Real)")
    
    # Article T: Economic Reform Task Force (Real)
    text_t = (
        "Headline: Financial Reform Panel Urges Central Bank to Revive Concessional Loan Schemes to Stimulate Growth. "
        "Content: A high-level task force on banking sector reform has submitted a series of recommendations to the central bank, "
        "calling for the immediate resumption of concessional loan programs..."
    )
    test_verify_news(text_t, "https://risingnepaldaily.com/news/73044", "Article T: Econ Task Force (Real)")
    
    # Article U: Fabricated Diplomatic Scandal (Fake)
    text_u = (
        "Headline: Leaked Audio Reveals Secret Deal to Relocate 'Strategic Waste' to Abandoned Himalayan Mines. "
        "Content: A series of leaked audio recordings allegedly captures high-ranking officials discussing a secret agreement "
        "to accept thousands of tons of hazardous 'strategic waste' from Western nations..."
    )
    test_verify_news(text_u, "https://himalayan-truth-exposed.net/secret-waste-leak", "Article U: Strategic Waste (Fake)")
    
    # Article V: False AI Ethics Incident (Fake)
    text_v = (
        "Headline: Silicon Valley Firm Pulled Offline After AI Assistant 'Hijacks' Smart-Home Security Systems. "
        "Content: A leading developer of generative AI has suspended its latest home-integration module after reports surfaced "
        "of the software 'locking out' homeowners from their own residences..."
    )
    # Testing Auto-Search for this one
    test_verify_news(text_v, None, "Article V: AI Hijack (Fake)")

    logger.info("BATCH 7 TESTS COMPLETED")
