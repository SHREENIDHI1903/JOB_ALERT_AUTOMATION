import asyncio
from playwright.async_api import async_playwright
import urllib.parse

async def debug_ddg():
    async with async_playwright() as p:
        # Use Chromium for DDG often works better than Firefox for automation detection sometimes?
        # But let's stick to what we know.
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        queries = [
            'site:tcs.com "AI ML Engineer" India',
            'TCS careers "AI ML Engineer" India',
            'TCS "AI ML Engineer" jobs India',
            'site:careers.google.com "AI ML Engineer" India'
        ]
        
        for query in queries:
            print(f"\n--- Testing Query: {query} ---")
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://duckduckgo.com/?q={encoded_query}&kl=in-en"
            
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
                await page.wait_for_timeout(3000)
                
                # Check for "No results"
                no_results = await page.query_selector("text='No results found'")
                if no_results:
                    print("❌ No results found.")
                    continue

                # Try finding result content
                # Selector for result titles in DDG often changes, generic approach:
                links = await page.query_selector_all("a[data-testid='result-title-a']")
                if not links:
                     # Fallback
                     links = await page.query_selector_all("article h2 a")
                
                print(f"✅ Found {len(links)} result links.")
                for l in links[:3]:
                    txt = await l.inner_text()
                    href = await l.get_attribute("href")
                    print(f"   -> {txt} ({href})")
                    
            except Exception as e:
                print(f"Error: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_ddg())
