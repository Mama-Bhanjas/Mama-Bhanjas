import requests
import json
import time
import sys

BASE_URL = "http://localhost:8002"

def test_endpoint(name, method, path, payload=None):
    print(f"\n--- Testing {name} ---")
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        else:
            response = requests.post(url, json=payload, timeout=60)
        
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            data = response.json()
            if data.get("success"):
                print("PASSED: Success signal received")
                return data
            else:
                print(f"FAILED: API returned success=False. Error: {data.get('error', 'Unknown')}")
        else:
            print(f"FAILED: Unexpected status code. Response: {response.text[:200]}")
    except Exception as e:
        print(f"ERROR: Request failed: {e}")
    return None

def run_test_suite():
    print("Starting AI Service Comprehensive Test Suite")
    
    # 1. Health/Root Check
    test_endpoint("Root/Health", "GET", "/")
    
    # 2. Text Processing (Standard Report)
    report_text = "Heavy rain triggering landslides in Taplejung district, blocking main roads near Phungling."
    test_endpoint("Text Processing", "POST", "/api/process/report", {
        "text": report_text,
        "source_type": "USER",
        "source_identifier": "test_script"
    })
    
    # 3. URL Extraction
    news_url = "https://thehimalayantimes.com/nepal/over-4600-disaster-incidents-recorded-in-six-months-across-nepal"
    test_endpoint("URL Extraction", "POST", "/api/process/report", {
        "text": news_url,
        "source_type": "WEB",
        "source_identifier": "test_script"
    })
    
    # 4. Real-time News Retrieval
    test_endpoint("Real-time News Retrieval", "GET", "/api/realtime/news")
    
    print("\n--- Test Suite Complete ---")

if __name__ == "__main__":
    run_test_suite()
