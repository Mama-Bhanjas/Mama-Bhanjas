import requests
import json
import time

URL = "http://localhost:8002/api/process/report"

# Test Payload with URL (that might not have a title metadata)
# We expect the AI to generate a title from the summary
payload = {
    "text": "https://ekantipur.com/news/2025/12/25/test-flood-news.html", # Mock URL
    "source_type": "WEB_USER"
}

# But for this test, we can pass text that LOOKS like a report but has no titl explicity provided
# to see if 'title' field is populated in output
payload_text = {
    "text": """
    URGENT: Massive landslide in Taplejung district.
    Heavy rainfall since last night has caused a major landslide blocking the Mechi Highway.
    Locals report 3 houses swept away. Police team deployed.
    Rescue operations are difficult due to continuous rain.
    Title: None provided.
    """,
    "source_identifier": "test_title_gen"
}

print("Testing Title Generation in AI Service...")
try:
    response = requests.post(URL, json=payload_text, timeout=60)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print("✅ Success!")
            output = data.get("data", {})
            print(f"Extracted Title: {output.get('title')}")
            print(f"Summary: {output.get('summary')}")
            print(f"Category: {output.get('primary_category')}")
            print(f"Verification: {output.get('verification', {}).get('status')}")
            
            if output.get('title') and "landslide" in output.get('title').lower():
                 print("✅ Title correctly generated/extracted!")
            else:
                 print("⚠️ Title generation might be weak.")
        else:
            print(f"❌ Failed: {data.get('error')}")
    else:
        print(f"❌ HTTP {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
