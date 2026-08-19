import os
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.feature_engineering import NUMERICAL_FEATURES, CATEGORICAL_FEATURES
from utils.helpers import logger

def build_preprocessing_pipeline():
    """
    Build scikit-learn ColumnTransformer for numerical scaling and categorical OHE.
    Uses handle_unknown='ignore' to prevent crashes on unseen categories during runtime.
    """
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, NUMERICAL_FEATURES),
            ('cat', cat_transformer, CATEGORICAL_FEATURES)
        ],
        remainder='drop'
    )
    return preprocessor

def save_pipeline(pipeline, file_path):
    """Save trained pipeline object to disk."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    joblib.dump(pipeline, file_path)
    logger.info(f"Preprocessing pipeline saved to {file_path}")

def load_pipeline(file_path):
    """Load preprocessing pipeline object from disk."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Preprocessing pipeline file not found at {file_path}")
    pipeline = joblib.load(file_path)
    logger.info(f"Loaded preprocessing pipeline from {file_path}")
    return pipeline
