from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Citation(BaseModel):
    page: int
    source_id: str

class Table(BaseModel):
    title: str = ""
    markdown: str
    page: int

class Section(BaseModel):
    title: str
    level: int = 1
    content: str = ""
    subsections: List['Section'] = Field(default_factory=list)
    page: Optional[int] = None

class Metadata(BaseModel):
    fund_name: Optional[str] = None
    amc_name: Optional[str] = None
    document_type: Optional[str] = None
    strategy_type: Optional[str] = None
    category: Optional[str] = None
    minimum_investment: Optional[int] = None
    benchmark: Optional[str] = None
    risk_band: Optional[int] = None
    fund_manager: Optional[str] = None
    exit_load: Optional[List[Dict[str, Any]]] = None
    subscription_frequency: Optional[str] = None
    redemption_frequency: Optional[str] = None
    notice_period: Optional[int] = None
    effective_date: Optional[str] = None
    source_type: Optional[str] = None

class Document(BaseModel):
    document_id: str
    document_type: str
    organization: str
    source_url: str
    effective_date: str = ""
    sections: List[Section] = Field(default_factory=list)
    tables: List[Table] = Field(default_factory=list)
    metadata: Metadata = Field(default_factory=Metadata)

Section.model_rebuild()
