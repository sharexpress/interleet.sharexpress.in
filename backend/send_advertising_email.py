import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pymongo import MongoClient

# Ensure app directory is in Python path for loading configs
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.core import config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.abspath(
    os.path.join(CURRENT_DIR, "app", "utils", "..", "..", "..", "frontend", "src", "assets", "logo.png")
)

if not os.path.exists(LOGO_PATH):
    # Fallback to local script relative path if not resolved
    LOGO_PATH = os.path.abspath(
        os.path.join(CURRENT_DIR, "..", "frontend", "src", "assets", "logo.png")
    )

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["interleet"]

# ─────────────────────────────────────────────────────────────────────────────
# HTML Email Template matching the OTP theme
# ─────────────────────────────────────────────────────────────────────────────
def get_advertisement_template(username: str, has_logo: bool = False) -> str:
    if has_logo:
        logo_html = '<img src="cid:logo" alt="Interleet Logo" style="height: 50px; width: auto; max-width: 180px; object-fit: contain; margin: 0 auto; display: block;" />'
    else:
        logo_html = """<span style="font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                      INTER<span style="color: #ff6500;">LEET</span>
                    </span>"""

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Boost Your Placement Coding Prep on Interleet</title>
</head>
<body style="margin: 0; padding: 0; background-color: #050505; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #ffffff;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #050505; padding: 40px 20px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px; background-color: #0f0f0f; border: 1px solid #1f1f1f; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
          <!-- Top Accent Line -->
          <tr>
            <td height="4" style="background-color: #ff6500; line-height: 4px; font-size: 4px;">&nbsp;</td>
          </tr>
          
          <!-- Content Padding -->
          <tr>
            <td style="padding: 40px 30px; text-align: left;">
              
              <!-- Brand Header -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                <tr>
                  <td align="center">
                    {logo_html}
                  </td>
                </tr>
              </table>

              <!-- Main Title -->
              <h1 style="font-size: 20px; font-weight: 800; margin: 0 0 4px 0; color: #ffffff; text-align: center; letter-spacing: -0.5px;">
                Build Industry-Ready Skills
              </h1>
              <p style="font-size: 13px; color: #ff6500; text-align: center; margin: 0 0 24px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                Interactive Platform to Make You Industry Ready
              </p>
              
              <!-- Greeting -->
              <p style="font-size: 14px; line-height: 1.6; color: #ffffff; margin: 0 0 16px 0;">
                Hey {username},
              </p>
              
              <!-- Body Description -->
              <p style="font-size: 14px; line-height: 1.6; color: #a1a1a1; margin: 0 0 20px 0;">
                To secure high-paying engineering roles in today's competitive tech industry, theoretical memorization and simple syntax tasks are no longer enough. You need to write, compile, and debug real production-grade code.
              </p>
              
              <p style="font-size: 14px; line-height: 1.6; color: #a1a1a1; margin: 0 0 20px 0;">
                Interleet provides an interactive browser-sandbox environment where you can solve actual developer challenges in JavaScript, Python, Go, Java, C++, and Rust with live visual feedback and behavioral test validation.
              </p>

              <!-- Features Box -->
              <div style="background-color: #141414; border: 1px solid #262626; border-radius: 8px; padding: 20px; margin: 24px 0;">
                <h3 style="font-size: 13px; margin: 0 0 12px 0; color: #ff6500; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">What you will build:</h3>
                <ul style="margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.8; color: #d4d4d8; list-style-type: square;">
                  <li><strong>Interactive UI Elements</strong>: Code Star Ratings, Autocomplete drop-downs, and Shopping Carts directly manipulating the DOM.</li>
                  <li><strong>Full-Stack APIs & Databases</strong>: Script live servers connected to SQLite and MongoDB.</li>
                  <li><strong>Algorithms & Concurrency</strong>: Resolve resource contentions, caching systems, and high-performance algorithms.</li>
                </ul>
              </div>

              <p style="font-size: 14px; line-height: 1.6; color: #a1a1a1; margin: 0 0 28px 0;">
                Skip the complex setups and config boilerplates. Open Interleet, pick a challenge, and write code directly in your browser.
              </p>
              
              <!-- CTA Button -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="center">
                    <a href="https://interleet.sharexpress.in/app/challenges" style="background-color: #ff6500; color: #ffffff !important; text-decoration: none !important; padding: 14px 28px; font-size: 14px; font-weight: 700; border-radius: 6px; display: inline-block; box-shadow: 0 4px 12px rgba(255, 101, 0, 0.3); border: none; outline: none; text-align: center;">
                      <span style="color: #ffffff !important; text-decoration: none !important;">Start Building Industry Skills</span>
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td style="background-color: #0a0a0a; border-top: 1px solid #1f1f1f; padding: 20px; text-align: center;">
              <p style="font-size: 11px; color: #525252; margin: 0 0 4px 0;">
                You received this as part of Interleet's academic engineering outreach program.
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
# ─────────────────────────────────────────────────────────────────────────────
# Bulk Email Logic with Parallel Threaded Dispatch
# ─────────────────────────────────────────────────────────────────────────────
import threading
from concurrent.futures import ThreadPoolExecutor

