import os
import json
import logging
from registry.discovery import discover_funds
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGISTRY_PATH = "data/fund_registry.json"
REPORT_PATH = "docs/registry_refresh_report.md"

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_registry(data):
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def generate_report(new_funds, all_funds):
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    
    amc_counts = {}
    strategy_counts = {}
    missing_metadata = 0
    
    for f in all_funds:
        amc = f.get("amc", "Unknown")
        strat = f.get("strategy", "Unknown")
        amc_counts[amc] = amc_counts.get(amc, 0) + 1
        strategy_counts[strat] = strategy_counts.get(strat, 0) + 1
        
        if not f.get("amc") or f.get("amc") == "Unknown AMC" or not f.get("strategy") or f.get("strategy") == "Unknown Strategy":
            missing_metadata += 1
            
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Registry Refresh Report\n\n")
        f.write(f"**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Overview\n")
        f.write(f"- **Total Funds in Registry:** {len(all_funds)}\n")
        f.write(f"- **New Funds Discovered Today:** {len(new_funds)}\n")
        f.write(f"- **Funds Missing Metadata:** {missing_metadata}\n\n")
        
        f.write("## New Funds Added\n")
        if new_funds:
            for nf in new_funds:
                f.write(f"- {nf['fund_name']} ({nf['amc']} - {nf['strategy']})\n")
        else:
            f.write("No new funds discovered.\n")
            
        f.write("\n## Funds by AMC\n")
        for amc, count in sorted(amc_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{amc}**: {count}\n")
            
        f.write("\n## Funds by Strategy\n")
        for strat, count in sorted(strategy_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{strat}**: {count}\n")

def run_refresh():
    logger.info("Starting Registry Refresh Job...")
    
    # Normally discovery would happen here and merge into sif_registry
    # For Phase 8.5/7.6, we are simulating this.
    
    # Save a daily snapshot of the registry
    registry_path = "data/sif_registry.json"
    if os.path.exists(registry_path):
        today_str = datetime.now().strftime('%Y-%m-%d')
        snapshot_dir = "data/snapshots"
        os.makedirs(snapshot_dir, exist_ok=True)
        snapshot_path = os.path.join(snapshot_dir, f"{today_str}-registry.json")
        
        with open(registry_path, "r", encoding="utf-8") as src:
            data = json.load(src)
            with open(snapshot_path, "w", encoding="utf-8") as dst:
                json.dump(data, dst, indent=2)
                
        logger.info(f"Daily snapshot saved to {snapshot_path}")
    
    logger.info("Registry Refresh complete.")

if __name__ == "__main__":
    run_refresh()
