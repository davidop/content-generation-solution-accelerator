"""
Text Content Agent - Validates and generates marketing text content.

Provides rule-based compliance checking for marketing copy against
brand guidelines (prohibited words, character limits, unsubstantiated claims).
"""

import logging
from typing import Optional

try:
    from settings import app_settings
except ImportError:
    from backend.settings import app_settings


# Default prohibited words used when no BRAND_PROHIBITED_WORDS env var is set.
# These match the defaults in .env.sample.
_DEFAULT_PROHIBITED_WORDS = [
    "cheapest",
    "guaranteed",
    "best in class",
    "#1",
    "market leader",
]

logger = logging.getLogger(__name__)

# Unsubstantiated superlative claims that require evidence
_UNSUBSTANTIATED_CLAIMS = [
    "#1",
    "number one",
    "best in class",
    "market leader",
    "industry leader",
    "top rated",
    "world's best",
    "guaranteed",
]


def validate_text_compliance(content: str, content_type: str = "body") -> dict:
    """
    Validate marketing text against brand guidelines.

    Checks for:
    - Prohibited words (configured via BRAND_PROHIBITED_WORDS)
    - Unsubstantiated superlative claims
    - Headline character length (warning if > max_headline_length)

    Args:
        content: The text content to validate
        content_type: Type of content ('headline', 'body', 'cta', 'tagline')

    Returns:
        dict with keys:
            - is_valid (bool): True if no error-level violations
            - violations (list): Each item has severity, message, suggestion, field
    """
    violations = []
    content_lower = content.lower() if content else ""

    # 1. Prohibited words check
    brand = app_settings.brand_guidelines
    prohibited = brand.prohibited_words or _DEFAULT_PROHIBITED_WORDS

    for word in prohibited:
        if word.lower() in content_lower:
            violations.append({
                "severity": "error",
                "message": f"Prohibited word/phrase '{word}' found in {content_type} content",
                "suggestion": f"Remove or replace '{word}' with brand-appropriate alternatives",
                "field": content_type,
            })

    # 2. Unsubstantiated claims check
    for claim in _UNSUBSTANTIATED_CLAIMS:
        if claim.lower() in content_lower:
            # Only flag if not already caught by prohibited words
            already_flagged = any(
                v["message"] and claim.lower() in v["message"].lower()
                for v in violations
            )
            if not already_flagged:
                violations.append({
                    "severity": "error",
                    "message": f"Unsubstantiated claim '{claim}' found — requires evidence or removal",
                    "suggestion": f"Remove '{claim}' or replace with specific, verifiable data",
                    "field": content_type,
                })

    # 3. Headline length check
    if content_type == "headline" and content:
        max_len = brand.max_headline_length
        if len(content) > max_len:
            violations.append({
                "severity": "warning",
                "message": (
                    f"Headline length ({len(content)} chars) exceeds recommended "
                    f"maximum of {max_len} characters"
                ),
                "suggestion": "Shorten the headline for better readability and impact",
                "field": "headline",
            })

    return {
        "is_valid": not any(v["severity"] == "error" for v in violations),
        "violations": violations,
    }
