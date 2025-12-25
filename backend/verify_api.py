import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8001"

def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(30):
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("Server is up!")
                return True
        except requests.ConnectionError:
            time.sleep(1)
    print("Server failed to start.")
    return False

def test_create_report():
    print("\nTesting Report Submission...")
    payload = {
        "text": "Severe flooding in the downtown area caused by heavy rains. Roads are blocked.",
        "source_type": "Twitter",
        "source_identifier": "@citizen_reporter"
    }
    response = requests.post(f"{BASE_URL}/reports/", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"Report Submitted! ID: {data['id']}, Verified: {data['is_verified']}, Status: {data['verification_status']}")
        print(f"AI Classification: {data['disaster_category']}")
        return data['id']
    else:
        print(f"Failed to submit report: {response.text}")
        return None

def test_get_report(report_id):
    print(f"\nTesting Get Report {report_id}...")
    response = requests.get(f"{BASE_URL}/reports/{report_id}")
    if response.status_code == 200:
        print("Report retrieved successfully.")
    else:
        print(f"Failed to retrieve report: {response.text}")

def test_get_summaries():
    print("\nTesting Summaries...")
    # Give AI pipeline a moment if async (it's sync here but good practice)
    time.sleep(2) 
    response = requests.get(f"{BASE_URL}/summaries/")
    if response.status_code == 200:
        data = response.json()
        print(f"Summaries Retrieved: {len(data)}")
        for summary in data:
            print(f"Category: {summary['category']}")
            print(f"Summary: {summary['summary_text']}")
            print(f"Reputation Score: {summary['reputation_score']}")
    else:
        print(f"Failed to retrieve summaries: {response.text}")

if __name__ == "__main__":
    if not wait_for_server():
        sys.exit(1)
    
    report_id = test_create_report()
    if report_id:
        test_get_report(report_id)
        test_get_summaries()
