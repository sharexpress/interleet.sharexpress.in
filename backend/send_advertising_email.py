import os
import sys
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient

# Ensure app directory is in Python path for loading configs
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.core import config

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["interleet"]

# ─────────────────────────────────────────────────────────────────────────────
# HTML Email Template
# ─────────────────────────────────────────────────────────────────────────────
def get_advertisement_template(username: str) -> str:
    brand_logo = """<span style="font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                      INTER<span style="color: #6366f1;">LEET</span>
                    </span>"""

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>20 New Frontend Challenges Live on Interleet</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0c0c0e; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #e4e4e7;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #0c0c0e; padding: 40px 20px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 550px; background-color: #18181b; border: 1px solid #27272a; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.6);">
          <!-- Top Accent Line -->
          <tr>
            <td height="4" style="background-color: #6366f1; line-height: 4px; font-size: 4px;">&nbsp;</td>
          </tr>
          
          <!-- Content Padding -->
          <tr>
            <td style="padding: 40px 30px; text-align: left;">
              
              <!-- Brand Header -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 32px;">
                <tr>
                  <td align="center">
                    {brand_logo}
                  </td>
                </tr>
              </table>

              <!-- Main Title -->
              <h1 style="font-size: 22px; font-weight: 800; margin: 0 0 16px 0; color: #ffffff; text-align: center;">
                🚀 20 New Interactive Frontend Challenges Are Live!
              </h1>
              
              <!-- Greeting -->
              <p style="font-size: 15px; line-height: 1.6; color: #f4f4f5; margin: 0 0 16px 0;">
                Hey {username},
              </p>
              
              <!-- Body Description -->
              <p style="font-size: 15px; line-height: 1.6; color: #a1a1aa; margin: 0 0 20px 0;">
                We have just expanded Interleet's interactive practice suite with <strong>20 brand-new, premium Frontend challenges</strong>. 
                Test your skills in JavaScript, CSS, and DOM manipulation against real-time browser sandbox test cases!
              </p>

              <!-- Features Box -->
              <div style="background-color: #09090b; border: 1px solid #27272a; border-radius: 8px; padding: 20px; margin: 24px 0;">
                <h3 style="font-size: 15px; margin: 0 0 12px 0; color: #6366f1; font-weight: 700;">What's new to build:</h3>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.8; color: #d4d4d8;">
                  <li><strong>Interactive Star Rating Component</strong></li>
                  <li><strong>Dynamic Shopping Cart Subtotal UI</strong></li>
                  <li><strong>Memory Match Card Game (Hard)</strong></li>
                  <li><strong>Autocomplete Dropdown Filter</strong></li>
                  <li><strong>Progress Bar Animator & Timers</strong></li>
                  <li><strong>Collapsible Accordion mutual exclusion menus</strong></li>
                </ul>
              </div>

              <p style="font-size: 15px; line-height: 1.6; color: #a1a1aa; margin: 0 0 28px 0;">
                All challenges execute inside our secure browser sandbox, providing instantaneous visual feedback and validation. Log in today to claim your XP and climb the system leaderboard!
              </p>
              
              <!-- CTA Button -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="center">
                    <a href="https://interleet.sharexpress.in/app/challenges" style="background-color: #6366f1; color: #ffffff; text-decoration: none; padding: 14px 30px; font-size: 15px; font-weight: 700; border-radius: 8px; display: inline-block; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); transition: all 0.2s;">
                      Start Solving Frontend Challenges
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td style="background-color: #0c0c0e; border-top: 1px solid #27272a; padding: 24px; text-align: center;">
              <p style="font-size: 12px; color: #52525b; margin: 0 0 8px 0;">
                You received this because you are a registered user of Interleet.
              </p>
              <p style="font-size: 11px; color: #3f3f46; margin: 0; text-transform: uppercase; letter-spacing: 1px;">
                &copy; 2026 Interleet. All rights reserved.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# Bulk Email Logic
# ─────────────────────────────────────────────────────────────────────────────
def send_bulk_advertisement(test_email=None):
    db = get_db()
    if test_email:
        users = [{"email": test_email, "username": "Admin (Test)"}]
        print(f"Running in TEST mode targeting: {test_email}")
    else:
        users = list(db.users.find({"email": {"$exists": True, "$ne": ""}}))
        print(f"Loaded {len(users)} users from database.")

    host = config.SMTP_HOST
    port = config.SMTP_PORT
    username = config.SMTP_USERNAME
    password = config.SMTP_PASSWORD
    from_email = config.SMTP_FROM_EMAIL
    from_name = config.SMTP_FROM_NAME

    if not username or not password or not from_email:
        print("ERROR: SMTP credentials are not configured in the environment.")
        return

    # Open single SMTP connection
    if port == 465:
        server = smtplib.SMTP_SSL(host, port, timeout=30)
    else:
        server = smtplib.SMTP(host, port, timeout=30)
        server.ehlo()
        if port == 587 or server.has_extn("STARTTLS"):
            server.starttls()
            server.ehlo()

    try:
        server.login(username, password)
        print("Successfully logged into SMTP server.")

        sent_count = 0
        for user in users:
            email = user.get("email")
            username = user.get("username", "Engineer")
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "🚀 20 New Interactive Frontend Challenges Are Live!"
            msg["From"] = f"{from_name} <{from_email}>" if from_name else from_email
            msg["To"] = email
            
            html_content = get_advertisement_template(username)
            msg.attach(MIMEText(html_content, "html"))
            
            try:
                server.sendmail(from_email, email, msg.as_string())
                print(f"  ✓ Sent email to {email}")
                sent_count += 1
            except Exception as e:
                print(f"  ✗ Failed to send to {email}: {e}")

        print(f"\nCompleted! Sent {sent_count}/{len(users)} advertisement emails.")
    finally:
        server.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "run":
            send_bulk_advertisement()
        elif sys.argv[1] == "test":
            target = sys.argv[2] if len(sys.argv) > 2 else "santushtkotai1221@gmail.com"
            send_bulk_advertisement(test_email=target)
        else:
            print("Invalid argument. Use 'run' or 'test'.")
    else:
        print("Dry run complete. Run with 'run' or 'test' argument.")

