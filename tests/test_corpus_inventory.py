import pytest
import os
from scripts.validate_corpus import validate_csv

def test_corpus_inventory_exists():
    """Verify corpus_inventory.csv exists in data/ directory."""
    assert os.path.exists("data/corpus_inventory.csv")

def test_corpus_inventory_validates_cleanly():
    """Verify corpus_inventory.csv passes all validation checks."""
    errors = validate_csv("data/corpus_inventory.csv")
    assert not errors, f"CSV validation failed with errors: {errors}"
