from typing import List, Dict, Any
from chunking.base_chunker import BaseChunker
from chunking.schema import Chunk, ChunkType

class ISIDChunker(BaseChunker):
    def chunk(self, doc_data: Dict[str, Any]) -> List[Chunk]:
        chunks = []
        base_metadata = self.extract_metadata(doc_data)
        
        # 1. Process Tables
        chunks.extend(self.process_tables(doc_data, base_metadata))
        
        # 2. Process Semantic Narrative
        doc_id = doc_data["document_id"]
        counter = 1
        
        def process_section(sec: Dict[str, Any], parent_title: str = ""):
            nonlocal counter
            title = sec.get("title", "").strip()
            content = sec.get("content", "").strip()
            
            # Semantic chunking implies we preserve the section identity
            context_header = f"Section: {title}"
            if parent_title:
                context_header = f"Section: {parent_title} > {title}"
            
            if content:
                contextual_text = f"[{context_header}]\n{content}"
                
                splits = self.splitter.split_text(contextual_text)
                
                for split in splits:
                    if not split.strip():
                        continue
                        
                    chunk_id = f"{doc_id}_isid_{counter}"
                    counter += 1
                    
                    chunk = Chunk(
                        chunk_id=chunk_id,
                        document_id=doc_id,
                        document_type=doc_data.get("document_type", "Unknown"),
                        organization=doc_data.get("organization", "Unknown"),
                        fund_name=base_metadata["fund_name"],
                        strategy_type=base_metadata["strategy"],
                        priority_tier=base_metadata["priority_tier"],
                        section_title=title,
                        parent_section=parent_title,
                        page_number=sec.get("page"),
                        chunk_type=ChunkType.NARRATIVE,
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
