import asyncio
import random
import urllib.parse
from playwright.async_api import async_playwright

class CompanyScraper:
    def __init__(self, companies):
        self.companies = companies
        self.results = []

    async def _search_company(self, company, page):
        """
        Uses DuckDuckGo to find career pages strict to the company domain.
        Query: site:{domain} ("AI" OR "Machine Learning" OR "Data Scientist") India
        """
        name = company["name"]
        domain = company.get("domain")
        
        if not domain:
            print(f"[WARN] Skipping {name} - No domain found")
            return

        # Simplified strict query
        query = f'site:{domain} ("AI" OR "Machine Learning" OR "Data Scientist") India'
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://duckduckgo.com/?q={encoded_query}&kl=in-en"

        try:
            print(f"[SEARCH] {name} ({domain})...")
            await page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(random.randint(2000, 4000))

            results = await page.query_selector_all("article")
            if not results:
                 results = await page.query_selector_all(".result")
            if not results:
                 results = await page.query_selector_all(".react-results--main li")

            print(f"[INFO] {name}: Found {len(results)} raw results")

            seen_urls = set()
            for i, res in enumerate(results[:5]): 
                try:
                    title_el = await res.query_selector("a[data-testid='result-title-a']")
                    if not title_el:
                         title_el = await res.query_selector("h2 a")
                    if not title_el:
                         title_el = await res.query_selector(".result__a")
                        
                    if title_el:
                        title = await title_el.inner_text()
                        link = await title_el.get_attribute("href")
                        
                        if not link:
                            continue
                        
                        # Safe print for Windows
                        safe_title = title.encode('ascii', 'ignore').decode('ascii')
                        print(f"  ? Checking: {safe_title} ({link})")

                        if link in seen_urls:
                            continue
                            
                        # Strict domain check
                        # Relaxed check: verify domain is somewhere in the URL
                        if domain not in link:
                            # Handle subdomains like careers.tcs.com vs tcs.com
                            # If domain is tcs.com, careers.tcs.com is fine.
                            # But if link is linkedin.com, it is not.
                            print(f"    -> [SKIP] Domain mismatch (Expected {domain})")
                            continue
                            
                        # Negative filtering
                        bad_keywords = ["news", "blog", "press", "article", "investor", "policy"]
                        if any(bk in link.lower() for bk in bad_keywords):
                            print(f"    -> [SKIP] Keyword filter")
                            continue

                        seen_urls.add(link)
                        
                        self.results.append({
                            "company": name,
                            "title": title.strip(),
                            "url": link,
                            "source": "Career Page"
                        })
                    else:
                        print(f"  [WARN] Result {i}: Could not find title element")
                except Exception as e:
                    print(f"  [WARN] Result {i}: Extraction error {e}")
                    continue
                    
        except Exception as e:
            print(f"[ERROR] Error searching for {name}: {e}")

    async def scrape(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            
            # Process in chunks to avoid overwhelming everything
            chunk_size = 5
            for i in range(0, len(self.companies), chunk_size):
                chunk = self.companies[i:i+chunk_size]
                
                page = await context.new_page()
                for company in chunk:
                    await self._search_company(company, page)
                    await page.wait_for_timeout(random.randint(1000, 3000))
                
                await page.close()
                print(f"Processed batch {i}-{i+chunk_size}")

            await browser.close()
        
        return self.results
