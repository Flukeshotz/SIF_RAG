import pytest
from ingestion.registry import load_registry, get_active_sources
from unittest.mock import patch, mock_open

def test_load_registry():
    mock_json = '[{"source_id": "test-1", "status": "active"}]'
    with patch("builtins.open", mock_open(read_data=mock_json)), \
         patch("pathlib.Path.exists", return_value=True):
        data = load_registry("dummy.json")
        assert len(data) == 1
        assert data[0]["source_id"] == "test-1"

def test_get_active_sources():
    mock_json = '[{"source_id": "1", "status": "active"}, {"source_id": "2", "status": "deprecated"}]'
    with patch("builtins.open", mock_open(read_data=mock_json)), \
         patch("pathlib.Path.exists", return_value=True):
        active = get_active_sources("dummy.json")
        assert len(active) == 1
        assert active[0]["source_id"] == "1"
