"""
PRODUCTION-READY MODEL TRAINING MODULE (PIPELINE VERSION)
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "crop_data.csv"
MODEL_PATH = BASE_DIR / "models" / "crop_pipeline.pkl"


# -------------------------
# LOAD DATA
# -------------------------
def load_data():
    df = pd.read_csv(DATA_PATH)

    if "label" not in df.columns:
        raise ValueError("Dataset must contain 'label' column")

    X = df.drop("label", axis=1)
    y = df["label"]

    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# -------------------------
# BUILD PIPELINE
# -------------------------
def build_pipeline():
    pipeline = Pipeline([
        ("model", RandomForestClassifier(random_state=42))
    ])
    return pipeline


# -------------------------
# TRAIN MODEL
# -------------------------
def train_model():
    X_train, X_test, y_train, y_test = load_data()

    pipeline = build_pipeline()

    param_grid = {
        "model__n_estimators": [50, 100, 150],
        "model__max_depth": [None, 10, 20, 30],
        "model__min_samples_split": [2, 5, 10],
    }

    grid = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
        refit=True
    )

    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_

    acc = best_model.score(X_test, y_test)

    print("Best Params:", grid.best_params_)
    print("Test Accuracy:", acc)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    print(f"Saved pipeline model → {MODEL_PATH}")

    return best_model


if __name__ == "__main__":
    train_model()