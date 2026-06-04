import re
import csv
import json
from pathlib import Path

# Paths
DEEP_RESEARCH_PATH = "docs/deep_research.txt"
OLD_CSV_PATH = "data/corpus_inventory.csv"
NEW_CSV_PATH = "data/corpus_inventory_v2.csv"
NEW_JSON_PATH = "data/source_registry_v2.json"
SCHEMA_PATH = "data/source_schema.json"

# Normalization maps
AMC_MAP = {
    "tata": "Tata Mutual Fund",
    "edelweiss": "Edelweiss Mutual Fund",
    "sbi": "SBI Mutual Fund",
    "quant": "Quant Mutual Fund",
    "icici": "ICICI Prudential AMC",
    "hsbc": "HSBC Mutual Fund",
    "360 one": "360 ONE Mutual Fund",
    "360one": "360 ONE Mutual Fund",
    "dsp": "DSP Mutual Fund",
    "mirae": "Mirae Asset Mutual Fund",
    "franklin": "Franklin Templeton",
    "aditya": "Aditya Birla Sun Life",
    "iti": "ITI Mutual Fund",
    "kotak": "Kotak Mutual Fund",
    "bandhan": "Bandhan Mutual Fund",
    "wealth company": "The Wealth Company",
    "wsif": "The Wealth Company",
    "sebi": "SEBI",
    "amfi": "AMFI",
    "nsdl": "NSDL"
}

def normalize_amc(text):
    text_lower = text.lower()
    for key, normalized in AMC_MAP.items():
        if key in text_lower:
            return normalized
    return "External / Uncategorized"

def infer_source_type_and_tier(title, url):
    title_l = title.lower()
    url_l = url.lower()
    
    if "sebi" in title_l or "sebi.gov.in" in url_l or "nsdl" in url_l:
        if "master direction" in title_l:
            return "Master Direction", 1
        return "SEBI Circular", 1
    if "amfi" in title_l or "amfiindia" in url_l:
        return "AMFI Circular", 2
    if "isid" in title_l or "isid" in url_l:
        return "ISID", 3
    if "kim" in title_l or "kim" in url_l:
        return "KIM", 3
    if "sid" in title_l and not "isid" in title_l:
        return "SID", 3
    if "factsheet" in title_l or "factsheet" in url_l:
        return "Factsheet", 4
    if "faq" in title_l or "faq" in url_l:
        return "FAQ", 5
    if "brochure" in title_l or "leaflet" in title_l or "presentation" in title_l or "deck" in title_l:
        return "Brochure", 5
    
    return "AMC Website", 5

def parse_deep_research():
    sources = []
    with open(DEEP_RESEARCH_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find all numbered links
    # Format: "1. Title text, https://url"
    pattern = r'(\d+)\.\s+(.+?),\s*(https?://[^\s]+)'
    matches = re.findall(pattern, content)
    
    for match in matches:
        title = match[1].strip()
        url = match[2].strip()
        
        # Clean trailing non-url chars if any
        url = url.rstrip('.,;)"\'')
        
        org = normalize_amc(title + " " + url)
        stype, tier = infer_source_type_and_tier(title, url)
        
        pdf_url = url if url.lower().endswith('.pdf') else ""
        landing_url = url if not url.lower().endswith('.pdf') else ""
        if not landing_url:
            landing_url = url
            
        ingestion_method = "direct_download" if pdf_url else "playwright_scrape"
        
        source_id = f"{org.replace(' ', '-').lower()}-{stype.replace(' ', '-').lower()}-{len(sources)+1}"
        
        sources.append({
            "source_id": source_id,
            "title": title,
            "organization": org,
            "source_type": stype,
            "landing_url": landing_url,
            "pdf_url": pdf_url,
            "priority_tier": tier,
            "ingestion_method": ingestion_method,
            "status": "active",
            "last_reviewed": "2026-06-04"
        })
    return sources

def parse_old_csv():
    sources = []
    with open(OLD_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            title = row["title"]
            url = row["url"].split(" ")[0].rstrip('.,;)"\'')
            org = normalize_amc(row["organization"])
            stype, tier = infer_source_type_and_tier(title, url)
            
            # Correct the 360 ONE DynaSIF KIM/ISID mismatch 
            if "360ONE" in url and "KIM" in url:
                stype = "KIM"
                
            pdf_url = url if url.lower().endswith('.pdf') else ""
            landing_url = url if not url.lower().endswith('.pdf') else ""
            if not landing_url:
                landing_url = url
                
            ingestion_method = "direct_download" if pdf_url else "playwright_scrape"
            source_id = f"{org.replace(' ', '-').lower()}-{stype.replace(' ', '-').lower()}-{i+1000}"
            
            sources.append({
                "source_id": source_id,
                "title": title,
                "organization": org,
                "source_type": stype,
                "landing_url": landing_url,
                "pdf_url": pdf_url,
                "priority_tier": tier,
                "ingestion_method": ingestion_method,
                "status": "active",
                "last_reviewed": "2026-06-04"
            })
    return sources

def main():
    dr_sources = parse_deep_research()
    csv_sources = parse_old_csv()
    
    all_sources = dr_sources + csv_sources
    unique_sources = {}
    
    for s in all_sources:
        url_key = s["pdf_url"] or s["landing_url"]
        
        # Skip generic/news links that aren't actual SIF sources if they don't have an AMC
        if s["organization"] == "External / Uncategorized" and s["source_type"] == "AMC Website":
            # If it's a reddit link, groww, value research, etc., we want to exclude it from primary corpus
            if any(x in url_key.lower() for x in ["reddit", "youtube", "economictimes", "valueresearch", "groww", "sifprime"]):
                continue
                
        if url_key not in unique_sources:
            unique_sources[url_key] = s
        else:
            if s["pdf_url"] and not unique_sources[url_key]["pdf_url"]:
                unique_sources[url_key] = s
                
    final_list = list(unique_sources.values())
    
    # Fix source_id uniqueness
    seen_ids = set()
    for i, s in enumerate(final_list):
        base_id = f"{s['organization'].replace(' ', '-').lower()}-{s['source_type'].replace(' ', '-').lower()}"
        base_id = re.sub(r'[^a-z0-9-]', '', base_id)
        
        new_id = base_id
        counter = 1
        while new_id in seen_ids:
            new_id = f"{base_id}-{counter}"
            counter += 1
        s['source_id'] = new_id
        seen_ids.add(new_id)
    
    fieldnames = [
        "source_id", "title", "organization", "source_type", 
        "landing_url", "pdf_url", "priority_tier", "ingestion_method", 
        "status", "last_reviewed"
    ]
    
    with open(NEW_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in final_list:
            writer.writerow(s)
            
    with open(NEW_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=2)
        
    print(f"Total sources generated: {len(final_list)}")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    if "relevance_score" in schema["properties"]:
        del schema["properties"]["relevance_score"]
        
    schema["properties"]["landing_url"] = {
        "type": "string",
        "format": "uri"
    }
    schema["properties"]["source_type"]["enum"] = [
        "SEBI Circular", "AMFI Circular", "Master Direction", 
        "ISID", "SID", "KIM", "Factsheet", "FAQ", "AMC Website", "Brochure"
    ]
    
    with open(SCHEMA_PATH, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)

if __name__ == "__main__":
    main()
