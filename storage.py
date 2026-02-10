import sqlite3
import os
from datetime import datetime


class JobDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to jobs.db in the same directory as this script
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs.db")
            
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                url TEXT,
                date_found TEXT,
                sent_alert INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def is_job_new(self, job_id):
        cursor = self.conn.execute(
            "SELECT 1 FROM jobs WHERE id = ?",
            (job_id,)
        )
        return cursor.fetchone() is None

    def add_job(self, job):
        self.conn.execute("""
            INSERT INTO jobs (id, title, company, location, url, date_found, sent_alert)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (
            job["id"],
            job["title"],
            job["company"],
            job["location"],
            job["url"],
            datetime.utcnow().isoformat()
        ))
        self.conn.commit()
