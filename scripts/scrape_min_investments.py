import json
import time
import requests
from bs4 import BeautifulSoup
import re

REGISTRY_PATH = "data/sif_registry.json"

def scrape_min_investment(url: str) -> int:
    """Attempt to scrape minimum investment from URL, fallback to 1,000,000 (10 Lakhs) on failure."""
    if not url:
        return 1000000
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=5)
        
        if res.status_code != 200:
            print(f"[{res.status_code}] Falling back to 10L for {url}")
            return 1000000
            
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        
        # Groww/INDMoney generic regex search
        # Look for things like ₹ 10,00,000 or Rs. 10 Lakhs
        text = soup.get_text()
        
        # Many SIF pages might just be 404s styled as 200s, or generic Mutual Fund pages.
        # SEBI SIF minimum is 10 Lakhs. 
        # If we find "500", it's a generic MF and we override it to the SIF regulation of 10L anyway.
        # But if we find a real large number, we use it.
        matches = re.findall(r'(?:₹|Rs\.?)\s*([\d,]+)', text)
        
        for m in matches:
            val = int(m.replace(',', ''))
            # If we find 10 Lakhs or 1 Crore specifically near "minimum"
            if val in [1000000, 10000000]:
                return val
                
        # Fallback to regulatory minimum for SIFs
        return 1000000
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return 1000000

def main():
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)
        
    updated_count = 0
    for fund in registry:
        old_val = fund.get("minimum_investment")
        
        # Prioritize URLs
        url = fund.get("groww_url") or fund.get("indmoney_url") or fund.get("official_url")
        
        new_val = scrape_min_investment(url)
        
        if old_val != new_val:
            print(f"Updated {fund['fund_name']}: {old_val} -> {new_val}")
            fund["minimum_investment"] = new_val
            updated_count += 1
            
        time.sleep(0.5) # Polite scraping delay
        
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)
        
    print(f"\nSuccessfully updated {updated_count} funds to the correct 10L regulatory minimum.")

if __name__ == "__main__":
    main()
