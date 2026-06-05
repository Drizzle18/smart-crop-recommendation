"""
main_routes.py

Main application routes.

Handles:
- Landing page
- About page
- Dashboard
- Crop prediction
- Saving prediction history
- Displaying prediction results
"""

# Standard Library
import os

from flask import abort

# Flask utilities

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)
# Caching
from sqlalchemy import func

# Flask-Login utilities
from flask_login import (
    login_required,
    current_user
)

# Database
from app.extensions import db

# Database models
from app.models.prediction import Prediction

# Machine Learning prediction function
from src.predict import predict_crop

from collections import Counter



# ------------------------------------------------
# Blueprint Configuration
# ------------------------------------------------

main_bp = Blueprint(
    "main",
    __name__
)


# ------------------------------------------------
# LANDING PAGE
# ------------------------------------------------

@main_bp.route("/")
def landing():
    """
    Public landing page.
    """

    return render_template(
        "landing.html"
    )


# ------------------------------------------------
# ABOUT PAGE
# ------------------------------------------------

@main_bp.route("/about")
def about():
    """
    About page.
    """

    return render_template(
        "about.html"
    )


# ------------------------------------------------
# SIGNUP PAGE
# ------------------------------------------------

@main_bp.route("/signup")
def signup():
    """
    Signup page.

    Note:
    Authentication routes already exist
    inside auth_routes.py.
    """

    return render_template(
        "signup.html"
    )


# ------------------------------------------------
# LOGIN PAGE
# ------------------------------------------------

@main_bp.route("/login")
def login():
    """
    Login page.

    Note:
    Authentication routes already exist
    inside auth_routes.py.
    """

    return render_template(
        "login.html"
    )



# ------------------------------------------------
# DASHBOARD ROUTE
# ------------------------------------------------

