import time
import random
import logging
import os
from playwright.sync_api import sync_playwright


class LinkedInScraper:
    """
    Scrapes LinkedIn job search result pages using Playwright.

    REQUIREMENTS:
    - Must be logged in (cookies via storage_state)
    - Scrolls the LEFT job list container (not the page)
    """

    def __init__(self, urls, max_scrolls=5):
        self.urls = urls
        self.max_scrolls = max_scrolls

        # Absolute path to cookies to avoid path issues
        self.cookie_path = os.path.join(
            os.path.dirname(__file__),
            "linkedin_cookies.json"
        )

    def _human_sleep(self, a=2, b=4):
        time.sleep(random.uniform(a, b))

    def scrape(self):
        jobs = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = browser.new_context(
                storage_state=self.cookie_path,
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800}
            )

            page = context.new_page()

            for url in self.urls:
                try:
                    # Load page and wait for LinkedIn JS to settle
                    page.goto(url, wait_until="networkidle", timeout=60000)
                    page.wait_for_timeout(5000)

                    print("Current URL after goto:", page.url)

                    # ---- CRITICAL PART: scroll LEFT jobs list container ----
                    # Try multiple possible selectors for the jobs list container
                    container_selectors = [
                        "div.jobs-search-results-list",
                        "div.scaffold-layout__list-container",
                        ".jobs-search__results-list",
                        ".jobs-search-results"
                    ]
                    
                    jobs_container = None
                    for selector in container_selectors:
                        try:
                            element = page.query_selector(selector)
                            if element:
                                jobs_container = element
                                print(f"[INFO] Found jobs container with selector: {selector}")
                                break
                        except Exception:
                            continue

                    if jobs_container:
                        for _ in range(self.max_scrolls):
                            jobs_container.evaluate(
                                "(el) => { el.scrollTop = el.scrollHeight; }"
                            )
                            self._human_sleep()
                    else:
                        print("[WARN] Jobs list container not found, attempting body scroll fallback")
                        # Fallback to body scroll if specific container not found
                        for _ in range(self.max_scrolls):
                            page.mouse.wheel(0, 2000)
                            self._human_sleep()

                    # ---- Stable selector for job cards ----
                    # Try multiple selectors for job cards
                    job_cards = []
                    card_selectors = [
                        'li[data-entity-urn^="urn:li:jobPosting"]',
                        '.jobs-search-results__list-item',
                        'div.job-card-container',
                        'li.jobs-search-results__list-item'
                    ]

                    for selector in card_selectors:
                        found_cards = page.query_selector_all(selector)
                        if found_cards:
                            job_cards = found_cards
                            print(f"[INFO] Found {len(job_cards)} job cards with selector: {selector}")
                            break
                    
                    if not job_cards:
                        print("[ERROR] No job cards found with any selector")
                        # Debug: Save page content
                        with open("debug_page.html", "w", encoding="utf-8") as f:
                            f.write(page.content())
                        print("[INFO] Saved page content to debug_page.html")

                    for card in job_cards:
                        try:
                            # Job ID (stable identifier)
                            job_id = card.get_attribute("data-entity-urn")
                            if not job_id:
                                # Try extracting from data-job-id if urn is missing
                                job_id = card.get_attribute("data-job-id")
                            
                            if not job_id:
                                continue

                            # Title (inside job card)
                            title_el = card.query_selector("h3.base-search-card__title") or \
                                       card.query_selector(".job-card-list__title") or \
                                       card.query_selector("strong") or \
                                       card.query_selector(".artdeco-entity-lockup__title")
                            title = title_el.inner_text().strip() if title_el else "Unknown Title"

                            # Company
                            company_el = card.query_selector("h4.base-search-card__subtitle") or \
                                         card.query_selector(".job-card-container__primary-description") or \
                                         card.query_selector(".job-card-container__company-name") or \
                                         card.query_selector(".artdeco-entity-lockup__subtitle")
                            company = company_el.inner_text().strip() if company_el else "Unknown Company"

                            # Location
                            location_el = card.query_selector("span.job-search-card__location") or \
                                          card.query_selector(".job-card-container__metadata-item") or \
                                          card.query_selector(".artdeco-entity-lockup__caption")
                            location = location_el.inner_text().strip() if location_el else "Unknown Location"

                            # Job link
                            link_el = card.query_selector('a[href*="/jobs/view/"]') or \
                                      card.query_selector('a.job-card-container__link') or \
                                      card.query_selector('a.job-card-list__title') or \
                                      card.query_selector('a.artdeco-entity-lockup__title')
                            
                            job_url = link_el.get_attribute("href") if link_el else ""
                            # Ensure URL is absolute
                            if job_url and not job_url.startswith("http"):
                                job_url = "https://www.linkedin.com" + job_url

                            jobs.append({
                                "id": job_id,
                                "title": title,
                                "company": company,
                                "location": location,
                                "url": job_url
                            })

                        except Exception:
                            logging.exception("Failed parsing job card")

                except Exception:
                    logging.exception(f"Failed scraping URL: {url}")

            browser.close()

        return jobs
