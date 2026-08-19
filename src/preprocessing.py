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
    """
    Load preprocessing pipeline object from disk.
    If unpickling fails due to a scikit-learn version mismatch across environments
    (e.g., _RemainderColsList AttributeError), refits and updates the pipeline in-environment.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Preprocessing pipeline file not found at {file_path}")
    
    try:
        pipeline = joblib.load(file_path)
        logger.info(f"Loaded preprocessing pipeline from {file_path}")
        return pipeline
    except Exception as e:
        logger.warning(f"Failed to unpickle pipeline ({str(e)}). Rebuilding and refitting pipeline for current environment...")
        from src.data_loader import load_and_validate_data
        from src.feature_engineering import add_engineered_features, prepare_feature_matrices
        
        data_path = os.path.join("data", "ecommerce_data.csv")
        df = load_and_validate_data(data_path)
        df_engineered = add_engineered_features(df)
        X, _ = prepare_feature_matrices(df_engineered, "profit")
        
        pipeline = build_preprocessing_pipeline()
        pipeline.fit(X)
        save_pipeline(pipeline, file_path)
        return pipeline
