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
logger.add("ai_service/test_sample_logs/verification_samples_batch6.log", format="{message}", encoding="utf-8", mode="w")

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
    logger.info("STARTING VERIFICATION BATCH 6 TESTS (DEC 24, 2025)")
    
    # Article N: Industrial Breakthrough in Clean Energy (Real)
    text_n = (
        "Headline: Next-Generation Gas Turbine Control System for Hydrogen Co-Firing Completes Functional Testing. "
        "Content: A collaborative engineering effort between two major Tokyo-based electronics and heavy industries corporations "
        "has resulted in the successful functional testing of a new gas turbine control system. The system integrates high-speed "
        "data processing with advanced control technology to optimize large-scale turbines. Specifically, the new interface allows "
        "for rapid load adjustments to balance the variable output of renewable energy sources and supports the co-firing of natural gas with hydrogen."
    )
    test_verify_news(text_n, "https://www.mhi.com/news/25122402.html", "Article N: Hydrogen Turbine (Real)")
    
    # Article O: Administrative Action in Urban Education (Real)
    text_o = (
        "Headline: Metropolitan Education Department Moves to Deregister Over 100 Non-Operational Schools. "
        "Content: The Education Department of a major capital city has initiated a formal process to deregister 107 schools "
        "that were granted operating permits but have failed to remain physically operational. Following a field inspection conducted earlier this year, "
        "authorities found that these institutions were not functioning at their designated locations. A public notice issued today gives the managers "
        "of these schools 15 days to contact the metropolitan office to prove their status."
    )
    test_verify_news(text_o, "https://myrepublica.nagariknetwork.com/news/kmc-initiates-process-to-deregister-107-non-operational-schools-99-78.html", "Article O: School Deregistration (Real)")
    
    # Article P: Fabricated Health Mandate (Fake)
    text_p = (
        "Headline: New Global Health Accord Requires 'Bio-Digital ID' for All International Travelers by Summer 2026. "
        "Content: In a closed-door session in Geneva, representatives from 190 nations have reportedly signed a secret annex to the Global Health Accord. "
        "The document mandates that all international travelers must carry a 'Bio-Digital ID' that links their biometric data directly to a live-updating "
        "vaccination and health database. Starting in June 2026, airline boarding passes will not be issued without a 'Green Status' verified by a central AI clearinghouse."
    )
    test_verify_news(text_p, "https://global-health-accord.net/bio-digital-id-secret-annex", "Article P: Bio-Digital ID (Fake)")
    
    # Article Q: False Technological Bug (Fake)
    text_q = (
        "Headline: Universal USB-C Vulnerability Discovered: 'Voltage Hijack' Can Remotely Overload and Ignite Devices. "
        "Content: Security researchers at an independent cybersecurity firm have discovered a hardware-level flaw in the universal USB-C charging protocol. "
        "Dubbed 'Voltage Hijack', the vulnerability allows a remote attacker to bypass the Power Delivery (PD) controller of a device while it is plugged into a 'smart' charging station. "
        "By overriding the voltage limits, the attacker can force 240V into a smartphone or laptop, causing the lithium-ion battery to undergo immediate thermal runaway."
    )
    # Testing Auto-Search for this one
    test_verify_news(text_q, None, "Article Q: Voltage Hijack (Fake)")

    logger.info("BATCH 6 TESTS COMPLETED")
