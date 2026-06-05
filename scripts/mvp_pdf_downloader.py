import asyncio
import json
import httpx
from pathlib import Path
import hashlib
from urllib.parse import urlparse

# Ensure directories exist
Path("data/raw").mkdir(parents=True, exist_ok=True)

# Domain semaphores to avoid connection errors on basic CDNs
domain_semaphores = {}

def get_semaphore(url: str) -> asyncio.Semaphore:
    domain = urlparse(url).netloc
    if domain not in domain_semaphores:
        # Default strict limit of 2 concurrent connections per domain
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
        "status_code": None,
        "size_kb": 0,
        "error": None
    }
    
    sem = get_semaphore(url)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/pdf,*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }
    
    async with sem:
        try:
            # 60 second timeout for large PDFs
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True, verify=False) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                content = response.content
                result["status_code"] = response.status_code
                result["size_kb"] = len(content) / 1024
                
                # Basic validation: ensure it's actually a PDF signature
                if content.startswith(b"%PDF-"):
                    result["success"] = True
                    
                    # Store file
                    filepath = Path(f"data/raw/{source['source_id']}.pdf")
                    filepath.write_bytes(content)
                    
                    # Store metadata (hash/version)
                    file_hash = hashlib.sha256(content).hexdigest()
                    meta = {
                        "source_id": source["source_id"],
                        "hash": file_hash,
                        "size_bytes": len(content),
                        "timestamp": "2026-06-04T00:00:00Z"
                    }
                    Path(f"data/raw/{source['source_id']}.json").write_text(json.dumps(meta, indent=2))
                    
                else:
                    result["error"] = "Downloaded content is not a valid PDF"
                    
        except httpx.HTTPStatusError as e:
            result["status_code"] = e.response.status_code
            result["error"] = f"HTTP Error {e.response.status_code}"
        except Exception as e:
            result["error"] = str(e)
            
    return result

async def main():
    print("Loading MVP registry...")
    with open("data/source_registry_mvp.json") as f:
        registry = json.load(f)
        
    # Filter for direct PDFs only
    pdf_sources = [s for s in registry if s.get("pdf_url")]
    print(f"Found {len(pdf_sources)} sources with direct PDF URLs out of {len(registry)} total MVP sources.")
    
    tasks = [download_pdf(s) for s in pdf_sources]
    results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    
    print(f"\nDownload Complete! Success rate: {success_rate:.1f}% ({success_count}/{total_count})")
    
    # Save report
    with open("docs/reports/direct_pdf_acquisition_report.md", "w") as f:
        f.write("# Phase 2.75 — Direct PDF Acquisition Report\n\n")
        f.write("## Summary\n")
        f.write(f"- **Targeted PDFs:** {total_count}\n")
        f.write(f"- **Successfully Downloaded:** {success_count} ({success_rate:.1f}%)\n")
        f.write(f"- **Failed:** {total_count - success_count}\n\n")
        
        f.write("## Detailed Results\n")
        f.write("| Source ID | Organization | Type | Success | Size (KB) | Error |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in results:
            success_mark = "✅" if r["success"] else "❌"
            err = r["error"] or ""
            f.write(f"| {r['source_id']} | {r['organization']} | {r['source_type']} | {success_mark} | {r['size_kb']:.1f} | {err} |\n")

if __name__ == "__main__":
    asyncio.run(main())
