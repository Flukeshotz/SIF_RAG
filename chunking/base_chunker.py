import tiktoken
from typing import List, Dict, Any, Optional
from chunking.schema import Chunk, ChunkType

class RecursiveTokenSplitter:
    def __init__(self, max_tokens: int = 700, overlap_tokens: int = 100):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.separators = ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        return self._split_text_recursive(text, self.separators)

    def _split_text_recursive(self, text: str, separators: List[str]) -> List[str]:
        # If it fits within the limit, return it
        if len(self.tokenizer.encode(text)) <= self.max_tokens:
            return [text]

        # Find the best separator
        separator = separators[-1]
        for s in separators:
            if s == "":
                separator = s
                break
            if s in text:
                separator = s
                break

        # Split by separator
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)

        # Merge splits up to max_tokens
        chunks = []
        current_chunk_splits = []
        current_length = 0

        for split in splits:
            split_length = len(self.tokenizer.encode(split))
            
            # If the single split is larger than max_tokens, recurse (unless we're at the char level)
            if split_length > self.max_tokens and len(separators) > 1:
                # Flush current chunk
                if current_chunk_splits:
                    chunks.append(separator.join(current_chunk_splits))
                    current_chunk_splits = []
                    current_length = 0
                    
                # Recurse on the large split
                next_separators = separators[separators.index(separator) + 1:]
                chunks.extend(self._split_text_recursive(split, next_separators))
                continue
                
            # If adding this split exceeds max_tokens, flush current chunk
            if current_length + split_length > self.max_tokens and current_chunk_splits:
                chunks.append(separator.join(current_chunk_splits))
                
                # Setup overlap
                overlap_splits = []
                overlap_length = 0
                for s in reversed(current_chunk_splits):
                    s_len = len(self.tokenizer.encode(s))
                    if overlap_length + s_len > self.overlap_tokens:
                        break
                    overlap_splits.insert(0, s)
                    overlap_length += s_len
                    
                current_chunk_splits = overlap_splits
                current_length = overlap_length

            current_chunk_splits.append(split)
            current_length += split_length

        if current_chunk_splits:
            chunks.append(separator.join(current_chunk_splits))

        return chunks

class BaseChunker:
    def __init__(self):
        self.splitter = RecursiveTokenSplitter(max_tokens=700, overlap_tokens=100)
        
    def extract_metadata(self, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract document-level metadata to enrich chunks."""
        meta = doc_data.get("metadata", {})
        return {
            "fund_name": meta.get("fund_name"),
            "amc": meta.get("amc_name"),
            "strategy": meta.get("strategy_type"),
            "risk_band": meta.get("risk_band"),
            "source_type": doc_data.get("document_type"),
            "priority_tier": meta.get("priority_tier", "standard"),
            "effective_date": meta.get("effective_date"),
            "source_hash": meta.get("source_hash")
        }

    def process_tables(self, doc_data: Dict[str, Any], base_metadata: Dict[str, Any]) -> List[Chunk]:
        """Convert tables into standalone chunks without splitting."""
        table_chunks = []
        doc_id = doc_data["document_id"]
        
        for i, t in enumerate(doc_data.get("tables", [])):
            markdown = t.get("markdown", "").strip()
            if not markdown:
                continue
                
            chunk_id = f"{doc_id}_table_{i+1}"
            
            chunk = Chunk(
                chunk_id=chunk_id,
                document_id=doc_id,
                document_type=doc_data.get("document_type", "Unknown"),
                organization=doc_data.get("organization", "Unknown"),
                fund_name=base_metadata["fund_name"],
                strategy_type=base_metadata["strategy"],
                priority_tier=base_metadata["priority_tier"],
                section_title=t.get("title"),
                page_number=t.get("page"),
                chunk_type=ChunkType.TABLE,
                text=markdown,
                metadata=base_metadata
            )
            table_chunks.append(chunk)
            
        return table_chunks
