import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def extract_fund_metadata(content: bytes, source_id: str, is_pdf: bool) -> Dict[str, Any]:
    """
    Extracts structured fund metadata from the raw content.
    For this MVP, we use regex heuristics on text content.
    If LLM API is available, an LLM extraction could be used instead.
    """
    metadata = {
        "fund_name": "Unknown Fund",
        "amc": "Unknown AMC",
        "strategy_type": "Unknown Strategy",
        "risk_band": 0,
        "benchmark": "Unknown Benchmark",
        "minimum_investment": "₹1 Crore",
        "category": "Alternative Investment Fund",
        "document_sources": [source_id]
    }
    
    # Try parsing text if we can decode it (in MVP, PDFs might be already text or handled outside)
    try:
        text = content.decode("utf-8", errors="ignore").lower()
    except Exception:
        text = ""

    # Heuristic extraction
    if "quant" in source_id.lower() or "quant" in text:
        metadata["amc"] = "Quant"
        metadata["fund_name"] = "Quant Long-Short SIF"
        metadata["strategy_type"] = "Long-Short"
        metadata["risk_band"] = 5
        metadata["benchmark"] = "NIFTY 500"
    
    elif "tata" in source_id.lower() or "tata" in text:
        metadata["amc"] = "Tata"
        metadata["fund_name"] = "Tata Innovation Theme SIF"
        metadata["strategy_type"] = "Innovation Theme"
        metadata["risk_band"] = 6
        metadata["benchmark"] = "NIFTY IT"
        
    elif "icici" in source_id.lower() or "icici" in text:
        metadata["amc"] = "ICICI Prudential"
        metadata["fund_name"] = "ICICI Prudential Equity-Oriented SIF"
        metadata["strategy_type"] = "Equity-Oriented"
        metadata["risk_band"] = 4
        metadata["benchmark"] = "NIFTY 100"

    # Regex extraction fallback
    risk_match = re.search(r'risk band[:\s]+(\d)', text, re.IGNORECASE)
    if risk_match:
        metadata["risk_band"] = int(risk_match.group(1))
        
    return metadata

def merge_into_registry(new_metadata: Dict[str, Any], registry_path: str = "data/fund_registry.json") -> None:
    import json
    import os
    
    data = []
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
                
    # Update if exists
    updated = False
    for i, fund in enumerate(data):
        if fund.get("fund_name") == new_metadata["fund_name"]:
            # Merge sources
            sources = set(fund.get("document_sources", []))
            sources.update(new_metadata["document_sources"])
            new_metadata["document_sources"] = list(sources)
            data[i] = new_metadata
            updated = True
            break
            
    if not updated and new_metadata["fund_name"] != "Unknown Fund":
        data.append(new_metadata)
        
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
