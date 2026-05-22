# email_service.py

import os
import time
from typing import Optional

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load variables from .env into the system environment
load_dotenv()


# -----------------------------
# CONFIG
# -----------------------------
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL =  "sivamapandeya239@gmail.com"


# -----------------------------
# CORE SENDER (single source)
# -----------------------------
def _send(
    to_email: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    retries: int = 2,
    backoff_sec: float = 0.5,
) -> bool:
    """
    Sends an email via SendGrid.
    - Skips invalid/unknown emails
    - Retries on transient failures
    """

    if not to_email or to_email.strip().lower() == "unknown":
        return False

    if not SENDGRID_API_KEY:
        print("SENDGRID_API_KEY not set")
        return False

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body_text,
        html_content=body_html if body_html else None,
    )

    attempt = 0
    while attempt <= retries:
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(message)
            return True
        except Exception as e:
            print(f"[Email attempt {attempt+1}] failed for {to_email}: {e}")
            attempt += 1
            if attempt <= retries:
                time.sleep(backoff_sec * attempt)

    return False


# -----------------------------
# TEMPLATES
# -----------------------------
def _html_wrapper(title: str, content: str) -> str:
    """Simple branded HTML wrapper"""
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <style>
    body {{ font-family: Arial, sans-serif; background:#f6f7fb; margin:0; padding:0; }}
    .container {{ max-width:600px; margin:30px auto; background:#ffffff; border-radius:8px; padding:24px; }}
    .header {{ font-size:20px; font-weight:bold; margin-bottom:12px; }}
    .content {{ font-size:14px; color:#333; line-height:1.6; }}
    .footer {{ margin-top:24px; font-size:12px; color:#777; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">{title}</div>
    <div class="content">{content}</div>
    <div class="footer">HR Team — Auth Bridge</div>
  </div>
</body>
</html>
"""


# -----------------------------
# EMAILS
# -----------------------------
def send_confirmation_email(to_email: str, name: str) -> bool:
    subject = "Application Received"

    text = f"""Hello {name},

Thank you for applying. We have received your profile successfully.

Our team will review your application and get back to you within 3 working days.

Best regards,
HR Team (Auth Bridge)
"""

    html = _html_wrapper(
        "Application Received",
        f"""
<p>Hello {name},</p>
<p>Thank you for applying. We have received your profile successfully.</p>
<p>Our team will review your application and get back to you within <b>3 working days</b>.</p>
<p>Best regards,<br/>HR Team</p>
""",
    )

    return _send(to_email, subject, text, html)


def send_shortlist_email(to_email: str, name: str) -> bool:
    subject = "Application Shortlisted"

    text = f"""Hello {name},

Great news! Your profile has been shortlisted.

Our team will contact you shortly with next steps.

Best regards,
HR Team
"""

    html = _html_wrapper(
        "You’re Shortlisted 🎉",
        f"""
<p>Hello {name},</p>
<p>Great news! Your profile has been <b>shortlisted</b>.</p>
<p>Our team will contact you shortly with the next steps.</p>
<p>Best regards,<br/>HR Team</p>
""",
    )

    return _send(to_email, subject, text, html)


def send_rejection_email(to_email: str, name: str) -> bool:
    subject = "Application Update"

    text = f"""Hello {name},

Thank you for your interest. After careful review, we will not be moving forward at this time.

We appreciate your effort and wish you the best.

Best regards,
HR Team
"""

    html = _html_wrapper(
        "Application Update",
        f"""
<p>Hello {name},</p>
<p>Thank you for your interest. After careful review, we will not be moving forward at this time.</p>
<p>We appreciate your effort and wish you the best.</p>
<p>Best regards,<br/>HR Team</p>
""",
    )

    return _send(to_email, subject, text, html)


def send_manager_approval_email(to_email: str, name: str) -> bool:
    subject = "Application Progressed to Next Stage"

    text = f"""Hello {name},

We are pleased to inform you that your candidature aligns with our requirements.

Your profile has been shortlisted for the next stage. Our team will contact you shortly with further details.

Best regards,
HR Team
"""

    html = _html_wrapper(
        "Next Stage 🚀",
        f"""
<p>Hello {name},</p>
<p>We are pleased to inform you that your candidature aligns with our requirements.</p>
<p>Your profile has been <b>shortlisted for the next stage</b>. Our team will contact you shortly with further details.</p>
<p>Best regards,<br/>HR Team</p>
""",
    )

    return _send(to_email, subject, text, html)