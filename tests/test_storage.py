import pytest
import os
import json
from pathlib import Path
from ingestion import storage

def test_save_document(tmp_path):
    storage.PDF_DIR = tmp_path / "pdf"
    storage.HTML_DIR = tmp_path / "html"
    
    filepath = storage.save_document("test-1", b"pdf data", True, "testhash")
    assert filepath.endswith(".pdf")
    assert "testhash" in filepath
    assert os.path.exists(filepath)
    
def test_save_and_load_metadata(tmp_path):
    storage.METADATA_DIR = tmp_path / "metadata"
    
    meta = {"test": "data"}
    storage.save_metadata("test-1", meta)
    
    loaded = storage.load_metadata("test-1")
    assert loaded == meta
