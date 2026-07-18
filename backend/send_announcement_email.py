#!/usr/bin/env python3
"""
send_announcement_email.py
Broadcast or send test emails announcing platform updates and 100% free access.
Usage:
  python3 send_announcement_email.py --test            (Sends test email to santushtkotai1221@gmail.com and hello@sharexpress.in)
  python3 send_announcement_email.py --all             (Broadcasts email to all users in MongoDB `interleet.users`)
"""

import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pymongo import MongoClient

def load_config():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(backend_dir, ".env"), override=True)

    host = os.getenv("SMTP_HOST", "smtp.hostinger.com")
    port = int(os.getenv("SMTP_PORT", "465"))
    username = os.getenv("SMTP_USERNAME", "noreply@sharexpress.in")
    password = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("SMTP_FROM_EMAIL", "noreply@sharexpress.in")
    from_name = os.getenv("SMTP_FROM_NAME", "Interleet Announcement")

    return {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "from_email": from_email,
        "from_name": from_name,
    }

def get_html_template():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(backend_dir, "email_templates", "platform_announcement.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

def send_email(smtp_server, config, to_email, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🎉 Major Update: Interleet is Now 100% Free for Everyone!"
    msg["From"] = f"{config['from_name']} <{config['from_email']}>"
    msg["To"] = to_email

    plain_text = """
🎉 Major Platform Update: Interleet is Now 100% Free!

We've removed all paywalls and subscription locks on Interleet. 
Experience FAANG-grade interview prep, multi-file engineering sandboxes, 
AI mock interviews, and system design tools completely free.

Feature Highlights:
• 300+ Full-Stack & Systems Challenges (Express, FastAPI, Gin, Multi-File)
• Multi-Database Engine (SQLite, MongoDB, PostgreSQL, MySQL)
• AI Voice & Chat Mock Interviews
• Interactive System Design Studio

Start Practicing Now: https://interleet.sharexpress.in/app/challenges
"""
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    smtp_server.sendmail(config["from_email"], [to_email], msg.as_string())

def main():
    parser = argparse.ArgumentParser(description="Send Interleet Announcement Email Campaign")
    parser.add_argument("--test", action="store_true", help="Send test email to test addresses")
    parser.add_argument("--all", action="store_true", help="Broadcast email to all users in MongoDB")
    parser.add_argument("--recipient", type=str, help="Send email to a specific recipient address")

    args = parser.parse_args()

    config = load_config()
    if not config["password"]:
        print("❌ Error: SMTP_PASSWORD is not set in .env")
        sys.exit(1)

    html_template = get_html_template()

    # Determine recipients
    recipients = []
    if args.test:
        recipients = ["santushtkotai1221@gmail.com", "hello@sharexpress.in"]
    elif args.recipient:
        recipients = [args.recipient]
    elif args.all:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        client = MongoClient(mongo_uri)
        db = client["interleet"]
        users = list(db.users.find({"email": {"$exists": True, "$ne": None}}))
        recipients = list(set([u["email"] for u in users if u.get("email")]))
        print(f"Loaded {len(recipients)} user emails from MongoDB.")
    else:
        print("Please specify --test, --all, or --recipient <email>")
        sys.exit(0)

    print(f"Connecting to Hostinger SMTP server {config['host']}:{config['port']}...")
    server = smtplib.SMTP_SSL(config["host"], config["port"])
    server.login(config["username"], config["password"])

    print(f"Sending campaign to {len(recipients)} recipient(s)...")
    success_count = 0

    for email in recipients:
        try:
            send_email(server, config, email, html_template)
            print(f"  ✅ Sent successfully to: {email}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ Failed sending to {email}: {e}")

    server.quit()
    print(f"\n🎉 Campaign Finished! Successfully sent {success_count} / {len(recipients)} emails.")

if __name__ == "__main__":
    main()
