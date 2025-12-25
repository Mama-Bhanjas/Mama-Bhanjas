import requests
from ..config import settings

class AIPipeline:
    def __init__(self):
        self.base_url = settings.AI_SERVICE_URL

    def classify_report(self, text: str) -> str:
        """
        Classifies the report text by calling the AI Service.
        """
        try:
            payload = {"text": text, "top_k": 1}
            response = requests.post(f"{self.base_url}/api/classify", json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("category"):
                return data["category"]
            return "Unclassified"
        except Exception as e:
            print(f"Error calling AI service (classify): {e}")
            return "Unclassified"

    def summarize_reports(self, texts: list[str]) -> str:
        """
        Generates a summary from a list of report texts by calling the AI Service.
        """
        if not texts:
            return ""
            
        try:
            # Join texts for a single summary request, or use batch if supported/needed.
            # The previous implementation joined distinct reports into one text.
            # We'll stick to that logic but use the summarize endpoint.
            # Ideally, if texts are many, valid approach is to join them.
            
            combined_text = " ".join(texts)
            # Truncating client-side if needed, but service should handle or we trust it.
            # Service has a min_length 50 validation on /api/summarize request.text
            
            if len(combined_text) < 50: 
                return combined_text # Too short to summarize via AI, return as is.

            payload = {
                "text": combined_text,
                "max_length": 150,
                "min_length": 30
            }
            
            response = requests.post(f"{self.base_url}/api/summarize", json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("summary"):
                return data["summary"]
            return ""
            
        except Exception as e:
            print(f"Error calling AI service (summarize): {e}")
            return ""

    def verify_news(self, text: str, source_url: str = None) -> dict:
        """
        Verifies news credibility via AI Service.
        """
        try:
            payload = {"text": text, "source_url": source_url}
            response = requests.post(f"{self.base_url}/api/verify/news", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling AI service (verify_news): {e}")
            return {"success": False, "error": str(e)}

    def verify_report(self, text: str) -> dict:
        """
        Verifies civic report validity via AI Service.
        """
        try:
            payload = {"text": text}
            response = requests.post(f"{self.base_url}/api/verify/report", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling AI service (verify_report): {e}")
            return {"success": False, "error": str(e)}

    def fact_check(self, text: str) -> dict:
        """
        Performs deep verification (internet search) via AI Service.
        """
        try:
            payload = {"text": text}
            response = requests.post(f"{self.base_url}/api/verify/factcheck", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling AI service (fact_check): {e}")
            return {"success": False, "error": str(e)}

    def process_report(self, text: str, source_url: str = None) -> dict:
        """
        Calls the Unified Processor to get classification, summary, NER, and verification in one go.
        """
        try:
            payload = {"text": text, "source_url": source_url}
            response = requests.post(f"{self.base_url}/api/process/report", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling AI service (process_report): {e}")
            return {"success": False, "error": str(e)}

ai_pipeline = AIPipeline()
