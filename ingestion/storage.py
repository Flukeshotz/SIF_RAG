import json
from pathlib import Path
from typing import Dict, Any, Optional

RAW_DATA_DIR = Path("data/raw")
PDF_DIR = RAW_DATA_DIR / "pdf"
HTML_DIR = RAW_DATA_DIR / "html"
METADATA_DIR = RAW_DATA_DIR / "metadata"

def ensure_directories():
    """Ensure raw data directories exist."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

def save_document(source_id: str, content: bytes, is_pdf: bool, content_hash: str) -> str:
    """Saves raw content and returns the filepath."""
    ensure_directories()
    
    ext = "pdf" if is_pdf else "html"
    target_dir = PDF_DIR if is_pdf else HTML_DIR
    
    filename = f"{source_id}_{content_hash}.{ext}"
    filepath = target_dir / filename
    
    with open(filepath, "wb") as f:
        f.write(content)
        
    return str(filepath)

def save_metadata(source_id: str, metadata: Dict[str, Any]) -> str:
    """Saves version metadata for a source."""
    ensure_directories()
    
    filepath = METADATA_DIR / f"{source_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    return str(filepath)

def load_metadata(source_id: str) -> Optional[Dict[str, Any]]:
    """Loads existing metadata for a source if it exists."""
    filepath = METADATA_DIR / f"{source_id}.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
