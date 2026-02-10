import os
import json
import time
import logging
import schedule
from dotenv import load_dotenv

load_dotenv()
from scraper import LinkedInScraper
from storage import JobDatabase
from notifier import send_email_alert


# Get the absolute path of the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "app.log"),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config():
    config_path = os.path.join(BASE_DIR, "config.json")
    with open(config_path, "r") as f:
        return json.load(f)


def job_run():
    try:
        config = load_config()
        scraper = LinkedInScraper(
            config["linkedin_urls"],
            config["max_scrolls"]
        )
        db = JobDatabase()

        scraped_jobs = scraper.scrape()
        new_jobs = []

        for job in scraped_jobs:
            if db.is_job_new(job["id"]):
                db.add_job(job)
                new_jobs.append(job)

        send_email_alert(new_jobs)

    except Exception:
        logging.exception("Fatal error in job run")


if __name__ == "__main__":
    config = load_config()
    hours = config["check_interval_hours"]

    job_run()  # run immediately
    schedule.every(hours).hours.do(job_run)

    while True:
        schedule.run_pending()
        time.sleep(60)
