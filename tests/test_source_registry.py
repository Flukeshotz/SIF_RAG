import pytest
import os
import json
from scripts.validate_corpus import validate_source_registry

def test_source_registry_exists():
    """Verify source_registry.json exists in data/ directory."""
    assert os.path.exists("data/source_registry.json")

def test_source_registry_validates_cleanly():
    """Verify source_registry.json passes all validation checks."""
    errors = validate_source_registry("data/source_registry.json")
    assert not errors, f"JSON registry validation failed with errors: {errors}"

def test_source_schema_exists():
    """Verify source_schema.json exists in data/ directory."""
    assert os.path.exists("data/source_schema.json")
