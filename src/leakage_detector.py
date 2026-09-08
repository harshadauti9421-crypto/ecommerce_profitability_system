import os
import json
import pandas as pd
from utils.helpers import logger

RESULTS_DIR = "research_results"

def detect_data_leakage(df, target_col="Profit"):
    """
    Scans dataset columns to distinguish Pre-Launch Input Features from Post-Launch Realized Outcomes.
    Flags target variables and post-purchase outcome variables (e.g. Sales, Quantity, Profit, Order Outcome).
    Generates leakage_report.json and leakage_report.csv.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    report_rows = []
    
    post_launch_outcomes = [
        "profit", "sales", "quantity", "post_launch_sales", 
        "actual_reviews", "future_profit", "actual_revenue", "ship_date", "row_id"
    ]
    
    for col in df.columns:
        col_lower = str(col).lower().replace(" ", "_").replace("-", "_")
        
        if col == target_col or col_lower == str(target_col).lower():
            status = "TARGET"
            reason = f"Primary prediction target column ('{col}')."
            decision = "REMOVE FROM INPUT FEATURES"
        elif col_lower in post_launch_outcomes or any(p in col_lower for p in ["sales", "profit", "ship_date"]):
            status = "POST-LAUNCH OUTCOME / POTENTIAL LEAKAGE"
            reason = f"Post-purchase realized transactional outcome column ('{col}'). Cannot be known prior to product launch."
            decision = "EXCLUDE FROM PRE-LAUNCH INPUT FEATURE MATRIX"
        else:
            status = "PRE-LAUNCH FEATURE"
            reason = f"Pre-launch available attribute or commercial input ('{col}')."
            decision = "INCLUDE IN PREDICTIVE FEATURE MATRIX"
            
        report_rows.append({
            "Column": col,
            "Status": status,
            "Reason": reason,
            "Decision": decision
        })
        
    df_report = pd.DataFrame(report_rows)
    csv_path = os.path.join(RESULTS_DIR, "leakage_report.csv")
    df_report.to_csv(csv_path, index=False)
    
    json_path = os.path.join(RESULTS_DIR, "leakage_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_rows, f, indent=2)
        
    logger.info(f"Target leakage analysis completed. Reports saved to {csv_path} and {json_path}")
    return df_report, report_rows
