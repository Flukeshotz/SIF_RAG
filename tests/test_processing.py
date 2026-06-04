import pytest
from processing.document_model import Document, Metadata, Section, Table
from processing.metadata_extractor import extract_metadata
from processing.validator import validate_document

def test_document_model():
    doc = Document(
        document_id="test",
        document_type="ISID",
        organization="Test Org",
        source_url="http://test.com"
    )
    assert doc.document_id == "test"
    assert doc.document_type == "ISID"
    
def test_metadata_extractor():
    text = "Tata Mutual Fund presents the new Hybrid Long-Short strategy. Minimum investment is Rs. 10,00,000. It has a Moderate risk."
    meta = extract_metadata(text, {"source_type": "ISID"}, [])
    
    assert meta.amc_name == "Tata Mutual Fund"
    assert meta.strategy_type == "Hybrid Long-Short"
    assert meta.minimum_investment == 1000000
    assert meta.risk_band == 3
    assert meta.document_type == "ISID"

def test_validator_valid():
    doc = Document(
        document_id="test",
        document_type="ISID",
        organization="Test Org",
        source_url="http://test.com",
        sections=[Section(title="A")],
        tables=[Table(markdown="test", page=1)],
        metadata=Metadata(fund_name="Fund A", minimum_investment=1000000, risk_band=3)
    )
    res = validate_document(doc)
    assert res["is_valid"] == True
    assert len(res["errors"]) == 0
    assert len(res["warnings"]) == 0

def test_validator_invalid_minimum():
    doc = Document(
        document_id="test",
        document_type="ISID",
        organization="Test Org",
        source_url="http://test.com",
        sections=[Section(title="A")],
        metadata=Metadata(fund_name="Fund A", minimum_investment=5000)
    )
    res = validate_document(doc)
    assert res["is_valid"] == False
    assert any("10L" in e for e in res["errors"])
