"""
Corpus Validation Utilities.
Validates the CSV inventory and JSON registries for Phase 1.
"""
import csv
import json
from pathlib import Path
from typing import Dict, List, Any

# Required fields for CSV
CSV_REQUIRED_FIELDS = ["title", "url", "source_type", "organization", "priority"]

# Valid enumerations
VALID_SOURCE_TYPES = {
    "SEBI Circular", "AMFI Circular", "ISID", "KIM", 
    "Factsheet", "FAQ", "AMC Website", "AMC Website / Brochure"
}

def validate_csv(csv_path: str) -> List[str]:
    """Validates the corpus_inventory.csv."""
    errors = []
    seen_urls = set()
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        # Check missing headers
        missing_headers = [h for h in CSV_REQUIRED_FIELDS if h not in reader.fieldnames]
        if missing_headers:
            errors.append(f"Missing required CSV headers: {missing_headers}")
            return errors
            
        for row_idx, row in enumerate(reader, start=2):
            # Check missing fields
            for field in CSV_REQUIRED_FIELDS:
                if not row.get(field) or not row[field].strip():
                    errors.append(f"Row {row_idx}: Missing value for field '{field}'")
            
            # Check duplicate URLs
            url = row.get("url", "").strip()
            if url:
                if url in seen_urls:
                    errors.append(f"Row {row_idx}: Duplicate URL found '{url}'")
                seen_urls.add(url)
            
            # Check invalid source types
            source_type = row.get("source_type", "").strip()
            if source_type and source_type not in VALID_SOURCE_TYPES:
                errors.append(f"Row {row_idx}: Invalid source_type '{source_type}'")
                
            # Check invalid priority tiers (must be Tier 1-5)
            priority_str = row.get("priority", "").strip().lower()
            if priority_str:
                if not priority_str.startswith("tier ") or len(priority_str) != 6:
                    errors.append(f"Row {row_idx}: Invalid priority format '{priority_str}'. Expected 'Tier X'.")
                else:
                    try:
                        tier = int(priority_str.split(" ")[1])
                        if not (1 <= tier <= 5):
                            errors.append(f"Row {row_idx}: Invalid priority tier {tier}. Must be 1-5.")
                    except ValueError:
                        errors.append(f"Row {row_idx}: Priority tier must contain an integer.")
                        
    return errors

def validate_source_registry(json_path: str) -> List[str]:
    """Validates the source_registry.json."""
    errors = []
    seen_urls = set()
    seen_ids = set()
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if not isinstance(data, list):
        return ["Root of source_registry.json must be a list of objects."]
        
    required_fields = [
        "source_id", "title", "organization", "source_type", 
        "url", "priority_tier", "ingestion_method", "status"
    ]
        
    for i, record in enumerate(data):
        for field in required_fields:
            if field not in record:
                errors.append(f"Record {i}: Missing required field '{field}'")
                
        # Validate uniqueness
        source_id = record.get("source_id")
        if source_id:
            if source_id in seen_ids:
                errors.append(f"Record {i}: Duplicate source_id '{source_id}'")
            seen_ids.add(source_id)
            
        url = record.get("url")
        if url:
            if url in seen_urls:
                errors.append(f"Record {i}: Duplicate URL '{url}'")
            seen_urls.add(url)
            
        # Validate priority tier
        tier = record.get("priority_tier")
        if tier is not None:
            if not isinstance(tier, int) or not (1 <= tier <= 5):
                errors.append(f"Record {i}: priority_tier must be integer 1-5. Got {tier}")
                
        # Validate source type
        stype = record.get("source_type")
        if stype and stype not in VALID_SOURCE_TYPES:
            errors.append(f"Record {i}: Invalid source_type '{stype}'")
            
    return errors

if __name__ == "__main__":
    csv_errors = validate_csv("data/corpus_inventory.csv")
    if csv_errors:
        print("CSV Errors:")
        for e in csv_errors:
            print(f" - {e}")
    else:
        print("CSV Validation Passed.")
        
    json_errors = validate_source_registry("data/source_registry.json")
    if json_errors:
        print("JSON Registry Errors:")
        for e in json_errors:
            print(f" - {e}")
    else:
        print("JSON Registry Validation Passed.")
