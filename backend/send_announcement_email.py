#!/usr/bin/env python3
"""
send_announcement_email.py
Broadcast or send test emails using the exact HTML email template with dynamic {{username}} and cid:logo image attachment.

Usage:
  python3 send_announcement_email.py --test            (Sends test email to santushtkotai1221@gmail.com and hello@sharexpress.in)
  python3 send_announcement_email.py --all             (Broadcasts email to all users in MongoDB `interleet.users`)
  python3 send_announcement_email.py --recipient foo@bar.com  (Send to specific email)
"""

import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
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
    from_name = os.getenv("SMTP_FROM_NAME", "Interleet")

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

def get_logo_image():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(backend_dir, "email_templates", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header("Content-ID", "<logo>")
            img.add_header("Content-Disposition", "inline", filename="logo.png")
            return img
    return None

def send_email(smtp_server, config, to_email, username, raw_html_template):
    msg = MIMEMultipart("related")
    msg["Subject"] = "Interleet is Now Free"
    msg["From"] = f"{config['from_name']} <{config['from_email']}>"
    msg["To"] = to_email

    # Personalize {{username}}
    personalized_html = raw_html_template.replace("{{username}}", username)

    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)

    plain_text = f"""
Hey {username},

Interleet is Now Free. Everything you need to practice real-world software engineering—now available to everyone at no cost.

Starting today, every developer can access Interleet completely for free. Along with free access, you now get your own Personalized AI Assistant that learns how you code and helps you improve faster.

Your Personalized AI can...
✓ Review your code and explain mistakes.
✓ Recommend challenges based on your strengths and weaknesses.
✓ Help debug production-style problems with detailed guidance.
✓ Create a personalized roadmap to become interview and industry ready.

Access Interleet Free: https://interleet.sharexpress.in/app/challenges

Learn by building.
Improve with AI.
Ship with confidence.

No subscriptions. No hidden charges. Just real engineering practice with AI.
"""
    msg_alternative.attach(MIMEText(plain_text, "plain"))
    msg_alternative.attach(MIMEText(personalized_html, "html"))

    # Attach logo inline
    logo_img = get_logo_image()
    if logo_img:
        msg.attach(logo_img)

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

    raw_html_template = get_html_template()

    # Determine recipients: [(email, username)]
    targets = []

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db = client["interleet"]

    if args.test:
        targets = [
            ("santushtkotai1221@gmail.com", "Santusht"),
            ("hello@sharexpress.in", "Sharexpress Team")
        ]
    elif args.recipient:
        name = args.recipient.split("@")[0].capitalize()
        targets = [(args.recipient, name)]
    elif args.all:
        users = list(db.users.find({"email": {"$exists": True, "$ne": None}}))
        seen = set()
        for u in users:
            email = u.get("email")
            if email and email not in seen:
                seen.add(email)
                uname = u.get("username") or u.get("full_name") or email.split("@")[0].capitalize()
                targets.append((email, uname))
        print(f"Loaded {len(targets)} recipient(s) from MongoDB `interleet.users`.")
    else:
        print("Please specify --test, --all, or --recipient <email>")
        sys.exit(0)

    print(f"Connecting to Hostinger SMTP server {config['host']}:{config['port']}...")
    server = smtplib.SMTP_SSL(config["host"], config["port"])
    server.login(config["username"], config["password"])

    print(f"Sending campaign to {len(targets)} recipient(s)...")
    success_count = 0

    for email, uname in targets:
        try:
            send_email(server, config, email, uname, raw_html_template)
            print(f"  ✅ Sent successfully to: {email} (Hey {uname})")
            success_count += 1
        except Exception as e:
            print(f"  ❌ Failed sending to {email}: {e}")

    server.quit()
    print(f"\n🎉 Campaign Finished! Successfully sent {success_count} / {len(targets)} emails.")

if __name__ == "__main__":
    main()
