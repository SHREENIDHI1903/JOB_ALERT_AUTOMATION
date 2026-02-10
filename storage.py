import sqlite3
import os
from datetime import datetime


class JobDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to top_250_jobs.db in the same directory as this script
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "top_250_jobs.db")
            
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                url TEXT PRIMARY KEY,
                company TEXT,
                title TEXT,
                source TEXT,
                date_found TEXT,
                sent_alert INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def is_job_new(self, job_url):
        cursor = self.conn.execute(
            "SELECT 1 FROM jobs WHERE url = ?",
            (job_url,)
        )
        return cursor.fetchone() is None

    def add_job(self, job):
        try:
            self.conn.execute("""
                INSERT INTO jobs (url, company, title, source, date_found, sent_alert)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (
                job["url"],
                job["company"],
                job["title"],
                job["source"],
                datetime.utcnow().isoformat()
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass # Already exists
