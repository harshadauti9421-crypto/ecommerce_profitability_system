import os
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
from utils.helpers import logger

MODELS_DIR = "models"
CONFORMAL_PATH = os.path.join(MODELS_DIR, "conformal_quantiles.json")

def load_conformal_quantiles():
    """Load precomputed validation residual quantiles for conformal prediction."""
    if os.path.exists(CONFORMAL_PATH):
        try:
            with open(CONFORMAL_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load conformal_quantiles.json: {e}")
    # Default fallback quantiles if training json missing
    return {
        "demand": {"q_80": 120.0, "q_90": 180.0, "q_95": 240.0, "std_residual": 140.0},
        "profit": {"q_80": 110000.0, "q_90": 175000.0, "q_95": 230000.0, "std_residual": 135000.0}
    }

def calculate_prediction_interval(point_estimate, residual_quantile, lower_min=0.0):
    """
    Calculate conformal prediction interval given a point estimate and residual quantile.
    """
    lower = max(lower_min, float(point_estimate - residual_quantile))
    upper = float(point_estimate + residual_quantile)
    width = float(upper - lower)
    return {
        "expected": float(point_estimate),
        "lower_bound": lower,
        "upper_bound": upper,
        "interval_width": width,
        "quantile_margin": float(residual_quantile)
    }

def estimate_uncertainty_all(*args, **kwargs):
    """
    End-to-end Split Conformal Prediction Interval calculation for PROFIT ONLY.
    Supports flexible arguments: estimate_uncertainty_all(point_profit, selling_price=..., discount_percent=..., confidence=0.90)
    or legacy signature estimate_uncertainty_all(point_demand, point_profit, ...).
    """
    if len(args) >= 2 and isinstance(args[0], (int, float, np.number)) and isinstance(args[1], (int, float, np.number)):
        # Legacy signature: (point_demand, point_profit, ...)
        point_profit = float(args[1])
        selling_price = float(args[2]) if len(args) > 2 else kwargs.get("selling_price", 0.0)
        discount_percent = float(args[3]) if len(args) > 3 else kwargs.get("discount_percent", 0.0)
        confidence = float(args[4]) if len(args) > 4 else kwargs.get("confidence", 0.90)
    elif len(args) >= 1:
        point_profit = float(args[0])
        selling_price = float(kwargs.get("selling_price", 0.0))
        discount_percent = float(kwargs.get("discount_percent", 0.0))
        confidence = float(kwargs.get("confidence", 0.90))
    else:
        point_profit = float(kwargs.get("point_profit", 0.0))
        selling_price = float(kwargs.get("selling_price", 0.0))
        discount_percent = float(kwargs.get("discount_percent", 0.0))
        confidence = float(kwargs.get("confidence", 0.90))

    quantiles = load_conformal_quantiles()
    
    # Pick quantile key based on requested confidence level
    if confidence >= 0.95:
        q_key = "q_95"
    elif confidence >= 0.90:
        q_key = "q_90"
    else:
        q_key = "q_80"
        
    profit_q = quantiles.get("profit", {}).get(q_key, 110.0)
    
    # Profit Interval
    profit_interval = calculate_prediction_interval(point_profit, profit_q, lower_min=-float("inf"))
    
    # Downside Risk & Loss Probability P(Profit < 0)
    std_prof_residual = quantiles.get("profit", {}).get("std_residual", profit_q / 1.645)
    if std_prof_residual > 0:
        z_score = (0.0 - point_profit) / std_prof_residual
        loss_prob = float(norm.cdf(z_score))
    else:
        loss_prob = 0.0 if point_profit >= 0 else 1.0
        
    loss_prob = float(np.clip(loss_prob, 0.0, 1.0))
    
    # Expected Downside Loss
    if loss_prob > 0.001:
        expected_downside = float(abs(min(0.0, profit_interval["lower_bound"])))
    else:
        expected_downside = 0.0
        
    return {
        "confidence_level": confidence,
        "profit": profit_interval,
        "loss_probability": loss_prob,
        "loss_probability_pct": float(loss_prob * 100.0),
        "expected_downside": expected_downside
    }

def evaluate_conformal_calibration(y_true, y_pred, quantiles_margin):
    """
    Evaluate empirical calibration metrics:
    - PICP: Prediction Interval Coverage Probability (fraction of actuals in interval)
    - MPIW: Mean Prediction Interval Width
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    lower_bounds = y_pred - quantiles_margin
    upper_bounds = y_pred + quantiles_margin
    
    covered = (y_true >= lower_bounds) & (y_true <= upper_bounds)
    picp = float(np.mean(covered))
    mpiw = float(np.mean(upper_bounds - lower_bounds))
    
    return {
        "PICP": picp,
        "PICP_pct": picp * 100.0,
        "MPIW": mpiw
    }
