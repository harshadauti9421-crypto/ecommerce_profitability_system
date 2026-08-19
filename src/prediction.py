import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd
import numpy as np

from src.feature_engineering import add_engineered_features, ALL_INPUT_FEATURES
from src.preprocessing import load_pipeline
from src.risk_engine import analyze_product_risk
from src.business_score import calculate_business_score
from src.launch_decision import determine_launch_decision
from src.recommendation_engine import generate_business_recommendations, generate_business_conclusion
from utils.helpers import logger

MODELS_DIR = "models"

def run_product_analysis(input_data):
    """
    End-to-end product profitability analysis pipeline:
    1. Preprocess user input
    2. Load trained models and preprocessing pipeline
    3. Predict demand & profit
    4. Calculate revenue & profit margin
    5. Evaluate risk, business score, launch decision, recommendations
    6. Generate automated executive conclusion
    """
    logger.info(f"Starting product analysis for: {input_data.get('product_name', 'Unknown')}")
    
    # 1. Convert dict/DataFrame to pandas DataFrame
    if isinstance(input_data, dict):
        df_input = pd.DataFrame([input_data])
    else:
        df_input = input_data.copy()
        
    # Standardize data types
    numeric_cols = [
        "selling_price", "cost_price", "discount_percent", 
        "advertising_cost", "shipping_cost", "return_rate", "product_rating"
    ]
    for col in numeric_cols:
        if col in df_input.columns:
            df_input[col] = pd.to_numeric(df_input[col], errors="coerce").fillna(0.0)
            
    # Add engineered features
    df_engineered = add_engineered_features(df_input)
    X_input = df_engineered[ALL_INPUT_FEATURES].copy()
    
    # Load pipeline and models
    pipeline_path = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
    demand_model_path = os.path.join(MODELS_DIR, "best_demand_model.pkl")
    profit_model_path = os.path.join(MODELS_DIR, "best_profit_model.pkl")
    
    if not os.path.exists(pipeline_path) or not os.path.exists(demand_model_path) or not os.path.exists(profit_model_path):
        raise FileNotFoundError("Trained models or preprocessor pipeline missing in 'models/'. Please run training step first.")
        
    pipeline = load_pipeline(pipeline_path)
    demand_model = joblib.load(demand_model_path)
    profit_model = joblib.load(profit_model_path)
    
    # Transform input
    X_transformed = pipeline.transform(X_input)
    
    # Make Predictions
    predicted_demand_raw = demand_model.predict(X_transformed)[0]
    predicted_demand = max(int(round(predicted_demand_raw)), 1)
    
    predicted_profit_raw = profit_model.predict(X_transformed)[0]
    predicted_profit = float(predicted_profit_raw)
    
    # Financial Calculations
    selling_price = float(df_input["selling_price"].iloc[0])
    cost_price = float(df_input["cost_price"].iloc[0])
    discount_percent = float(df_input["discount_percent"].iloc[0])
    advertising_cost = float(df_input["advertising_cost"].iloc[0])
    shipping_cost = float(df_input["shipping_cost"].iloc[0])
    return_rate = float(df_input["return_rate"].iloc[0])
    product_rating = float(df_input["product_rating"].iloc[0])
    competition_level = str(df_input["competition_level"].iloc[0])
    product_name = str(df_input.get("product_name", pd.Series(["Product"])).iloc[0])
    
    net_price = selling_price * (1.0 - discount_percent / 100.0)
    predicted_revenue = round(net_price * predicted_demand, 2)
    
    # Profit Margin calculation with zero division safety
    if predicted_revenue > 0:
        profit_margin = round((predicted_profit / predicted_revenue) * 100.0, 2)
    else:
        profit_margin = 0.0
        
    # Risk Analysis
    risk_res = analyze_product_risk(
        predicted_demand=predicted_demand,
        predicted_revenue=predicted_revenue,
        predicted_profit=predicted_profit,
        profit_margin=profit_margin,
        selling_price=selling_price,
        cost_price=cost_price,
        advertising_cost=advertising_cost,
        shipping_cost=shipping_cost,
        discount_percent=discount_percent,
        return_rate=return_rate,
        competition_level=competition_level
    )
    
    # Business Score
    score_res = calculate_business_score(
        predicted_demand=predicted_demand,
        predicted_revenue=predicted_revenue,
        predicted_profit=predicted_profit,
        profit_margin=profit_margin,
        advertising_cost=advertising_cost,
        return_rate=return_rate,
        competition_level=competition_level
    )
    
    # Launch Decision
    decision_res = determine_launch_decision(
        business_score=score_res,
        risk_level=risk_res["risk_level"],
        predicted_profit=predicted_profit,
        profit_margin=profit_margin
    )
    
    # Recommendations
    recommendations = generate_business_recommendations(
        selling_price=selling_price,
        cost_price=cost_price,
        discount_percent=discount_percent,
        advertising_cost=advertising_cost,
        shipping_cost=shipping_cost,
        return_rate=return_rate,
        product_rating=product_rating,
        predicted_demand=predicted_demand,
        predicted_revenue=predicted_revenue,
        predicted_profit=predicted_profit,
        profit_margin=profit_margin
    )
    
    top_rec = recommendations[0] if recommendations else "Maintain current strategy."
    
    # Conclusion
    conclusion = generate_business_conclusion(
        product_name=product_name,
        predicted_demand=predicted_demand,
        predicted_revenue=predicted_revenue,
        predicted_profit=predicted_profit,
        profit_margin=profit_margin,
        risk_level=risk_res["risk_level"],
        business_score=score_res,
        launch_decision=decision_res,
        top_recommendation=top_rec
    )
    
    return {
        "product_name": product_name,
        "predicted_demand": predicted_demand,
        "predicted_revenue": predicted_revenue,
        "predicted_profit": predicted_profit,
        "profit_margin": profit_margin,
        "risk_analysis": risk_res,
        "business_score": score_res,
        "launch_decision": decision_res,
        "recommendations": recommendations,
        "conclusion": conclusion,
        "X_input": X_input,
        "X_transformed": X_transformed
    }

