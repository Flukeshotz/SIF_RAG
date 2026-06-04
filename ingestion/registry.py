import json
from pathlib import Path
from typing import List, Dict, Any, Optional

def load_registry(registry_path: str = "data/source_registry_v2.json") -> List[Dict[str, Any]]:
    """Loads and returns the source registry."""
    path = Path(registry_path)
    if not path.exists():
        raise FileNotFoundError(f"Registry not found at {registry_path}")
        
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    return data

def get_active_sources(registry_path: str = "data/source_registry_v2.json") -> List[Dict[str, Any]]:
    """Returns only active sources from the registry."""
    data = load_registry(registry_path)
    return [s for s in data if s.get("status") == "active"]
