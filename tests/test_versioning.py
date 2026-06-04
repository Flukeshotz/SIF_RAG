import pytest
from unittest.mock import patch
from ingestion import versioning

def test_update_version_new():
    with patch("ingestion.storage.load_metadata", return_value=None), \
         patch("ingestion.storage.save_metadata") as mock_save:
             
        is_new, metadata = versioning.update_version("test-1", "hash123", "/path/to/file")
        
        assert is_new is True
        assert len(metadata["versions"]) == 1
        assert metadata["versions"][0]["content_hash"] == "hash123"
        mock_save.assert_called_once()

def test_update_version_existing_same_hash():
    existing_meta = {
        "source_id": "test-1",
        "versions": [{"content_hash": "hash123"}]
    }
    with patch("ingestion.storage.load_metadata", return_value=existing_meta), \
         patch("ingestion.storage.save_metadata") as mock_save:
             
        is_new, metadata = versioning.update_version("test-1", "hash123", "/path/to/file")
        
        assert is_new is False
        assert len(metadata["versions"]) == 1
        mock_save.assert_not_called()

def test_update_version_existing_new_hash():
    existing_meta = {
        "source_id": "test-1",
        "versions": [{"version_id": 1, "content_hash": "hash123"}]
    }
    with patch("ingestion.storage.load_metadata", return_value=existing_meta), \
         patch("ingestion.storage.save_metadata") as mock_save:
             
        is_new, metadata = versioning.update_version("test-1", "hash456", "/path/to/newfile")
        
        assert is_new is True
        assert len(metadata["versions"]) == 2
        assert metadata["versions"][1]["content_hash"] == "hash456"
        assert metadata["versions"][1]["version_id"] == 2
        mock_save.assert_called_once()
