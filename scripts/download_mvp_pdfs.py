import asyncio
import json
import httpx
from pathlib import Path
import hashlib
from datetime import datetime
import csv
from urllib.parse import urlparse

# Ensure directories exist
Path("data/raw/pdf").mkdir(parents=True, exist_ok=True)
Path("data/raw/metadata").mkdir(parents=True, exist_ok=True)

# Concurrency limiting to prevent CDN drops
domain_semaphores = {}

def get_semaphore(url: str) -> asyncio.Semaphore:
    domain = urlparse(url).netloc
    if domain not in domain_semaphores:
        domain_semaphores[domain] = asyncio.Semaphore(2)
    return domain_semaphores[domain]

async def download_pdf(source: dict) -> dict:
    url = source["pdf_url"]
    if not url.startswith("http"):
        url = "https://" + url
        
    result = {
        "source_id": source["source_id"],
        "organization": source["organization"],
        "source_type": source["source_type"],
        "url": url,
        "success": False,
        "error": None
    }
    
    sem = get_semaphore(url)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/pdf,*/*",
        "Connection": "keep-alive"
    }
    
    async with sem:
        try:
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True, verify=False) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                content = response.content
                if content.startswith(b"%PDF-"):
                    result["success"] = True
                    
                    # Store PDF
                    pdf_path = Path(f"data/raw/pdf/{source['source_id']}.pdf")
                    pdf_path.write_bytes(content)
                    
                    # Store metadata
                    file_hash = hashlib.sha256(content).hexdigest()
                    meta = {
                        "source_id": source["source_id"],
                        "title": source["title"],
                        "organization": source["organization"],
                        "document_type": source["source_type"],
                        "downloaded_at": datetime.utcnow().isoformat() + "Z",
                        "sha256": file_hash
                    }
                    meta_path = Path(f"data/raw/metadata/{source['source_id']}.json")
                    meta_path.write_text(json.dumps(meta, indent=2))
                else:
                    result["error"] = "Downloaded content is not a valid PDF blob."
        except httpx.HTTPStatusError as e:
            result["error"] = f"HTTP {e.response.status_code}"
        except Exception as e:
            result["error"] = str(e)
            
    return result

async def main():
    print("Loading MVP registry...")
    with open("data/source_registry_mvp.json") as f:
        registry = json.load(f)
        
    pdf_sources = []
    missing_urls = []
    
    for s in registry:
        if s.get("pdf_url"):
            pdf_sources.append(s)
        else:
            missing_urls.append(s)
            
    print(f"Total MVP Sources: {len(registry)}")
    print(f"Direct PDFs to Download: {len(pdf_sources)}")
    print(f"Missing PDF URLs (Skipped): {len(missing_urls)}")
    
    # Log missing to CSV
    with open("missing_pdf_urls.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["source_id", "organization", "source_type", "landing_url"])
        for m in missing_urls:
            writer.writerow([m["source_id"], m["organization"], m["source_type"], m.get("landing_url")])
            
    # Download
    tasks = [download_pdf(s) for s in pdf_sources]
    results = await asyncio.gather(*tasks)
    
    success = sum(1 for r in results if r["success"])
    failed = len(results) - success
    
    # Generate Report
    with open("docs/manual_acquisition_report.md", "w") as f:
        f.write("# MVP Manual Acquisition Report\n\n")
        f.write("## Summary Metrics\n")
        f.write(f"- **Total MVP Sources:** {len(registry)}\n")
        f.write(f"- **Sources with Direct PDFs:** {len(pdf_sources)}\n")
        f.write(f"- **Successful PDF Downloads:** {success}\n")
        f.write(f"- **Failed Downloads:** {failed}\n")
        f.write(f"- **Missing PDF URLs (Requires Manual Hunt):** {len(missing_urls)}\n\n")
        
        f.write("## Download Audit\n")
        f.write("| Source ID | Organization | Type | Status | Error |\n")
        f.write("|---|---|---|---|---|\n")
        for r in results:
            status = "✅ Success" if r["success"] else "❌ Failed"
            err = r["error"] or ""
            f.write(f"| {r['source_id']} | {r['organization']} | {r['source_type']} | {status} | {err} |\n")

if __name__ == "__main__":
    asyncio.run(main())
