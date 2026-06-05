"""
auth_routes.py

Authentication routes.

Handles:
- User registration
- User login
- User logout
- Forgot password
- Password reset
"""

import re
# Flask utilities
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for
)

# Password hashing utilities
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Flask-Login utilities
from flask_login import (
    login_user,
    logout_user,
    login_required
)

# Database extension
from app.extensions import db

# Database models
from app.models.user import User

# Email services
from app.services.email_service import (
    send_reset_email
)

# Token services
from app.services.token_service import (
    generate_reset_token,
    verify_reset_token
)

# Create authentication blueprint
auth_bp = Blueprint(
    "auth",
    __name__
)


# ------------------------------------------------
# SIGNUP ROUTE
# ------------------------------------------------

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handles user registration.
    """

    if request.method == "GET":

        return render_template(
            "signup.html"
        )

    first_name = request.form.get(
        "first_name",
        ""
    ).strip()

    last_name = request.form.get(
        "last_name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    terms = request.form.get(
        "terms"
    )

    # Required validation

    if not first_name:

        flash(
            "First name is required.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    if not last_name:

        flash(
            "Last name is required.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    if not email:

        flash(
            "Email address is required.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    if not password:

        flash(
            "Password is required.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    if not confirm_password:

        flash(
            "Confirm password is required.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    # Email validation

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(
        email_pattern,
        email
    ):

        flash(
            "Enter a valid email address.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    # Password validation

    if password != confirm_password:

        flash(
            "Passwords do not match.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    if len(password) < 8:

        flash(
            "Password must be at least 8 characters.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    if not any(
        char.isupper()
        for char in password
    ):

        flash(
            "Password must contain at least one uppercase letter.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    if not any(
        char.isdigit()
        for char in password
    ):

        flash(
            "Password must contain at least one number.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    # Terms validation

    if not terms:

        flash(
            "You must accept the Terms and Privacy Policy.",
            "danger"
        )

        return redirect(
            url_for("auth.signup")
        )

    # Duplicate email check

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        flash(
            "Email already registered.",
            "warning"
        )

        return redirect(
            url_for("auth.signup")
        )

    # Hash password

    hashed_password = generate_password_hash(
        password
    )

    # Create user

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hashed_password
    )

    db.session.add(
        new_user
    )

    db.session.commit()

    flash(
        "Account created successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )


# ------------------------------------------------
# LOGIN ROUTE
# ------------------------------------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    """

    if request.method == "GET":

        return render_template(
            "login.html"
        )

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )

    if not email or not password:

        flash(
            "Email and password are required.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if not user or not check_password_hash(
        user.password_hash,
        password
    ):

        flash(
            "Invalid email or password.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    login_user(
        user
    )

    flash(
        "Login successful.",
        "success"
    )

    return redirect(
        url_for("main.dashboard")
    )


# ------------------------------------------------
# FORGOT PASSWORD ROUTE
# ------------------------------------------------

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():
    """
    Handles password recovery.

    Generates a secure reset token
    and sends a password reset email
    if the account exists.
    """

    # --------------------------------
    # Render Page
    # --------------------------------

    if request.method == "GET":

        return render_template(
            "forgot_password.html"
        )

    # --------------------------------
    # Collect + sanitize email input
    # --------------------------------

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    # --------------------------------
    # Find user account
    # --------------------------------

    user = User.query.filter_by(
        email=email
    ).first()

    # --------------------------------
    # Generate reset email
    # --------------------------------

    if user:

        # Generate secure token
        token = generate_reset_token(
            user.email
        )

        # Create reset URL
        reset_link = url_for(
            "auth.reset_password",
            token=token,
            _external=True
        )

        # Send reset email
        send_reset_email(
            user.email,
            reset_link
        )

    # --------------------------------
    # Security Message
    # Prevents email enumeration
    # --------------------------------

    flash(
        (
            "If the email exists, "
            "a password reset link "
            "has been sent."
        ),
        "info"
    )

    return redirect(
        url_for("auth.login")
    )


# ------------------------------------------------
# RESET PASSWORD ROUTE
# ------------------------------------------------

@auth_bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):
    """
    Handles password reset.
    """

    email = verify_reset_token(
        token
    )

    if not email:

        flash(
            "Invalid or expired reset link.",
            "danger"
        )

        return redirect(
            url_for(
                "auth.forgot_password"
            )
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        flash(
            "User account not found.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    if request.method == "GET":

        return render_template(
            "reset_password.html",
            token=token
        )

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    if password != confirm_password:

        flash(
            "Passwords do not match.",
            "danger"
        )

        return redirect(
            request.url
        )

    if len(password) < 8:

        flash(
            "Password must be at least 8 characters.",
            "danger"
        )

        return redirect(
            request.url
        )

    hashed_password = generate_password_hash(
        password
    )

    user.password_hash = hashed_password

    db.session.commit()

    flash(
        "Password reset successful.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )


# ------------------------------------------------
# LOGOUT ROUTE
# ------------------------------------------------

@auth_bp.route("/logout")
@login_required
def logout():
    """
    Handles user logout.
    """

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("main.landing")
    )