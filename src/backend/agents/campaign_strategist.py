"""
Campaign Strategist Agent - Interprets briefs and builds campaign strategy.

Responsible for:
1. Parsing the user's request and campaign context into a structured brief
2. Generating a channel-specific campaign strategy with positioning and KPIs
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def build_campaign_strategy(
    user_message: str,
    product: str = "",
    target: str = "",
    channels: Optional[list] = None,
    brand_tone: str = "",
    budget: str = "",
) -> dict:
    """
    Build a structured campaign strategy from campaign context.

    This is a rule-based strategy builder for demo purposes.
    In production, this would call an LLM agent via the orchestrator.

    Args:
        user_message: The user's original request message
        product: Product name/description
        target: Target audience segment
        channels: List of marketing channels
        brand_tone: Desired brand tone
        budget: Budget level (bajo/medio/alto)

    Returns:
        dict with strategy fields ready for the campaign response
    """
    channels = channels or ["Instagram", "LinkedIn"]

    # Map budget to spend range
    budget_map = {
        "bajo": "$500–$2,000/month",
        "low": "$500–$2,000/month",
        "medio": "$2,000–$10,000/month",
        "medium": "$2,000–$10,000/month",
        "alto": "$10,000–$50,000/month",
        "high": "$10,000–$50,000/month",
    }
    budget_range = budget_map.get(budget.lower(), "$2,000–$10,000/month")

    # Channel-specific tactics
    channel_tactics = []
    for ch in channels:
        ch_lower = ch.lower()
        if "instagram" in ch_lower:
            channel_tactics.append({
                "channel": "Instagram",
                "format": "Reels + carousel posts",
                "frequency": "5–7 posts/week",
                "objective": "Brand awareness and engagement",
            })
        elif "tiktok" in ch_lower:
            channel_tactics.append({
                "channel": "TikTok",
                "format": "Short-form video (15–30s)",
                "frequency": "3–5 videos/week",
                "objective": "Viral reach and product discovery",
            })
        elif "linkedin" in ch_lower:
            channel_tactics.append({
                "channel": "LinkedIn",
                "format": "Thought leadership articles + sponsored posts",
                "frequency": "3–4 posts/week",
                "objective": "B2B awareness and lead generation",
            })
        elif "twitter" in ch_lower or "x" in ch_lower:
            channel_tactics.append({
                "channel": "Twitter/X",
                "format": "Tweets + threads",
                "frequency": "Daily",
                "objective": "Community engagement and trend participation",
            })
        elif "email" in ch_lower:
            channel_tactics.append({
                "channel": "Email",
                "format": "Newsletter + promotional campaigns",
                "frequency": "2–3 emails/week",
                "objective": "Retention and conversion",
            })
        else:
            channel_tactics.append({
                "channel": ch,
                "format": "Mixed content",
                "frequency": "3–5 times/week",
                "objective": "Brand awareness",
            })

    strategy = {
        "positioning": (
            f"Position {product or 'the product'} as the go-to choice for "
            f"{target or 'the target audience'} by emphasizing quality, "
            f"innovation, and lifestyle alignment."
        ),
        "tone": brand_tone or "Professional and engaging",
        "target_audience": {
            "age_range": target or "25–40",
            "interests": ["fitness", "technology", "lifestyle"],
            "persona": f"Active, tech-savvy {target or '25–40'} consumer looking for quality",
        },
        "channels": channel_tactics,
        "budget": {
            "level": budget or "medio",
            "estimated_range": budget_range,
            "allocation": _allocate_budget(channels),
        },
        "kpis": [
            {"metric": "Reach", "target": "50,000+ impressions/month"},
            {"metric": "Engagement Rate", "target": "3–5%"},
            {"metric": "Click-through Rate", "target": "2–4%"},
            {"metric": "Conversion Rate", "target": "1–3%"},
        ],
        "campaign_duration": "4–6 weeks",
        "phase": "Awareness → Consideration → Conversion",
    }

    logger.info(f"Campaign strategy built for product='{product}', channels={channels}")
    return strategy


def _allocate_budget(channels: list) -> dict:
    """Distribute budget evenly across channels."""
    if not channels:
        return {}
    share = round(100 / len(channels))
    allocation = {ch: f"{share}%" for ch in channels}
    return allocation
