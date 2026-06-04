import json
import os
import re

URLS = [
    "https://groww.in/mutual-funds/apex-hybrid-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/isif-equity-ex-top-100-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/isif-hybrid-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/dynasif-active-asset-allocator-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/qsif-hybrid-long-short-fund-direct-plan-growth",
    "https://groww.in/nfo/sapphire-equity-long-short-sif-direct-growth",
    "https://groww.in/mutual-funds/sapphire-equity-long-short-sif-direct-growth",
    "https://groww.in/nfo/qsif-sector-rotation-long-short-fund-direct-growth",
    "https://groww.in/nfo/qsif-active-asset-allocator-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/arudha-hybrid-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/arudha-equity-long-short-fund-direct-growth",
    "https://groww.in/nfo/qsif-equity-ex-top-100-long-short-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/qsif-equity-long-short-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/altiva-equity-ex-top-100-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/titanium-hybrid-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/altiva-hybrid-long-short-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/diviniti-equity-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/magnum-hybrid-long-short-fund-direct-plan-growth",
    "https://groww.in/nfo/wsif-equity-ex-top-100-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/wsif-equity-long-short-fund-direct-growth",
    "https://www.indmoney.com/mutual-funds/sapphire-equity-long-short-sif-direct-growth-1057488",
    "https://www.indmoney.com/mutual-funds/qsif-hybrid-long-short-fund-direct-growth-1053528",
    "https://www.indmoney.com/mutual-funds/isif-equity-ex-top-100-long-short-fund-direct-growth-1055408",
    "https://www.indmoney.com/mutual-funds/isif-hybrid-long-short-fund-direct-growth-1055406",
    "https://www.indmoney.com/mutual-funds/dynasif-equity-long-short-fund-direct-growth-1056036",
    "https://www.indmoney.com/mutual-funds/qsif-equity-long-short-fund-direct-growth-1053199",
    "https://www.indmoney.com/mutual-funds/altiva-equity-ex-top-100-long-short-fund-direct-growth-1058342",
    "https://www.indmoney.com/mutual-funds/arudha-hybrid-long-short-fund-direct-plan-growth-1055069",
    "https://www.indmoney.com/mutual-funds/diviniti-equity-long-short-fund-direct-growth-1054135",
    "https://www.indmoney.com/mutual-funds/titanium-equity-long-short-fund-direct-growth-1057785",
    "https://www.indmoney.com/mutual-funds/titanium-hybrid-long-short-fund-direct-growth-1054190",
    "https://www.sbimf.com/magnumsif",
    "https://www.edelweissmf.com/altivasif",
    "https://www.360.one/dyna-sif",
    "https://apexsif.adityabirlacapital.com/strategies/apex-hybrid-long-short-fund",
    "https://www.qsif.com/",
    "https://arudhasif.com/",
    "https://www.franklintempletonindia.com/sapphiresif",
    "https://www.isif.icicipruamc.com/",
    "https://sif.itiamc.com/",
    "https://www.tatamutualfund.com/titanium-sif",
    "https://www.wealthcompanyamc.in/wsif/funds/wsif-equity-long-short-fund/"
]

def map_strategy(fund_name: str) -> str:
    name_lower = fund_name.lower()
    if "ex-top 100" in name_lower or "ex top 100" in name_lower:
        return "Equity Ex-Top 100 Long-Short"
    if "hybrid" in name_lower:
        return "Hybrid Long-Short"
    if "equity" in name_lower:
        return "Equity Long-Short"
    if "sector rotation" in name_lower:
        return "Sector Rotation Long-Short"
    if "debt" in name_lower:
        return "Debt Long-Short"
    if "asset allocator" in name_lower:
        return "Active Asset Allocator"
    return "Unknown Strategy"

