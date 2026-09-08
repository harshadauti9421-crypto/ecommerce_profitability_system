def analyze_product_risk(
    predicted_profit,
    profit_margin,
    selling_price,
    cost_price,
    advertising_cost,
    shipping_cost,
    discount_percent,
    return_rate,
    competition_level,
    uncertainty_dict=None
):
    """
    Calculate dynamic multi-factor risk score incorporating prediction uncertainty & downside loss probability for PROFIT ONLY.
    Does NOT use random numbers. Fully deterministic based on business financial metrics & conformal prediction intervals.
    """
    positive_factors = []
    negative_factors = []
    risk_score = 0 # 0 (lowest risk) to 100 (highest risk)
    
    # 1. Profitability & Margin Risk
    if profit_margin >= 30.0:
        positive_factors.append(f"Strong profit margin ({profit_margin:.1f}%) provides a healthy financial buffer.")
    elif profit_margin >= 15.0:
        risk_score += 15
        positive_factors.append(f"Acceptable profit margin ({profit_margin:.1f}%).")
    elif profit_margin > 0.0:
        risk_score += 35
        negative_factors.append(f"Thin profit margin ({profit_margin:.1f}%), susceptible to cost overruns.")
    else:
        risk_score += 55
        negative_factors.append(f"Negative profitability ({profit_margin:.1f}%), product operates at a net financial loss.")

    # 2. Cost Price vs Selling Price (Unit Economics Safety)
    if cost_price >= selling_price:
        risk_score += 30
        negative_factors.append(f"Cost price (₹{cost_price:,.2f}) exceeds selling price (₹{selling_price:,.2f}), causing instant loss.")
    elif selling_price > 0 and (cost_price / selling_price) <= 0.50:
        positive_factors.append(f"Favorable COGS ratio ({(cost_price/selling_price)*100:.1f}% of selling price).")

    # 3. Ad Cost & Shipping Intensity relative to Selling Price
    if selling_price > 0:
        ship_ratio = (shipping_cost / selling_price) * 100.0
        if ship_ratio > 20.0:
            risk_score += 20
            negative_factors.append(f"High shipping cost ratio ({ship_ratio:.1f}% of selling price).")
        elif ship_ratio <= 10.0:
            positive_factors.append(f"Favorable shipping cost ratio ({ship_ratio:.1f}% of selling price).")

    # 4. Discount Risk
    if discount_percent > 40.0:
        risk_score += 20
        negative_factors.append(f"Heavy discount rate ({discount_percent:.1f}%) erodes unit margin.")
    elif discount_percent <= 15.0:
        positive_factors.append(f"Conservative discount strategy ({discount_percent:.1f}%).")

    # 5. Return Rate Risk
    if return_rate > 15.0:
        risk_score += 25
        negative_factors.append(f"High expected return rate ({return_rate:.1f}%), increasing reverse logistics loss.")
    elif return_rate <= 5.0:
        positive_factors.append(f"Low return rate ({return_rate:.1f}%), minimizing return handling costs.")

    # 6. Competition Level
    if competition_level == "High":
        risk_score += 15
        negative_factors.append("High market competition may trigger price pressure.")
    elif competition_level == "Low":
        positive_factors.append("Low competition offers market capture opportunity.")

    # 7. Prediction Uncertainty & Downside Risk Incorporation
    if uncertainty_dict:
        loss_prob = uncertainty_dict.get("loss_probability", 0.0)
        loss_prob_pct = uncertainty_dict.get("loss_probability_pct", loss_prob * 100.0)
        profit_interval = uncertainty_dict.get("profit", {})
        lower_bound = profit_interval.get("lower_bound", predicted_profit)
        interval_width = profit_interval.get("interval_width", 0.0)
        
        if loss_prob > 0.30:
            risk_score += 25
            negative_factors.append(f"High risk of operating loss: P(Profit < 0) = {loss_prob_pct:.1f}%.")
        elif loss_prob > 0.10:
            risk_score += 15
            negative_factors.append(f"Moderate risk of operating loss: P(Profit < 0) = {loss_prob_pct:.1f}%.")
        else:
            positive_factors.append(f"Low downside risk: P(Profit < 0) = {loss_prob_pct:.1f}%.")
            
        if lower_bound < 0:
            risk_score += 15
            negative_factors.append(f"Lower 90% conformal bound is negative (₹{lower_bound:,.2f}).")
        else:
            positive_factors.append(f"Lower 90% conformal profit bound remains positive (₹{lower_bound:,.2f}).")
            
        if interval_width > abs(predicted_profit) * 1.5 and predicted_profit > 0:
            risk_score += 15
            negative_factors.append(f"High prediction volatility (90% CI width: ₹{interval_width:,.2f}).")

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

