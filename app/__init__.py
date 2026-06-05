"""
__init__.py

Application factory configuration.

This file creates and configures the Flask app,
loads environment variables,
initializes extensions,
configures authentication,
and registers blueprints.
"""

# Flask core
from flask import Flask

# Environment variable loader
from dotenv import load_dotenv

import os


# ------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ------------------------------------------------

# Load values from .env file
load_dotenv()


# ------------------------------------------------
# IMPORT BLUEPRINTS
# ------------------------------------------------

from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp


# ------------------------------------------------
# IMPORT FLASK EXTENSIONS
# ------------------------------------------------

from app.extensions import (
    db,
    login_manager,
    mail,
    migrate
)


def create_app():
    """
    Application Factory Function.

    Creates and configures
    the Flask application instance.
    """

    # ------------------------------------------
    # CREATE FLASK APPLICATION
    # ------------------------------------------

    app = Flask(__name__)

    # ------------------------------------------
    # APPLICATION SECURITY CONFIGURATION
    # ------------------------------------------

    # Secret key used for:
    # - session management
    # - flash messages
    # - CSRF protection
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY"
    )

    # ------------------------------------------
    # DATABASE CONFIGURATION
    # ------------------------------------------

    # PostgreSQL database connection URI
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        os.getenv("DATABASE_URL")

    # Disable modification tracking
    # improves performance
    # removes SQLAlchemy warnings
    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False

    # SQLAlchemy engine options
    # Helps prevent stale cloud connections
    app.config[
        "SQLALCHEMY_ENGINE_OPTIONS"
    ] = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    # ------------------------------------------
    # EMAIL CONFIGURATION
    # ------------------------------------------

    # SMTP server provider
    app.config["MAIL_SERVER"] = os.getenv(
        "MAIL_SERVER"
    )

    # SMTP server port
    app.config["MAIL_PORT"] = int(
        os.getenv("MAIL_PORT")
    )

    # Enable TLS encryption
    app.config["MAIL_USE_TLS"] = (
        os.getenv("MAIL_USE_TLS") == "True"
    )

    # Email account username
    app.config["MAIL_USERNAME"] = os.getenv(
        "MAIL_USERNAME"
    )

    # Email account password
    app.config["MAIL_PASSWORD"] = os.getenv(
        "MAIL_PASSWORD"
    )

    # Default email sender
    app.config[
        "MAIL_DEFAULT_SENDER"
    ] = os.getenv(
        "MAIL_DEFAULT_SENDER"
    )

    # ------------------------------------------
    # INITIALIZE FLASK EXTENSIONS
    # ------------------------------------------

    # Initialize SQLAlchemy ORM
    db.init_app(app)

    # Initialize authentication manager
    login_manager.init_app(app)

    # Initialize email service
    mail.init_app(app)

    # Initialize database migrations
    migrate.init_app(app, db)

    # Configure protected route redirect
    login_manager.login_view = "auth.login"

    # ------------------------------------------
    # FLASK-LOGIN USER LOADER
    # ------------------------------------------

    @login_manager.user_loader
    def load_user(user_id):
        """
        Reload user from session.

        Flask-Login stores only the user's ID
        inside the session.

        This function tells Flask-Login
        how to retrieve that user
        from the database.
        """

        # Local import prevents circular imports
        from app.models.user import User

        return User.query.get(
            int(user_id)
        )

    # ------------------------------------------
    # IMPORT DATABASE MODELS
    # IMPORTANT:
    # SQLAlchemy must discover models
    # before migrations/database operations.
    # ------------------------------------------

    from app.models.user import User
    from app.models.prediction import Prediction

    # ------------------------------------------
    # REGISTER APPLICATION BLUEPRINTS
    # ------------------------------------------

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # ------------------------------------------
    # RETURN CONFIGURED APPLICATION
    # ------------------------------------------

    return app