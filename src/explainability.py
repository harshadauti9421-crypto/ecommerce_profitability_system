import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import permutation_importance

import shap
from src.preprocessing import load_pipeline
from src.feature_engineering import add_engineered_features, prepare_feature_matrices
from src.data_loader import load_and_validate_data
from utils.helpers import logger

MODELS_DIR = "models"
DATA_PATH = os.path.join("data", "ecommerce_data.csv")

def get_feature_names(pipeline):
    """Retrieve transformed feature names from ColumnTransformer."""
    try:
        if hasattr(pipeline, "get_feature_names_out"):
            names = list(pipeline.get_feature_names_out())
            # Clean prefixes like num__ or cat__
            clean_names = [n.replace("num__", "").replace("cat__", "") for n in names]
            return clean_names
        return [f"feature_{i}" for i in range(100)]
    except Exception as e:
        logger.warning(f"Could not extract feature names from pipeline: {str(e)}")
        return [f"feature_{i}" for i in range(100)]

def explain_prediction_shap(X_input_df, model_type="profit"):
    """
    Generate SHAP global feature importance and local prediction explanation.
    Includes safe fallback to Permutation Importance if SHAP fails.
    Returns:
    - fig_global: matplotlib figure for global importance
    - fig_local: matplotlib figure for local single prediction contribution
    - explanation_df: DataFrame listing top feature contributions
    """
    logger.info(f"Generating SHAP explanation for model type: '{model_type}'")
    
    try:
        pipeline = load_pipeline(os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl"))
        model_path = os.path.join(MODELS_DIR, f"best_{model_type}_model.pkl")
        model = joblib.load(model_path)
        
        feature_names = get_feature_names(pipeline)
        X_trans = pipeline.transform(X_input_df)
        
        # Load sample training background data for SHAP explainer
        df_bg = load_and_validate_data(DATA_PATH).sample(n=min(200, 1000), random_state=42)
        X_bg, _ = prepare_feature_matrices(df_bg, "profit")
        X_bg_trans = pipeline.transform(X_bg)
        
        shap_values = None
        
        # Attempt TreeExplainer for tree models
        try:
            if hasattr(model, "feature_importances_"):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer(X_trans)
            elif hasattr(model, "coef_"):
                explainer = shap.LinearExplainer(model, X_bg_trans)
                shap_values = explainer(X_trans)
            else:
                # KernelExplainer / Explainer fallback
                explainer = shap.Explainer(model.predict, X_bg_trans[:50])
                shap_values = explainer(X_trans[:1])
        except Exception as shap_err:
            logger.warning(f"Primary SHAP explainer failed ({str(shap_err)}). Trying KernelExplainer...")
            explainer = shap.KernelExplainer(model.predict, X_bg_trans[:30])
            shap_vals_raw = explainer.shap_values(X_trans[:1])
            shap_values = shap.Explanation(
                values=shap_vals_raw[0] if isinstance(shap_vals_raw, list) else shap_vals_raw,
                feature_names=feature_names[:X_trans.shape[1]]
            )

        # Build Local Feature Importance Plot
        fig_local, ax_local = plt.subplots(figsize=(8, 5))
        vals = shap_values.values[0] if hasattr(shap_values, "values") else shap_values[0]
        if vals.ndim > 1:
            vals = vals.ravel()
            
        top_indices = np.argsort(np.abs(vals))[-10:] # Top 10 features
        top_names = [feature_names[i] if i < len(feature_names) else f"Feat_{i}" for i in top_indices]
        top_vals = vals[top_indices]
        
        colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in top_vals]
        ax_local.barh(top_names, top_vals, color=colors)
        ax_local.set_xlabel("SHAP Value (Impact on Prediction)")
        ax_local.set_title(f"Local SHAP Explanation - Why Model Predicted This {model_type.capitalize()}")
        ax_local.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        
        # Build Global Feature Importance Plot (Background sample)
        fig_global, ax_global = plt.subplots(figsize=(8, 5))
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            g_indices = np.argsort(importances)[-10:]
            g_names = [feature_names[i] if i < len(feature_names) else f"Feat_{i}" for i in g_indices]
            g_vals = importances[g_indices]
            ax_global.barh(g_names, g_vals, color="#3498db")
            ax_global.set_xlabel("Feature Importance Score")
            ax_global.set_title(f"Global Model Feature Importance ({model_type.capitalize()})")
        else:
            # Permutation importance fallback
            perm_imp = permutation_importance(model, X_bg_trans[:100], model.predict(X_bg_trans[:100]), n_repeats=5, random_state=42)
            g_indices = np.argsort(perm_imp.importances_mean)[-10:]
            g_names = [feature_names[i] if i < len(feature_names) else f"Feat_{i}" for i in g_indices]
            g_vals = perm_imp.importances_mean[g_indices]
            ax_global.barh(g_names, g_vals, color="#9b59b6")
            ax_global.set_xlabel("Permutation Importance")
            ax_global.set_title(f"Global Permutation Importance ({model_type.capitalize()})")
            
        ax_global.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        
        # Summary DataFrame
        explanation_df = pd.DataFrame({
            "Feature": top_names[::-1],
            "Impact": top_vals[::-1],
            "Effect": ["Increased Prediction" if v >= 0 else "Decreased Prediction" for v in top_vals[::-1]]
        })
        
        return fig_global, fig_local, explanation_df

    except Exception as e:
        logger.error(f"SHAP explanation fallback triggered due to: {str(e)}")
        # Safe Fallback Plot
        fig_global, ax_global = plt.subplots(figsize=(8, 4))
        ax_global.text(0.5, 0.5, "Global Importance (Standard Model Feature Ranking)", ha="center", va="center")
        fig_local, ax_local = plt.subplots(figsize=(8, 4))
        ax_local.text(0.5, 0.5, "Local Explanation Unavailable (Using Permutation Importance)", ha="center", va="center")
        explanation_df = pd.DataFrame([{"Feature": "General Parameters", "Impact": 0.0, "Effect": "Neutral"}])
        return fig_global, fig_local, explanation_df
