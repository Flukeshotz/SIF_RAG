import logging
import json
from typing import Dict, Any, Tuple
from generation.llm import get_groq_client

logger = logging.getLogger(__name__)

INTENT_SYSTEM_PROMPT = """You are an Intent Classifier for the SIF Copilot.
Classify the user's query into exactly ONE of these categories:
1. MARKET_INVENTORY (Questions about what funds exist, listing funds, counting funds, AMCs, or filtering by live/nfo status)
2. MARKET_COMPARISON (Questions explicitly asking to compare two or more specific funds)
3. REGULATORY (Questions about SEBI rules, limits, definitions, and frameworks)
4. PRODUCT_DETAIL (Questions asking to explain a specific fund's strategy, documents, or details)
5. ADVISORY (Questions asking for recommendations, advice, or predictions)

Also extract any entities like 'amc' (e.g. Quant, Tata, ICICI), 'strategy' (e.g. Hybrid Long Short), or 'status' (e.g. Live, NFO).

Return your response strictly as JSON:
{
    "intent": "CATEGORY_NAME",
    "entities": {
        "amc": "value or null",
        "strategy": "value or null",
        "status": "value or null"
    }
}
"""

def route_query(query: str) -> Tuple[str, Dict[str, Any]]:
    """
    Classifies a query using deterministic heuristics first, falling back to Groq Intent Classification.
    """
    lower_q = query.lower()
    
    # 1. Deterministic Heuristics (Bypass LLM)
    discovery_exact_matches = [
        "what sifs exist", "show all sifs", "list all sifs", "how many sifs", 
        "which sifs", "show funds", "all sifs"
    ]
    is_deterministic_discovery = any(m in lower_q for m in discovery_exact_matches) or lower_q.startswith("show all")
    
    if is_deterministic_discovery:
        params = {}
        if "quant" in lower_q: params["filter_amc"] = "Quant"
        if "tata" in lower_q: params["filter_amc"] = "Tata"
        if "icici" in lower_q: params["filter_amc"] = "ICICI"
        if "hybrid" in lower_q: params["filter_strategy"] = "Hybrid Long-Short"
        if "equity" in lower_q and "ex" not in lower_q: params["filter_strategy"] = "Equity Long-Short"
        if "ex-top 100" in lower_q or "ex top 100" in lower_q: params["filter_strategy"] = "Equity Ex-Top 100 Long-Short"
        if "live" in lower_q: params["filter_status"] = "Live"
        if "nfo" in lower_q: params["filter_status"] = "NFO"
        return "discovery", params
        
    if "compare" in lower_q or "vs" in lower_q:
        funds_to_compare = []
        if "quant" in lower_q: funds_to_compare.append("Quant")
        if "tata" in lower_q: funds_to_compare.append("Tata")
        if "icici" in lower_q: funds_to_compare.append("ICICI")
        if "hybrid" in lower_q: funds_to_compare.append("Hybrid Long-Short")
        if "equity" in lower_q: funds_to_compare.append("Equity Long-Short")
        if funds_to_compare:
            return "comparison", {"funds": funds_to_compare}

    # 2. LLM Fallback (if deterministic fails)
    client = get_groq_client()
    if not client:
        return "rag", {}

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": INTENT_SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            temperature=0.0,
            max_tokens=100,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        intent = result.get("intent", "REGULATORY")
        entities = result.get("entities", {})
        
        params = {}
        if entities.get("amc"): params["filter_amc"] = entities["amc"]
        if entities.get("strategy"): params["filter_strategy"] = entities["strategy"]
        if entities.get("status"): params["filter_status"] = entities["status"]
        
        if intent == "MARKET_INVENTORY":
            return "discovery", params
        elif intent == "MARKET_COMPARISON":
            return "comparison", params
        elif intent == "PRODUCT_DETAIL" or intent == "REGULATORY":
            return "rag", params
        elif intent == "ADVISORY":
            return "rag", params
        else:
            return "rag", params
            
    except Exception as e:
        logger.error(f"Intent classification failed: {e}")
        return "rag", {}
