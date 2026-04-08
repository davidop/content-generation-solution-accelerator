"""
Campaign Impact Hub Orchestrator - Simplified 3-agent campaign workflow.

This orchestrator coordinates three specialized agents to produce a complete
campaign response from a simple frontend payload:

  1. CampaignStrategist  → interprets brief, builds strategy
  2. ContentCreator      → generates channel-specific content
  3. PerformanceAnalyst  → returns analytics and campaign plan

The result is a structured JSON object ready for immediate UI consumption.
"""

import logging
from typing import Optional

from agents.campaign_strategist import build_campaign_strategy
from agents.content_creator import generate_campaign_content
from agents.performance_analyst import analyze_campaign_performance
from models import CampaignContext, CampaignResponse, CampaignCards

logger = logging.getLogger(__name__)


async def run_campaign_workflow(
    user_message: str,
    campaign_context: Optional[dict] = None,
) -> CampaignResponse:
    """
    Execute the simplified campaign generation workflow.

    Orchestrates the three campaign agents in sequence:
    1. Interpret the brief and build the strategy (CampaignStrategist)
    2. Generate content for each channel (ContentCreator)
    3. Produce analytics and execution plan (PerformanceAnalyst)

    Args:
        user_message: The user's free-text campaign request
        campaign_context: Optional structured context from the frontend:
            {
                "product": "...",
                "target": "25-40",
                "channels": ["Instagram", "TikTok"],
                "brandTone": "...",
                "budget": "medio"
            }

    Returns:
        CampaignResponse: Structured response ready for the UI
    """
    # Parse context
    ctx = campaign_context or {}
    product = ctx.get("product", "")
    target = ctx.get("target", "")
    channels = ctx.get("channels", ["Instagram"])
    brand_tone = ctx.get("brandTone", "")
    budget = ctx.get("budget", "medio")

    logger.info(
        f"Campaign workflow started — product='{product}', "
        f"channels={channels}, target='{target}'"
    )

    # ── Step 1: Campaign Strategist ──────────────────────────────────────────
    try:
        strategy = build_campaign_strategy(
            user_message=user_message,
            product=product,
            target=target,
            channels=channels,
            brand_tone=brand_tone,
            budget=budget,
        )
        logger.info("CampaignStrategist completed")
    except Exception as e:
        logger.exception(f"CampaignStrategist failed: {e}")
        strategy = {"error": str(e), "positioning": "", "channels": []}

    # ── Step 2: Content Creator ──────────────────────────────────────────────
    try:
        content = generate_campaign_content(
            product=product,
            target=target,
            channels=channels,
            brand_tone=brand_tone,
            user_message=user_message,
        )
        logger.info("ContentCreator completed")
    except Exception as e:
        logger.exception(f"ContentCreator failed: {e}")
        content = {"error": str(e)}

    # ── Step 3: Performance Analyst ──────────────────────────────────────────
    try:
        analytics, campaign_plan = analyze_campaign_performance(
            product=product,
            target=target,
            channels=channels,
            budget=budget,
        )
        logger.info("PerformanceAnalyst completed")
    except Exception as e:
        logger.exception(f"PerformanceAnalyst failed: {e}")
        analytics = {"error": str(e)}
        campaign_plan = {}

    # ── Build summary ────────────────────────────────────────────────────────
    summary = _build_summary(product, target, channels, brand_tone, budget)

    # ── Build UI cards ───────────────────────────────────────────────────────
    cards = CampaignCards(
        overview={
            "product": product,
            "target": target,
            "channels": channels,
            "tone": brand_tone,
            "budget": budget,
            "summary": summary,
        },
        strategy={
            "positioning": strategy.get("positioning", ""),
            "kpis": strategy.get("kpis", []),
            "phase": strategy.get("phase", ""),
            "duration": strategy.get("campaign_duration", ""),
        },
        content={ch: assets for ch, assets in (content or {}).items()},
        analytics={
            "predicted_performance": analytics.get("predicted_performance", []),
            "roi_estimate": analytics.get("roi_estimate", {}),
            "optimization_tips": analytics.get("optimization_tips", []),
        },
    )

    response = CampaignResponse(
        summary=summary,
        strategy=strategy,
        content=content,
        analytics=analytics,
        campaignPlan=campaign_plan,
        cards=cards,
    )

    logger.info("Campaign workflow completed successfully")
    return response


def _build_summary(
    product: str,
    target: str,
    channels: list,
    brand_tone: str,
    budget: str,
) -> str:
    """Build a concise campaign overview summary."""
    channel_str = ", ".join(channels) if channels else "social media"
    return (
        f"Campaign for {product or 'the product'} targeting {target or 'your audience'} "
        f"across {channel_str}. "
        f"Tone: {brand_tone or 'engaging'}. "
        f"Budget level: {budget or 'medium'}. "
        "Strategy, content, and analytics ready for execution."
    )
