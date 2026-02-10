import asyncio
import json
import os
import logging
from dotenv import load_dotenv

# Load .env from parent directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(PARENT_DIR, "linkedin_job_alert", ".env")) # Correct path to .env

from scraper import CompanyScraper
from storage import JobDatabase
from notifier import send_email_alert

# Setup logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_companies():
    config_path = os.path.join(BASE_DIR, "companies.json")
    with open(config_path, "r") as f:
        return json.load(f)

async def main():
    print("🚀 Starting Top 250 Companies Job Alert...")
    companies = load_companies()
    
    scraper = CompanyScraper(companies)
    db = JobDatabase()
    
    print(f"🔍 Scraping {len(companies)} companies for 'AI ML Engineer' roles...")
    scraped_jobs = await scraper.scrape()
    
    new_jobs = []
    print(f"📊 Found {len(scraped_jobs)} potential jobs.")
    
    for job in scraped_jobs:
        if db.is_job_new(job["url"]):
            db.add_job(job)
            new_jobs.append(job)
            print(f"   [NEW] {job['company']}: {job['title']}")
    
    if new_jobs:
        print(f"📧 Sending email for {len(new_jobs)} new jobs...")
        send_email_alert(new_jobs)
    else:
        print("😴 No new unique jobs found.")

if __name__ == "__main__":
    asyncio.run(main())
