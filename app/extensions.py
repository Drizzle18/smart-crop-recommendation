"""
extensions.py

This file centralizes Flask extensions used across
the application.

Keeping extensions here prevents circular imports
and makes the application easier to scale.
"""

# Flask SQLAlchemy handles ORM/database operations
from flask_sqlalchemy import SQLAlchemy

# Flask-Login manages authentication sessions
from flask_login import LoginManager

# Flask-Mail handles email sending functionality
from flask_mail import Mail

# Flask-Migrate handles database migrations
# (schema versioning / table updates)
from flask_migrate import Migrate


# ------------------------------------------------
# DATABASE EXTENSION
# ------------------------------------------------

# Create SQLAlchemy instance
# (actual app connection happens later in __init__.py)
db = SQLAlchemy()


# ------------------------------------------------
# AUTHENTICATION EXTENSION
# ------------------------------------------------

# Create LoginManager instance
# Responsible for:
# - login sessions
# - user authentication
# - protected routes
# - current_user management
login_manager = LoginManager()


# ------------------------------------------------
# EMAIL EXTENSION
# ------------------------------------------------

# Create Mail instance
# Responsible for:
# - password reset emails
# - notification emails
# - future system email features
#
# Actual app configuration and initialization
# happen later inside __init__.py
mail = Mail()


# ------------------------------------------------
# DATABASE MIGRATION EXTENSION
# ------------------------------------------------

# Create Flask-Migrate instance
#
# Responsible for:
# - database schema migrations
# - creating migration scripts
# - upgrading database tables
# - keeping models and database synchronized
#
# Actual app initialization
# happens later inside __init__.py
migrate = Migrate()