from playwright.sync_api import sync_playwright
import time
import os

def capture_screenshots():
    os.makedirs("docs/screenshots", exist_ok=True)
    with sync_playwright() as p:
        # Check if browser needs to be installed or just use system chromium
        try:
            browser = p.chromium.launch()
        except Exception as e:
            import subprocess
            subprocess.run(["playwright", "install", "chromium"])
            browser = p.chromium.launch()

        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        print("Navigating to http://localhost:5173")
        page.goto("http://localhost:5173")
        
        # Dismiss any tour popups by clicking 'Skip' if present
        try:
            page.wait_for_selector("text=SIF Terminal", timeout=10000)
            time.sleep(2)
            skip_btn = page.locator("button:has-text('Skip')")
            if skip_btn.is_visible():
                skip_btn.click()
            time.sleep(1)
        except Exception as e:
            pass

        print("Capturing Home Page...")
        page.screenshot(path="docs/screenshots/home.png")
        
        print("Navigating to Market Explorer...")
        page.click("text=Market Explorer")
        # removed wait_for_selector
        time.sleep(2)
        page.screenshot(path="docs/screenshots/market_explorer.png")
        
        print("Navigating to Insights/Corpus Intelligence...")
        try:
            page.click("text=Corpus Intelligence")
            time.sleep(2)
            page.screenshot(path="docs/screenshots/corpus_intelligence.png")
        except:
            pass

        print("Navigating back to Research...")
        page.click("text=Research")
        time.sleep(2)
        
        print("Submitting query...")
        page.fill("input[placeholder*='Ask anything']", "Explain exit load constraints for SIFs")
        page.keyboard.press("Enter")
        
        print("Waiting for response...")
        try:
            # Wait for citations to load
            page.wait_for_selector("text=Source", timeout=15000)
            time.sleep(3)
            page.screenshot(path="docs/screenshots/rag_answer.png")
            
            # Click the first source to open Evidence Explorer
            print("Opening Evidence Explorer...")
            page.click("text=Source 1")
            time.sleep(2)
            page.screenshot(path="docs/screenshots/evidence_explorer.png")
        except Exception as e:
            print("Could not capture RAG answer:", e)

        browser.close()

if __name__ == "__main__":
    capture_screenshots()
