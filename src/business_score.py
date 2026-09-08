def calculate_business_score(*args, **kwargs):
    """
    Calculate a dynamic Business Score (0 - 100) based on weighted business pillars for PROFIT ONLY.
    Pillars (Max 100 pts):
    1. Profit Margin Score (max 35 pts)
    2. Absolute Profitability Score (max 35 pts)
    3. Unit Economics & Cost Safety (max 15 pts)
    4. Operational Return Safety (max 5 pts)
    5. Shipping & Logistics Efficiency (max 5 pts)
    6. Market Competition Advantage (max 5 pts)
    """
    # Handle signature variations gracefully
    if len(args) >= 3 and isinstance(args[0], (int, float, str)) and isinstance(args[1], (int, float)):
        # Legacy signature: (predicted_demand, predicted_revenue, predicted_profit, profit_margin, ...)
        if len(args) >= 4:
            predicted_profit = float(args[2])
            profit_margin = float(args[3])
        else:
            predicted_profit = float(args[0]) if isinstance(args[0], (int, float)) else 0.0
            profit_margin = float(args[1])
        advertising_cost = float(args[4]) if len(args) > 4 else float(kwargs.get("advertising_cost", 0.0))
        return_rate = float(args[5]) if len(args) > 5 else float(kwargs.get("return_rate", 5.0))
        competition_level = str(args[6]) if len(args) > 6 else str(kwargs.get("competition_level", "Medium"))
    else:
        predicted_profit = float(kwargs.get("predicted_profit", args[0] if len(args) > 0 and isinstance(args[0], (int, float)) else 0.0))
        profit_margin = float(kwargs.get("profit_margin", args[1] if len(args) > 1 and isinstance(args[1], (int, float)) else 0.0))
        advertising_cost = float(kwargs.get("advertising_cost", 0.0))
        return_rate = float(kwargs.get("return_rate", 5.0))
        competition_level = str(kwargs.get("competition_level", "Medium"))

    cost_price = float(kwargs.get("cost_price", 40.0))
    selling_price = float(kwargs.get("selling_price", 100.0))
    shipping_cost = float(kwargs.get("shipping_cost", 10.0))

    # 1. Profit Margin Score (0 - 35)
    if profit_margin >= 35.0:
        margin_pts = 35.0
    elif profit_margin > 0.0:
        margin_pts = (profit_margin / 35.0) * 35.0
    else:
        margin_pts = 0.0

    # 2. Absolute Profitability Score (0 - 35)
    # Benchmark: ₹5,00,000+ profit gets max 35 pts
    if predicted_profit >= 500000:
        profit_pts = 35.0
    elif predicted_profit > 0:
        profit_pts = (predicted_profit / 500000.0) * 35.0
    else:
        profit_pts = 0.0

    # 3. Unit Economics & Cost Safety Score (0 - 15)
    if selling_price > 0:
        cogs_ratio = cost_price / selling_price
        if cogs_ratio <= 0.40:
            econ_pts = 15.0
        elif cogs_ratio < 1.0:
            econ_pts = max(0.0, (1.0 - cogs_ratio) / 0.60 * 15.0)
        else:
            econ_pts = 0.0
    else:
        econ_pts = 0.0

    # 4. Operational Return Safety Score (0 - 5)
    if return_rate <= 3.0:
        return_pts = 5.0
    elif return_rate <= 20.0:
        return_pts = max(0.0, (1.0 - (return_rate - 3.0) / 17.0) * 5.0)
    else:
        return_pts = 0.0

    # 5. Shipping & Logistics Efficiency (0 - 5)
    if selling_price > 0:
        ship_ratio = shipping_cost / selling_price
        if ship_ratio <= 0.10:
            ship_pts = 5.0
        elif ship_ratio <= 0.25:
            ship_pts = max(0.0, (1.0 - (ship_ratio - 0.10) / 0.15) * 5.0)
        else:
            ship_pts = 0.0
    else:
        ship_pts = 0.0

    # 6. Competition Advantage (0 - 5)
    if competition_level == "Low":
        comp_pts = 5.0
    elif competition_level == "Medium":
        comp_pts = 3.0
    else:
        comp_pts = 1.0

    raw_score = margin_pts + profit_pts + econ_pts + return_pts + ship_pts + comp_pts
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
            "Profit Margin (Max 35)": round(margin_pts, 1),
            "Absolute Profit (Max 35)": round(profit_pts, 1),
            "Unit Economics (Max 15)": round(econ_pts, 1),
            "Return Safety (Max 5)": round(return_pts, 1),
            "Logistics Efficiency (Max 5)": round(ship_pts, 1),
            "Competition Factor (Max 5)": round(comp_pts, 1)
        }
    }

