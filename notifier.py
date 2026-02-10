import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_alert(new_jobs):
    if not new_jobs:
        return

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")
    recipient = os.getenv("EMAIL_ADDRESS")

    if not sender or not password:
        print("❌ EMAIL_ADDRESS or EMAIL_APP_PASSWORD not set in .env")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Top 250 Companies Job Alert ({len(new_jobs)} new jobs)"
    msg["From"] = sender
    msg["To"] = recipient

    rows = ""
    for job in new_jobs:
        rows += f"""
        <tr>
            <td>{job['company']}</td>
            <td>{job['title']}</td>
            <td><a href="{job['url']}">View Job</a></td>
            <td>{job['source']}</td>
        </tr>
        """

    html = f"""
    <html>
        <body>
            <h3>New Jobs from Top 250 Companies</h3>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Company</th>
                    <th>Title</th>
                    <th>Link</th>
                    <th>Source</th>
                </tr>
                {rows}
            </table>
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"✅ Email sent with {len(new_jobs)} new jobs.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
