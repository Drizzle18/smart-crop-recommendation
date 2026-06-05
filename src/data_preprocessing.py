"""
DATA PREPROCESSING MODULE

This module is responsible for loading and preparing the dataset
for machine learning tasks.

It performs the following operations:
- Loads the crop dataset from CSV file
- Separates input features (soil and environmental conditions)
  from the target variable (crop label)
- Splits the dataset into training and testing sets

This ensures that the model receives clean and structured data
for training and evaluation.
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "crop_data.csv"


def load_raw_data():
    """Loads and validates the raw crop dataset."""

    df = pd.read_csv(DATA_PATH)

    if "label" not in df.columns:
        raise ValueError("Dataset must contain a 'label' column.")

    df = df.copy()
    df.dropna(subset=["label"], inplace=True)

    feature_columns = df.columns.drop("label")
    non_numeric = [col for col in feature_columns if df[col].dtype == object]
    if non_numeric:
        raise ValueError(
            f"Expected numeric feature columns, but found non-numeric columns: {non_numeric}"
        )

    df[feature_columns] = df[feature_columns].fillna(df[feature_columns].median())
    return df


def load_data(test_size: float = 0.2, random_state: int = 42):
    """
    Loads dataset and splits it into training and testing sets.

    Returns:
        X_train: Training feature set
        X_test: Testing feature set
        y_train: Training labels
        y_test: Testing labels
    """

    df = load_raw_data()
    X = df.drop("label", axis=1)
    y = df["label"]

    stratify = y if y.nunique() > 1 else None
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )