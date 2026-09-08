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

def estimate_uncertainty_all(point_demand, point_profit, selling_price, discount_percent, confidence=0.90):
    """
    End-to-end Split Conformal Prediction Interval calculation for Demand, Revenue, and Profit.
    """
    quantiles = load_conformal_quantiles()
    
    # Pick quantile key based on requested confidence level
    if confidence >= 0.95:
        q_key = "q_95"
    elif confidence >= 0.90:
        q_key = "q_90"
    else:
        q_key = "q_80"
        
    demand_q = quantiles.get("demand", {}).get(q_key, 180.0)
    profit_q = quantiles.get("profit", {}).get(q_key, 175000.0)
    
    # 1. Demand Interval
    demand_interval = calculate_prediction_interval(point_demand, demand_q, lower_min=1.0)
    
    # 2. Revenue Interval derived from Demand Interval & Net Unit Price
    net_unit_price = max(1.0, selling_price * (1.0 - discount_percent / 100.0))
    expected_revenue = point_demand * net_unit_price
    rev_lower = demand_interval["lower_bound"] * net_unit_price
    rev_upper = demand_interval["upper_bound"] * net_unit_price
    
    revenue_interval = {
        "expected": float(expected_revenue),
        "lower_bound": float(rev_lower),
        "upper_bound": float(rev_upper),
        "interval_width": float(rev_upper - rev_lower)
    }
    
    # 3. Profit Interval
    profit_interval = calculate_prediction_interval(point_profit, profit_q, lower_min=-float("inf"))
    
    # 4. Downside Risk & Loss Probability P(Profit < 0)
    std_prof_residual = quantiles.get("profit", {}).get("std_residual", profit_q / 1.645)
    if std_prof_residual > 0:
        # Standard normal CDF approximation for empirical loss probability
        z_score = (0.0 - point_profit) / std_prof_residual
        loss_prob = float(norm.cdf(z_score))
    else:
        loss_prob = 0.0 if point_profit >= 0 else 1.0
        
    loss_prob = float(np.clip(loss_prob, 0.0, 1.0))
    
    # Expected Downside Loss
    if loss_prob > 0.001:
        # Expected value of loss conditional on profit < 0
        expected_downside = float(abs(min(0.0, profit_interval["lower_bound"])))
    else:
        expected_downside = 0.0
        
    return {
        "confidence_level": confidence,
        "demand": demand_interval,
        "revenue": revenue_interval,
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
