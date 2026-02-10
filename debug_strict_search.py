import asyncio
from playwright.async_api import async_playwright
import urllib.parse

async def debug_strict():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        # Test different strict queries for TCS
        # The goal: Find hits on tcs.com, NOT linkedin.com
        queries = [
            'site:tcs.com "AI ML Engineer" India',                 # Original (Failed?)
            'site:tcs.com (AI OR "Machine Learning") India',       # Broader keywords
            'site:tcs.com careers "AI"',                          # Focused on careers
            'site:ibscareers.com "AI Engineer"',                   # Another domain test
            'site:infosys.com "Artificial Intelligence" India'     # Another company
        ]
        
        for query in queries:
            print(f"\n--- Testing Query: {query} ---")
            encoded_query = urllib.parse.quote(query)
            # kl=in-en restricts to India-English region
            search_url = f"https://duckduckgo.com/?q={encoded_query}&kl=in-en"
            
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
                await page.wait_for_timeout(3000)
                
                # Check for "No results"
                no_results = await page.query_selector("text='No results found'")
                if no_results:
                    print(f"[-] No results found for: {query}")
                    continue

                links = await page.query_selector_all("article h2 a")
                if not links:
                     links = await page.query_selector_all("a[data-testid='result-title-a']")
                
                print(f"[+] Found {len(links)} result links.")
                found_any = False
                for l in links[:3]:
                    txt = await l.inner_text()
                    href = await l.get_attribute("href")
                    print(f"   -> {txt} ({href})")
                    found_any = True
                
                if not found_any:
                    print("   (Selectors failed to extract links)")
                    
            except Exception as e:
                print(f"Error: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_strict())
