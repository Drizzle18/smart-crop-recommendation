# Smart Crop Recommendation

Professional crop recommendation web application using a Random Forest model to suggest optimal crops based on soil and environmental inputs.

---

## Overview

Smart Crop Recommendation is a Flask web application that lets authenticated users submit soil and climate parameters (N, P, K, pH, temperature, humidity, rainfall) and receive a recommended crop along with explanations. The app stores prediction history per user, allows viewing/deleting past predictions, and ships with a pre-trained scikit-learn pipeline.

This README documents repository layout, setup, runtime, model training, database details, and how to extend or deploy the application.

---


## Project Objectives

The Smart Crop Recommendation System was developed to:

- Help farmers make informed crop selection decisions.
- Reduce poor crop yield caused by unsuitable environmental conditions.
- Apply Machine Learning techniques to agriculture.
- Provide a simple and user-friendly platform for crop recommendation.
- Store and manage prediction history for future reference.
- Demonstrate the practical application of Artificial Intelligence in agriculture.

## Features

- User registration, login, logout, password reset via email
- Input form for soil & climate parameters and prediction UI
- Trained Random Forest pipeline (`crop_pipeline.pkl`) for production predictions
- Prediction history stored per user (with  inputs and timestamp)
- Search and filter history, responsive UI
- Simple explanation engine that returns human-friendly reasons for recommendations

---

## Tech Stack

- Python 3.10+ (venv recommended)
- Flask (web framework)
- SQLAlchemy + Flask-Migrate (database + migrations)
- Flask-Login (auth)
- scikit-learn, pandas, joblib (ML/model persistence)
- PostgreSQL (configured via `DATABASE_URL`)

---

## Repository Structure (key files)

- `app/` — Flask application package
	- `__init__.py` — application factory
	- `extensions.py` — shared extension instances (`db`, `login_manager`, `mail`, `migrate`)
	- `routes/` — route blueprints
		- `main_routes.py` — dashboard, predict, history, result
		- `auth_routes.py` — signup/login/logout/password reset
	- `models/` — SQLAlchemy models
		- `user.py` — `User` model
		- `prediction.py` — `Prediction` model
	- `templates/` — Jinja2 HTML templates (`predict.html`, `result.html`, `dashboard.html`, `history.html`, etc.)
	- `static/` — CSS, JS, images (UI assets)
- `src/` — ML code and training utilities
	- `data_preprocessing.py` — data loading & validation
	- `train_model.py` — GridSearchCV training and export (saves pipeline to `models/crop_pipeline.pkl`)
	- `predict.py` — loads pipeline and returns prediction + explanation
- `models/` — serialized model artifacts used in production (`crop_pipeline.pkl`, `crop_model.pkl`)
- `migrations/` — Alembic migration scripts
- `.env` — environment variables (not committed; contains `DATABASE_URL`, `SECRET_KEY`, mail settings)
- `requirements.txt` — pinned Python dependencies

---

## Quick Start — Development

Prerequisites:
- Python 3.10+ installed
- PostgreSQL or a hosted PostgreSQL instance (connection URI in `DATABASE_URL`)

1. Clone the repo and create a virtual environment