def simulate_price_sensitivity(input_data, min_mult=0.6, max_mult=1.6, steps=15):
    """
    Simulate demand, revenue, and profit across a range of selling prices to generate an interactive Price Elasticity Curve.
    Finds the profit-maximizing optimal selling price.
    """
    base_sp = float(input_data["selling_price"])
    prices = np.linspace(base_sp * min_mult, base_sp * max_mult, steps)
    
    pipeline_path = os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl")
    demand_model_path = os.path.join(MODELS_DIR, "best_demand_model.pkl")
    profit_model_path = os.path.join(MODELS_DIR, "best_profit_model.pkl")
    
    pipeline = load_pipeline(pipeline_path)
    demand_model = joblib.load(demand_model_path)
    profit_model = joblib.load(profit_model_path)
    
    records = []
    
    for sp in prices:
        sim_dict = dict(input_data)
        sim_dict["selling_price"] = round(sp, 2)
        
        df_sim = pd.DataFrame([sim_dict])
        for col in ["cost_price", "discount_percent", "advertising_cost", "shipping_cost", "return_rate", "product_rating"]:
            if col in df_sim.columns:
                df_sim[col] = pd.to_numeric(df_sim[col], errors="coerce").fillna(0.0)
                
        df_engineered = add_engineered_features(df_sim)
        X_input = df_engineered[ALL_INPUT_FEATURES].copy()
        X_transformed = pipeline.transform(X_input)
        
        d_pred = max(int(round(demand_model.predict(X_transformed)[0])), 1)
        p_pred = float(profit_model.predict(X_transformed)[0])
        
        disc = float(sim_dict["discount_percent"])
        net_p = sp * (1.0 - disc / 100.0)
        rev = round(net_p * d_pred, 2)
        margin = round((p_pred / rev) * 100.0, 2) if rev > 0 else 0.0
        
        records.append({
            "Selling Price (₹)": round(sp, 2),
            "Predicted Demand (Units)": d_pred,
            "Predicted Revenue (₹)": rev,
            "Predicted Profit (₹)": round(p_pred, 2),
            "Profit Margin (%)": margin
        })
        
    df_res = pd.DataFrame(records)
    optimal_idx = df_res["Predicted Profit (₹)"].idxmax()
    optimal_row = df_res.iloc[optimal_idx]
    
    return df_res, optimal_row

