import smtplib
import asyncio
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.core import config

logger = logging.getLogger(__name__)

# Dynamic path to frontend/src/assets/logo.png
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..", "..", "frontend", "src", "assets", "logo.png")
)


def _send_smtp_sync(to_email: str, subject: str, otp_code: str):
    """Synchronous function to perform the SMTP transaction."""
    host = config.SMTP_HOST
    port = config.SMTP_PORT
    username = config.SMTP_USERNAME
    password = config.SMTP_PASSWORD
    from_email = config.SMTP_FROM_EMAIL
    from_name = config.SMTP_FROM_NAME

    if not username or not password or not from_email:
        raise ValueError(
            "SMTP credentials (SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM_EMAIL) "
            "are not configured in the environment."
        )

    # Create MIMEMultipart message with related subtype for inline images
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>" if from_name else from_email
    msg["To"] = to_email

    # Check if logo exists
    has_logo = os.path.exists(LOGO_PATH)

    # Generate HTML content
    html_content = get_otp_email_template(otp_code, has_logo=has_logo)

    # Attach HTML content in alternative subpart
    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_content, "html"))

    # Attach the logo if it exists
    if has_logo:
        try:
            from PIL import Image
            import io

            # Compress the large logo down to a web-optimized 300px width in-memory
            with Image.open(LOGO_PATH) as img:
                img.thumbnail((300, 300))
                buffer = io.BytesIO()
                img.save(buffer, format="PNG", optimize=True)
                img_data = buffer.getvalue()

            msg_image = MIMEImage(img_data)
            msg_image.add_header("Content-ID", "<logo>")
            msg_image.add_header("Content-Disposition", "inline", filename="logo.png")
            msg.attach(msg_image)
            logger.info(f"Attached optimized inline logo (size: {len(img_data)} bytes)")
        except Exception as img_err:
            logger.error(f"Failed to attach optimized logo image: {img_err}")

    # Connect using SSL or STARTTLS
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
        server.sendmail(from_email, to_email, msg.as_string())
    finally:
        server.quit()


async def send_otp_email(to_email: str, subject: str, otp_code: str) -> bool:
    """Asynchronously send an HTML OTP email using standard smtplib inside asyncio.to_thread."""
    try:
        await asyncio.to_thread(_send_smtp_sync, to_email, subject, otp_code)
        logger.info(f"Successfully sent OTP email to {to_email}")
        return True
    except ValueError as ve:
        # Expected if credentials are not set during local development
        logger.warning(f"Skipping email sending to {to_email}: {ve}")
        return False
    except Exception as e:
        logger.exception(f"Failed to send email to {to_email}: {e}")
        return False


def get_otp_email_template(otp_code: str, has_logo: bool = False) -> str:
    """Return a premium, SAAS-styled responsive HTML email template for OTP verification."""
    if has_logo:
        logo_html = '<img src="cid:logo" alt="Interleet Logo" style="height: 50px; width: auto; max-width: 180px; object-fit: contain; margin: 0 auto; display: block;" />'
    else:
        logo_html = """<span style="font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;">
                      INTER<span style="color: #ff6500;">LEET</span>
                    </span>"""

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verify your email</title>
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
            <td style="padding: 40px 30px; text-align: center;">
              
              <!-- Brand Header -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 30px;">
                <tr>
                  <td align="center">
                    {logo_html}
                  </td>
                </tr>
              </table>

              <!-- Main Title -->
              <h1 style="font-size: 20px; font-weight: 700; margin: 0 0 12px 0; color: #ffffff;">
                Verification Code
              </h1>
              
              <!-- Description -->
              <p style="font-size: 14px; line-height: 1.6; color: #a1a1a1; margin: 0 0 24px 0;">
                To complete your authentication, please use the verification code below. This code is valid for <strong>5 minutes</strong>.
              </p>
              
              <!-- OTP Box -->
              <div style="background-color: #141414; border: 1px solid #262626; border-radius: 8px; padding: 20px 10px; margin: 24px 0; text-align: center;">
                <span style="font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 36px; font-weight: 800; letter-spacing: 6px; color: #ff6500; display: inline-block; padding-left: 6px;">
                  {otp_code}
                </span>
              </div>
              
              <!-- Security Warning -->
              <p style="font-size: 12px; line-height: 1.5; color: #666666; margin: 24px 0 0 0;">
                If you did not request this verification code, please ignore this email or contact support if you suspect unauthorized access.
              </p>

            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td style="background-color: #0a0a0a; border-top: 1px solid #1f1f1f; padding: 20px; text-align: center;">
              <p style="font-size: 11px; color: #525252; margin: 0; text-transform: uppercase; letter-spacing: 1px;">
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
