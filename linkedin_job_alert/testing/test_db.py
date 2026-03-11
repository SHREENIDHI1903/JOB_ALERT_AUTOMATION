import sys
import os
import tempfile

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from storage import JobDatabase

# Create a temporary file for the test database
with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
    db_path = tmp_db.name

try:
    print(f"Testing with temporary DB: {db_path}")
    db = JobDatabase(db_path)

    job = {
        "id": "test-job-123",
        "title": "Test Engineer",
        "company": "Test Corp",
        "location": "Remote",
        "url": "https://example.com"
    }

    print("Is new job?", db.is_job_new(job["id"]))
    db.add_job(job)
    print("Is new job after insert?", db.is_job_new(job["id"]))

finally:
    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Cleaned up temporary test database")
