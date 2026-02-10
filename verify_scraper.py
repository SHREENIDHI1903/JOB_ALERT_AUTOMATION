
import asyncio
from scraper import CompanyScraper

async def verify():
    # Test strict search with a few companies
    companies = [
        {"name": "TCS", "domain": "tcs.com"},
        {"name": "Infosys", "domain": "infosys.com"},
        {"name": "Google", "domain": "careers.google.com"} 
    ]
    
    print("[TEST] Verifying Strict Scraper...")
    scraper = CompanyScraper(companies)
    results = await scraper.scrape()
    
    print(f"\n[DONE] Found {len(results)} jobs.")
    for job in results:
        print(f"   - [{job['company']}] {job['title']} ({job['url']})")

if __name__ == "__main__":
    asyncio.run(verify())
