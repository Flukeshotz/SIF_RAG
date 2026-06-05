import json
import time
import requests
import uuid
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings.model import EmbeddingModel
from db.qdrant_connection import get_client, init_collection
from qdrant_client.models import PointStruct

REGISTRY_PATH = "data/sif_registry.json"

def clean_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    # Remove script and style elements
    for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        script.extract()
    text = soup.get_text(separator="\n")
    # Collapse multiple newlines
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text

def main():
    print("Loading registry...")
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    # Initialize Embedding Model
    embedder = EmbeddingModel()
    
    # Initialize Qdrant Client
    client = get_client()
    collection_name = "sif_documents"
    init_collection(client, collection_name)

    # Initialize Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    total_uploaded = 0
    failures = 0
    skipped = 0
    
    points_to_upload = []

    print(f"Processing {len(registry)} funds...")
    for fund in registry:
        url = fund.get("groww_url") or fund.get("indmoney_url") or fund.get("official_url")
        if not url:
            skipped += 1
            continue

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            res = requests.get(url, headers=headers, timeout=10)
            
            if res.status_code != 200:
                print(f"Skipping {url} (Status: {res.status_code})")
                skipped += 1
                continue
                
            clean_content = clean_text(res.text)
            
            if len(clean_content) < 100:
                print(f"Skipping {url} (Content too short)")
                skipped += 1
                continue
                
            chunks = text_splitter.split_text(clean_content)
            
            if not chunks:
                continue
                
            # Batch generate embeddings for chunks of this document
            embeddings = embedder.encode_documents(chunks)
            
            for i, (chunk_text, vector) in enumerate(zip(chunks, embeddings)):
                chunk_id = f"{url}-chunk-{i}"
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id))
                
                payload = {
                    "chunk_id": chunk_id,
                    "document_id": url,
                    "document_type": "Webpage",
                    "organization": fund.get("amc", "Unknown AMC"),
                    "fund_name": fund.get("fund_name", "Unknown Fund"),
                    "strategy_type": fund.get("strategy", "Unknown Strategy"),
                    "priority_tier": "1",
                    "chunk_type": "Paragraph",
                    "page_number": 1,
                    "text": chunk_text
                }
                
                points_to_upload.append(PointStruct(id=point_id, vector=vector.tolist(), payload=payload))
            
            print(f"Processed {url} -> {len(chunks)} chunks")
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            failures += 1
            
        time.sleep(1) # Polite scraping delay
        
    print(f"Generated {len(points_to_upload)} vectors to upload.")
    
    if points_to_upload:
        try:
            # Batch upload to Qdrant (max 100 per batch)
            batch_size = 100
            for i in range(0, len(points_to_upload), batch_size):
                batch = points_to_upload[i:i + batch_size]
                client.upload_points(
                    collection_name=collection_name,
                    points=batch
                )
            total_uploaded += len(points_to_upload)
            print("Successfully uploaded to Qdrant.")
        except Exception as e:
            print(f"Error uploading to Qdrant: {e}")
            failures += 1

    print(f"\\n--- Ingestion Report ---")
    print(f"Successfully processed funds: {len(registry) - skipped - failures}")
    print(f"Skipped funds (403/404): {skipped}")
    print(f"Failures: {failures}")
    print(f"Total Vector Chunks Uploaded: {total_uploaded}")

if __name__ == "__main__":
    main()
