import os
import json
import logging
import time
from typing import Dict, Any, Tuple, List
from pathlib import Path

logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# Intent pattern sets (case‑insensitive)
# ------------------------------------------------------------
INVENTORY_ACTIONS = {"show", "list", "display", "give", "how many"}
INVENTORY_OBJECTS = {"sif", "sifs", "fund", "funds", "strategy", "strategies", "amc", "amcs"}
COMPARISON_ACTIONS = {"compare", "vs", "versus", "difference", "different", "better"}
ADVISORY_PHRASES = {"should i", "recommend", "advice", "what should i do", "which fund should i pick", "can you advise"}
MARKET_DISCOVERY_TRIGGERS = {"newest", "latest", "recent", "popular", "entered", "launched"}

# ------------------------------------------------------------
# Dynamic entity dictionaries – loaded once at import time
# ------------------------------------------------------------
REGISTRY_PATH = Path(__file__).resolve().parents[1] / "data" / "sif_registry.json"
KNOWN_AMCS: set = set()
KNOWN_FUNDS: set = set()
KNOWN_STRATEGIES: set = set()

AMC_ALIASES = {
    "quant": "quant mutual fund",
    "tata": "tata mutual fund",
    "icici": "icici prudential",
    "edelweiss": "edelweiss mutual fund",
    "sbi": "sbi mutual fund",
    "franklin": "franklin templeton",
    "360 one": "360 one mutual fund",
    "bandhan": "bandhan mutual fund",
    "iti": "iti mutual fund",
    "aditya birla": "aditya birla sun life",
    "absl": "aditya birla sun life",
    "wealth company": "the wealth company"
}

def _load_registry() -> None:
    if not REGISTRY_PATH.is_file():
        logger.warning(f"Registry file not found at {REGISTRY_PATH}, entity extraction will be limited.")
        return
    try:
        with REGISTRY_PATH.open() as f:
            data = json.load(f)
        # Expected structure: List of dicts with 'amc', 'fund_name', 'strategy'
        for item in data:
            if "amc" in item and item["amc"]:
                KNOWN_AMCS.add(item["amc"].lower())
            if "fund_name" in item and item["fund_name"]:
                KNOWN_FUNDS.add(item["fund_name"].lower())
            if "strategy" in item and item["strategy"]:
                KNOWN_STRATEGIES.add(item["strategy"].lower())
    except Exception as e:
        logger.error(f"Failed to load SIF registry for entity extraction: {e}")

_load_registry()

# ------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------
def _tokenise(text: str) -> List[str]:
    return [t.strip() for t in text.lower().split() if t.strip()]

def _match_pattern(tokens: List[str], actions: set, objects: set) -> bool:
    # Look for any action token followed later by any object token (allow "all" in between)
    for i, tok in enumerate(tokens):
        if tok in actions:
            # Scan remaining tokens for an object
            for later in tokens[i+1:]:
                if later in objects:
                    return True
                if later == "all":
                    continue
    return False

def extract_entities(query: str) -> Dict[str, List[str]]:
    """Simple entity extraction based on the dynamically loaded registry sets.
    Returns a dict with possible keys: 'amc', 'fund', 'strategy', each containing a list of matches.
    """
    result = {"amc": [], "fund": [], "strategy": []}
    lowered = query.lower()
    
    # 1. Alias matching for AMCs
    tokens = _tokenise(query)
    for alias, canonical in AMC_ALIASES.items():
        if len(alias.split()) == 1:
            if alias in tokens:
                result["amc"].append(canonical)
        else:
            if alias in lowered:
                result["amc"].append(canonical)
                
    # Substring matching for multi-word entities (like "tata mutual fund")
    for amc in KNOWN_AMCS:
        # Avoid matching common words like "the" or "fund" on their own
        if amc in lowered and amc not in ("fund", "the", "mutual fund"):
            result["amc"].append(amc)
            
    for fund in KNOWN_FUNDS:
        if fund in lowered:
            result["fund"].append(fund)
            
    for strategy in KNOWN_STRATEGIES:
        if strategy in lowered:
            result["strategy"].append(strategy)
            
    # Remove duplicates and clean up empty lists
    final_result = {}
    for k, v in result.items():
        if v:
            # Sort by length descending to match longest possible entity first (optional)
            final_result[k] = list(set(v))
            
    return final_result

