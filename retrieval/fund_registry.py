import json
import os
from typing import List, Dict, Any, Optional

REGISTRY_PATH = os.path.join("data", "fund_registry.json")

def load_registry() -> List[Dict[str, Any]]:
    if not os.path.exists(REGISTRY_PATH):
        return []
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_registry(data: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_all_funds() -> List[Dict[str, Any]]:
    return load_registry()

def sort_funds(funds: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """Sort funds by a specific key. e.g. 'risk_band'"""
    def _safe_key(f):
        val = f.get(key, 0)
        # Handle string numbers
        if isinstance(val, str) and val.isdigit():
            return int(val)
        return val if val is not None else 0
        
    return sorted(funds, key=_safe_key, reverse=reverse)

def compare_funds(fund_names: List[str]) -> List[Dict[str, Any]]:
    """Return specific funds by name for comparison."""
    funds = load_registry()
    matched = []
    for f in funds:
        for name in fund_names:
            if name.lower() in f.get("fund_name", "").lower() or name.lower() in f.get("amc", "").lower():
                if f not in matched:
                    matched.append(f)
    return matched

def filter_funds_by_strategy(strategy: str) -> List[Dict[str, Any]]:
    funds = load_registry()
    return [f for f in funds if strategy.lower() in f.get("strategy_type", "").lower()]
