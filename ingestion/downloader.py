import httpx
import asyncio
import logging
import json
from typing import Tuple
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

class DownloadError(Exception):
    pass

def load_policies():
    try:
        with open("config/domain_policies.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"default": {"route": "static", "max_concurrent": 5, "timeout_seconds": 30.0}, "domains": {}}

POLICIES = load_policies()

def get_policy(url: str) -> dict:
    domain = urlparse(url).netloc
    if domain in POLICIES["domains"]:
        return POLICIES["domains"][domain]
    return POLICIES["default"]

def discover_pdf_links(html_content: bytes, base_url: str) -> str:
    """Attempts to find a direct PDF link in HTML content."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True).lower()
            if href.lower().endswith(".pdf") or "download" in text or "isid" in text or "kim" in text:
                return urljoin(base_url, href)
    except Exception as e:
        logger.error(f"Error discovering PDF links: {e}")
    return ""

async def _download_static(url: str, timeout: float) -> Tuple[bytes, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, verify=False) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.content, response.headers.get("content-type", "unknown")

async def _download_dynamic(url: str, timeout: float, is_waf: bool = False) -> Tuple[bytes, str]:
    async with async_playwright() as p:
        # For WAF, we use a headed or slow-mimicking browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        try:
            # wait_until="networkidle" ensures dynamic content loads
            response = await page.goto(url, timeout=timeout * 1000, wait_until="networkidle")
            
            if is_waf:
                # Artificial delay to let bot checks clear
                await asyncio.sleep(5)
                
            if response and response.status >= 400:
                raise DownloadError(f"HTTP {response.status}")
                
            content = await page.content()
            content_type = response.headers.get("content-type", "text/html")
            
            # Playwright returns HTML string, encode it
            return content.encode("utf-8"), content_type
            
        except PlaywrightTimeoutError:
            raise DownloadError("Timeout")
        finally:
            await browser.close()

async def download_file(url: str, source_type: str = "AMC Website") -> Tuple[bytes, str]:
    """
    Downloads a file, automatically routing based on domain policy.
    If HTML is returned for a document type (ISID, KIM), attempts PDF discovery.
    """
    policy = get_policy(url)
    route = policy["route"]
    timeout = policy["timeout_seconds"]
    
    content, content_type = b"", ""
    retries = 3
    
    for attempt in range(retries):
        try:
            if route == "static":
                content, content_type = await _download_static(url, timeout)
            elif route == "dynamic":
                content, content_type = await _download_dynamic(url, timeout)
            elif route == "waf":
                content, content_type = await _download_dynamic(url, timeout, is_waf=True)
                
            # Document Type Healing (PDF Discovery)
            if source_type in ["ISID", "KIM", "SID", "Factsheet", "SEBI Circular", "AMFI Circular"]:
                # If we got HTML but wanted a PDF document
                if "html" in content_type.lower():
                    pdf_link = discover_pdf_links(content, url)
                    if pdf_link:
                        logger.info(f"Discovered PDF link: {pdf_link}")
                        # Fetch the PDF statically since we have the direct link now
                        content, content_type = await _download_static(pdf_link, timeout)
                        
            return content, content_type
            
        except (httpx.HTTPStatusError, httpx.RequestError, DownloadError) as e:
            if attempt == retries - 1:
                status_code = getattr(e, "response", None)
                if status_code:
                    status_code = status_code.status_code
                    logger.error(f"HTTP error downloading {url}: {status_code}")
                    raise DownloadError(f"HTTP {status_code}")
                raise DownloadError(f"Request failed: {str(e)}")
            await asyncio.sleep(2 ** attempt)
            
    raise DownloadError("Max retries exceeded")
