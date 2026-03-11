import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def send_agentic_email_alert(recipient_email, top_jobs):
    if not top_jobs:
        return

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")
    
    if not sender or not password:
        logger.error("Email credentials missing in .env")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🤖 AI Job Alert: {len(top_jobs)} Top Matches Found"
    msg["From"] = f"🤖 Agentic Job Alert <{sender}>"
    msg["To"] = recipient_email

    rows = ""
    for job in top_jobs:
        rows += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 10px;">
                <strong style="color: #1a73e8;">{job['title']}</strong><br>
                <span style="color: #666;">{job['company']} | {job['location']}</span>
            </td>
            <td style="padding: 10px; text-align: center;">
                <span style="background: #e8f0fe; color: #1a73e8; padding: 4px 8px; border-radius: 4px; font-weight: bold;">
                    {job['ai_score']}/10
                </span>
            </td>
            <td style="padding: 10px;">
                <p style="margin: 0; font-size: 0.9em; color: #444;">{job['ai_analysis']}</p>
            </td>
            <td style="padding: 10px; text-align: center;">
                <a href="{job['link']}" style="background: #1a73e8; color: white; padding: 6px 12px; text-decoration: none; border-radius: 4px;">View</a>
            </td>
        </tr>
        """

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 800px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px;">🤖 Agentic Job Recommendations</h2>
                <p>Based on your preferences, our local AI has identified the following top job matches:</p>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f8f9fa;">
                            <th style="padding: 10px; text-align: left;">Job Details</th>
                            <th style="padding: 10px;">AI Score</th>
                            <th style="padding: 10px; text-align: left;">AI Reasoning</th>
                            <th style="padding: 10px;">Link</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
                <p style="font-size: 0.8em; color: #888; margin-top: 20px;">
                    This email was generated locally using Ollama and your Agentic Job Alert system.
                </p>
            </div>
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            logger.info(f"Email alert sent to {recipient_email}")
            return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
