from datetime import datetime
from typing import Dict, Any, Tuple
from . import storage

def update_version(source_id: str, new_hash: str, filepath: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Checks if the hash is new. If so, adds a new version to the metadata.
    Returns (is_new_version, metadata_dict)
    """
    metadata = storage.load_metadata(source_id)
    now_iso = datetime.utcnow().isoformat() + "Z"
    
    if not metadata:
        metadata = {
            "source_id": source_id,
            "created_at": now_iso,
            "updated_at": now_iso,
            "versions": []
        }
    
    # Check current latest version
    if metadata["versions"]:
        latest = metadata["versions"][-1]
        if latest["content_hash"] == new_hash:
            return False, metadata
            
    # New version detected
    new_version = {
        "version_id": len(metadata["versions"]) + 1,
        "content_hash": new_hash,
        "filepath": filepath,
        "ingested_at": now_iso
    }
    
    metadata["versions"].append(new_version)
    metadata["updated_at"] = now_iso
    
    storage.save_metadata(source_id, metadata)
    
    return True, metadata
