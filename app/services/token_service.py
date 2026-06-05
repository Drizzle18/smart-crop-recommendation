"""
token_service.py

Password reset token utilities.
"""

from itsdangerous import (
    URLSafeTimedSerializer
)

from flask import current_app


def generate_reset_token(email):
    """
    Generate secure password reset token.
    """

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        email,
        salt="password-reset"
    )


def verify_reset_token(
    token,
    max_age=3600
):
    """
    Verify reset token.
    Default expiry: 1 hour.
    """

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=max_age
        )

        return email

    except Exception:

        return None