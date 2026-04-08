"""
Performance Analyst Agent - Generates campaign analytics and insights.

Responsible for:
- Predicting performance benchmarks per channel
- Suggesting optimization tactics
- Building the execution timeline (campaign plan)
- Returning basic ROI estimates
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def analyze_campaign_performance(
    product: str = "",
    target: str = "",
    channels: Optional[list] = None,
    budget: str = "",
) -> dict:
    """
    Generate predicted performance analytics and campaign plan.

    This is a benchmark-based estimator for demo purposes.
    In production, this would call an LLM agent with historical data.

    Args:
        product: Product name/description
        target: Target audience
        channels: List of marketing channels
        budget: Budget level

    Returns:
        dict with analytics and campaign plan sections
    """
    channels = channels or ["Instagram"]

    channel_benchmarks = _get_channel_benchmarks(channels, budget)
    campaign_plan = _build_campaign_plan(channels)
    roi_estimate = _estimate_roi(budget, channels)

    analytics = {
        "predicted_performance": channel_benchmarks,
        "roi_estimate": roi_estimate,
        "recommended_kpis": [
            {
                "kpi": "Cost Per Click (CPC)",
                "benchmark": "$0.50–$2.00",
                "optimization": "Test 3–5 creative variants to find the best performer",
            },
            {
                "kpi": "Return on Ad Spend (ROAS)",
                "benchmark": "3–5x",
                "optimization": "Focus spend on best-performing channels after week 2",
            },
            {
                "kpi": "Engagement Rate",
                "benchmark": "3–6%",
                "optimization": "Use UGC and behind-the-scenes content to boost engagement",
            },
        ],
        "optimization_tips": _get_optimization_tips(channels),
        "audience_insights": {
            "target_segment": target or "25–40",
            "peak_activity": _get_peak_times(channels),
            "content_preferences": ["short-form video", "lifestyle imagery", "user reviews"],
        },
    }

    logger.info(f"Performance analytics generated for {len(channels)} channels")
    return analytics, campaign_plan


def _get_channel_benchmarks(channels: list, budget: str) -> list:
    """Return predicted performance benchmarks per channel."""
    benchmarks = []
    for ch in channels:
        ch_lower = ch.lower()
        if "instagram" in ch_lower:
            benchmarks.append({
                "channel": "Instagram",
                "estimated_reach": "15,000–40,000/month",
                "engagement_rate": "3–5%",
                "cpc": "$0.70–$1.50",
                "best_format": "Reels",
            })
        elif "tiktok" in ch_lower:
            benchmarks.append({
                "channel": "TikTok",
                "estimated_reach": "20,000–80,000/month",
                "engagement_rate": "5–9%",
                "cpc": "$0.50–$1.20",
                "best_format": "15–30s vertical video",
            })
        elif "linkedin" in ch_lower:
            benchmarks.append({
                "channel": "LinkedIn",
                "estimated_reach": "5,000–15,000/month",
                "engagement_rate": "2–4%",
                "cpc": "$2.00–$5.00",
                "best_format": "Sponsored article",
            })
        elif "email" in ch_lower:
            benchmarks.append({
                "channel": "Email",
                "estimated_reach": "3,000–10,000/send",
                "open_rate": "20–30%",
                "click_rate": "2–5%",
                "best_format": "HTML newsletter",
            })
        else:
            benchmarks.append({
                "channel": ch,
                "estimated_reach": "5,000–20,000/month",
                "engagement_rate": "2–4%",
                "cpc": "$1.00–$3.00",
                "best_format": "Mixed content",
            })
    return benchmarks


def _build_campaign_plan(channels: list) -> dict:
    """Build a phased campaign execution timeline."""
    return {
        "phases": [
            {
                "phase": "Phase 1 — Setup & Awareness",
                "weeks": "Week 1–2",
                "activities": [
                    "Finalize creative assets",
                    "Set up campaign tracking (UTMs, pixels)",
                    "Launch awareness content on all channels",
                    "Monitor initial engagement metrics",
                ],
            },
            {
                "phase": "Phase 2 — Optimization & Consideration",
                "weeks": "Week 3–4",
                "activities": [
                    "A/B test top-performing creatives",
                    "Retarget engaged users with conversion content",
                    "Increase spend on best-performing channels",
                    "Publish user testimonials / social proof",
                ],
            },
            {
                "phase": "Phase 3 — Conversion & Retention",
                "weeks": "Week 5–6",
                "activities": [
                    "Deploy conversion-focused ads",
                    "Launch email nurture sequence",
                    "Offer limited-time promotion or bundle",
                    "Gather post-campaign performance data",
                ],
            },
        ],
        "total_duration": "6 weeks",
        "channels_included": channels,
        "review_checkpoints": ["End of Week 2", "End of Week 4", "Campaign close"],
    }


def _estimate_roi(budget: str, channels: list) -> dict:
    """Estimate ROI range based on budget level."""
    multipliers = {
        "bajo": (2.0, 3.5),
        "low": (2.0, 3.5),
        "medio": (3.0, 5.0),
        "medium": (3.0, 5.0),
        "alto": (4.0, 7.0),
        "high": (4.0, 7.0),
    }
    low_mult, high_mult = multipliers.get(budget.lower(), (3.0, 5.0))
    return {
        "roas_range": f"{low_mult}x–{high_mult}x",
        "payback_period": "3–6 weeks",
        "confidence": "Medium — based on industry benchmarks",
        "note": "Actual results depend on creative quality, targeting precision, and offer strength",
    }


def _get_optimization_tips(channels: list) -> list:
    """Return actionable optimization tips for the selected channels."""
    tips = [
        "Post at peak engagement times for each platform",
        "Use platform-native formats (Reels for Instagram, vertical video for TikTok)",
        "Test 3–5 headline variants in the first two weeks",
        "Include social proof elements (reviews, UGC) to boost trust",
        "Retarget website visitors with channel-specific ads",
    ]
    if any("tiktok" in c.lower() for c in channels):
        tips.append("Collaborate with micro-influencers (10K–100K followers) for TikTok reach")
    if any("email" in c.lower() for c in channels):
        tips.append("Segment email list by engagement level for higher open rates")
    return tips


def _get_peak_times(channels: list) -> dict:
    """Return peak engagement windows per channel."""
    peak_times = {}
    for ch in channels:
        ch_lower = ch.lower()
        if "instagram" in ch_lower:
            peak_times["Instagram"] = "Tue–Fri, 11am–1pm and 7pm–9pm"
        elif "tiktok" in ch_lower:
            peak_times["TikTok"] = "Tue–Thu, 6am–10am and 7pm–11pm"
        elif "linkedin" in ch_lower:
            peak_times["LinkedIn"] = "Tue–Thu, 8am–10am and 12pm–2pm"
        elif "email" in ch_lower:
            peak_times["Email"] = "Tue/Thu, 9am–11am"
        else:
            peak_times[ch] = "Mon–Fri, 9am–5pm"
    return peak_times
