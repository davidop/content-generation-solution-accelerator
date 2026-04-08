"""
Compliance Agent - Comprehensive brand and content compliance checking.

Aggregates validation results across all content types (headline, body,
CTA, image prompt, image alt text) and returns a consolidated report.
"""

import logging
from typing import Optional

try:
    # When run directly inside src/backend/agents/ (e.g., app.py imports)
    from agents.text_content_agent import validate_text_compliance
except ImportError:
    # When imported as backend.agents.compliance_agent (e.g., from tests/)
    from backend.agents.text_content_agent import validate_text_compliance

logger = logging.getLogger(__name__)

# Image prompt terms that indicate policy violations
_PROHIBITED_IMAGE_TERMS = [
    "competitor",
    "real person",
    "violence",
    "weapon",
    "nude",
    "explicit",
    "deepfake",
    "hate",
]


def comprehensive_compliance_check(
    headline: str = "",
    body: str = "",
    cta_text: Optional[str] = None,
    image_prompt: str = "",
    image_alt_text: str = "",
) -> dict:
    """
    Run compliance checks across all content fields.

    Args:
        headline: Marketing headline text
        body: Body copy text
        cta_text: Call-to-action text.
            - ``None`` (default) → CTA not required for this content type; no warning raised.
            - ``""`` (empty string) → CTA is expected but missing; a warning is raised.
            - Any non-empty string → CTA is present; no warning raised.
        image_prompt: Image generation prompt
        image_alt_text: Accessibility alt text for the image

    Returns:
        dict with keys:
            - is_valid (bool): True if no error-level violations
            - violations (list): All violations across fields
            - summary (str): Human-readable summary
            - approval_status (str): 'APPROVED', 'REVIEW_RECOMMENDED', or 'BLOCKED'
    """
    violations = []

    # Validate headline
    if headline:
        result = validate_text_compliance(headline, "headline")
        violations.extend(result["violations"])

    # Validate body copy
    if body:
        result = validate_text_compliance(body, "body")
        violations.extend(result["violations"])

    # CTA presence check — warn only when cta_text is explicitly empty string
    if cta_text is not None and cta_text == "":
        violations.append({
            "severity": "warning",
            "message": "Call-to-action (CTA) is missing from the content",
            "suggestion": "Add a clear CTA such as 'Shop Now', 'Learn More', or 'Get Started'",
            "field": "cta",
        })

    # Image prompt policy check
    if image_prompt:
        image_lower = image_prompt.lower()
        for term in _PROHIBITED_IMAGE_TERMS:
            if term in image_lower:
                violations.append({
                    "severity": "error",
                    "message": f"Prohibited term '{term}' found in image prompt",
                    "suggestion": (
                        f"Remove the reference to '{term}' from the image prompt "
                        "to comply with content policy"
                    ),
                    "field": "image_prompt",
                })

    error_count = sum(1 for v in violations if v["severity"] == "error")
    warning_count = sum(1 for v in violations if v["severity"] == "warning")
    info_count = sum(1 for v in violations if v["severity"] == "info")

    if error_count > 0:
        approval_status = "BLOCKED"
    elif warning_count > 0:
        approval_status = "REVIEW_RECOMMENDED"
    else:
        approval_status = "APPROVED"

    parts = []
    if error_count:
        parts.append(f"{error_count} error(s)")
    if warning_count:
        parts.append(f"{warning_count} warning(s)")
    if info_count:
        parts.append(f"{info_count} info item(s)")
    summary = f"Found {', '.join(parts)}" if parts else "No issues found — content is compliant"

    return {
        "is_valid": error_count == 0,
        "violations": violations,
        "summary": summary,
        "approval_status": approval_status,
    }
