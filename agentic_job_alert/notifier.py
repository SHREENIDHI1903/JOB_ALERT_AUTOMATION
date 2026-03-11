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

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"LinkedIn Job Alert ({len(new_jobs)} new jobs)"
    msg["From"] = sender
    msg["To"] = recipient

    rows = ""
    for job in new_jobs:
        rows += f"""
        <tr>
            <td>{job['title']}</td>
            <td>{job['company']}</td>
            <td>{job['location']}</td>
            <td><a href="{job['url']}">View</a></td>
        </tr>
        """

    html = f"""
    <html>
        <body>
            <h3>New LinkedIn Jobs Found</h3>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Title</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Link</th>
                </tr>
                {rows}
            </table>
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