@main_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Authenticated user dashboard.

    Displays:
    - Total predictions
    - Most recommended crop
    - Latest recommended crop
    - Recent prediction history
    """

    # --------------------------------
    # Get user's predictions
    # --------------------------------

    predictions = Prediction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Prediction.created_at.desc()
    ).all()

    # --------------------------------
    # Total predictions
    # --------------------------------

    total_predictions = len(predictions)

    # --------------------------------
    # Most recommended crop
    # --------------------------------

    top_crop = "--"

    if predictions:

        crop_counts = Counter(
            p.crop for p in predictions
        )

        top_crop = crop_counts.most_common(1)[0][0]

    # --------------------------------
    # Latest prediction
    # --------------------------------

    latest_prediction = None
    latest_crop = "--"

    if predictions:

        latest_prediction = predictions[0]

        latest_crop = latest_prediction.crop

    # --------------------------------
    # Average confidence
    # --------------------------------

    avg_confidence = 0

    if predictions:

        confidences = [
            p.confidence
            for p in predictions
            if p.confidence
        ]

        if confidences:

            avg_confidence = round(
                sum(confidences) /
                len(confidences),
                1
            )

    # --------------------------------
    # Render dashboard
    # --------------------------------
    
    Model_ACCURACY = 99.55

    return render_template(
        "dashboard.html",
        user=current_user,
        predictions=predictions,
        total_predictions=total_predictions,
        top_crop=top_crop,
        latest_crop=latest_crop,
        latest_prediction=latest_prediction,
        confidence=Model_ACCURACY
    )

# ------------------------------------------------
# CROP PREDICTION
# ------------------------------------------------

@main_bp.route(
    "/predict",
    methods=["GET", "POST"]
)
@login_required
def predict():
    """
    Handles crop prediction workflow.

    Flow:
    1. Receive user inputs
    2. Run ML prediction
    3. Save prediction to database
    4. Load crop image
    5. Display result page
    """

    if request.method == "POST":

        try:

            # ------------------------------------
            # Collect Form Inputs
            # ------------------------------------

            data = {
                "N": float(request.form.get("N")),
                "P": float(request.form.get("P")),
                "K": float(request.form.get("K")),
                "temperature": float(
                    request.form.get("temperature")
                ),
                "humidity": float(
                    request.form.get("humidity")
                ),
                "ph": float(
                    request.form.get("ph")
                ),
                "rainfall": float(
                    request.form.get("rainfall")
                )
            }

            # ------------------------------------
            # ------------------------------------
            # Input Validation
            # ------------------------------------

            if (
                data["N"] < 0 or
                data["P"] < 0 or
                data["K"] < 0 or
                data["temperature"] < 5 or
                data["temperature"] > 50 or
                data["humidity"] < 10 or
                data["humidity"] > 100 or
                data["ph"] < 3 or
                data["ph"] > 10 or
                data["rainfall"] < 0
            ):

                flash(
                    "Please enter realistic agricultural values.",
                    "danger"
                )

                return redirect(
                    url_for("main.predict")
                )

            # ------------------------------------
            # Prevent Invalid Test Inputs
            # ------------------------------------

            if (
                data["N"] == 0 and
                data["P"] == 0 and
                data["K"] == 0 and
                data["rainfall"] == 0
            ):

                flash(
                    "Input values cannot all be zero.",
                    "danger"
                )

                return redirect(
                    url_for("main.predict")
                )

            # ------------------------------------
            # Run ML Model
            # ------------------------------------

            result = predict_crop(data)

            crop = result["crop"]

            explanation = result["explanation"]

            # Get confidence from predict_crop, default to model accuracy
            confidence = result.get(
                "confidence",
                99.55
            )

            # ------------------------------------
            # Save Prediction History
            # ------------------------------------

            prediction_record = Prediction(
                user_id=current_user.id,
                crop=crop,
                confidence=confidence,
                N=data["N"],
                P=data["P"],
                K=data["K"],
                ph=data["ph"],
                temperature=data["temperature"],
                humidity=data["humidity"],
                rainfall=data["rainfall"]
            )

            db.session.add(
                prediction_record
            )

            db.session.commit()

            # ------------------------------------
            # Automatically Load Crop Image
            # ------------------------------------

            image_path = (
                f"images/crops/{crop.lower()}.jpg"
            )

            static_folder = os.path.join(
                "app",
                "static",
                image_path
            )

            if os.path.exists(
                static_folder
            ):
                crop_image = image_path
            else:
                crop_image = (
                    "images/crops/default.jpg"
                )

            # ------------------------------------
            # Render Result Page
            # ------------------------------------

            MODEL_ACCURACY = 99.55

            return render_template(
                "result.html",
                prediction=crop,
                confidence=MODEL_ACCURACY,
                explanation=explanation,
                inputs=data,
                crop_image=crop_image,
                user=current_user
            )

        except Exception as e:

            db.session.rollback()

            print(
                f"Prediction Error: {e}"
            )

            flash(
                f"Prediction Error: {str(e)}",
                "danger"
            )

            return redirect(
                url_for("main.predict")
                )

    return render_template(
        "predict.html",
        user=current_user
    )

# ------------------------------------------------
# PREDICTION HISTORY
# ------------------------------------------------

@main_bp.route("/history")
@login_required
def history():

    history = (
        Prediction.query
        .filter_by(user_id=current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    top_crop = None

    if history:

        top_crop = (
            db.session.query(
                Prediction.crop,
                func.count(Prediction.crop)
            )
            .filter(
                Prediction.user_id == current_user.id
            )
            .group_by(Prediction.crop)
            .order_by(
                func.count(Prediction.crop).desc()
            )
            .first()
        )

        if top_crop:
            top_crop = top_crop[0]

    return render_template(
        "history.html",
        history=history,
        top_crop=top_crop,
        user=current_user
    )



# ------------------------------------------------
# DELETE PREDICTION HISTORY ENTRY
# ------------------------------------------------

@main_bp.route(
    "/history/delete/<int:id>",
    methods=["POST"]
)
@login_required
def delete_history(id):

    prediction = Prediction.query.get_or_404(id)

    if prediction.user_id != current_user.id:

        abort(403)

    db.session.delete(prediction)

    db.session.commit()

    return redirect(
        url_for("main.history")
    )


@main_bp.route("/prediction/<int:prediction_id>")
@login_required
def view_prediction(prediction_id):
    """
    View a previously saved prediction.
    """

    prediction = Prediction.query.get_or_404(
        prediction_id
    )

    # Security check
    if prediction.user_id != current_user.id:
        abort(403)

    crop_image = (
        f"images/crops/{prediction.crop.lower()}.jpg"
    )

    inputs = {
        "N": prediction.N,
        "P": prediction.P,
        "K": prediction.K,
        "ph": prediction.ph,
        "temperature": prediction.temperature,
        "humidity": prediction.humidity,
        "rainfall": prediction.rainfall
    }
    MODEL_ACCURACY = 99.55
   
    return render_template(
        "result.html",
        prediction=prediction.crop,
        confidence=MODEL_ACCURACY,
        explanation=[
            "This recommendation was retrieved from your prediction history."
        ],
        inputs=inputs,
        crop_image=crop_image,
        user=current_user
    )