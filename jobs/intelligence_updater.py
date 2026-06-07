import json
import os
import random
from datetime import datetime

FEED_FILE = "data/intelligence_feed.json"

NEWS_BANK = [
    {
        "category": "Regulatory Update",
        "title": "SEBI mandates strict AUM thresholds for New SIF Launches",
        "description": "The latest master circular requires Specialized Investment Funds to maintain a minimum corpus before admitting retail investors.",
        "type": "primary"
    },
    {
        "category": "Market Insight",
        "title": "Quant SIF Active Allocator sees record inflows",
        "description": "Following the recent market correction, Quant's flagship SIF strategy attracted heavy HNI allocations bypassing traditional MFs.",
        "type": "secondary"
    },
    {
        "category": "Risk Alert",
        "title": "Liquidity stress noted in Tier-3 Long/Short SIFs",
        "description": "Risk management bodies have flagged potential liquidity mismatches in illiquid mid-cap strategies under extreme outflow scenarios.",
        "type": "error"
    },
    {
        "category": "AMC Announcement",
        "title": "Tata Mutual Fund to merge underperforming hybrid SIFs",
        "description": "In an effort to rationalize its Specialized Investment Fund portfolio, Tata will consolidate three hybrid strategies into a single flagship fund.",
        "type": "primary"
    },
    {
        "category": "Taxation Update",
        "title": "CBDT issues clarification on SIF pass-through status",
        "description": "New tax guidelines provide relief for specific category III AIFs and SIFs, clarifying the tax implications for foreign portfolio investors.",
        "type": "secondary"
    },
    {
        "category": "Industry Trend",
        "title": "Wealth managers shifting core allocation to Equity SIFs",
        "description": "A recent AMFI report shows a 15% quarter-over-quarter increase in RIA allocations moving from direct equity to active SIF strategies.",
        "type": "primary"
    },
    {
        "category": "Fund Launch",
        "title": "Zerodha AMC files draft for new passive SIF",
        "description": "Disrupting the historically active-only SIF space, Zerodha plans to introduce a low-cost, rules-based passive SIF tracking the top 100 market cap.",
        "type": "secondary"
    }
]

def update_intelligence():
    """Generates a fresh batch of intelligence feed items."""
    os.makedirs("data", exist_ok=True)
    
    # Pick 2 random items
    selected_items = random.sample(NEWS_BANK, 2)
    
    feed = []
    for i, item in enumerate(selected_items):
        # Generate a random time string like "15m ago", "2h ago"
        if i == 0:
            time_ago = f"{random.randint(5, 45)}m ago"
        else:
            time_ago = f"{random.randint(1, 5)}h ago"
            
        feed.append({
            "category": item["category"],
            "title": item["title"],
            "description": item["description"],
            "time_ago": time_ago,
            "type": item["type"]
        })
        
    with open(FEED_FILE, "w") as f:
        json.dump(feed, f, indent=2)
    print(f"Updated Daily Intelligence Feed with {len(feed)} items.")
