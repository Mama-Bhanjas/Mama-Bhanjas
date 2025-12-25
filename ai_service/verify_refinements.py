
import sys
import os
from loguru import logger

# Add ai_service to path
sys.path.append(os.getcwd())

from ai_service.pipelines.verification import VerificationPipeline
from ai_service.models.classifier import CategoryClassifier
from ai_service.models.summarizer import TextSummarizer
from ai_service.models.ner import EntityExtractor

def run_verification():
    logger.info("Starting Verification of Refined AI Pipelines")
    
    # 1. Test Verification Pipeline (The most critical one)
    logger.info("--- Testing Verification Pipeline ---")
    vp = VerificationPipeline()
    
    fake_news = "BREAKING: NASA confirms moon is made of blue cheese after latest lunar landing."
    real_news = "The Federal Reserve kept interest rates unchanged on Wednesday, citing solid economic growth but acknowledging inflation remains elevated."
    
    res_fake = vp.verify_news(fake_news)
    logger.info(f"Fake News Result: {res_fake['status']} (Confidence: {res_fake['confidence']:.2f})")
    
    res_real = vp.verify_news(real_news)
    logger.info(f"Real News Result: {res_real['status']} (Confidence: {res_real['confidence']:.2f})")

    # 2. Test Classification Logic
    logger.info("--- Testing Classification Logic ---")
    classifier = CategoryClassifier()
    text_civic = "There is a massive pothole on Main Street that is causing traffic jams and damaging cars."
    res_class = classifier.classify(text_civic)
    logger.info(f"Category: {res_class['category']} (Confidence: {res_class['confidence']:.2f})")

    # 3. Test Summarization
    logger.info("--- Testing Summarization Pipeline ---")
    summarizer = TextSummarizer()
    long_text = (
        "The city's public works department announced a major initiative yesterday to replace over 5,000 streetlights "
        "with energy-efficient LED fixtures across the downtown area. The project, which is estimated to cost $2.4 million, "
        "is expected to reduce citywide electricity consumption by 15% and save taxpayers approximately $400,000 annually "
        "in maintenance and energy costs. Construction is scheduled to begin early next month and conclude by the end of the year. "
        "Residents can expect minor traffic delays as crews work near busy intersections during off-peak hours."
    )
    res_sum = summarizer.summarize(long_text)
    logger.info(f"Summary: {res_sum['summary']}")

    # 4. Test NER
    logger.info("--- Testing NER Pipeline ---")
    ner = EntityExtractor()
    ner_text = "The protest started in Kathmandu near the Narayanhiti Palace and moved towards New Road."
    entities = ner.extract_entities(ner_text)
    locations = ner.get_locations(ner_text)
    logger.info(f"Entities: {[e['entity'] for e in entities]}")
    logger.info(f"Locations: {locations}")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
