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
import logging
from flask import Flask

# Environment variable loader
from dotenv import load_dotenv

# Standard library
import os

# SQLAlchemy exceptions
from sqlalchemy.exc import SQLAlchemyError


# ------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ------------------------------------------------

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

from app.errors import register_error_handlers


def create_app():
    """
    Application Factory Function.
    """

    # ------------------------------------------
    # CREATE FLASK APPLICATION
    # ------------------------------------------

    app = Flask(__name__)

    # ------------------------------------------
    # APPLICATION SECURITY CONFIGURATION
    # ------------------------------------------

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY"
    )

    # ------------------------------------------
    # DATABASE CONFIGURATION
    # ------------------------------------------

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        os.getenv("DATABASE_URL")
    )

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False

    app.config[
        "SQLALCHEMY_ENGINE_OPTIONS"
    ] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 8
    }

    # ------------------------------------------
    # EMAIL CONFIGURATION
    # ------------------------------------------

    app.config["MAIL_SERVER"] = os.getenv(
        "MAIL_SERVER"
    )

    app.config["MAIL_PORT"] = int(
        os.getenv("MAIL_PORT")
    )

    app.config["MAIL_USE_TLS"] = (
        os.getenv("MAIL_USE_TLS") == "True"
    )

    app.config["MAIL_USERNAME"] = os.getenv(
        "MAIL_USERNAME"
    )

    app.config["MAIL_PASSWORD"] = os.getenv(
        "MAIL_PASSWORD"
    )

    app.config["MAIL_DEFAULT_SENDER"] = os.getenv(
        "MAIL_DEFAULT_SENDER"
    )

    # ------------------------------------------
    # INITIALIZE FLASK EXTENSIONS
    # ------------------------------------------

    db.init_app(app)

    login_manager.init_app(app)

    mail.init_app(app)

    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # ------------------------------------------
    # FLASK-LOGIN USER LOADER
    # ------------------------------------------

    @login_manager.user_loader
    def load_user(user_id):
        """
        Reload user from session.
        """

        from app.models.user import User

        try:

            return db.session.get(
                User,
                int(user_id)
            )

        except SQLAlchemyError as e:

            logger.error(
                f"Failed to load user: {e}"
            )

            try:
                db.session.rollback()
            except Exception:
                pass

            return None

        except Exception as e:

            logger.error(
                f"Unexpected user loader error: {e}"
            )

            return None

    # ------------------------------------------
    # IMPORT DATABASE MODELS
    # ------------------------------------------

    from app.models.user import User
    from app.models.prediction import Prediction

    # ------------------------------------------
    # REGISTER APPLICATION BLUEPRINTS
    # ------------------------------------------

    app.register_blueprint(main_bp)

    app.register_blueprint(auth_bp)

    # ------------------------------------------
    # REGISTER GLOBAL ERROR HANDLERS
    # ------------------------------------------

    register_error_handlers(app)

    # ------------------------------------------
    # RETURN CONFIGURED APPLICATION
    # ------------------------------------------

    return app