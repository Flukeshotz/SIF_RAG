import re
import json
import os
import urllib.parse
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

SEED_URLS = [
    "https://groww.in/mutual-funds/magnum-hybrid-long-short-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/sapphire-equity-long-short-sif-direct-growth",
    "https://groww.in/mutual-funds/isif-hybrid-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/altiva-hybrid-long-short-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/qsif-equity-long-short-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/isif-equity-ex-top-100-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/titanium-hybrid-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/dynasif-equity-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/diviniti-equity-long-short-fund-direct-growth",
    "https://groww.in/mutual-funds/wsif-equity-long-short-fund-direct-growth"
]

def map_strategy(fund_name: str) -> str:
    name_lower = fund_name.lower()
    
    # Priority mapping
    if "ex top 100" in name_lower:
        return "Equity Ex Top 100 Long Short"
    if "hybrid" in name_lower:
        return "Hybrid Long Short"
    if "equity" in name_lower:
        return "Equity Long Short"
    if "sector rotation" in name_lower:
        return "Sector Rotation Long Short"
    if "debt" in name_lower:
        return "Debt Long Short"
    if "asset allocator" in name_lower:
        return "Active Asset Allocator"
        
    return "Unknown Strategy"

def extract_amc(fund_name: str) -> str:
    # First word usually indicates AMC for SIFs
    parts = fund_name.split()
    if len(parts) > 0:
        # Some custom mapping for known ones in the seeds
        first = parts[0].lower()
        if first == "magnum": return "SBI"
        if first == "sapphire": return "Sapphire"
        if first == "isif": return "ICICI"
        if first == "altiva": return "Altiva"
        if first == "qsif": return "Quant"
        if first == "titanium": return "Tata"
        if first == "dynasif": return "DSP"
        if first == "diviniti": return "Diviniti"
        if first == "wsif": return "WhiteOak"
        
        return parts[0]
    return "Unknown AMC"

def extract_metadata_from_url(url: str) -> dict:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    slug = path.strip("/").split("/")[-1]
    
    # Clean slug to fund name
    # e.g. "magnum-hybrid-long-short-fund-direct-plan-growth"
    raw_name = slug.replace("-direct-plan-growth", "").replace("-direct-growth", "").replace("-", " ")
    fund_name = raw_name.title().replace("Isif", "iSIF").replace("Qsif", "qSIF").replace("Sif", "SIF")
    
    strategy = map_strategy(fund_name)
    amc = extract_amc(fund_name)
    
    return {
        "fund_name": fund_name,
        "amc": amc,
        "strategy": strategy,
        "category": "Alternative Investment Fund",
        "url": url,
        "source": "Groww",
        "status": "Active",
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

def discover_funds() -> list:
    """
    Simulates scraping Groww by iterating over seed URLs and search patterns.
    """
    discovered_funds = []
    logger.info(f"Starting discovery on {len(SEED_URLS)} seed URLs...")
    for url in SEED_URLS:
        try:
            metadata = extract_metadata_from_url(url)
            discovered_funds.append(metadata)
        except Exception as e:
            logger.error(f"Error parsing URL {url}: {e}")
            
    return discovered_funds
