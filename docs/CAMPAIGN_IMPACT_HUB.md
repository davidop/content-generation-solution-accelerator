# Campaign Impact Hub — Quick Start Guide

A simplified marketing campaign backend built on top of the [Content Generation Solution Accelerator](../README.md).

---

## What Has Been Simplified

| Original | Campaign Impact Hub |
|---|---|
| 6 agents (Triage, Planning, Research, TextContent, ImageContent, Compliance) | 3 agents (CampaignStrategist, ContentCreator, PerformanceAnalyst) |
| Image generation pipeline | Disabled — strategy and copy only |
| Advanced compliance validation via LLM | Lightweight rule-based compliance checks |
| CosmosDB product catalog required | Optional — works without any database |
| Complex multi-turn brief refinement | Single-shot campaign generation |
| Foundry / Agent Framework required | Works with any Azure OpenAI deployment |

The `/api/run` endpoint accepts a simple JSON payload from any frontend (e.g., GitHub Spark, React) and returns a fully structured JSON response ready for UI rendering.

---

## Architecture

```
Frontend (GitHub Spark / React)
    │
    │  POST /api/run
    ▼
┌─────────────────────────────────────┐
│         Campaign Impact Hub         │
│                                     │
│  ┌────────────────────────────────┐ │
│  │  1. CampaignStrategist         │ │
│  │     Interprets brief + builds  │ │
│  │     channel strategy + KPIs    │ │
│  └──────────────┬─────────────────┘ │
│                 │                   │
│  ┌──────────────▼─────────────────┐ │
│  │  2. ContentCreator             │ │
│  │     Generates channel-specific │ │
│  │     captions, scripts, emails  │ │
│  └──────────────┬─────────────────┘ │
│                 │                   │
│  ┌──────────────▼─────────────────┐ │
│  │  3. PerformanceAnalyst         │ │
│  │     Predicted metrics + ROI    │ │
│  │     + 6-week execution plan    │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
    │
    │  Structured JSON response
    ▼
Frontend renders cards
```

---

## Quick Deploy with `azd`

```bash
# 1. Install Azure Developer CLI
# https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd

# 2. Clone and enter the repository
git clone https://github.com/davidop/content-generation-solution-accelerator
cd content-generation-solution-accelerator

# 3. Log in
azd auth login

# 4. Deploy (all Azure resources + app)
azd up
```

For the minimal demo, you can **skip** the following optional features to speed up deployment by setting these parameters to `false` in `azure.yaml` or during `azd up`:

- `enableMonitoring` → disables Log Analytics / App Insights
- `enableScalability` → uses basic SKUs
- `enableRedundancy` → disables geo-replication
- `enablePrivateNetworking` → disables VNet / private endpoints

---

## Required Environment Variables

Copy `.env.sample` to `.env` and fill in the minimum required values:

```dotenv
# Azure OpenAI (required)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_GPT_MODEL=gpt-4o-mini     # or gpt-4o, gpt-5.1, etc.
AZURE_OPENAI_API_VERSION=2024-06-01

# Disable image generation for the demo (optional, saves cost)
AZURE_OPENAI_IMAGE_MODEL=none

# Disable Foundry mode (use direct Azure OpenAI)
USE_FOUNDRY=false
```

Optional (only needed for the full accelerator features):

```dotenv
AZURE_COSMOS_ENDPOINT=...          # Chat history storage
AZURE_BLOB_ACCOUNT_NAME=...        # Product images
AZURE_AI_SEARCH_ENDPOINT=...       # Product catalog search
```

---

## Local Development

```bash
cd src/backend
pip install -r requirements.txt

# Run the server
python -m hypercorn app:app --config hypercorn.conf.py
```

---

## Testing the `/api/run` Endpoint

### With `curl`

```bash
curl -X POST http://localhost:5000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a campaign for a fitness smartwatch"
      }
    ],
    "context": {
      "campaignContext": {
        "product": "Smartwatch fitness",
        "target": "25-40",
        "channels": ["Instagram", "TikTok"],
        "brandTone": "energético y cercano",
        "budget": "medio"
      },
      "uiState": {
        "view": "campaign"
      }
    }
  }'
```

### Expected Response

```json
{
  "summary": "Campaign for Smartwatch fitness targeting 25-40 across Instagram, TikTok...",
  "strategy": {
    "positioning": "Position Smartwatch fitness as the go-to choice...",
    "tone": "energético y cercano",
    "target_audience": { "age_range": "25-40", ... },
    "channels": [...],
    "kpis": [...],
    "campaign_duration": "4–6 weeks"
  },
  "content": {
    "instagram": {
      "caption": "🚀 Introducing Smartwatch fitness...",
      "headline": "Meet Smartwatch fitness 🔥",
      "cta": "Shop Now →",
      "hashtags": [...]
    },
    "tiktok": {
      "hook": "POV: You just found the Smartwatch fitness...",
      "script_outline": [...],
      ...
    }
  },
  "analytics": {
    "predicted_performance": [...],
    "roi_estimate": { "roas_range": "3x–5x", ... },
    "optimization_tips": [...]
  },
  "campaignPlan": {
    "phases": [...],
    "total_duration": "6 weeks"
  },
  "cards": {
    "overview": { "product": "Smartwatch fitness", ... },
    "strategy": { "positioning": "...", "kpis": [...], ... },
    "content": { "instagram": {...}, "tiktok": {...} },
    "analytics": { "predicted_performance": [...], ... }
  }
}
```

---

## Connecting to GitHub Spark or React

The `/api/run` endpoint accepts CORS from any origin by default. Point your frontend fetch call to:

```
POST https://<your-backend-url>/api/run
Content-Type: application/json
```

**GitHub Spark (JavaScript) example:**

```javascript
const response = await fetch("https://<backend-url>/api/run", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    messages: [{ role: "user", content: userInput }],
    context: {
      campaignContext: {
        product: selectedProduct,
        target: targetAudience,
        channels: selectedChannels,
        brandTone: tone,
        budget: budgetLevel,
      },
    },
  }),
});

const campaign = await response.json();
// campaign.cards.overview, campaign.cards.strategy, etc.
```

**React example:**

```jsx
import { useState } from "react";

function CampaignBuilder() {
  const [campaign, setCampaign] = useState(null);

  const generate = async () => {
    const res = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: "Generate a campaign" }],
        context: {
          campaignContext: {
            product: "Fitness Smartwatch",
            target: "25-40",
            channels: ["Instagram", "TikTok"],
            brandTone: "energetic and approachable",
            budget: "medium",
          },
        },
      }),
    });
    setCampaign(await res.json());
  };

  return (
    <div>
      <button onClick={generate}>Generate Campaign</button>
      {campaign && <pre>{JSON.stringify(campaign.cards, null, 2)}</pre>}
    </div>
  );
}
```

---

## Error Handling

| HTTP Status | Meaning |
|---|---|
| 200 | Success — full campaign response |
| 400 | Invalid request payload — check the request format |
| 500 | Server error — check logs for details |
| 504 | Timeout — the workflow took too long; retry |

All error responses include the same JSON structure as a success response (with empty objects), so the UI never receives unexpected non-JSON output.

---

## Health Check

```bash
curl http://localhost:5000/health
# {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

---

## Running Tests

```bash
cd src
pip install -r backend/requirements-dev.txt
pytest tests/ -v
```
