"""
email_service.py

Email service utilities.

Handles outgoing email functionality
for the application.

Currently supports:

- Password reset emails

Future support:

- Welcome emails
- Account verification
- Notifications
- System alerts
"""

# Flask-Mail email message object
from flask_mail import Message

# Import Mail extension instance
from app.extensions import mail


def send_reset_email(
    user_email,
    reset_link
):
    """
    Send password reset email.

    Args:
        user_email (str):
            Recipient email address.

        reset_link (str):
            Generated password reset URL.
    """

    # ------------------------------------------
    # Email Subject
    # ------------------------------------------

    subject = (
        "Password Reset - "
        "Smart Crop Recommendation System"
    )

    # ------------------------------------------
    # Plain Text Email Body
    # ------------------------------------------

    body = f"""
Hello,

A password reset request was received
for your Smart Crop Recommendation System account.

To reset your password,
click the link below:

{reset_link}

If you did not request this change,
please ignore this email.

For security reasons,
do not share this link with anyone.

Smart Crop Recommendation System
"""

    # ------------------------------------------
    # Create Email Message
    # ------------------------------------------

    message = Message(
        subject=subject,
        recipients=[user_email],
        body=body
    )

    # ------------------------------------------
    # Send Email
    # ------------------------------------------

    mail.send(message)