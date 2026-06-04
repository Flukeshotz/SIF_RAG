from typing import List, Dict, Any
from chunking.base_chunker import BaseChunker
from chunking.schema import Chunk, ChunkType

class FactsheetChunker(BaseChunker):
    def chunk(self, doc_data: Dict[str, Any]) -> List[Chunk]:
        chunks = []
        base_metadata = self.extract_metadata(doc_data)
        
        # 1. Process Tables (Only Asset Allocation and Risk allowed)
        # Sanitizer should have handled this, but we'll double check
        for t in self.process_tables(doc_data, base_metadata):
            md = t.text.lower()
            if "allocation" in md or "risk" in md or "exit load" in md:
                chunks.append(t)
        
        # 2. Process Factsheet Commentary
        doc_id = doc_data["document_id"]
        counter = 1
        
        def process_section(sec: Dict[str, Any], parent_title: str = ""):
            nonlocal counter
            title = sec.get("title", "").strip()
            content = sec.get("content", "").strip()
            
            # Additional safety filter for NAV/Holdings
            lower_title = title.lower()
            if "nav" in lower_title or "holdings" in lower_title or "performance" in lower_title:
                return
            
            context_header = f"Factsheet Commentary: {title}"
            if parent_title:
                context_header = f"Factsheet Commentary: {parent_title} > {title}"
            
            if content:
                contextual_text = f"[{context_header}]\n{content}"
                
                splits = self.splitter.split_text(contextual_text)
                
                for split in splits:
                    if not split.strip():
                        continue
                        
                    chunk_id = f"{doc_id}_factsheet_{counter}"
                    counter += 1
                    
                    chunk = Chunk(
                        chunk_id=chunk_id,
                        document_id=doc_id,
                        document_type=doc_data.get("document_type", "Factsheet"),
                        organization=doc_data.get("organization", "Unknown"),
                        fund_name=base_metadata["fund_name"],
                        strategy_type=base_metadata["strategy"],
                        priority_tier=base_metadata["priority_tier"],
                        section_title=title,
                        parent_section=parent_title,
                        page_number=sec.get("page"),
                        chunk_type=ChunkType.FACTSHEET_COMMENTARY,
                        text=split.strip(),
                        metadata=base_metadata
                    )
                    chunks.append(chunk)
            
            # Recurse into subsections
            for sub in sec.get("subsections", []):
                process_section(sub, title)

        for section in doc_data.get("sections", []):
            process_section(section)
            
        return chunks
