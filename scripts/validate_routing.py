import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from retrieval.query_router import route_query

def test_queries():
    queries = [
        "What SIFs exist?",
        "Compare iSIF and Titanium",
        "What is the minimum investment for SIFs?",
        "Explain the Hybrid Long-Short strategy",
        "Show live SIFs",
        "Compare Tata vs Quant funds",
    ]
    for q in queries:
        route, params = route_query(q)
        print(f"Query: {q}\nRoute: {route}\nParams: {json.dumps(params)}\n---")

if __name__ == "__main__":
    test_queries()
