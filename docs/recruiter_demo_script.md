# SIF Copilot Demo Script

**1. The Hook (0:00-0:30)**
"SIF is a brand new asset class introduced by SEBI. No standard tracker exists. I built a RAG system and an autonomous web-scraper to build the first comprehensive tracker."

**2. The Architecture (0:30-1:30)**
"Look at the Market Explorer. If I ask 'Show all live funds', it bypasses the LLM completely via heuristic routing, hitting the internal JSON registry in 10ms. This saves massive token costs and guarantees accuracy."

**3. The Intelligence (1:30-2:30)**
"Now watch the Evidence Explorer. If I ask 'Explain exit load constraints', it hits Qdrant, retrieves the exact SEBI PDF chunk, generates the answer with Groq's Llama 3.1, and renders the citation so you can verify the text yourself."
