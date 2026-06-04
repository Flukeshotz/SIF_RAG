import pytest
import os
import json

def load_registry():
    with open("data/source_registry_v2.json", "r") as f:
        return json.load(f)

def test_registry_size():
    data = load_registry()
    assert len(data) >= 60, f"Expected 60+ sources, got {len(data)}"

def test_no_duplicate_urls():
    data = load_registry()
    seen = set()
    for item in data:
        url = item.get("pdf_url") or item.get("landing_url")
        assert url not in seen, f"Duplicate URL found: {url}"
        seen.add(url)

def test_amc_coverage():
    data = load_registry()
    orgs = {item["organization"] for item in data}
    
    required_amcs = [
        "Franklin Templeton", "Aditya Birla Sun Life", "ITI Mutual Fund", 
        "Kotak Mutual Fund", "Bandhan Mutual Fund", "The Wealth Company",
        "Tata Mutual Fund", "SBI Mutual Fund"
    ]
    
    for amc in required_amcs:
        assert any(amc in org for org in orgs), f"Missing coverage for {amc}"

def test_no_invalid_source_types():
    data = load_registry()
    with open("data/source_schema.json", "r") as f:
        schema = json.load(f)
        
    valid_types = set(schema["properties"]["source_type"]["enum"])
    for item in data:
        assert item["source_type"] in valid_types, f"Invalid source type: {item['source_type']}"

def test_tier_1_sources_present():
    data = load_registry()
    tier_1 = [item for item in data if item["priority_tier"] == 1]
    assert len(tier_1) > 0, "No Tier 1 regulatory sources found"
    
def test_tier_2_sources_present():
    data = load_registry()
    tier_2 = [item for item in data if item["priority_tier"] == 2]
    assert len(tier_2) > 0, "No Tier 2 AMFI sources found"