def send_bulk_advertisement(test_email=None, cold_mode=False):
    db = get_db()
    if test_email:
        users = [{"email": test_email, "username": "Admin (Test)"}]
        print(f"Running in TEST mode targeting: {test_email}")
    elif cold_mode:
        import json
        json_path = os.path.abspath(os.path.join(CURRENT_DIR, "..", "candidates_info.json"))
        if not os.path.exists(json_path):
            json_path = os.path.abspath(os.path.join(CURRENT_DIR, "candidates_info.json"))
        print(f"Loading cold leads from: {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)
        users = [{"email": c["email"], "username": c["name"]} for c in candidates]
        print(f"Loaded {len(users)} cold leads from JSON.")
    else:
        users = list(db.users.find({"email": {"$exists": True, "$ne": ""}}))
        print(f"Loaded {len(users)} users from database.")

    # Deduplication logic using sent_emails.txt file
    sent_list_path = os.path.abspath(os.path.join(CURRENT_DIR, "sent_emails.txt"))
    already_sent = set()
    if os.path.exists(sent_list_path):
        with open(sent_list_path, "r", encoding="utf-8") as sf:
            for l in sf:
                e = l.strip()
                if e:
                    already_sent.add(e.lower())
    print(f"Loaded {len(already_sent)} already sent email records from: {sent_list_path}")

    original_count = len(users)
    users = [u for u in users if u.get("email", "").lower() not in already_sent]
    print(f"Filtered out {original_count - len(users)} already sent emails. Remaining to send: {len(users)}")

    host = config.SMTP_HOST
    port = config.SMTP_PORT
    username = config.SMTP_USERNAME
    password = config.SMTP_PASSWORD
    from_email = config.SMTP_FROM_EMAIL
    from_name = config.SMTP_FROM_NAME

    if not username or not password or not from_email:
        print("ERROR: SMTP credentials are not configured in the environment.")
        return

    # Check if logo exists
    has_logo = os.path.exists(LOGO_PATH)
    print(f"Logo path: {LOGO_PATH} (Exists: {has_logo})")

    # Load and optimized logo if exists
    img_data = None
    if has_logo:
        try:
            from PIL import Image
            import io
            with Image.open(LOGO_PATH) as img:
                img.thumbnail((300, 300))
                buffer = io.BytesIO()
                img.save(buffer, format="PNG", optimize=True)
                img_data = buffer.getvalue()
            print("Successfully loaded and optimized inline logo.")
        except Exception as e:
            print(f"Warning: Failed to optimize logo: {e}")
            has_logo = False

    # Thread-safe counters
    sent_count = 0
    failed_count = 0
    counter_lock = threading.Lock()

    # Worker function for parallel execution
    def worker(batch, worker_id):
        nonlocal sent_count, failed_count
        
        try:
            # Open separate SMTP connection per thread/worker
            if port == 465:
                server = smtplib.SMTP_SSL(host, port, timeout=30)
            else:
                server = smtplib.SMTP(host, port, timeout=30)
                server.ehlo()
                if port == 587 or server.has_extn("STARTTLS"):
                    server.starttls()
                    server.ehlo()
        except Exception as conn_err:
            print(f"  [Worker {worker_id}] ✗ Connection failed: {conn_err}")
            with counter_lock:
                failed_count += len(batch)
            return

        try:
            server.login(username, password)
        except Exception as login_err:
            print(f"  [Worker {worker_id}] ✗ Login failed: {login_err}")
            with counter_lock:
                failed_count += len(batch)
            try:
                server.quit()
            except Exception:
                pass
            return

            
            thread_sent = 0
            thread_failed = 0
            for user in batch:
                email = user.get("email")
                user_name = user.get("username", "Engineer")
                
                msg = MIMEMultipart("related")
                msg["Subject"] = "🚀 Upgrade Your Coding Skills: 79 Interactive Challenges Live on Interleet!"
                msg["From"] = f"{from_name} <{from_email}>" if from_name else from_email
                msg["To"] = email
                
                html_content = get_advertisement_template(user_name, has_logo=has_logo)
                
                msg_alternative = MIMEMultipart("alternative")
                msg.attach(msg_alternative)
                msg_alternative.attach(MIMEText(html_content, "html"))
                
                if has_logo and img_data:
                    try:
                        msg_image = MIMEImage(img_data)
                        msg_image.add_header("Content-ID", "<logo>")
                        msg_image.add_header("Content-Disposition", "inline", filename="logo.png")
                        msg.attach(msg_image)
                    except Exception as e:
                        pass
                
                import time
                
                # Retry loop for rate-limiting
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        server.sendmail(from_email, email, msg.as_string())
                        thread_sent += 1
                        time.sleep(0.5)  # Pace sending to avoid hitting SMTP limits
                        
                        # Safe append to sent list file
                        with counter_lock:
                            with open(sent_list_path, "a", encoding="utf-8") as sf:
                                sf.write(f"{email.lower()}\n")
                        break
                    except Exception as e:
                        err_str = str(e)
                        if "450" in err_str or "421" in err_str or "too much mail" in err_str.lower():
                            print(f"  [Worker {worker_id}] Rate limited for {email}, retrying in 5s... (Attempt {attempt+1}/{max_retries})")
                            time.sleep(5)
                            # Reconnect connection
                            try:
                                server.noop()
                            except Exception:
                                try:
                                    server.quit()
                                except Exception:
                                    pass
                                if port == 465:
                                    server = smtplib.SMTP_SSL(host, port, timeout=30)
                                else:
                                    server = smtplib.SMTP(host, port, timeout=30)
                                    server.ehlo()
                                    if port == 587 or server.has_extn("STARTTLS"):
                                        server.starttls()
                                        server.ehlo()
                                server.login(username, password)
                        else:
                            if attempt == max_retries - 1:
                                print(f"  [Worker {worker_id}] ✗ Failed to send to {email}: {e}")
                                thread_failed += 1
                            break

            # Update global counters safely
            with counter_lock:
                sent_count += thread_sent
                failed_count += thread_failed
            print(f"  ✓ Worker {worker_id} complete. Sent: {thread_sent}, Failed: {thread_failed}")
        finally:
            try:
                server.quit()
            except Exception:
                pass


    # Split users into N batches (e.g. 3 threads maximum to prevent SMTP IP rate limits)
    num_threads = 3 if len(users) >= 3 else len(users)
    if num_threads == 0:
        print("No users found to email.")
        return

    # Calculate batch chunks
    batch_size = (len(users) + num_threads - 1) // num_threads
    batches = [users[i:i + batch_size] for i in range(0, len(users), batch_size)]

    print(f"Starting parallel execution with {len(batches)} workers...")
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for idx, batch in enumerate(batches):
            # Stagger startup to prevent concurrent SMTP login collisions
            import time
            time.sleep(1)
            futures.append(executor.submit(worker, batch, idx + 1))
        for f in futures:
            try:
                f.result()
            except Exception as e:
                print(f"Error in thread execution: {e}")



    print(f"\nCompleted Parallel Campaign! Total Sent: {sent_count}, Failed: {failed_count}.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "run":
            send_bulk_advertisement()
        elif sys.argv[1] == "cold":
            send_bulk_advertisement(cold_mode=True)
        elif sys.argv[1] == "test":
            target = sys.argv[2] if len(sys.argv) > 2 else "santushtkotai1221@gmail.com"
            send_bulk_advertisement(test_email=target)
        else:
            print("Invalid argument. Use 'run', 'cold', or 'test'.")
    else:
        print("Dry run complete. Run with 'run', 'cold', or 'test' argument.")

