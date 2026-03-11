import sqlite3
import json
from datetime import datetime
import os

class JobStore:
    def __init__(self, db_path="jobs_agentic.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    link TEXT UNIQUE,
                    source TEXT,
                    raw_data TEXT,
                    ai_score REAL,
                    ai_analysis TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_job(self, job_data, ai_score=0.0, ai_analysis=""):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO jobs (title, company, location, link, source, raw_data, ai_score, ai_analysis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job_data['title'],
                    job_data['company'],
                    job_data['location'],
                    job_data['link'],
                    job_data['source'],
                    json.dumps(job_data),
                    ai_score,
                    ai_analysis
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving job: {e}")
            return False

    def get_all_jobs(self, min_score=0.0):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM jobs WHERE ai_score >= ? ORDER BY ai_score DESC, created_at DESC", (min_score,))
            return [dict(row) for row in cursor.fetchall()]

    def clear_jobs(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM jobs")
            conn.commit()
