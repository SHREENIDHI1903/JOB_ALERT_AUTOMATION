import asyncio
from scraper import CompanyScraper

# Test with a small subset of companies
test_companies = [
    {"name": "Google India", "domain": "careers.google.com"},
    {"name": "TCS", "domain": "tcs.com"}
]

async def test_scraper():
    print("[TEST] Testing Scraper with 2 companies...")
    scraper = CompanyScraper(test_companies)
    results = await scraper.scrape()
    
    print(f"\n[DONE] Scraper finished. Found {len(results)} jobs.")
    for job in results:
        print(f"   - [{job['company']}] {job['title']}")

if __name__ == "__main__":
    asyncio.run(test_scraper())
