import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import sys

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env from parent directory
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)

sender = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_APP_PASSWORD")

msg = MIMEText("SMTP test successful.")
msg["Subject"] = "SMTP Test"
msg["From"] = sender
msg["To"] = sender

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.send_message(msg)

print("✅ Email sent successfully")
