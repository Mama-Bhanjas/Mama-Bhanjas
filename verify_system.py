#!/usr/bin/env python3
"""
Final System Verification Script
Tests all three layers: AI Service, Backend, Frontend
"""

import requests
import time
from datetime import datetime

def check_service(name, url, timeout=5):
    """Check if a service is running"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name} is running")
            return True
        else:
            print(f"⚠️  {name} returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} is NOT running")
        return False
    except Exception as e:
        print(f"❌ {name} error: {e}")
        return False

def main():
    print("=" * 70)
    print("FINAL SYSTEM VERIFICATION")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Check all services
    print("\n📡 Checking Services...")
    ai_ok = check_service("AI Service (Port 8002)", "http://localhost:8002/")
    backend_ok = check_service("Backend API (Port 8000)", "http://localhost:8000/")
    frontend_ok = check_service("Frontend (Port 3000)", "http://localhost:3000/")
    
    if not all([ai_ok, backend_ok, frontend_ok]):
        print("\n⚠️  Some services are not running. Please start all services.")
        return
    
    # Test Backend → AI Service integration
    print("\n🔗 Testing Backend → AI Service Integration...")
    try:
        response = requests.get("http://localhost:8000/news/realtime", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend can communicate with AI Service")
            print(f"   News Intelligence Items: {len(data.get('data', {}).get('news_intelligence', []))}")
        else:
            print(f"❌ Integration test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Integration error: {e}")
    
    # Test database
    print("\n💾 Testing Database...")
    try:
        response = requests.get("http://localhost:8000/reports/")
        if response.status_code == 200:
            reports = response.json()
            print(f"✅ Database accessible")
            print(f"   Total Reports: {len(reports)}")
            if reports:
                latest = reports[-1]
                print(f"   Latest Report:")
                print(f"     - Category: {latest.get('disaster_category', 'N/A')}")
                print(f"     - Location: {latest.get('location', 'N/A')}")
                print(f"     - Verified: {latest.get('is_verified', False)}")
                print(f"     - Submitted By: {latest.get('submitted_by', 'Anonymous')}")
                if latest.get('summary'):
                    print(f"     - Has AI Summary: Yes")
                if latest.get('confidence_score'):
                    print(f"     - AI Confidence: {latest['confidence_score']:.1%}")
        else:
            print(f"❌ Database test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SYSTEM STATUS SUMMARY")
    print("=" * 70)
    print(f"AI Service:  {'✅ Running' if ai_ok else '❌ Down'}")
    print(f"Backend API: {'✅ Running' if backend_ok else '❌ Down'}")
    print(f"Frontend:    {'✅ Running' if frontend_ok else '❌ Down'}")
    
    if all([ai_ok, backend_ok, frontend_ok]):
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n📱 Access the application at: http://localhost:3000")
        print("📊 Backend API docs at: http://localhost:8000/docs")
        print("🤖 AI Service at: http://localhost:8002/")
    else:
        print("\n⚠️  SOME SYSTEMS ARE DOWN - Please check the services above")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
