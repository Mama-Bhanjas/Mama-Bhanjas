
import requests
import time
import sys

def verify_integration():
    print("INTEGRATION VERIFICATION: Checking Backend -> AI Service Proxy...")
    print("=" * 60)
    
    # Configuration
    BACKEND_URL = "http://localhost:8000"
    AI_SERVICE_URL = "http://localhost:8002"
    
    try:
        # 1. Check if AI Service Realtime Endpoint is up (The Source)
        print(f"1. Checking AI Service Source ({AI_SERVICE_URL}/api/realtime/news)...")
        try:
            ai_resp = requests.get(f"{AI_SERVICE_URL}/api/realtime/news", timeout=5)
            if ai_resp.status_code == 200:
                print("   ✅ AI Service is responding.")
                data = ai_resp.json()
                print(f"   - Data present: {data.get('success')}")
            else:
                print(f"   ❌ AI Service returned {ai_resp.status_code}")
        except requests.exceptions.ConnectionError:
             print("   ⚠️ AI Service is NOT running. Please start it with 'python -m ai_service.api'")
             return

        # 2. Check the New Backend Proxy Endpoint
        print(f"\n2. Checking Backend Proxy ({BACKEND_URL}/news/realtime)...")
        try:
            be_resp = requests.get(f"{BACKEND_URL}/news/realtime", timeout=5)
            if be_resp.status_code == 200:
                print("   ✅ Backend Proxy is working!")
                proxy_data = be_resp.json()
                
                # Validation
                if proxy_data == data:
                     print("   ✅ Data Integrity: Exact match between Proxy and Source.")
                else:
                     print("   ⚠️ Data Mismatch: Proxy returned different data than source.")
            else:
                 print(f"   ❌ Backend Proxy returned {be_resp.status_code}")
                 print(f"   - Error: {be_resp.text}")
                 
        except requests.exceptions.ConnectionError:
             print("   ⚠️ Backend is NOT running. Please start it with 'uvicorn backend.app.main:app --port 8000'")

    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    verify_integration()
