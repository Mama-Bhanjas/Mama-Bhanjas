import requests
import json

# Test the complete end-to-end flow
BASE_URL = "http://localhost:8000"

print("=" * 70)
print("TESTING COMPLETE INTEGRATION - Backend + AI Service")
print("=" * 70)

# Test 1: Submit a new report with all fields
print("\n📝 Test 1: Submitting a new disaster report...")
test_report = {
    "text": "Major flooding reported in Kathmandu valley. Water levels rising rapidly near Bagmati river.",
    "source_type": "WEB_USER",
    "source_identifier": "test_integration",
    "location": "Kathmandu",
    "disaster_category": "flood",
    "submitted_by": "Test User"
}

try:
    response = requests.post(f"{BASE_URL}/reports/", json=test_report, timeout=60)
    if response.status_code in [200, 201]:
        print("✅ Report submitted successfully!")
        result = response.json()
        print(f"\nReport ID: {result['id']}")
        print(f"Category: {result['disaster_category']}")
        print(f"Location: {result['location']}")
        print(f"Submitted By: {result.get('submitted_by', 'N/A')}")
        print(f"Verification Status: {result['verification_status']}")
        print(f"Is Verified: {result['is_verified']}")
        if result.get('summary'):
            print(f"AI Summary: {result['summary'][:100]}...")
        if result.get('confidence_score'):
            print(f"AI Confidence: {result['confidence_score']:.2%}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Fetch all reports
print("\n\n📋 Test 2: Fetching all reports...")
try:
    response = requests.get(f"{BASE_URL}/reports/")
    if response.status_code == 200:
        reports = response.json()
        print(f"✅ Found {len(reports)} reports in database")
        if reports:
            print("\nLatest Report:")
            latest = reports[-1]
            print(f"  - ID: {latest['id']}")
            print(f"  - Category: {latest['disaster_category']}")
            print(f"  - Location: {latest.get('location', 'N/A')}")
            print(f"  - Submitted By: {latest.get('submitted_by', 'Anonymous')}")
            print(f"  - Verified: {latest['is_verified']}")
            if latest.get('summary'):
                print(f"  - Summary: {latest['summary'][:80]}...")
    else:
        print(f"❌ Failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Check realtime news
print("\n\n📰 Test 3: Checking realtime news integration...")
try:
    response = requests.get(f"{BASE_URL}/news/realtime")
    if response.status_code == 200:
        news_data = response.json()
        print(f"✅ Realtime news endpoint working")
        print(f"Success: {news_data.get('success')}")
        if news_data.get('data'):
            intel = news_data['data'].get('news_intelligence', [])
            print(f"News Intelligence Items: {len(intel)}")
    else:
        print(f"❌ Failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("INTEGRATION TEST COMPLETE")
print("=" * 70)
