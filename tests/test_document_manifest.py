import pytest
import os
import json

def test_document_manifest_exists():
    """Verify document_manifest.json exists in data/ directory."""
    assert os.path.exists("data/document_manifest.json")

def test_document_manifest_structure():
    """Verify document_manifest.json has the correct structure and fields."""
    with open("data/document_manifest.json", "r") as f:
        data = json.load(f)
        
    assert "manifest_id" in data
    assert "generated_at" in data
    assert "summary" in data
    assert "sources" in data
    
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0
    
    source = data["sources"][0]
    assert "source_id" in source
    assert "expected_documents" in source
    assert "source_ownership" in source
    assert "status" in source
    assert "ingestion_readiness" in source
