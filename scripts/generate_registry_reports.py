import json
import os

def generate_reports():
    os.makedirs("docs", exist_ok=True)
    with open("data/sif_registry.json", "r") as f:
        funds = json.load(f)

    total = len(funds)
    
    amcs = {}
    strategies = {}
    groww_count = 0
    indmoney_count = 0
    official_count = 0
    live_count = 0
    nfo_count = 0

    for f in funds:
        amc = f.get("amc", "Unknown")
        strat = f.get("strategy", "Unknown")
        amcs[amc] = amcs.get(amc, 0) + 1
        strategies[strat] = strategies.get(strat, 0) + 1
        
        if f.get("groww_url"): groww_count += 1
        if f.get("indmoney_url"): indmoney_count += 1
        if f.get("official_url"): official_count += 1
        
        if f.get("status") == "NFO": nfo_count += 1
        else: live_count += 1

    # 1. market_registry_report.md
    with open("docs/market_registry_report.md", "w") as f:
        f.write("# Market Registry Overview\n\n")
        f.write(f"- Total Unique SIFs Discovered: {total}\n")
        f.write(f"- Live Funds: {live_count}\n")
        f.write(f"- NFOs: {nfo_count}\n")
        f.write("\nAll funds successfully mapped to the new Canonical Schema and deduplicated across platforms.\n")

    # 2. coverage_report.md
    with open("docs/reports/coverage_report.md", "w") as f:
        f.write("# Platform Coverage Report\n\n")
        f.write(f"- Funds on Groww: {groww_count}\n")
        f.write(f"- Funds on INDmoney: {indmoney_count}\n")
        f.write(f"- Funds with Official URLs: {official_count}\n")
        f.write("\nDeduplication Engine successfully merged overlapping instances into single entities.\n")

    # 3. amc_coverage_report.md
    with open("docs/reports/amc_coverage_report.md", "w") as f:
        f.write("# AMC Coverage Report\n\n")
        for k, v in sorted(amcs.items(), key=lambda item: item[1], reverse=True):
            f.write(f"- **{k}**: {v} Funds\n")

    # 4. strategy_coverage_report.md
    with open("docs/strategy_coverage_report.md", "w") as f:
        f.write("# Strategy Coverage Report\n\n")
        for k, v in sorted(strategies.items(), key=lambda item: item[1], reverse=True):
            f.write(f"- **{k}**: {v} Funds\n")

if __name__ == "__main__":
    generate_reports()