# CSV logging – ensure directory exists
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "routing_audit.csv"
if not LOG_FILE.is_file():
    LOG_FILE.write_text("query,matched_rule,confidence,route,groq_called\n")

def log_decision(query: str, matched_rule: str, confidence: float, route: str, groq_called: bool) -> None:
    line = f"\"{query}\",{matched_rule},{confidence:.3f},{route},{groq_called}\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

# ------------------------------------------------------------
# Core routing function
# ------------------------------------------------------------
def route_query(query: str) -> Tuple[str, Dict[str, Any]]:
    """Routes a user query to one of the categories:
    inventory, comparison, advisory, market_discovery, or rag (fallback).
    Returns a tuple (route, params) where params may contain extracted entities.
    """
    start_time = time.perf_counter()
    tokens = _tokenise(query)
    lowered = query.lower()

    # 1. Inventory detection (deterministic, highest priority)
    if _match_pattern(tokens, INVENTORY_ACTIONS, INVENTORY_OBJECTS):
        # Avoid false positives where a comparison action appears earlier – inventory wins per rule A.
        confidence = 1.0
        params = extract_entities(query)
        log_decision(query, "inventory", confidence, "inventory", False)
        return "inventory", params

    # 2. Comparison detection
    if any(tok in COMPARISON_ACTIONS for tok in tokens):
        entities = extract_entities(query)
        amcs = entities.get("amc", [])
        
        # New Rule: If comparing exactly 2 AMCs, route to amc_comparison to bypass RAG
        if len(amcs) == 2:
            confidence = 1.0
            log_decision(query, "amc_comparison", confidence, "amc_comparison", False)
            return "amc_comparison", {"amcs": amcs}
            
        # Simple heuristic: need at least two recognizable entities (amc/fund/strategy)
        total_extracted = sum(len(v) for v in entities.values())
        if total_extracted >= 2:
            confidence = 1.0
            log_decision(query, "comparison", confidence, "comparison", False)
            return "comparison", entities
        # Fallback to advisory if not enough entities
        if any(phrase in lowered for phrase in ADVISORY_PHRASES):
            confidence = 1.0
            log_decision(query, "advisory", confidence, "advisory", False)
            return "advisory", {}

    # 3. Advisory detection (stand‑alone phrases)
    if any(phrase in lowered for phrase in ADVISORY_PHRASES):
        confidence = 1.0
        log_decision(query, "advisory", confidence, "advisory", False)
        return "advisory", {}

    # 4. Market discovery detection
    if any(tok in MARKET_DISCOVERY_TRIGGERS for tok in tokens):
        confidence = 1.0
        params = extract_entities(query)
        log_decision(query, "market_discovery", confidence, "market_discovery", False)
        return "market_discovery", params

    # 5. LLM fallback – may invoke Groq
    from generation.llm import get_groq_client
    client = get_groq_client()
    if not client:
        # No Groq available – treat as rag with empty params
        log_decision(query, "llm_fallback", 0.0, "rag", False)
        return "rag", {}
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Classify the user query into one of the predefined categories and extract entities if possible. Output as a JSON object."},
                {"role": "user", "content": query}
            ],
            temperature=0.0,
            max_tokens=100,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        intent = result.get("intent", "rag").lower()
        entities = result.get("entities", {})
        confidence = result.get("confidence", 0.5) if isinstance(result.get("confidence"), (int, float)) else 0.5
        log_decision(query, "llm_fallback", confidence, intent, True)
        # Map intents to our internal route names
        intent_map = {
            "market_inventory": "inventory",
            "market_comparison": "comparison",
            "advisory": "advisory",
            "market_discovery": "market_discovery",
            "regulatory": "rag",
            "product_detail": "rag",
            "risk": "rag"
        }
        route = intent_map.get(intent, "rag")
        return route, entities
    except Exception as e:
        logger.error(f"LLM routing failed: {e}")
        log_decision(query, "llm_error", 0.0, "rag", True)
        return "rag", {}

def print_decision_tree() -> str:
    """Returns a human‑readable representation of the routing decision order."""
    tree = (
        "Routing Decision Tree\n"
        "├─ Inventory (deterministic) → inventory\n"
        "├─ Comparison (deterministic) → comparison\n"
        "├─ Advisory (deterministic) → advisory\n"
        "├─ Market Discovery (deterministic) → market_discovery\n"
        "└─ LLM fallback (Groq) → rag / regulatory / product / risk"
    )
    return tree
