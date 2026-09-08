"""
SHAP Explainable AI Module for Page 2 Business Dashboard
Provides local and global feature attribution for Net Profit and Demand models
without altering any predictions or retraining models.
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import shap

from src.ui.theme import COLORS
from utils.helpers import logger

MODELS_DIR = "models"

def clean_feature_name(name):
    """Clean pipeline feature names for human readability."""
    clean = name.replace("num__", "").replace("cat__", "")
    parts = clean.split("_")
    return " ".join([p.capitalize() for p in parts])

def get_feature_names_from_pipeline(pipeline):
    """Extract readable feature names from scikit-learn ColumnTransformer."""
    try:
        raw_names = pipeline.get_feature_names_out()
        return [clean_feature_name(f) for f in raw_names]
    except Exception:
        from src.feature_engineering import ALL_INPUT_FEATURES
        return ALL_INPUT_FEATURES

def explain_model_prediction_shap(model, X_transformed, feature_names):
    """
    Computes local SHAP values for a single prediction instance using TreeExplainer or Explainer.
    Returns structured positive factors, negative factors, base value, and feature attribution DataFrame.
    """
    try:
        # Determine appropriate SHAP explainer
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_transformed)
            base_value = explainer.expected_value
        except Exception:
            explainer = shap.Explainer(model, X_transformed)
            shap_values = explainer(X_transformed).values
            base_value = explainer.expected_value if hasattr(explainer, "expected_value") else 0.0

        if isinstance(shap_values, list):
            shap_vals = shap_values[0]
        else:
            shap_vals = shap_values

        if hasattr(base_value, "__len__") and len(base_value) > 0:
            base_val = float(base_value[0])
        else:
            base_val = float(base_value)

        # Handle 2D vs 1D array shapes
        if len(shap_vals.shape) > 1:
            vals = shap_vals[0]
        else:
            vals = shap_vals

        df_shap = pd.DataFrame({
            "Feature": feature_names[:len(vals)],
            "SHAP Value": vals,
            "Absolute SHAP": np.abs(vals),
            "Direction": ["↑ Positive" if v >= 0 else "↓ Negative" for v in vals]
        })
        df_shap = df_shap.sort_values(by="Absolute SHAP", ascending=False).reset_index(drop=True)

        pos_factors = df_shap[df_shap["SHAP Value"] > 0].head(5).to_dict(orient="records")
        neg_factors = df_shap[df_shap["SHAP Value"] < 0].head(5).to_dict(orient="records")

        return {
            "status": "SUCCESS",
            "base_value": base_val,
            "df_shap": df_shap,
            "pos_factors": pos_factors,
            "neg_factors": neg_factors
        }
    except Exception as e:
        logger.warning(f"SHAP explanation exception: {e}")
        return {
            "status": "ERROR",
            "message": str(e)
        }

def render_shap_explainability_section(analysis_result, df_dataset=None):
    """
    Renders Page 2 SHAP Explainable AI section.
    Displays local feature attributions, waterfall/bar charts, top positive/negative factors,
    and global feature importance for Net Profit & Demand models.
    """
    st.markdown("<div class='section-header-title'>🧠 EXPLAINABLE AI — WHY THIS PREDICTION? (SHAP ATTRIBUTION)</div>", unsafe_allow_html=True)

    if analysis_result is None or "X_transformed" not in analysis_result:
        st.info("Run product analysis first to view SHAP model explanations.")
        return

    X_transformed = analysis_result["X_transformed"]
    
    pipeline_path = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
    if not os.path.exists(pipeline_path):
        st.warning("Preprocessing pipeline not found. SHAP explanations unavailable.")
        return

    try:
        pipeline = joblib.load(pipeline_path)
        feature_names = get_feature_names_from_pipeline(pipeline)
    except Exception as e:
        st.warning(f"Unable to load feature pipeline: {e}")
        return

    # Profit Model Explanation
    profit_model_path = os.path.join(MODELS_DIR, "best_profit_model.pkl")
    if os.path.exists(profit_model_path):
        try:
            profit_model = joblib.load(profit_model_path)
            p_exp = explain_model_prediction_shap(profit_model, X_transformed, feature_names)

            if p_exp["status"] == "SUCCESS":
                st.markdown(f"#### Net Profit Model Attribution &nbsp;|&nbsp; Base Output: `₹{p_exp['base_value']:,.2f}`")
                
                pos_col, neg_col = st.columns(2)
                with pos_col:
                    st.markdown("### 🟢 Top Positive Factors (Pushing Profit Higher)")
                    for f in p_exp["pos_factors"]:
                        st.markdown(f"- **{f['Feature']}**: <span style='color:#047857; font-weight:700;'>+₹{f['SHAP Value']:,.2f}</span>", unsafe_allow_html=True)
                    if not p_exp["pos_factors"]:
                        st.caption("None identified for this product scenario.")

                with neg_col:
                    st.markdown("### 🔴 Top Negative Factors (Pushing Profit Lower)")
                    for f in p_exp["neg_factors"]:
                        st.markdown(f"- **{f['Feature']}**: <span style='color:#B91C1C; font-weight:700;'>-₹{abs(f['SHAP Value']):,.2f}</span>", unsafe_allow_html=True)
                    if not p_exp["neg_factors"]:
                        st.caption("None identified for this product scenario.")

                st.markdown("---")

                # Local SHAP Contribution Bar Chart
                st.markdown("### 📊 Local SHAP Feature Contribution Chart (Net Profit)")
                df_top = p_exp["df_shap"].head(10).sort_values(by="SHAP Value", ascending=True)
                
                fig_p_shap = px.bar(
                    df_top,
                    x="SHAP Value",
                    y="Feature",
                    orientation="h",
                    color="Direction",
                    color_discrete_map={"↑ Positive": COLORS["positive"], "↓ Negative": COLORS["negative"]},
                    title="Top Features Influencing Net Profit Prediction (₹)"
                )
                fig_p_shap.update_layout(
                    paper_bgcolor=COLORS["card_bg"],
                    plot_bgcolor=COLORS["card_bg"],
                    font=dict(color=COLORS["text_primary"]),
                    xaxis=dict(gridcolor="#F1F5F9", tickfont=dict(color=COLORS["text_secondary"])),
                    yaxis=dict(gridcolor="#F1F5F9", tickfont=dict(color=COLORS["text_primary"], size=12)),
                    height=360
                )
                st.plotly_chart(fig_p_shap, use_container_width=True)

                # Display SHAP Contribution Table
                with st.expander("📋 Detailed SHAP Value Contribution Table"):
                    st.dataframe(p_exp["df_shap"][["Feature", "SHAP Value", "Direction"]], hide_index=True, use_container_width=True)

            else:
                st.warning("SHAP explainability is currently unavailable for this model configuration.")
                st.caption(f"Technical note: {p_exp.get('message', '')}")
        except Exception as err:
            st.info("Explainability is temporarily unavailable for this model. The prediction and business analysis remain available.")
            logger.warning(f"Profit SHAP rendering error: {err}")

    st.caption("ℹ️ **SHAP Research Interpretation**: SHAP values indicate how individual features contribute to the model prediction. Positive SHAP values push the prediction higher, while negative SHAP values push it lower. The magnitude represents the strength of contribution relative to the model's output. SHAP provides model attribution, not causal inference.")

