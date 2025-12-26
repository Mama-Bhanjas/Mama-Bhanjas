
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from io import BytesIO
from typing import Optional, Dict
from loguru import logger
from urllib.parse import urlparse

class ContentExtractor:
    """
    Utility to extract text content from various sources like URLs and PDFs
    """
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def extract_from_url(self, url: str) -> Dict[str, any]:
        """
        Extract main text content from a URL
        """
        try:
            logger.info(f"Extracting content from URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get title
            title = soup.title.string.strip() if soup.title else ""
            
            # Get text - heuristic: find the largest text block
            # In a real production app, we might use trafilatura or readability-lxml
            # For now, we take all paragraph text
            paragraphs = soup.find_all('p')
            text = "\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
            
            if not text:
                # Fallback to get_text() on body if no paragraphs found
                text = soup.get_text(separator='\n', strip=True)
            
            return {
                "success": True,
                "text": text,
                "title": title,
                "url": url
            }
        except Exception as e:
            logger.error(f"URL extraction failed for {url}: {e}")
            return {"success": False, "error": str(e)}

    def extract_from_pdf(self, pdf_input: any) -> Dict[str, any]:
        """
        Extract text from a PDF file (path or bytes)
        """
        try:
            if isinstance(pdf_input, bytes):
                reader = PdfReader(BytesIO(pdf_input))
            else:
                reader = PdfReader(pdf_input)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return {
                "success": True,
                "text": text.strip(),
                "num_pages": len(reader.pages)
            }
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            return {"success": False, "error": str(e)}

    def is_url(self, source: Optional[str]) -> bool:
        """Check if a string is a valid URL"""
        if not source or not isinstance(source, str):
            return False
        try:
            result = urlparse(source)
            return bool(result.scheme and result.netloc)
        except Exception:
            return False
