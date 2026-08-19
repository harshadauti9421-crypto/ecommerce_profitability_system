import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor

from src.data_loader import load_and_validate_data
from src.feature_engineering import add_engineered_features, prepare_feature_matrices
from src.preprocessing import build_preprocessing_pipeline, save_pipeline
from src.evaluate_models import calculate_metrics
from utils.helpers import logger

DATA_PATH = os.path.join("data", "ecommerce_data.csv")
MODELS_DIR = "models"

def train_and_evaluate_all():
    """
    Main training workflow:
    1. Load & validate dataset
    2. Add engineered features
    3. Split 70% Train, 15% Val, 15% Test
    4. Fit ColumnTransformer on Train
    5. Train 4 regression models for Demand & Profit
    6. Evaluate on Validation set to pick best model
    7. Evaluate on Test set for final reporting table
    8. Save all models, best models, preprocessor, and metrics JSON
    """
    logger.info("--- Starting Model Training & Evaluation Workflow ---")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # 1. Load dataset
    df = load_and_validate_data(DATA_PATH)
    df_engineered = add_engineered_features(df)
    
    # Define Targets
    targets = {
        "demand": "demand",
        "profit": "profit"
    }
    
    overall_metrics = {
        "demand": {"models": {}, "best_model": None},
        "profit": {"models": {}, "best_model": None}
    }
    
    trained_demand_models = {}
    trained_profit_models = {}
    
    preprocessor = build_preprocessing_pipeline()
    
    for target_key, target_col in targets.items():
        logger.info(f"\n================ Training Models for Target: '{target_col.upper()}' ================")
        
        X, y = prepare_feature_matrices(df_engineered, target_col)
        
        # 70% Train, 15% Val, 15% Test
        X_train_full, X_test, y_train_full, y_test = train_test_split(
            X, y, test_size=0.15, random_state=42
        )
        
        # 0.15 / (1.0 - 0.15) = 0.17647 => 70% train, 15% val overall
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_full, y_train_full, test_size=0.17647, random_state=42
        )
        
        logger.info(f"Data Split shapes -> Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
        
        # Fit preprocessor on X_train only
        if target_key == "demand":
            X_train_trans = preprocessor.fit_transform(X_train)
            save_pipeline(preprocessor, os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl"))
        else:
            X_train_trans = preprocessor.transform(X_train)
            
        X_val_trans = preprocessor.transform(X_val)
        X_test_trans = preprocessor.transform(X_test)
        
        # Define the 4 models
        models = {
            "Multiple Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1),
            "XGBoost": XGBRegressor(n_estimators=60, max_depth=6, random_state=42, n_jobs=-1, learning_rate=0.1),
            "Artificial Neural Network": MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=40, batch_size=256, random_state=42)
        }
        
        best_val_r2 = -float("inf")
        best_model_name = None
        best_model_obj = None
        
        target_trained_dict = {}
        
        for name, model in models.items():
            logger.info(f"Training {name}...")
            model.fit(X_train_trans, y_train)
            
            # Predict on Val and Test
            val_preds = model.predict(X_val_trans)
            test_preds = model.predict(X_test_trans)
            
            val_metrics = calculate_metrics(y_val, val_preds)
            test_metrics = calculate_metrics(y_test, test_preds)
            
            logger.info(f"-> {name} | Val R2: {val_metrics['R2']} | Test R2: {test_metrics['R2']} | Test MAE: {test_metrics['MAE']}")
            
            overall_metrics[target_key]["models"][name] = {
                "val": val_metrics,
                "test": test_metrics
            }
            
            target_trained_dict[name] = model
            
            # Model selection based on Validation R2
            if val_metrics["R2"] > best_val_r2:
                best_val_r2 = val_metrics["R2"]
                best_model_name = name
                best_model_obj = model
                
        logger.info(f"*** WINNING MODEL for {target_key.upper()}: '{best_model_name}' (Val R2: {best_val_r2}) ***")
        overall_metrics[target_key]["best_model"] = best_model_name
        
        # Save winning model and all models
        if target_key == "demand":
            joblib.dump(best_model_obj, os.path.join(MODELS_DIR, "best_demand_model.pkl"))
            joblib.dump(target_trained_dict, os.path.join(MODELS_DIR, "all_demand_models.pkl"))
        else:
            joblib.dump(best_model_obj, os.path.join(MODELS_DIR, "best_profit_model.pkl"))
            joblib.dump(target_trained_dict, os.path.join(MODELS_DIR, "all_profit_models.pkl"))
            
    # Save overall metrics JSON
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(overall_metrics, f, indent=2)
        
    logger.info(f"All training complete. Metrics saved to {metrics_path}")
    return overall_metrics

if __name__ == "__main__":
    train_and_evaluate_all()
