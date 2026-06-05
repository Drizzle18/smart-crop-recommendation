"""
user.py

Defines the User database model.

Stores registered users for:
- Authentication
- Authorization
- Session management
"""

# Handles timestamp creation
from datetime import datetime

# Flask-Login helper mixin
from flask_login import UserMixin

# SQLAlchemy database instance
from app.extensions import db


class User(UserMixin, db.Model):
    """
    User Database Model.

    Represents application users.
    """

    # --------------------------------
    # Database Table Name
    # --------------------------------

    __tablename__ = "users"

    # --------------------------------
    # Primary Key
    # --------------------------------

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # --------------------------------
    # User Personal Information
    # --------------------------------

    first_name = db.Column(
        db.String(80),
        nullable=False
    )

    last_name = db.Column(
        db.String(80),
        nullable=False
    )

    # --------------------------------
    # Authentication Information
    # --------------------------------

    # User email address
    # Used during login.
    # unique=True prevents duplicate accounts.

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    # Stores HASHED password only.
    # Never store raw passwords.

    password_hash = db.Column(
        db.Text,
        nullable=False
    )

    # --------------------------------
    # Account Metadata
    # --------------------------------

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # --------------------------------
    # Relationships
    # --------------------------------

    # One User -> Many Predictions
    #
    # Example:
    # user.predictions
    #
    # Allows easy retrieval of all
    # prediction records belonging
    # to a specific user.

    predictions = db.relationship(
        "Prediction",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # --------------------------------
    # Object Representation
    # --------------------------------

    def __repr__(self):
        """
        Developer-friendly object output.
        Useful for debugging.
        """

        return (
            f"<User {self.email}>"
        )