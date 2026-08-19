def analyze_product_risk(
    predicted_demand,
    predicted_revenue,
    predicted_profit,
    profit_margin,
    selling_price,
    cost_price,
    advertising_cost,
    shipping_cost,
    discount_percent,
    return_rate,
    competition_level
):
    """
    Calculate dynamic multi-factor risk score and extract positive/negative drivers.
    Does NOT use random numbers. Fully deterministic based on business financial metrics.
    """
    positive_factors = []
    negative_factors = []
    risk_score = 0 # 0 (lowest risk) to 100 (highest risk)
    
    # 1. Profitability & Margin Risk
    if profit_margin >= 30.0:
        positive_factors.append(f"Strong profit margin ({profit_margin:.1f}%) provides a healthy buffer.")
    elif profit_margin >= 15.0:
        risk_score += 15
        positive_factors.append(f"Acceptable profit margin ({profit_margin:.1f}%).")
    elif profit_margin > 0.0:
        risk_score += 35
        negative_factors.append(f"Thin profit margin ({profit_margin:.1f}%), susceptible to cost overruns.")
    else:
        risk_score += 55
        negative_factors.append(f"Negative profitability ({profit_margin:.1f}%), product operates at a loss.")

    # 2. Demand Potential
    if predicted_demand >= 1000:
        positive_factors.append(f"Robust predicted demand ({predicted_demand:,} units).")
    elif predicted_demand >= 300:
        positive_factors.append(f"Moderate predicted demand ({predicted_demand:,} units).")
    else:
        risk_score += 25
        negative_factors.append(f"Low predicted demand ({predicted_demand:,} units), risking inventory stagnation.")

    # 3. Ad Cost vs Revenue (Advertising Intensity)
    if predicted_revenue > 0:
        ad_ratio = (advertising_cost / predicted_revenue) * 100.0
        if ad_ratio > 35.0:
            risk_score += 25
            negative_factors.append(f"High advertising expense relative to revenue ({ad_ratio:.1f}%).")
        elif ad_ratio < 15.0:
            positive_factors.append(f"Efficient advertising budget ratio ({ad_ratio:.1f}% of revenue).")
            
    # 4. Shipping Cost relative to Selling Price
    if selling_price > 0:
        ship_ratio = (shipping_cost / selling_price) * 100.0
        if ship_ratio > 20.0:
            risk_score += 20
            negative_factors.append(f"High shipping cost ratio ({ship_ratio:.1f}% of selling price).")
        elif ship_ratio <= 10.0:
            positive_factors.append(f"Favorable shipping cost ratio ({ship_ratio:.1f}% of selling price).")

    # 5. Discount Risk
    if discount_percent > 40.0:
        risk_score += 20
        negative_factors.append(f"Heavy discount rate ({discount_percent:.1f}%) erodes unit margin.")
    elif discount_percent <= 15.0:
        positive_factors.append(f"Conservative discount strategy ({discount_percent:.1f}%).")

    # 6. Return Rate Risk
    if return_rate > 15.0:
        risk_score += 25
        negative_factors.append(f"High expected return rate ({return_rate:.1f}%), increasing reverse logistics loss.")
    elif return_rate <= 5.0:
        positive_factors.append(f"Low return rate ({return_rate:.1f}%), minimizing return handling costs.")

    # 7. Competition Level
    if competition_level == "High":
        risk_score += 15
        negative_factors.append("High market competition may trigger price wars.")
    elif competition_level == "Low":
        positive_factors.append("Low competition offers market capture opportunity.")

    # Categorize final risk level
    if risk_score <= 25:
        risk_level = "Low Risk"
    elif risk_score <= 55:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"
        
    return {
        "risk_level": risk_level,
        "risk_score": min(risk_score, 100),
        "positive_factors": positive_factors,
        "negative_factors": negative_factors
    }
