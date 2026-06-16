"""
Global error handlers for Smart Crop Recommendation System
"""

from flask import render_template, request, jsonify

from sqlalchemy.exc import (
    SQLAlchemyError,
    OperationalError
)

from app.extensions import db


def register_error_handlers(app):

    # ----------------------------------
    # 404
    # ----------------------------------
    @app.errorhandler(404)
    def not_found(error):

        if request.path.startswith("/api/") or request.is_json:
            return jsonify({
                "status": "error",
                "message": "Page not found."
            }), 404

        return render_template(
            "error.html",
            error_title="Page Not Found",
            error_message=(
                "The page you are looking for "
                "does not exist or may have been moved."
            )
        ), 404

    # ----------------------------------
    # 403
    # ----------------------------------
    @app.errorhandler(403)
    def forbidden(error):

        if request.path.startswith("/api/") or request.is_json:
            return jsonify({
                "status": "error",
                "message": "Access denied."
            }), 403

        return render_template(
            "error.html",
            error_title="Access Denied",
            error_message=(
                "You do not have permission "
                "to access this page."
            )
        ), 403

    # ----------------------------------
    # Database Connection Errors
    # ----------------------------------
    @app.errorhandler(OperationalError)
    def operational_error(error):

        db.session.rollback()

        app.logger.error(
            f"Database Operational Error: {error}"
        )

        if request.path.startswith("/api/") or request.is_json:
            return jsonify({
                "status": "error",
                "message": "Database connection unavailable."
            }), 500

        return render_template(
            "error.html",
            error_title="Database Connection Error",
            error_message=(
                "Unable to connect to the database. "
                "Please check your internet connection "
                "and try again later."
            )
        ), 500

    # ----------------------------------
    # Other SQLAlchemy Errors
    # ----------------------------------
    @app.errorhandler(SQLAlchemyError)
    def database_error(error):

        db.session.rollback()

        app.logger.error(
            f"Database Error: {error}"
        )

        if request.path.startswith("/api/") or request.is_json:
            return jsonify({
                "status": "error",
                "message": "Database error occurred."
            }), 500

        return render_template(
            "error.html",
            error_title="Database Error",
            error_message=(
                "A database error occurred. "
                "Please try again later."
            )
        ), 500

    # ----------------------------------
    # Internal Server Error
    # ----------------------------------
    @app.errorhandler(500)
    def internal_error(error):

        db.session.rollback()

        if request.path.startswith("/api/") or request.is_json:
            return jsonify({
                "status": "error",
                "message": "Internal server error."
            }), 500

        return render_template(
            "error.html",
            error_title="Server Error",
            error_message=(
                "Something went wrong on our side. "
                "Please try again later."
            )
        ), 500

    # ----------------------------------
    # Catch-All
    # ----------------------------------
    @app.errorhandler(Exception)
    def general_error(error):

        db.session.rollback()

        app.logger.error(
            f"Unexpected Error: {error}"
        )

        if request.path.startswith("/api/") or request.is_json:
            return jsonify({
                "status": "error",
                "message": "Unexpected application error."
            }), 500

        return render_template(
            "error.html",
            error_title="Unexpected Error",
            error_message=(
                "An unexpected error occurred. "
                "Please try again."
            )
        ), 500