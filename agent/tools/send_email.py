import os, smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", "no-reply@example.com")

def send_email(to: str, subject: str, html: str) -> dict:
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        return {"status": "error", "reason": "SMTP non configuré"}

    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Agent LLM", SMTP_FROM))
    msg["To"] = to

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, [to], msg.as_string())

    return {"status": "sent", "to": to}
