import json
import os
from typing import List, Dict, Any

REGISTRY_PATH = "data/sif_registry.json"

def _load_registry() -> List[Dict[str, Any]]:
    if not os.path.exists(REGISTRY_PATH):
        return []
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def get_all_funds() -> List[Dict[str, Any]]:
    """Return all funds in the registry."""
    return _load_registry()

def get_funds_by_amc(amc: str) -> List[Dict[str, Any]]:
    """Return funds matching the given AMC string (case-insensitive substring match)."""
    funds = _load_registry()
    amc_lower = amc.lower()
    return [f for f in funds if amc_lower in f.get("amc", "").lower() or amc_lower in f.get("brand", "").lower()]

def get_funds_by_strategy(strategy: str) -> List[Dict[str, Any]]:
    """Return funds matching the given strategy."""
    funds = _load_registry()
    strat_lower = strategy.lower()
    return [f for f in funds if strat_lower in f.get("strategy", "").lower()]

def get_live_funds() -> List[Dict[str, Any]]:
    """Return only active/live funds."""
    funds = _load_registry()
    return [f for f in funds if f.get("status", "").lower() == "live"]

def get_nfo_funds() -> List[Dict[str, Any]]:
    """Return only funds in NFO status."""
    funds = _load_registry()
    return [f for f in funds if f.get("status", "").lower() == "nfo"]

def search_funds(query: str) -> List[Dict[str, Any]]:
    """Search funds by name, AMC, brand, or strategy."""
    funds = _load_registry()
    q_lower = query.lower()
    results = []
    for f in funds:
        if (q_lower in f.get("fund_name", "").lower() or 
            q_lower in f.get("amc", "").lower() or 
            q_lower in f.get("brand", "").lower() or 
            q_lower in f.get("strategy", "").lower()):
            results.append(f)
    return results

def compare_funds(fund_names: List[str]) -> List[Dict[str, Any]]:
    """Return specific funds by name or AMC for comparison."""
    funds = _load_registry()
    matched = []
    
    # Check if a strategy was passed instead of specific funds
    # e.g., ["Hybrid Long-Short"]
    if len(fund_names) == 1 and ("long-short" in fund_names[0].lower() or "allocator" in fund_names[0].lower()):
        return compare_funds_by_strategy(fund_names[0])
        
    for f in funds:
        for name in fund_names:
            if name.lower() in f.get("fund_name", "").lower() or name.lower() in f.get("amc", "").lower():
                if f not in matched:
                    matched.append(f)
    return matched

def compare_funds_by_strategy(strategy: str) -> List[Dict[str, Any]]:
    """Return all funds within a specific strategy for comparison."""
    funds = _load_registry()
    strat_lower = strategy.lower()
    return [f for f in funds if strat_lower in f.get("strategy", "").lower()]
