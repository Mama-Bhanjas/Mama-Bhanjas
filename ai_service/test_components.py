"""
Direct component testing without API server
Tests individual pipelines and models
"""
import sys
import os
sys.path.insert(0, os.getcwd())

from loguru import logger
from ai_service.utils import setup_logging

setup_logging(log_level="INFO")

def test_content_extractor():
    """Test URL content extraction"""
    print("\n=== Testing Content Extractor ===")
    try:
        from ai_service.utils.content_extractor import ContentExtractor
        extractor = ContentExtractor()
        
        # Test URL detection
        url = "https://thehimalayantimes.com/nepal/flood-alert"
        is_url = extractor.is_url(url)
        print(f"URL Detection: {'PASS' if is_url else 'FAIL'}")
        
        # Test text detection
        text = "This is regular text"
        is_not_url = not extractor.is_url(text)
        print(f"Text Detection: {'PASS' if is_not_url else 'FAIL'}")
        
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False

def test_classification():
    """Test classification pipeline"""
    print("\n=== Testing Classification Pipeline ===")
    try:
        from ai_service.pipelines.classify import ClassificationPipeline
        
        classifier = ClassificationPipeline(
            model_name="Sachin1224/nepal-disaster-classifier"
        )
        
        text = "Heavy flooding in Kathmandu valley affecting hundreds of families"
        result = classifier.process(text)
        
        print(f"Category: {result.get('category')}")
        print(f"Confidence: {result.get('confidence'):.2f}")
        print(f"Status: {'PASS' if result.get('success') else 'FAIL'}")
        
        return result.get('success', False)
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_summarization():
    """Test summarization pipeline"""
    print("\n=== Testing Summarization Pipeline ===")
    try:
        from ai_service.pipelines.summarize import SummarizationPipeline
        
        summarizer = SummarizationPipeline(
            model_name="Sachin1224/nepal-disaster-summarizer"
        )
        
        text = """Heavy rainfall has triggered severe flooding across the Kathmandu valley, 
        affecting over 500 families in multiple districts. Emergency services have been deployed 
        to assist with evacuations. The meteorological department has issued warnings for 
        continued heavy rainfall over the next 48 hours."""
        
        result = summarizer.process(text)
        
        print(f"Summary: {result.get('summary')}")
        print(f"Status: {'PASS' if result.get('success') else 'FAIL'}")
        
        return result.get('success', False)
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ner():
    """Test NER pipeline"""
    print("\n=== Testing NER Pipeline ===")
    try:
        from ai_service.pipelines.ner import NERPipeline
        
        ner = NERPipeline(ner_model="Sachin1224/nepal-disaster-ner")
        
        text = "Flooding reported in Kathmandu and Pokhara districts affecting local communities"
        result = ner.process(text)
        
        print(f"Locations: {result.get('locations')}")
        print(f"Entities: {len(result.get('entities', []))} found")
        print(f"Status: {'PASS' if result.get('success') else 'FAIL'}")
        
        return result.get('success', False)
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_component_tests():
    """Run all component tests"""
    print("Starting Component Tests\n")
    print("=" * 50)
    
    results = {}
    
    # Test 1: Content Extractor
    results['content_extractor'] = test_content_extractor()
    
    # Test 2: Classification
    results['classification'] = test_classification()
    
    # Test 3: Summarization  
    results['summarization'] = test_summarization()
    
    # Test 4: NER
    results['ner'] = test_ner()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_name:20s}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    success = run_component_tests()
    sys.exit(0 if success else 1)
