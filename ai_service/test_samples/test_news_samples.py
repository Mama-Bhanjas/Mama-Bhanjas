#!/usr/bin/env python3
"""
Test script for articles: now also runs fact-check and logs sources
"""
import os
import requests
from loguru import logger

BASE_URL = os.environ.get("AI_SERVICE_URL", "http://localhost:8000")

# Configure logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
logger.add("ai_service/test_sample_logs/test_news_samples.log", format="{message}", encoding="utf-8", mode="w")

def log_factcheck(text, title):
    logger.info("\nSending for Fact-Check (Internet Search)...")
    try:
        resp = requests.post(f"{BASE_URL}/api/verify/factcheck", json={"text": text}, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if not data.get("success"):
            logger.warning(f"Fact-check response not successful: {data}")
            return

        logger.info(f"Fact-check Status: {data.get('status')} (Confidence: {data.get('confidence')})")
        explanation = data.get("explanation") or ""
        logger.info(f"Explanation: {explanation}")

        primary = data.get("primary_sources", [])
        sources = data.get("sources", [])

        if primary:
            logger.info("Primary corroborating sources:")
            for s in primary:
                logger.info(f"- {s.get('title')[:200]} | {s.get('domain')} | {s.get('url')}")
        elif sources:
            logger.info("Top found sources (best-effort):")
            for s in sources[:5]:
                logger.info(f"- {s.get('title')[:200]} | {s.get('domain')} | {s.get('url')} | Status: {s.get('status')} | Reachable: {s.get('reachable')}")

    except Exception as e:
        logger.error(f"Fact-check failed: {e}")

def test_article(title, text):
    logger.info("="*60)
    logger.info(f"TESTING ARTICLE: {title}")
    logger.info("="*60)

    # 1. Classify
    logger.info("Sending for Classification...")
    try:
        cls_resp = requests.post(
            f"{BASE_URL}/api/classify",
            json={"text": text, "top_k": 3},
            timeout=10
        )
        cls_resp.raise_for_status()
        cls_data = cls_resp.json()

        logger.info(f"Category: {cls_data.get('category')} (Confidence: {cls_data.get('confidence'):.2f})")
        top = cls_data.get('top_categories') or []
        logger.info("Top 3: " + ", ".join([f"{c.get('category')}({c.get('confidence'):.2f})" for c in top]))
    except Exception as e:
        logger.error(f"Classification failed: {e}")

    # 2. Summarize
    logger.info("\nSending for Summarization...")
    try:
        sum_resp = requests.post(
            f"{BASE_URL}/api/summarize",
            json={
                "text": text,
                "max_length": 100,
                "min_length": 30
            },
            timeout=15
        )
        sum_resp.raise_for_status()
        sum_data = sum_resp.json()

        logger.info(f"Summary: {sum_data.get('summary')}")
        logger.info(f"Compressed: {sum_data.get('original_length')} chars -> {sum_data.get('summary_length')} chars ({sum_data.get('compression_ratio'):.2f} ratio)")
    except Exception as e:
        logger.error(f"Summarization failed: {e}")

    # 3. Fact-check (Internet search + source list)
    logger.info("\n")
    log_factcheck(text, title)
    logger.info("\n")

if __name__ == "__main__":
    # Sample 1: Infrastructure/Transportation
    article_infra = """
    The city municipal corporation has announced a major pothole repair drive starting next Monday.
    Residents of the downtown area have been complaining about the poor condition of the roads, particularly on Main Street and 5th Avenue, for months.
    The City Commissioner stated that a budget of $5 million has been allocated for this project, which aims to resurface over 50 kilometers of roads.
    Traffic diversions will be in place during the night to minimize disruption to commuters.
    Local road safety activists have welcomed the move but say it is long overdue.
    """

    # Sample 2: Health
    article_health = """
    Local health officials are advising residents to take precautions against dengue fever following a spike in cases.
    The Department of Health reported 50 new cases in the last week alone, mostly concentrated in the Riverside district.
    Authorities are urging people to eliminate standing water where mosquitoes breed and to wear insect repellent.
    A fumigation campaign is being launched in the affected neighborhoods starting tomorrow.
    Hospitals have been put on alert to handle any potential surge in patients requiring admission.
    """

    # Sample 3: Environment (General News style)
    article_env = """
    A new report suggests that urban green spaces are vital for mental health in crowded cities.
    Researchers found that people living within 300 meters of a park reported 30% lower levels of stress and anxiety compared to those in concrete-only neighborhoods.
    The study, published in the Journal of Environmental Psychology, surveyed over 2,000 residents across five major metropolitan areas.
    City planners are now being urged to prioritize pocket parks and tree-lined avenues in future development plans to improve public well-being.
    """

    test_article("City Road Repairs", article_infra)
    test_article("Dengue Outbreak Warning", article_health)
    test_article("Urban Parks Study", article_env)