#!/usr/bin/env python3
"""
send_announcement_email.py
Broadcast or send test emails using the refined HTML template with dynamic {{username}} and inline logo.png.

Usage:
  python3 send_announcement_email.py --test              (Sends test email to santushtkotai1221@gmail.com and hello@sharexpress.in)
  python3 send_announcement_email.py --on-platform       (Sends email to registered platform users in MongoDB interleet.users)
  python3 send_announcement_email.py --off-platform      (Sends email to off-platform candidate leads in candidates_info.json)
  python3 send_announcement_email.py --all               (Sends to BOTH on-platform users and off-platform lead candidates)
  python3 send_announcement_email.py --recipient foo@bar.com  (Send to specific email)
"""

import os
import sys
import json
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
    msg["Subject"] = "🎉 Great News! Interleet Is Now Free"
    msg["From"] = f"{config['from_name']} <{config['from_email']}>"
    msg["To"] = to_email

    # Personalize {{username}}
    personalized_html = raw_html_template.replace("{{username}}", username)

    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)

    plain_text = f"""
Hey {username},

We built Interleet to help developers practice what companies actually expect during placements and interviews—not just solve theoretical coding problems.

Today, we're excited to announce that Interleet is completely free for everyone. Whether you're preparing for campus placements, internships, or software engineering roles, you now have full access to our interactive platform.

Everything You Can Access:
✓ Personalized AI Mentor - Receive learning recommendations based on your performance.
✓ AI Mock Interviews - Practice realistic technical interviews with AI.
✓ Professional Coding Challenges - Solve frontend, backend, DevOps, database, system design, and full-stack problems.
✓ Interactive Browser Sandbox - Write, compile, execute, and debug code instantly.
✓ Instant AI Code Reviews - Get explanations and debugging assistance.
✓ Leaderboards & Progress Tracking.

Start Learning for Free: https://interleet.sharexpress.in/app/challenges

Learn real skills.
Practice with AI.
Ace your next interview.

No subscriptions. No setup required. Just open your browser and start building.
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
    parser.add_argument("--on-platform", action="store_true", help="Send to registered users in MongoDB interleet.users")
    parser.add_argument("--off-platform", action="store_true", help="Send to candidate lead emails in candidates_info.json")
    parser.add_argument("--all", action="store_true", help="Broadcast email to BOTH on-platform users and off-platform candidates")
    parser.add_argument("--recipient", type=str, help="Send email to a specific recipient address")

    args = parser.parse_args()

    config = load_config()
    if not config["password"]:
        print("❌ Error: SMTP_PASSWORD is not set in .env")
        sys.exit(1)

    raw_html_template = get_html_template()

    # Determine recipients: [(email, username)]
    targets = []
    seen = set()

    # 1. On-platform users (MongoDB)
    if args.on_platform or args.all:
        try:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
            client = MongoClient(mongo_uri)
            db = client["interleet"]
            users = list(db.users.find({"email": {"$exists": True, "$ne": None}}))
            for u in users:
                email = u.get("email")
                if email and email not in seen:
                    seen.add(email)
                    uname = u.get("username") or u.get("full_name") or email.split("@")[0].capitalize()
                    targets.append((email, uname))
            print(f"Loaded {len(targets)} on-platform registered users from MongoDB.")
        except Exception as e:
            print(f"Warning: Failed to fetch MongoDB users: {e}")

    # 2. Off-platform candidate leads (candidates_info.json)
    if args.off_platform or args.all:
        candidates_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "candidates_info.json")
        if os.path.exists(candidates_file):
            with open(candidates_file, "r") as f:
                candidates = json.load(f)
                cand_count = 0
                for c in candidates:
                    email = c.get("Email") or c.get("email")
                    if email and email not in seen:
                        seen.add(email)
                        name = c.get("Name") or c.get("name") or email.split("@")[0].capitalize()
                        targets.append((email, name))
                        cand_count += 1
                print(f"Loaded {cand_count} off-platform lead candidates from candidates_info.json.")

    # 3. Test or specific recipient
    if args.test:
        targets = [
            ("santushtkotai1221@gmail.com", "Santusht"),
            ("hello@sharexpress.in", "Sharexpress Team")
        ]
    elif args.recipient:
        name = args.recipient.split("@")[0].capitalize()
        targets = [(args.recipient, name)]

    if not targets:
        print("Please specify --test, --on-platform, --off-platform, --all, or --recipient <email>")
        sys.exit(0)

    print(f"Connecting to Hostinger SMTP server {config['host']}:{config['port']}...")
    server = smtplib.SMTP_SSL(config["host"], config["port"])
    server.login(config["username"], config["password"])

    print(f"Sending campaign to {len(targets)} total recipient(s)...")
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
