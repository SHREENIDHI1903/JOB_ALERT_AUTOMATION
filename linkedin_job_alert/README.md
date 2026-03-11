# LinkedIn Job Alert Bot 🤖

A Python bot that scrapes LinkedIn for new jobs matching your criteria and emails you alerts. It runs locally on your machine.

## 🚀 Quick Start

### 1. Install Dependencies
Open a terminal in this folder:
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Email
Create a file named `.env` in this folder (if not already there) and add your Gmail App Password credentials:
```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_16_char_app_password
```
*(See guide inside `project_guide.md` if you need help generating an App Password)*

### 3. Customize Search
Edit `config.json` to change keywords or location:
```json
{
    "check_interval_hours": 4,
    "linkedin_urls": [
        "https://www.linkedin.com/jobs/search/?keywords=AI%20ML%20Engineer&f_E=1%2C2&location=India"
    ],
    "max_scrolls": 6
}
```

### 4. Login (One-Time Setup)
You must save your LinkedIn login session so the bot doesn't get blocked.
Run this command:
```bash
python save_cookies.py
```
- A browser window will open.
- Log in to LinkedIn manually.
- Wait for the home feed to load.
- The script will save `linkedin_cookies.json` and close automatically.

---

## ▶️ How to Run
Once setup is done, start the bot:

```bash
python main.py
```

- It will run effectively immediately.
- It will check for **new** jobs (deduplicated against `jobs.db`).
- It will send you an email if new jobs are found.
- It will keep running and check again every 4 hours.

## 🕒 Running in the Background (Optional)

If you don't want to keep a terminal window open 24/7, you can use **Windows Task Scheduler**.

1.  **Open Task Scheduler** (Search in Start Menu).
2.  **Create Basic Task** -> Name it "LinkedIn Job Alert".
3.  **Trigger**: "Daily" -> Recur every 1 day -> Start anytime.
4.  **Action**: "Start a program".
    - **Program/script**: `path\to\python.exe` (Find it with `where python` in terminal).
    - **Add arguments**: `d:\Personal_Projects\JOB_ALERT\linkedin_job_alert\main.py`
    - **Start in**: `d:\Personal_Projects\JOB_ALERT\linkedin_job_alert`
5.  **Finish**.
6.  **Properties**: Right-click the task -> Properties -> Triggers -> Edit.
    - Check "Repeat task every:" -> "4 hours".
    - "for a duration of:" -> "Indefinitely".

**Note:** If you use Task Scheduler, you should **comment out** the `schedule` loop at the bottom of `main.py` so it just runs once and exits, letting Windows handle the repetition.

## 📂 Files
- `main.py`: The entry point and scheduler.
- `scraper.py`: Playwright script that navigates LinkedIn.
- `notifier.py`: Sends the email alerts.
- `storage.py`: Manages the SQLite database (`jobs.db`) to avoid duplicate alerts.
- `app.log`: Check this if something goes wrong.
