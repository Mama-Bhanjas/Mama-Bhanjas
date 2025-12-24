
import time
import requests
import sys
from loguru import logger

def verify_api():
    base_url = "http://localhost:8000"
    
    # Wait for API to be ready
    logger.info("Waiting for API to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                logger.info("API is ready!")
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        logger.error("API failed to start in time.")
        sys.exit(1)

    # Test Classification
    logger.info("Testing classification endpoint...")
    payload = {
        "text": "The garbage collection truck hasn't come to our street in 3 days. There is trash piling up correctly.",
        "top_k": 3
    }
    
    try:
        response = requests.post(f"{base_url}/api/classify", json=payload)
        response.raise_for_status()
        result = response.json()
        logger.info(f"Classification Success! \nResult: {result}")
        
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        try: 
            logger.error(f"Response: {response.text}") 
        except: 
            pass
        sys.exit(1)

    logger.info("Verificaton Complete!")

if __name__ == "__main__":
    verify_api()
