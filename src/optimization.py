import numpy as np
import pandas as pd
from utils.helpers import logger

def run_price_optimization(base_input, run_analysis_fn, price_min=None, price_max=None, steps=15, objective="Maximize Profit", min_margin=0.0):
    """
    Evaluates candidate unit selling prices dynamically around current price.
    Calculates profit, margin, risk, score, and uncertainty for each candidate on Real Data models.
    """
    current_price = float(base_input.get("selling_price", 100.0))
    if price_min is None:
        price_min = max(1.0, current_price * 0.6)
    if price_max is None:
        price_max = current_price * 1.5
        
    candidate_prices = np.linspace(price_min, price_max, steps)
    results = []
    
    for p in candidate_prices:
        scenario_input = base_input.copy()
        scenario_input["selling_price"] = float(p)
        
        res = run_run_product_analysis_safe(run_analysis_fn, scenario_input)
        if res:
            financials = res["financials"]
            risk_info = res["risk"]
            score_info = res["business_score"]
            uncertainty = res.get("uncertainty", {})
            b_score = score_info.get("score", score_info.get("business_score", 0)) if isinstance(score_info, dict) else 0
            
            results.append({
                "selling_price": float(p),
                "expected_profit": financials["predicted_profit"],
                "profit_margin": financials["net_profit_margin"],
                "risk_score": risk_info["risk_score"],
                "risk_level": risk_info["risk_level"],
                "business_score": b_score,
                "loss_probability": uncertainty.get("loss_probability_pct", 0.0),
                "profit_lower": uncertainty.get("profit", {}).get("lower_bound", financials["predicted_profit"])
            })
            
    df_results = pd.DataFrame(results)
    if df_results.empty:
        return {"df_curves": pd.DataFrame(), "optimal": None}
        
    valid_df = df_results[df_results["profit_margin"] >= min_margin]
    if valid_df.empty:
        valid_df = df_results
        
    if objective == "Maximize Profit Margin":
        optimal_idx = valid_df["profit_margin"].idxmax()
    elif objective == "Maximize Business Score":
        optimal_idx = valid_df["business_score"].idxmax()
    else:
        optimal_idx = valid_df["expected_profit"].idxmax()
        
    optimal_row = valid_df.loc[optimal_idx].to_dict()
    
    return {
        "df_curves": df_results,
        "optimal": optimal_row,
        "current_price": current_price
    }

def run_discount_optimization(base_input, run_analysis_fn, steps=11, objective="Maximize Profit", min_margin=0.0):
    """
    Evaluates promotional discount levels from 0% to 50% on Real Data models.
    """
    candidate_discounts = np.linspace(0.0, 50.0, steps)
    results = []
    
    for d in candidate_discounts:
        scenario_input = base_input.copy()
        scenario_input["discount_percent"] = float(d)
        
        res = run_run_product_analysis_safe(run_analysis_fn, scenario_input)
        if res:
            financials = res["financials"]
            risk_info = res["risk"]
            score_info = res["business_score"]
            b_score = score_info.get("score", score_info.get("business_score", 0)) if isinstance(score_info, dict) else 0
            
            results.append({
                "discount_percent": float(d),
                "expected_profit": financials["predicted_profit"],
                "profit_margin": financials["net_profit_margin"],
                "risk_score": risk_info["risk_score"],
                "business_score": b_score
            })
            
    df_results = pd.DataFrame(results)
    if df_results.empty:
        return {"df_curves": pd.DataFrame(), "optimal": None}
        
    valid_df = df_results[df_results["profit_margin"] >= min_margin]
    if valid_df.empty:
        valid_df = df_results
        
    if objective == "Maximize Profit Margin":
        optimal_idx = valid_df["profit_margin"].idxmax()
    elif objective == "Maximize Business Score":
        optimal_idx = valid_df["business_score"].idxmax()
    else:
        optimal_idx = valid_df["expected_profit"].idxmax()
        
    optimal_row = valid_df.loc[optimal_idx].to_dict()
    
    return {
        "df_curves": df_results,
        "optimal": optimal_row,
        "current_discount": float(base_input.get("discount_percent", 0.0))
    }

