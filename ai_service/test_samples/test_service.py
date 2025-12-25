"""
Test script for AI Service
Run this to verify all components are working
"""
import sys
from loguru import logger

# Configure simple logging for tests
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("ai_service/test_sample_logs/test_service.log", format="{message}", encoding="utf-8", mode="w")


def test_classification():
    """Test classification pipeline"""
    logger.info("Testing Classification Pipeline...")
    
    try:
        from ai_service.pipelines.classify import ClassificationPipeline
        
        pipeline = ClassificationPipeline()
        
        test_text = "There is a large pothole on Main Street that needs immediate repair. It's causing traffic issues."
        
        result = pipeline.process(test_text)
        
        if result['success']:
            logger.success(f"✓ Classification successful!")
            logger.info(f"  Category: {result['category']}")
            logger.info(f"  Confidence: {result['confidence']:.3f}")
            logger.info(f"  Top categories: {[c['category'] for c in result['top_categories']]}")
            return True
        else:
            logger.error(f"✗ Classification failed: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Classification test error: {e}")
        return False


def test_summarization():
    """Test summarization pipeline"""
    logger.info("\nTesting Summarization Pipeline...")
    
    try:
        from ai_service.pipelines.summarize import SummarizationPipeline
        
        pipeline = SummarizationPipeline()
        
        test_text = """
        The city council meeting was held yesterday to discuss the ongoing infrastructure problems 
        in the downtown area. Multiple residents reported issues with broken streetlights, damaged 
        sidewalks, and potholes on major roads. The council voted to allocate additional funding 
        for repairs and maintenance. Work is expected to begin next month and continue for approximately 
        three months. Residents are encouraged to report any additional issues through the city's 
        online portal or by calling the public works department directly.
        """
        
        result = pipeline.process(test_text)
        
        if result['success']:
            logger.success(f"✓ Summarization successful!")
            logger.info(f"  Summary: {result['summary']}")
            logger.info(f"  Compression ratio: {result['compression_ratio']:.2f}")
            return True
        else:
            logger.error(f"✗ Summarization failed: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Summarization test error: {e}")
        return False


def test_clustering():
    """Test clustering pipeline"""
    logger.info("\nTesting Clustering Pipeline...")
    
    try:
        from ai_service.pipelines.cluster import ClusteringPipeline
        
        pipeline = ClusteringPipeline()
        
        test_texts = [
            "Broken streetlight on Oak Avenue",
            "Pothole on Main Street needs repair",
            "Graffiti on the community center wall",
            "Street light not working on Elm Street",
            "Large pothole causing traffic issues",
            "Vandalism at the park",
        ]
        
        result = pipeline.cluster_kmeans(test_texts, n_clusters=2)
        
        logger.success(f"✓ Clustering successful!")
        logger.info(f"  Number of clusters: {result['num_clusters']}")
        
        for cluster in result['clusters']:
            logger.info(f"\n  Cluster {cluster['cluster_id']} (size: {cluster['size']}):")
            logger.info(f"    Representative: {cluster['representative_text']}")
            
        return True
            
    except Exception as e:
        logger.error(f"✗ Clustering test error: {e}")
        return False


def test_similarity():
    """Test similarity search"""
    logger.info("\nTesting Similarity Search...")
    
    try:
        from ai_service.pipelines.cluster import ClusteringPipeline
        
        pipeline = ClusteringPipeline()
        
        query = "Street light is broken"
        corpus = [
            "Pothole on the road",
            "Broken streetlight needs fixing",
            "Graffiti on building",
            "Traffic light malfunction",
            "Damaged sidewalk",
        ]
        
        results = pipeline.find_similar(query, corpus, top_k=3)
        
        logger.success(f"✓ Similarity search successful!")
        logger.info(f"  Query: {query}")
        logger.info(f"  Top matches:")
        
        for i, match in enumerate(results, 1):
            logger.info(f"    {i}. {match['text']} (similarity: {match['similarity']:.3f})")
            
        return True
            
    except Exception as e:
        logger.error(f"✗ Similarity search test error: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("AI Service Test Suite")
    logger.info("=" * 60)
    
    results = {
        "Classification": test_classification(),
        "Summarization": test_summarization(),
        "Clustering": test_clustering(),
        "Similarity Search": test_similarity()
    }
    
    logger.info("\n" + "=" * 60)
    logger.info("Test Results Summary")
    logger.info("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    logger.info(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        logger.success("\n🎉 All tests passed!")
        return 0
    else:
        logger.warning(f"\n⚠️  {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
