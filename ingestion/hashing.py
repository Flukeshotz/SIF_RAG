import hashlib

def generate_hash(content: bytes) -> str:
    """Generates a SHA-256 hash of the given bytes."""
    return hashlib.sha256(content).hexdigest()
