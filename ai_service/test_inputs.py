
import requests
import os

BASE_URL = "http://localhost:8002"

def test_url_processing():
    print("\n--- TESTING URL PROCESSING ---")
    url = "https://thehimalayantimes.com/nepal/over-4600-disaster-incidents-recorded-in-six-months-across-nepal"
    payload = {
        "text": url,
        "source_url": url
    }
    try:
        response = requests.post(f"{BASE_URL}/api/process/report", json=payload, timeout=120)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            res_data = data.get('data', {})
            print(f"REPORT_ID: {res_data.get('report_id')}")
            print(f"VERIFICATION: {res_data.get('verification', {}).get('status')}")
            print(f"CATEGORY: {res_data.get('primary_category')}")
            print(f"DISASTER_TYPE: {res_data.get('disaster_type')}")
            print(f"LOCATIONS: {res_data.get('location_entities')}")
            print(f"EXTRACTED TEXT:\n{res_data.get('extracted_text')[:300]}...")
        else:
            print(f"Failed: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_url_processing()
