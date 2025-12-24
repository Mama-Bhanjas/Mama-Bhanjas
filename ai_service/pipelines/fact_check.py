"""
Fact Checking Pipeline
Verifies claims by searching the internet for corroborating sources
"""
from typing import Dict, List, Optional
import time
from loguru import logger
from duckduckgo_search import DDGS
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from ai_service.utils.source_checker import SourceChecker
from ai_service.utils import TextPreprocessor

# Reasonable request timeout for external fetches
REQUEST_TIMEOUT = 5.0


class FactCheckPipeline:
    """
    Pipeline that searches the web to verify news
    """

    def __init__(self):
        self.source_checker = SourceChecker()
        self.preprocessor = TextPreprocessor()
        logger.info("FactCheck pipeline initialized")

    def _normalize_result(self, raw_result: dict) -> Dict[str, Optional[str]]:
        """
        Extract url and title robustly from raw DDGS result dicts.
        """
        url = raw_result.get("href") or raw_result.get("url") or raw_result.get("link") or ""
        title = raw_result.get("title") or raw_result.get("text") or ""
        return {"url": url, "title": title}

    def _fetch_title_if_missing(self, url: str, current_title: str) -> tuple[str, bool]:
        """
        Try to fetch page and extract a title if missing. Returns (title, reachable)
        """
        if not url:
            return current_title or "", False

        try:
            # prefer HEAD to check reachability quickly
            head = requests.head(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            if head.status_code >= 400:
                # fallback to GET if HEAD blocked
                resp = requests.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            else:
                # HEAD okay; try GET but allow quick failure
                resp = requests.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)

            if resp.status_code >= 400:
                return current_title or "", False

            # Try to extract a meaningful title
            if not current_title:
                try:
                    soup = BeautifulSoup(resp.content, "html.parser")
                    page_title = soup.title.string.strip() if soup.title and soup.title.string else ""
                    if page_title:
                        return page_title, True
                except Exception:
                    pass

            return current_title or "", True

        except Exception:
            return current_title or "", False

    def _domain_of(self, url: str) -> str:
        try:
            parsed = urlparse(url if "://" in url else f"https://{url}")
            domain = parsed.netloc.lower().replace("www.", "")
            return domain
        except Exception:
            return ""

    def verify_claim(self, text: str) -> Dict[str, any]:
        """
        Verify a text claim by searching for it

        Args:
            text: The news text to verify

        Returns:
            Verification result with found sources
        """
        # 1. Generate Query
        clean_text = self.preprocessor.clean_text(text)
        words = clean_text.split()
        # Improve query: use first 20 words and quote key noun phrases when possible
        if len(words) > 20:
            query = " ".join(words[:20]) + " news"
        else:
            query = clean_text + " news"

        logger.info(f"Fact checking query: {query}")

        # 2. Search Web
        sources: List[Dict] = []
        try:
            with DDGS(proxies=None) as ddgs:
                # increase max_results a bit; we will filter and dedupe
                raw_results = list(ddgs.text(query, max_results=12))

            found_trusted = False
            found_untrusted = False
            trusted_sources = []
            untrusted_sources = []
            seen_domains = set()

            for r in raw_results:
                nr = self._normalize_result(r)
                url = nr["url"]
                title = nr["title"]

                if not url:
                    continue

                # Basic filtering of non-http schemes
                if not url.lower().startswith(("http://", "https://")):
                    url = "https://" + url.lstrip("/")

                domain = self._domain_of(url)
                if not domain:
                    continue

                # Dedupe by domain (prefer first trusted entry per domain)
                if domain in seen_domains:
                    continue
                seen_domains.add(domain)

                # skip some obvious non-news or country/irrelevant engines by domain heuristics
                if any(x in domain for x in ["baidu.com", "zhihu.com", "sogou.com"]):
                    continue

                # Enrich source info
                title_enriched, reachable = self._fetch_title_if_missing(url, title)
                if title_enriched:
                    title = title_enriched

                source_result = self.source_checker.check_source(url)
                status = source_result.get("status", "Unknown")
                score = source_result.get("source_score", 0.0)
                reasons = source_result.get("reasons", [])

                source_info = {
                    "url": url,
                    "domain": domain,
                    "title": title or url,
                    "status": status,
                    "source_score": score,
                    "reasons": reasons,
                    "reachable": reachable
                }

                if status == "Trusted":
                    found_trusted = True
                    trusted_sources.append(source_info)
                elif status == "Untrusted":
                    found_untrusted = True
                    untrusted_sources.append(source_info)

                sources.append(source_info)

            # 3. Rank / choose primary sources
            primary_sources = []
            if trusted_sources:
                # sort trusted by source_score descending
                trusted_sources.sort(key=lambda s: s.get("source_score", 0.0), reverse=True)
                primary_sources = trusted_sources[:3]
            elif sources:
                # fallback: prefer reachable sources with higher source_score
                sources.sort(key=lambda s: (s.get("reachable", False), s.get("source_score", 0.0)), reverse=True)
                primary_sources = sources[:3]

            # 4. Formulate Verdict
            verification_status = "Unverified"
            confidence = 0.0
            explanation = "No relevant sources found."

            if trusted_sources:
                verification_status = "Verified"
                confidence = 1.0
                top_titles = ", ".join([s["title"] for s in trusted_sources[:2]])
                explanation = f"Corroborated by trusted sources: {top_titles}"
            elif found_untrusted and not trusted_sources:
                verification_status = "Fake"
                confidence = 0.9
                top_titles = ", ".join([s["title"] for s in untrusted_sources[:2]])
                explanation = f"Found only on known untrusted sources: {top_titles}"
            elif sources:
                verification_status = "Unverified"
                confidence = 0.45
                explanation = f"Found on {len(sources)} sources; none match our Trusted list. Manual review recommended."

            return {
                "success": True,
                "status": verification_status,
                "confidence": confidence,
                "is_reliable": verification_status == "Verified",
                "sources": sources,
                "primary_sources": primary_sources,
                "explanation": explanation
            }

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "status": "Error",
                "is_reliable": False
            }