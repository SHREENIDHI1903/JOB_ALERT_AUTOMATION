import logging
import random
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobScraper:
    def __init__(self, headless=True):
        self.headless = headless

    def _human_delay(self, min_s=2, max_s=5):
        time.sleep(random.uniform(min_s, max_s))

    def scrape_linkedin_jobs(self, search_url, max_pages=1):
        """
        Scrapes LinkedIn job search results.
        """
        jobs = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                logger.info(f"Navigating to {search_url}")
                page.goto(search_url, wait_until="networkidle")
                self._human_delay(3, 6)

                # Simple initial scroll
                for _ in range(3):
                    page.mouse.wheel(0, 1000)
                    self._human_delay(1, 2)

                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')

                # Re-using the resilient selectors identified earlier
                card_selectors = [
                    'div.job-search-card',
                    'div.base-card',
                    'li.jobs-search-results__list-item',
                    'div.base-search-card'
                ]

                job_cards = []
                for selector in card_selectors:
                    found = soup.select(selector)
                    if found:
                        job_cards = found
                        logger.info(f"Found {len(job_cards)} jobs using selector: {selector}")
                        break

                for card in job_cards:
                    try:
                        title_tag = card.select_one('.base-search-card__title, .job-search-card__title, h3')
                        company_tag = card.select_one('.base-search-card__subtitle, .job-search-card__subtitle, h4')
                        location_tag = card.select_one('.job-search-card__location, .base-search-card__metadata')
                        link_tag = card.select_one('a[href*="/jobs/view/"]')

                        if title_tag and link_tag:
                            job_data = {
                                "title": title_tag.get_text(strip=True),
                                "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                                "location": location_tag.get_text(strip=True) if location_tag else "N/A",
                                "link": link_tag['href'].split('?')[0],
                                "source": "LinkedIn"
                            }
                            jobs.append(job_data)
                    except Exception as e:
                        logger.error(f"Error parsing job card: {e}")

            except Exception as e:
                logger.error(f"Scraping failed: {e}")
            finally:
                browser.close()

        return jobs
