"""
Creates all database tables.
"""

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():

    # Import models BEFORE create_all()
    from app.models.user import User

    db.create_all()

    print("Database tables created successfully.")