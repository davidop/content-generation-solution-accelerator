"""
Content Creator Agent - Generates marketing copy for each channel.

Responsible for producing ready-to-publish content assets:
- Channel-specific captions and posts
- Hashtag sets
- Email subject lines and preview text
- Ad copy variants
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def generate_campaign_content(
    product: str = "",
    target: str = "",
    channels: Optional[list] = None,
    brand_tone: str = "",
    user_message: str = "",
) -> dict:
    """
    Generate marketing content for each specified channel.

    This is a template-based content generator for demo purposes.
    In production, this would call an LLM agent via the orchestrator.

    Args:
        product: Product name/description
        target: Target audience
        channels: List of marketing channels
        brand_tone: Desired brand tone
        user_message: Original user request for additional context

    Returns:
        dict with content assets per channel
    """
    channels = channels or ["Instagram"]
    tone_desc = brand_tone or "energético y cercano"

    content_assets = {}

    for ch in channels:
        ch_lower = ch.lower()

        if "instagram" in ch_lower:
            content_assets["instagram"] = _instagram_content(product, target, tone_desc)
        elif "tiktok" in ch_lower:
            content_assets["tiktok"] = _tiktok_content(product, target, tone_desc)
        elif "linkedin" in ch_lower:
            content_assets["linkedin"] = _linkedin_content(product, target, tone_desc)
        elif "twitter" in ch_lower or "x" in ch_lower:
            content_assets["twitter"] = _twitter_content(product, target, tone_desc)
        elif "email" in ch_lower:
            content_assets["email"] = _email_content(product, target, tone_desc)
        else:
            content_assets[ch.lower()] = _generic_content(ch, product, target, tone_desc)

    logger.info(f"Content generated for {len(content_assets)} channels")
    return content_assets


def _instagram_content(product: str, target: str, tone: str) -> dict:
    return {
        "caption": (
            f"🚀 Introducing {product or 'our latest product'} — built for the "
            f"{target or 'modern'} lifestyle. ✨\n\n"
            "Performance meets style in every detail. Ready to level up?\n\n"
            "#Innovation #NewProduct #LifestyleTech"
        ),
        "headline": f"Meet {product or 'your new favorite'} 🔥",
        "cta": "Shop Now →",
        "hashtags": [
            f"#{(product or 'product').replace(' ', '')}",
            "#NewLaunch",
            "#TechLife",
            "#FitnessGoals",
            "#Innovation",
        ],
        "story_copy": f"Swipe up to discover {product or 'it'} 👆",
        "format_recommendation": "Square (1:1) for feed, vertical (9:16) for Stories/Reels",
    }


def _tiktok_content(product: str, target: str, tone: str) -> dict:
    return {
        "hook": f"POV: You just found the {product or 'product'} everyone's talking about 👀",
        "script_outline": [
            "0–3s: Hook — close-up of product in use",
            "3–8s: Problem — show everyday frustration it solves",
            "8–20s: Solution — demonstrate key features naturally",
            "20–30s: CTA — 'Link in bio for yours!'",
        ],
        "caption": (
            f"This {product or 'product'} just changed everything 🤯 "
            "#FYP #NewProduct #MustHave"
        ),
        "hashtags": ["#FYP", "#NewProduct", "#MustHave", "#TechTok", "#LifeHack"],
        "cta": "Link in bio 🔗",
        "music_suggestion": "Trending upbeat track — check TikTok Creative Center",
        "format_recommendation": "Vertical (9:16), 15–30 seconds",
    }


def _linkedin_content(product: str, target: str, tone: str) -> dict:
    return {
        "headline": f"How {product or 'our product'} is redefining the market for {target or 'professionals'}",
        "body": (
            f"We're excited to introduce {product or 'our latest solution'} — "
            "designed from the ground up to meet the demands of today's fast-paced world.\n\n"
            f"Built for {target or 'professionals'} who refuse to compromise on quality, "
            "it combines cutting-edge technology with intuitive design.\n\n"
            "What makes the difference? Real performance where it counts.\n\n"
            "👉 Learn more in the comments below."
        ),
        "cta": "Learn More",
        "hashtags": ["#Innovation", "#ProductLaunch", "#Technology", "#Leadership"],
        "format_recommendation": "Landscape (1.91:1) for sponsored content",
    }


def _twitter_content(product: str, target: str, tone: str) -> dict:
    return {
        "tweet": (
            f"Introducing {product or 'our newest product'} 🚀 "
            f"Designed for {target or 'you'}. "
            "Performance redefined. #NewLaunch #Innovation"
        ),
        "thread_hook": f"Thread: Why {product or 'this'} is the product of the year 🧵",
        "cta": "Check it out →",
        "hashtags": ["#NewLaunch", "#Innovation", "#Tech"],
        "format_recommendation": "16:9 image or short video (2:20)",
    }


def _email_content(product: str, target: str, tone: str) -> dict:
    return {
        "subject_line": f"Introducing {product or 'something new'} — made for you",
        "preview_text": "Discover what everyone's talking about →",
        "headline": f"Meet {product or 'your new essential'}",
        "body": (
            f"Hi there,\n\n"
            f"We built {product or 'this product'} with one person in mind: you.\n\n"
            f"Whether you're in the office or on the move, it's designed to keep up with "
            f"the demands of {target or 'your lifestyle'}.\n\n"
            "Here's what you get:\n"
            "• Exceptional performance\n"
            "• Sleek, modern design\n"
            "• Backed by our quality guarantee\n\n"
            "Ready to experience the difference?"
        ),
        "cta": "Shop Now",
        "ps_line": f"P.S. Limited stock available — don't miss your chance to own {product or 'it'}.",
    }


def _generic_content(channel: str, product: str, target: str, tone: str) -> dict:
    return {
        "headline": f"Introducing {product or 'our newest product'}",
        "body": (
            f"Designed for {target or 'everyone'}, {product or 'our product'} "
            "delivers exceptional quality and performance."
        ),
        "cta": "Learn More",
        "hashtags": ["#NewProduct", "#Innovation"],
        "format_recommendation": f"Standard {channel} format",
    }
