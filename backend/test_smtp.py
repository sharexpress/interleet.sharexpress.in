#!/usr/bin/env python3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def send_test_email():
    # Load backend .env config
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(backend_dir, ".env"), override=True)

    host = os.getenv("SMTP_HOST", "smtp.hostinger.com")
    port = int(os.getenv("SMTP_PORT", "465"))
    username = os.getenv("SMTP_USERNAME", "noreply@sharexpress.in")
    password = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("SMTP_FROM_EMAIL", "noreply@sharexpress.in")
    from_name = os.getenv("SMTP_FROM_NAME", "Interleet Test")

    to_emails = ["hello@sharexpress.in", "santushtkotai1221@gmail.com"]

    print("SMTP Settings:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Username: {username}")
    print(f"  From: {from_name} <{from_email}>")
    print(f"  Recipients: {', '.join(to_emails)}")

    if not password:
        print("Error: SMTP_PASSWORD is not set in .env")
        return

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Interleet DNS & SMTP Delivery Test"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = ", ".join(to_emails)

    text_body = "This is a test email to verify that SMTP delivery to sharexpress.in domain works after updating the MX records."
    html_body = f"""
    <html>
      <body style="font-family: sans-serif; background: #0c0c0e; color: #f4f4f5; padding: 20px;">
        <div style="max-width: 500px; margin: 0 auto; background: #18181b; border: 1px solid #27272a; padding: 20px; border-radius: 8px;">
          <h2 style="color: #ff6500; margin-top: 0;">Interleet DNS & Mail Delivery Test</h2>
          <p>Hello Santusht,</p>
          <p>This test email was sent to verify that mail delivery is working perfectly now that the incorrect <code>mail.sharexpress.in</code> MX record has been deleted from your Cloudflare settings.</p>
          <hr style="border: 0; border-top: 1px solid #27272a; margin: 15px 0;" />
          <p style="font-size: 12px; color: #71717a;">Sent via Hostinger SMTP (<code>noreply@sharexpress.in</code>) to: <strong>hello@sharexpress.in</strong></p>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        print("Connecting to SMTP server...")
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=15)
        else:
            server = smtplib.SMTP(host, port, timeout=15)
            server.ehlo()
            server.starttls()
            server.ehlo()

        print("Logging in...")
        server.login(username, password)

        print("Sending email...")
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
        print("✅ Success! Test email sent successfully to the recipients.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    send_test_email()
