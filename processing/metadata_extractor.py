import re
from typing import Dict, Any, List
from processing.document_model import Metadata, Section, Table

# Enums
AMC_ENUM = [
    "SBI Mutual Fund", "Tata Mutual Fund", "Edelweiss Mutual Fund", 
    "ICICI Prudential Mutual Fund", "Quant Mutual Fund", "Franklin Templeton Mutual Fund",
    "Aditya Birla Sun Life Mutual Fund", "HSBC Mutual Fund", "ITI Mutual Fund",
    "360 ONE Mutual Fund", "DSP Mutual Fund", "Kotak Mutual Fund",
    "Mirae Asset Mutual Fund", "Bandhan Mutual Fund", "The Wealth Company Mutual Fund"
]

STRATEGY_ENUM = [
    "Hybrid Long-Short", "Equity Long-Short", "Equity Ex-Top 100 Long-Short",
    "Sector Rotation Long-Short", "Debt Long-Short", "Sectoral Debt Long-Short",
    "Active Asset Allocator"
]

def extract_metadata(text: str, source_metadata: Dict[str, Any], tables: List[Table]) -> Metadata:
    meta = Metadata()
    
    # Pre-fill from source registry
    meta.source_type = source_metadata.get("source_type")
    meta.document_type = meta.source_type
    
    # 1. Fund Name (Very naive regex, often best to just take from title)
    meta.fund_name = source_metadata.get("title", "")
    
    # 2. AMC Name
    for amc in AMC_ENUM:
        if amc.lower() in text.lower() or amc.split(" ")[0].lower() in text.lower():
            meta.amc_name = amc
            break
            
    # 3. Strategy Type & Category
    for strat in STRATEGY_ENUM:
        if strat.lower() in text.lower():
            meta.strategy_type = strat
            meta.category = strat
            break
            
    # 4. Minimum Investment (Look for ₹10 Lakhs or 10,00,000)
    if re.search(r'(₹|Rs\.?)\s*10,?00,?000', text) or re.search(r'10\s*Lakhs?', text, re.IGNORECASE):
        meta.minimum_investment = 1000000
        
    # 5. Risk Band (Look for "Risk-o-meter" context)
    risk_match = re.search(r'(Very High|Moderately High|Moderate|Low to Moderate|Low)\s*risk', text, re.IGNORECASE)
    if risk_match:
        val = risk_match.group(1).lower()
        mapping = {"low": 1, "low to moderate": 2, "moderate": 3, "moderately high": 4, "very high": 5}
        meta.risk_band = mapping.get(val)
        
    # 6. Fund Manager
    fm_match = re.search(r'Fund Manager[s]?\s*[:\-]?\s*([A-Za-z\s]+)(?:\n|$)', text, re.IGNORECASE)
    if fm_match:
        meta.fund_manager = fm_match.group(1).strip()
        
    # 7. Benchmark
    bench_match = re.search(r'Benchmark\s*[:\-]?\s*(.*?)(?:\n|$)', text, re.IGNORECASE)
    if bench_match:
        meta.benchmark = bench_match.group(1).strip()
        
    # 8. Subscription/Redemption Frequency
    freq_mapping = ["Daily", "Weekly", "Fortnightly", "Monthly", "Quarterly", "Interval"]
    for freq in freq_mapping:
        if re.search(r'Subscription.*?Frequency.*?{}'.format(freq), text, re.IGNORECASE | re.DOTALL):
            meta.subscription_frequency = freq
        if re.search(r'Redemption.*?Frequency.*?{}'.format(freq), text, re.IGNORECASE | re.DOTALL):
            meta.redemption_frequency = freq
            
    # 9. Notice Period
    notice_match = re.search(r'notice period.*?(\d+)\s*days', text, re.IGNORECASE)
    if notice_match:
        meta.notice_period = int(notice_match.group(1))

    # 10. Exit Load (Extract from tables if possible)
    exit_loads = []
    for t in tables:
        if "exit" in t.markdown.lower() and "load" in t.markdown.lower():
            # Simplistic extraction
            for row in t.markdown.split('\n'):
                if '%' in row or 'Nil' in row:
                    # Just store the raw row for now since parsing markdown tables safely requires more logic
                    exit_loads.append({"raw_rule": row.strip('| ')})
    if exit_loads:
        meta.exit_load = exit_loads

    return meta
