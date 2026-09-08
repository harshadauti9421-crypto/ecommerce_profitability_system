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

from src.data_loader import load_and_validate_data, generate_data_quality_report
from src.feature_engineering import add_engineered_features, prepare_feature_matrices
from src.preprocessing import build_preprocessing_pipeline, save_pipeline
from src.evaluate_models import calculate_metrics, rank_and_select_models
from utils.helpers import logger

DATA_PATH = os.path.join("data", "ecommerce_sales_dataset.csv")
MODELS_DIR = "models"

def train_and_evaluate_all():
    """
    Main training workflow for Global E-Commerce Sales Dataset | 2021–2024 (10,000 records)
    """
    logger.info("--- Starting Model Training & Evaluation Workflow ---")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # 1. Load dataset
    df = load_and_validate_data(DATA_PATH if os.path.exists(DATA_PATH) else None)
    generate_data_quality_report(df, dataset_name="Global E-Commerce Sales Dataset | 2021–2024", dataset_type="REAL-WORLD DATA")
    df_engineered = add_engineered_features(df)
    
    # Define Target: Profit ONLY
    targets = {
        "profit": "profit"
    }
    
    overall_metrics = {
        "profit": {"models": {}, "best_model": None}
    }
    
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
        X_train_trans = preprocessor.fit_transform(X_train)
        save_pipeline(preprocessor, os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl"))
            
        X_val_trans = preprocessor.transform(X_val)
        X_test_trans = preprocessor.transform(X_test)
        
        # Define supported ML Regressors dynamically
        models = {
            "Multiple Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1),
            "XGBoost": XGBRegressor(n_estimators=60, max_depth=6, random_state=42, n_jobs=-1, learning_rate=0.1)
        }

        try:
            from lightgbm import LGBMRegressor
            models["LightGBM"] = LGBMRegressor(n_estimators=60, max_depth=6, random_state=42, verbose=-1)
        except Exception:
            pass

        try:
            from catboost import CatBoostRegressor
            models["CatBoost"] = CatBoostRegressor(iterations=60, depth=6, random_state=42, verbose=0)
        except Exception:
            pass

        models["Artificial Neural Network"] = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=40, batch_size=256, random_state=42)

        target_trained_dict = {}
        
        for name, model in models.items():
            try:
                logger.info(f"Training {name}...")
                model.fit(X_train_trans, y_train)
                
                # Predict on Val and Test
                val_preds = model.predict(X_val_trans)
                test_preds = model.predict(X_test_trans)
                
                val_metrics = calculate_metrics(y_val, val_preds)
                test_metrics = calculate_metrics(y_test, test_preds)
                
                logger.info(f"-> {name} | Val R2: {val_metrics['R2']} | Test R2: {test_metrics['R2']} | Test MAE: {test_metrics['MAE']} | Test RMSE: {test_metrics['RMSE']}")
                
                overall_metrics[target_key]["models"][name] = {
                    "val": val_metrics,
                    "test": test_metrics
                }
                
                target_trained_dict[name] = model
            except Exception as train_err:
                logger.error(f"Failed training for model {name}: {str(train_err)}")
                overall_metrics[target_key]["models"][name] = {
                    "status": "Failed",
                    "error": str(train_err)
                }

        # Select winner dynamically using strict 4-tier decision hierarchy
        best_model_name, selection_reason, _ = rank_and_select_models(overall_metrics[target_key]["models"])
        
        if best_model_name is not None and best_model_name in target_trained_dict:
            best_model_obj = target_trained_dict[best_model_name]
            logger.info(f"*** WINNING MODEL for {target_key.upper()}: '{best_model_name}' ***")
            logger.info(f"    Selection Reason: {selection_reason}")
            overall_metrics[target_key]["best_model"] = best_model_name
            overall_metrics[target_key]["selection_reason"] = selection_reason
        else:
            best_model_obj = None
            logger.error(f"No valid winning model could be selected for {target_key.upper()}.")
            overall_metrics[target_key]["best_model"] = None
            overall_metrics[target_key]["selection_reason"] = "No valid model evaluated."
        
        # Compute empirical conformal prediction quantiles on validation set for PROFIT
        val_preds_win = best_model_obj.predict(X_val_trans)
        val_residuals = np.abs(y_val - val_preds_win)
        q_80 = float(np.percentile(val_residuals, 80))
        q_90 = float(np.percentile(val_residuals, 90))
        q_95 = float(np.percentile(val_residuals, 95))
        std_res = float(np.std(y_val - val_preds_win))
        
        overall_metrics["conformal"] = {
            "profit": {
                "q_80": q_80,
                "q_90": q_90,
                "q_95": q_95,
                "std_residual": std_res
            }
        }

        # Save winning profit model and all profit models
        joblib.dump(best_model_obj, os.path.join(MODELS_DIR, "best_profit_model.pkl"))
        joblib.dump(target_trained_dict, os.path.join(MODELS_DIR, "all_profit_models.pkl"))
            
    # Save conformal quantiles JSON
    conformal_path = os.path.join(MODELS_DIR, "conformal_quantiles.json")
    with open(conformal_path, "w", encoding="utf-8") as f:
        json.dump(overall_metrics.get("conformal", {}), f, indent=2)
    logger.info(f"Conformal prediction quantiles saved to {conformal_path}")

    # Save overall metrics JSON
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(overall_metrics, f, indent=2)
        
    logger.info(f"All training complete. Metrics saved to {metrics_path}")
    return overall_metrics

if __name__ == "__main__":
    train_and_evaluate_all()
