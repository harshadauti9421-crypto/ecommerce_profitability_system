def calculate_business_score(
    predicted_demand,
    predicted_revenue,
    predicted_profit,
    profit_margin,
    advertising_cost,
    return_rate,
    competition_level
):
    """
    Calculate a dynamic Business Score (0 - 100) based on weighted business pillars.
    Zero random values.
    Pillars:
    1. Profit Margin Score (max 30 pts)
    2. Absolute Profitability Score (max 25 pts)
    3. Demand Volume Score (max 20 pts)
    4. Operational Return Safety Score (max 10 pts)
    5. Advertising Efficiency / ROAS (max 10 pts)
    6. Market Competition Advantage (max 5 pts)
    """
    # 1. Profit Margin Score (0 - 30)
    if profit_margin >= 35.0:
        margin_pts = 30.0
    elif profit_margin > 0.0:
        margin_pts = (profit_margin / 35.0) * 30.0
    else:
        margin_pts = 0.0

    # 2. Absolute Profitability Score (0 - 25)
    # Benchmark: ₹5,00,000+ profit gets max 25 pts
    if predicted_profit >= 500000:
        profit_pts = 25.0
    elif predicted_profit > 0:
        profit_pts = (predicted_profit / 500000.0) * 25.0
    else:
        profit_pts = 0.0

    # 3. Demand Volume Score (0 - 20)
    # Benchmark: 2,000+ units gets max 20 pts
    if predicted_demand >= 2000:
        demand_pts = 20.0
    elif predicted_demand > 0:
        demand_pts = (predicted_demand / 2000.0) * 20.0
    else:
        demand_pts = 0.0

    # 4. Operational Return Safety Score (0 - 10)
    if return_rate <= 3.0:
        return_pts = 10.0
    elif return_rate <= 20.0:
        return_pts = (1.0 - (return_rate - 3.0) / 17.0) * 10.0
    else:
        return_pts = 0.0

    # 5. Ad Efficiency / ROAS Score (0 - 10)
    if predicted_revenue > 0:
        roas = predicted_revenue / max(advertising_cost, 1.0)
        if roas >= 5.0:
            ad_pts = 10.0
        elif roas >= 1.0:
            ad_pts = (roas / 5.0) * 10.0
        else:
            ad_pts = 0.0
    else:
        ad_pts = 0.0

    # 6. Competition Advantage (0 - 5)
    if competition_level == "Low":
        comp_pts = 5.0
    elif competition_level == "Medium":
        comp_pts = 3.0
    else:
        comp_pts = 1.0

    raw_score = margin_pts + profit_pts + demand_pts + return_pts + ad_pts + comp_pts
    final_score = int(round(min(max(raw_score, 0), 100)))

    if final_score >= 80:
        label = "Excellent"
    elif final_score >= 65:
        label = "Good"
    elif final_score >= 50:
        label = "Moderate"
    else:
        label = "Poor"

    return {
        "score": final_score,
        "label": label,
        "breakdown": {
            "Profit Margin (Max 30)": round(margin_pts, 1),
            "Absolute Profit (Max 25)": round(profit_pts, 1),
            "Demand Volume (Max 20)": round(demand_pts, 1),
            "Return Safety (Max 10)": round(return_pts, 1),
            "Ad Efficiency (Max 10)": round(ad_pts, 1),
            "Competition Factor (Max 5)": round(comp_pts, 1)
        }
    }