```bash
git clone <repo-url>
cd smart-crop-recommendation
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file at the project root (or export env vars). Required keys:

```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/dbname
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=you@example.com
MAIL_PASSWORD=yourpassword
MAIL_DEFAULT_SENDER=you@example.com
```

4. Initialize the database (first-time only)

```bash
python create_db.py
# or use flask-migrate commands if you prefer
flask db upgrade
```

5. Run the app

```bash
python -m app.main
# Open http://127.0.0.1:5000/
```

---

## Model / Training

- Training code: `src/train_model.py` — builds a `sklearn` pipeline (RandomForestClassifier), runs `GridSearchCV`, prints best parameters and test accuracy, and writes a pipeline to `models/crop_pipeline.pkl`.
- Production prediction loader: `src/predict.py` — loads `models/crop_pipeline.pkl` via `joblib` and returns a `dict` with `crop`, `explanation`, `summary`, and now `confidence`.
- Pre-trained artifacts shipped in `models/` can be replaced by retraining with `train_model.py`.

To retrain locally and save a new pipeline:

```bash
python src/train_model.py
```

Tip: validate `data/crop_data.csv` before running training.

---

## Model Performance

The recommendation model was trained using a Random Forest Classifier.

### Performance Metrics

| Metric | Value |
|----------|----------|
| Accuracy | 99.55% |
| Algorithm | Random Forest |
| Training Method | GridSearchCV |
| Framework | Scikit-Learn |

The model achieved an accuracy score of **99.55%** on the test dataset, demonstrating strong predictive performance for crop recommendation tasks.

## Database Schema

- `users` table: `id`, `first_name`, `last_name`, `email` (unique), `password_hash`, `created_at`
- `predictions` table: `id`, `user_id` (FK -> users.id), `crop`, `confidence` (float), `N`, `P`, `K`, `ph`, `temperature`, `humidity`, `rainfall`, `created_at`

The migration that created the `predictions` table is in `migrations/versions/d533ed443e1e_create_predictions_table.py`.

---

## Routes / Usage

- Public
	- `/` — Landing
	- `/about` — About
	- `/signup` — Create account
	- `/login` — Login

- Authenticated (after login)
	- `/predict` — Input form to request a crop recommendation
	- `/dashboard` — Overview and recent predictions
	- `/history` — Full prediction history with search/filter
	- `/prediction/<id>` — View a previous prediction
	- `/history/delete/<id>` (POST) — Delete a history item

Use the UI or the templates in `app/templates/` for references.

---

## System Workflow

1. User registers an account.
2. User logs into the system.
3. User enters environmental and soil parameters:
   - Nitrogen (N)
   - Phosphorus (P)
   - Potassium (K)
   - Temperature
   - Humidity
   - pH
   - Rainfall
4. The Flask backend validates the inputs.
5. The trained Random Forest model generates a prediction.
6. The recommendation result is displayed with:
   - Crop name
   - Crop image
   - Explanation
   - Model accuracy
7. Prediction history is stored in PostgreSQL.
8. Users can review or delete previous predictions.

## Author

**Michael Uchenna**

- Final Year Computer Science Student
- Spiritan University Nneochi Nigeria
- Developer of the Smart Crop Recommendation System.

### Roles

- Machine Learning Engineer
- Backend Developer
- Frontend Developer
- Database Designer

### Technologies Used

- Python
- Flask
- PostgreSQL
- Scikit-Learn
- HTML
- CSS
- JavaScript
- Bootstrap

GitHub:https://github.com/Drizzle18




## System Workflow

1. User registers an account.
2. User logs into the system.
3. User enters environmental and soil parameters:
   - Nitrogen (N)
   - Phosphorus (P)
   - Potassium (K)
   - Temperature
   - Humidity
   - pH
   - Rainfall
4. The Flask backend validates the inputs.
5. The trained Random Forest model generates a prediction.
6. The recommendation result is displayed with:
   - Crop name
   - Crop image
   - Explanation
   - Model accuracy
7. Prediction history is stored in PostgreSQL.
8. Users can review or delete previous predictions.


## Acknowledgements

This project was developed as a Final Year Project in Computer Science in spiritan University Nneochi Nigera (2026).

Special thanks to:

- The creators of the Crop Recommendation Dataset.
- The Scikit-Learn development team.
- Flask framework contributors.
- Open-source communities whose tools made this project possible.


## Contributing

Contributions are welcome. Open an issue to discuss, fork the repo, create a branch for your change, and submit a pull request. Keep changes focused and add tests where relevant.

---

## License

Specify your license here (e.g., MIT). If unsure, add `LICENSE` later.

---

## Contact

Questions or help — please contact the project creator listed above.

