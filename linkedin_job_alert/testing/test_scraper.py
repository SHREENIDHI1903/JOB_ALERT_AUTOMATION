import sys
import os

# Add parent directory to path to allow importing storage
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from scraper import LinkedInScraper

urls = [
    "https://www.linkedin.com/jobs/search/?keywords=Python%20Developer&location=Remote"
]

scraper = LinkedInScraper(urls, max_scrolls=3)
jobs = scraper.scrape()

print(f"Jobs found: {len(jobs)}")

for job in jobs[:5]:
    print(job)
