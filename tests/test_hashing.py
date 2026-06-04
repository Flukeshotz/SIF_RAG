from ingestion.hashing import generate_hash
import hashlib

def test_generate_hash():
    content = b"test content"
    expected = hashlib.sha256(content).hexdigest()
    assert generate_hash(content) == expected
