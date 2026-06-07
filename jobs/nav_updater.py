import json
import os
import random
from datetime import datetime

REGISTRY_FILE = "data/sif_registry.json"
NAV_FILE = "data/nav_data.json"

def update_navs():
    """Generates or updates NAV data for all funds in the registry."""
    os.makedirs("data", exist_ok=True)
    
    # Load registry
    if not os.path.exists(REGISTRY_FILE):
        print(f"Registry not found at {REGISTRY_FILE}, skipping NAV update.")
        return
        
    try:
        with open(REGISTRY_FILE, "r") as f:
            funds = json.load(f)
    except Exception as e:
        print(f"Error reading registry: {e}")
        return
        
    # Load existing nav data if present
    nav_data = []
    if os.path.exists(NAV_FILE):
        try:
            with open(NAV_FILE, "r") as f:
                nav_data = json.load(f)
        except Exception:
            nav_data = []
            
    nav_dict = {item["fund_id"]: item for item in nav_data}
    updated_navs = []
    
    for fund in funds:
        fund_id = fund.get("fund_id")
        brand = fund.get("brand", "SIF")
        if fund_id in nav_dict:
            # Random walk
            current = nav_dict[fund_id]
            nav = current["nav"]
            change = random.uniform(-0.015, 0.015)  # -1.5% to +1.5% step
            new_nav = round(nav * (1 + change), 2)
            
            # Simple dampening to avoid runaway prices
            if new_nav > 300: new_nav = 300
            if new_nav < 5: new_nav = 5
            
            # Daily change calc (from today's open, but we just simulate a smooth wandering change)
            current_pct = current.get("change_percent", 0)
            # Drift towards 0 slowly
            drift = -current_pct * 0.1
            pct_change = round(current_pct + (change * 100) + drift, 2)
            pct_change = max(-4.9, min(4.9, pct_change))
            
            updated_navs.append({
                "fund_id": fund_id,
                "ticker": f"{brand.upper()} SIF" if brand else "SIF",
                "nav": new_nav,
                "change_percent": pct_change,
                "last_updated": datetime.utcnow().isoformat()
            })
        else:
            # Generate initial
            initial_nav = round(random.uniform(15.0, 150.0), 2)
            initial_change = round(random.uniform(-2.0, 2.0), 2)
            updated_navs.append({
                "fund_id": fund_id,
                "ticker": f"{brand.upper()} SIF" if brand else "SIF",
                "nav": initial_nav,
                "change_percent": initial_change,
                "last_updated": datetime.utcnow().isoformat()
            })
            
    # Save
    with open(NAV_FILE, "w") as f:
        json.dump(updated_navs, f, indent=2)
    print(f"Updated NAVs for {len(updated_navs)} funds.")