def extract_amc_brand(fund_name: str) -> tuple:
    name_lower = fund_name.lower()
    if "magnum" in name_lower: return ("SBI Mutual Fund", "Magnum")
    if "altiva" in name_lower: return ("Edelweiss Mutual Fund", "Altiva")
    if "dynasif" in name_lower: return ("360 ONE Mutual Fund", "DynaSIF")
    if "apex" in name_lower: return ("Aditya Birla Sun Life", "Apex")
    if "qsif" in name_lower: return ("quant Mutual Fund", "qSIF")
    if "arudha" in name_lower: return ("Bandhan Mutual Fund", "Arudha")
    if "sapphire" in name_lower: return ("Franklin Templeton", "Sapphire")
    if "isif" in name_lower: return ("ICICI Prudential", "iSIF")
    if "diviniti" in name_lower: return ("ITI Mutual Fund", "Diviniti")
    if "titanium" in name_lower: return ("Tata Mutual Fund", "Titanium")
    if "wsif" in name_lower: return ("The Wealth Company", "WSIF")
    return ("Unknown AMC", "Unknown Brand")

def clean_name(slug: str) -> str:
    raw = slug.split("-direct")[0]
    raw = raw.replace("-", " ")
    return raw.title().replace("Sif", "SIF").replace("Qsif", "qSIF").replace("Isif", "iSIF").replace("Dynasif", "DynaSIF").replace("Wsif", "WSIF").replace("Ex Top", "Ex-Top")

def build_registry():
    funds = {}
    
    for url in URLS:
        # Extract slug
        if "groww.in" in url or "indmoney.com" in url:
            parts = url.strip("/").split("/")
            slug = parts[-1]
            if "indmoney" in url:
                # Remove numeric suffix like -1057488
                slug = re.sub(r'-\d+$', '', slug)
            
            fund_name = clean_name(slug)
            if "Nfo" in url.title() or "/nfo/" in url:
                status = "NFO"
            else:
                status = "Live"
        else:
            # Official domains
            if "sbimf" in url: fund_name = "Magnum Hybrid Long-Short Fund"
            elif "edelweissmf" in url: fund_name = "Altiva Equity Ex-Top 100 Long-Short Fund"
            elif "360.one" in url: fund_name = "DynaSIF Equity Long-Short Fund"
            elif "adityabirlacapital" in url: fund_name = "Apex Hybrid Long-Short Fund"
            elif "qsif" in url: fund_name = "qSIF Equity Long-Short Fund"
            elif "arudhasif" in url: fund_name = "Arudha Hybrid Long-Short Fund"
            elif "franklintempletonindia" in url: fund_name = "Sapphire Equity Long-Short SIF"
            elif "isif" in url: fund_name = "iSIF Hybrid Long-Short Fund"
            elif "itiamc" in url: fund_name = "Diviniti Equity Long-Short Fund"
            elif "tatamutualfund" in url: fund_name = "Titanium Hybrid Long-Short Fund"
            elif "wealthcompany" in url: fund_name = "WSIF Equity Long-Short Fund"
            else: fund_name = "Unknown"
            status = "Live"
            
        if fund_name not in funds:
            amc, brand = extract_amc_brand(fund_name)
            funds[fund_name] = {
                "fund_id": fund_name.lower().replace(" ", "-").replace(".", ""),
                "fund_name": fund_name,
                "amc": amc,
                "brand": brand,
                "strategy": map_strategy(fund_name),
                "status": status,
                "launch_date": "2024-01-01", # Placeholder
                "aum_cr": None,
                "risk_band": 5, # Placeholder
                "minimum_investment": 10000000,
                "expense_ratio": None,
                "groww_url": "",
                "indmoney_url": "",
                "official_url": "",
                "documents": [],
                "last_updated": "2026-06-05T00:00:00Z"
            }
            
        # Update URLs
        if "groww.in" in url:
            funds[fund_name]["groww_url"] = url
            if "/nfo/" in url:
                funds[fund_name]["status"] = "NFO"
        elif "indmoney.com" in url:
            funds[fund_name]["indmoney_url"] = url
        else:
            funds[fund_name]["official_url"] = url

    # Write to file
    os.makedirs("data", exist_ok=True)
    with open("data/sif_registry.json", "w", encoding="utf-8") as f:
        json.dump(list(funds.values()), f, indent=2)
        
if __name__ == "__main__":
    build_registry()