def run_advertising_optimization(base_input, run_analysis_fn, max_budget=100000.0, steps=15, objective="Maximize Profit", min_margin=0.0):
    """
    Advertising expenditure is UNAVAILABLE in real Global E-Commerce Sales Dataset | 2021–2024.
    Returns explicit research unavailable notification without fabricating fake values.
    """
    return {
        "df_curves": pd.DataFrame(),
        "optimal": None,
        "status": "UNAVAILABLE",
        "message": "Advertising expenditure is unavailable in the real Global E-Commerce Sales Dataset | 2021–2024. Fabricating advertising values has been disabled per research policy."
    }

def run_joint_optimization(base_input, run_analysis_fn, objective="Maximize Profit", min_margin=0.0):
    """
    Executes actionable Real-Data Optimization across Selling Price and Discount %.
    Produces Strategy Comparison: CURRENT STRATEGY vs OPTIMIZED STRATEGY vs EXPECTED IMPROVEMENT.
    """
    current_res = run_run_product_analysis_safe(run_analysis_fn, base_input)
    if not current_res:
        return None
        
    price_opt = run_price_optimization(base_input, run_analysis_fn, objective=objective, min_margin=min_margin)
    disc_opt = run_discount_optimization(base_input, run_analysis_fn, objective=objective, min_margin=min_margin)
    ad_opt = run_advertising_optimization(base_input, run_analysis_fn, objective=objective, min_margin=min_margin)
    
    best_price = price_opt["optimal"]["selling_price"] if price_opt.get("optimal") else float(base_input.get("selling_price", 100.0))
    best_disc = disc_opt["optimal"]["discount_percent"] if disc_opt.get("optimal") else float(base_input.get("discount_percent", 0.0))
    
    joint_input = base_input.copy()
    joint_input["selling_price"] = best_price
    joint_input["discount_percent"] = best_disc
    
    opt_res = run_run_product_analysis_safe(run_analysis_fn, joint_input)
    if not opt_res:
        opt_res = current_res
        
    cur_fin = current_res["financials"]
    opt_fin = opt_res["financials"]
    
    cur_score = current_res["business_score"].get("score", current_res["business_score"].get("business_score", 0))
    opt_score = opt_res["business_score"].get("score", opt_res["business_score"].get("business_score", 0))
    
    comparison = {
        "current": {
            "price": float(base_input.get("selling_price", 100.0)),
            "discount": float(base_input.get("discount_percent", 0.0)),
            "advertising": "UNAVAILABLE",
            "expected_profit": cur_fin["predicted_profit"],
            "profit_margin": cur_fin["net_profit_margin"],
            "risk_level": current_res["risk"]["risk_level"],
            "business_score": cur_score
        },
        "optimized": {
            "price": float(best_price),
            "discount": float(best_disc),
            "advertising": "UNAVAILABLE",
            "expected_profit": opt_fin["predicted_profit"],
            "profit_margin": opt_fin["net_profit_margin"],
            "risk_level": opt_res["risk"]["risk_level"],
            "business_score": opt_score
        },
        "improvement": {
            "profit_change": opt_fin["predicted_profit"] - cur_fin["predicted_profit"],
            "profit_change_pct": ((opt_fin["predicted_profit"] - cur_fin["predicted_profit"]) / abs(cur_fin["predicted_profit"]) * 100.0) if cur_fin["predicted_profit"] != 0 else 0.0,
            "margin_change": opt_fin["net_profit_margin"] - cur_fin["net_profit_margin"],
            "business_score_change": opt_score - cur_score
        }
    }
    
    return {
        "comparison": comparison,
        "price_opt": price_opt,
        "discount_opt": disc_opt,
        "ad_opt": ad_opt,
        "joint_result": opt_res
    }

def run_run_product_analysis_safe(run_analysis_fn, input_data):
    """Safely invokes run_product_analysis."""
    try:
        return run_analysis_fn(input_data)
    except Exception as e:
        logger.warning(f"Real data optimization scenario exception: {e}")
        return None

