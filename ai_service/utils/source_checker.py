"""
Enhanced Source Verification Utility
Evaluates credibility of news/report sources using multiple signals
"""

from urllib.parse import urlparse
from typing import Dict, Tuple, List


class SourceChecker:
    """
    Evaluates source credibility using domain reputation,
    TLD trust, HTTPS usage, and suspicious patterns.
    """

    # Highly trusted global news & institutions
    TRUSTED_DOMAINS = {
        # International / Major Agencies
        "reuters.com", "apnews.com", "bloomberg.com", "afp.com", "upi.com",
        "bbc.com", "bbc.co.uk", "dw.com", "france24.com", "aljazeera.com",
        "euronews.com", "cbc.ca", "abc.net.au", "npr.org", "pbs.org",
        "nytimes.com", "wsj.com", "washingtonpost.com", "usatoday.com", 
        "latimes.com", "chicagotribune.com", "bostonglobe.com",
        "cnn.com", "nbcnews.com", "cbsnews.com", "abcnews.go.com", "msnbc.com",
        "cnbc.com", "foxnews.com", "time.com", "newsweek.com", "usnews.com",
        "theguardian.com", "independent.co.uk", "telegraph.co.uk", "standard.co.uk",
        "ft.com", "economist.com", 
        # Tech/Science
        "wired.com", "theverge.com", "arstechnica.com", "techcrunch.com", 
        "scientificamerican.com", "nature.com", "science.org",
        # Fact Checkers
        "snopes.com", "politifact.com", "factcheck.org", "fullfact.org",
        # Organizations
        "who.int", "un.org", "reliefweb.int",
        # Regional (Nepal)
        "kathmandupost.com", "kathmandugazette.com", "risingnepal.org.np",
        "nepalnews.com", "khabarhub.com", "himalayadiary.com", "setopati.com",
        "spacenews.com", "tass.com",
        # Universities/Research
        "rmit.edu.au", "sciencedaily.com", "mit.edu", "harvard.edu", "stanford.edu"
    }

    # Known satire, clickbait, misinformation
    UNTRUSTED_DOMAINS = {
        "theonion.com", "clickbait-central.com", "satire-world.com", "onion.com",
        "babylonbee.com", "dailybuzz.live", "infowars.com", "naturalnews.com",
        "breitbart.com", "gatewaypundit.com", "zerohedge.com", "sputniknews.com",
        "rt.com", "conspiracy-theories.net", "thetruthobserver.blog",
        "londondailytruth.site", "tech-expose.blog", "ocean-council.online",
        "medical-truth.blog"
    }

    # Trusted top-level domains
    TRUSTED_TLDS = {".gov", ".edu", ".int"}

    # Suspicious patterns often found in fake news sites
    SUSPICIOUS_KEYWORDS = {
        "clickbait", "viral", "shocking", "truth-revealed",
        "breaking-now", "exclusive", "thetruth", "observer",
        "dailytruth", "leaked-document", "lockout", "smart-fridge",
        "silicon-based", "clandestine", "shadow-biosphere",
        "official-notice", "emergency-alert", "truth", "leaked",
        "memory-wipe", "MNEM-7", "expiration-date", "bank-collective",
        "tidal-tax", "continental-shield", "micro-cellular", "ocean-council"
    }

    SUSPICIOUS_TLDS = {".blog", ".site", ".online", ".xyz", ".top", ".buzz"}

    def check_source(self, url: str) -> Dict:
        """
        Check credibility of a source URL

        Returns:
            {
                status: Trusted | Untrusted | Unknown | Invalid
                source_score: float (0.0 - 1.0)
                reasons: list[str]
            }
        """
        reasons: List[str] = []

        if not url:
            return {
                "status": "Unknown",
                "source_score": 0.5,
                "reasons": ["No source URL provided"]
            }

        try:
            parsed = urlparse(url if "://" in url else f"https://{url}")
            domain = parsed.netloc.lower().replace("www.", "")

            if not domain:
                return {
                    "status": "Invalid",
                    "source_score": 0.0,
                    "reasons": ["Invalid URL format"]
                }

            score = 0.5  # neutral baseline

            # 1️⃣ HTTPS check
            if parsed.scheme == "https":
                score += 0.1
                reasons.append("Uses HTTPS")

            # 2️⃣ Trusted domain (including subdomains)
            for trusted in self.TRUSTED_DOMAINS:
                if domain == trusted or domain.endswith(f".{trusted}"):
                    score = 0.9
                    reasons.append("Recognized trusted news or institutional source")
                    return {
                        "status": "Trusted",
                        "source_score": round(score, 2),
                        "reasons": reasons
                    }

            # 3️⃣ Untrusted domain
            for untrusted in self.UNTRUSTED_DOMAINS:
                if domain == untrusted or domain.endswith(f".{untrusted}"):
                    return {
                        "status": "Untrusted",
                        "source_score": 0.0,
                        "reasons": ["Known misinformation or satire domain"]
                    }

            # 4️⃣ Trusted TLD
            for tld in self.TRUSTED_TLDS:
                if domain.endswith(tld):
                    score += 0.2
                    reasons.append(f"Trusted top-level domain ({tld})")

            # 5️⃣ Suspicious TLD
            for tld in self.SUSPICIOUS_TLDS:
                if domain.endswith(tld):
                    score -= 0.15
                    reasons.append(f"Generic or suspicious top-level domain ({tld})")

            # 5️⃣ Suspicious keyword patterns
            for word in self.SUSPICIOUS_KEYWORDS:
                if word in domain:
                    score -= 0.2
                    reasons.append("Suspicious domain naming pattern")

            # Clamp score
            score = min(max(score, 0.0), 1.0)

            status = (
                "Trusted" if score >= 0.75 else
                "Untrusted" if score <= 0.4 else
                "Unknown"
            )

            return {
                "status": status,
                "source_score": round(score, 2),
                "reasons": reasons or ["No strong credibility signals detected"]
            }

        except Exception as e:
            return {
                "status": "Invalid",
                "source_score": 0.0,
                "reasons": ["Error parsing URL"]
            }
