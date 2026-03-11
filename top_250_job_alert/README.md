# Top 250 Companies Job Alert 🏢

A specialized scraper that searches for "AI ML Engineer" roles across the top ~50+ Indian companies using search engine queries (DuckDuckGo).

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install firefox
```
*Note: This scraper uses Firefox to rotate browser fingerprints.*

### 2. Configure Email
The bot is designed to **reuse your existing credentials** from the `linkedin_job_alert` folder.

-   It looks for `.env` at: `../linkedin_job_alert/.env`
-   **You do NOT need to create a new `.env` file here.**
-   If you want to use different credentials, you *can* create a `.env` file in this folder, but you must edit `main.py` to remove the parent directory loading logic.

### 3. Run the Bot
```bash
python main.py
```

## ⚙️ How it works
1.  Loads `companies.json` (List of top companies).
2.  Queries DuckDuckGo: `site:company.com "AI ML Engineer" India`.
3.  Extracts job titles and links.
4.  Storage: Saves to `top_250_jobs.db` to avoid duplicates.
5.  Notify: Sends an email summary.

## 📂 Files
- `main.py`: Entry point.
- `scraper.py`: Async scraper using Playwright & DuckDuckGo.
- `companies.json`: Configurable list of target companies.
- `storage.py`: SQLite database manager.
- `notifier.py`: Email sender.
