
import requests
import json
import sys

def test_backend_endpoints():
    BASE_URL = "http://localhost:8000"
    print(f"🚀 STARTING COMPREHENSIVE BACKEND TEST ({BASE_URL})")
    print("=" * 60)

    endpoints_to_test = [
        # (Method, Path, Payload, Name)
        ("GET", "/", None, "Root Endpoint"),
        ("GET", "/news/realtime", None, "Realtime News Proxy"),
        ("POST", "/reports/", {
            "text": "Flood warning issued for Koshi River area in Nepal.",
            "source_type": "Citizen",
            "location": "Sunsari",
            "disaster_category": "Flood"
        }, "Create Report (Direct Text)"),
        ("POST", "/reports/", {
            "text": "https://risingnepaldaily.com/news/38622", # Test URL extraction
            "source_type": "News Link",
            "source_identifier": "https://risingnepaldaily.com/news/38622"
        }, "Create Report (URL Link)"),
        ("GET", "/reports/", None, "List All Reports"),
        ("POST", "/verify/news", {
            "text": "There is a massive earthquake in Kathmandu right now.",
            "source_url": "http://testsource.com"
        }, "Verify News credibility"),
        ("POST", "/verify/report", {
            "text": "The bridge near our house has collapsed due to heavy rain."
        }, "Verify civic report validity"),
        ("POST", "/verify/factcheck", {
            "text": "Is there a flood in Pokhara today?"
        }, "Fact-check/Search News"),
    ]

    success_count = 0
    total_count = len(endpoints_to_test)

    for method, path, payload, name in endpoints_to_test:
        print(f"\n🔹 Testing: {name} ({method} {path})")
        try:
            url = f"{BASE_URL}{path}"
            if method == "GET":
                resp = requests.get(url, timeout=15)
            elif method == "POST":
                resp = requests.post(url, json=payload, timeout=30) # AI calls take time
            
            if resp.status_code in [200, 201]:
                print(f"   ✅ SUCCESS ({resp.status_code})")
                # print(f"   - Response: {json.dumps(resp.json(), indent=2)[:200]}...")
                success_count += 1
            else:
                print(f"   ❌ FAILED ({resp.status_code})")
                print(f"   - Error: {resp.text}")
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")

    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULT: {success_count}/{total_count} Endpoints Working.")
    if success_count == total_count:
        print("🎉 ALL BACKEND ENDPOINTS ARE FULLY OPERATIONAL!")
    else:
        print("⚠️ SOME ENDPOINTS FAILED. CHECK LOGS.")

if __name__ == "__main__":
    test_backend_endpoints()
