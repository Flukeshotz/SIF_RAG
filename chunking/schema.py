from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class ChunkType(str, Enum):
    REGULATORY = "regulatory"
    NARRATIVE = "narrative"
    TABLE = "table"
    FAQ = "faq"
    FACTSHEET_COMMENTARY = "factsheet_commentary"

class Chunk(BaseModel):
    chunk_id: str = Field(..., description="Unique identifier for the chunk, usually document_id + counter")
    document_id: str
    document_type: str
    organization: str
    fund_name: Optional[str] = None
    strategy_type: Optional[str] = None
    priority_tier: Optional[str] = None
    section_title: Optional[str] = None
    parent_section: Optional[str] = None
    page_number: Optional[int] = None
    chunk_type: ChunkType
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional document-level metadata like effective_date, source_hash, etc.")
