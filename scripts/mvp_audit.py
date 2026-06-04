import asyncio
import json
from urllib.parse import urlparse
from ingestion import registry
from ingestion import downloader

domain_semaphores = {}

def get_semaphore(url: str) -> asyncio.Semaphore:
    domain = urlparse(url).netloc
    if domain not in domain_semaphores:
        policy = downloader.get_policy(url)
        limit = policy["max_concurrent"]
        domain_semaphores[domain] = asyncio.Semaphore(limit)
    return domain_semaphores[domain]

async def audit_source(source):
    url = source.get("pdf_url") or source.get("landing_url")
    result = {
        "source_id": source["source_id"],
        "organization": source["organization"],
        "source_type": source.get("source_type", "unknown"),
        "priority_tier": source.get("priority_tier", 5),
        "url": url,
        "status_code": None,
        "content_type": "unknown",
        "download_success": False,
        "file_size": 0,
        "hash_generated": False,
        "version_created": False,
        "error_type": None
    }
    
    if not url:
        result["error_type"] = "no_url"
        return result
        
    sem = get_semaphore(url)
    
    async with sem:
        try:
            content, content_type = await downloader.download_file(url, source["source_type"])
            
            result["status_code"] = 200
            result["download_success"] = True
            
            content_type = content_type.lower()
            if "pdf" in content_type:
                result["content_type"] = "application/pdf"
            elif "html" in content_type:
                result["content_type"] = "text/html"
            elif "plain" in content_type:
                result["content_type"] = "text/plain"
            else:
                result["content_type"] = content_type
                
            result["file_size"] = len(content)
            result["hash_generated"] = True
            result["version_created"] = True
            
        except downloader.DownloadError as e:
            msg = str(e)
            if "HTTP 403" in msg:
                result["error_type"] = "forbidden"
                result["status_code"] = 403
            elif "HTTP 404" in msg:
                result["error_type"] = "not_found"
                result["status_code"] = 404
            elif "HTTP 429" in msg:
                result["error_type"] = "too_many_requests"
                result["status_code"] = 429
            elif "Timeout" in msg:
                result["error_type"] = "timeout"
            else:
                result["error_type"] = "connection_error"
        except Exception as e:
            result["error_type"] = "parsing_error"
            
    return result

async def main():
    sources = registry.get_active_sources("data/source_registry_mvp.json")
    print(f"Starting MVP audit of {len(sources)} sources...")
    
    tasks = [audit_source(s) for s in sources]
    results = []
    
    for i in range(0, len(tasks), 5):
        batch = tasks[i:i+5]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
        print(f"Processed {len(results)}/{len(sources)}...")
        await asyncio.sleep(2)
            
    total = len(results)
    success = sum(1 for r in results if r["download_success"])
    failed = total - success
    pdf_count = sum(1 for r in results if r["content_type"] == "application/pdf")
    html_count = sum(1 for r in results if r["content_type"] == "text/html")
    
    forbidden = sum(1 for r in results if r["error_type"] == "forbidden")
    not_found = sum(1 for r in results if r["error_type"] == "not_found")
    too_many = sum(1 for r in results if r["error_type"] == "too_many_requests")
    timeout = sum(1 for r in results if r["error_type"] == "timeout")
    conn_error = sum(1 for r in results if r["error_type"] == "connection_error")
    parsing_error = sum(1 for r in results if r["error_type"] == "parsing_error")
    
    storage_bytes = sum(r["file_size"] for r in results)
    storage_mb = storage_bytes / (1024 * 1024)
    
    success_rate = (success/total)*100 if total > 0 else 0
    
    with open("data/raw/mvp_audit_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Audit complete! Success rate: {success_rate:.1f}%")
    
    with open("docs/mvp_acquisition_report.md", "w") as f:
        f.write("# Phase 2.75 — MVP Acquisition Report\n\n")
        f.write("## 1. Summary Metrics\n")
        f.write(f"- **Total Sources:** {total}\n")
        f.write(f"- **Successful Downloads:** {success} ({success_rate:.1f}%)\n")
        f.write(f"- **Failed Downloads:** {failed}\n")
        f.write(f"- **PDF Count:** {pdf_count}\n")
        f.write(f"- **HTML Count:** {html_count}\n")
        f.write(f"- **Storage Size:** {storage_mb:.2f} MB\n\n")
        
        f.write("## 2. Failure Classification\n")
        f.write(f"- **Forbidden (403):** {forbidden}\n")
        f.write(f"- **Not Found (404):** {not_found}\n")
        f.write(f"- **Too Many Requests (429):** {too_many}\n")
        f.write(f"- **Timeouts:** {timeout}\n")
        f.write(f"- **Connection Errors:** {conn_error}\n")
        f.write(f"- **Parsing Errors:** {parsing_error}\n\n")
        
        f.write("## 3. Detailed Source Audit\n\n")
        f.write("| Source ID | Organization | Type | Status Code | Content Type | Success | Size (MB) |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in results:
            size_mb = f"{r['file_size']/(1024*1024):.2f}" if r['file_size'] else "0"
            status = r['status_code'] or r['error_type']
            success_str = "✅" if r['download_success'] else "❌"
            f.write(f"| {r['source_id']} | {r['organization']} | {r['source_type']} | {status} | {r['content_type']} | {success_str} | {size_mb} |\n")

if __name__ == "__main__":
    asyncio.run(main())
