def determine_launch_decision(business_score, risk_level, predicted_profit, profit_margin):
    """
    Determine business launch recommendation based on calculated metrics.
    Outputs:
    - 🟢 LAUNCH
    - 🟡 LAUNCH WITH MODIFICATIONS
    - 🔴 DO NOT LAUNCH
    With detailed rationale string.
    """
    score = business_score["score"]
    
    if predicted_profit <= 0 or profit_margin <= 0 or score < 50 or risk_level == "High Risk":
        decision = "🔴 DO NOT LAUNCH"
        badge_color = "red"
        if predicted_profit <= 0:
            rationale = "The product is projected to run at an absolute financial loss. Commercial viability is unachievable under current cost structures."
        elif risk_level == "High Risk":
            rationale = "Excessive operational or commercial risk factors expose the business to severe loss potential despite nominal positive profit."
        else:
            rationale = "The overall Business Score is insufficient (< 50/100), indicating poor return potential relative to operational effort."
            
    elif score >= 75 and risk_level == "Low Risk" and profit_margin >= 20.0:
        decision = "🟢 LAUNCH"
        badge_color = "green"
        rationale = "Strong product fundamentals with high business score, robust profit margin, and low risk profile. Recommended for immediate product launch or aggressive promotion."
        
    else:
        decision = "🟡 LAUNCH WITH MODIFICATIONS"
        badge_color = "orange"
        reasons = []
        if profit_margin < 20.0:
            reasons.append(f"profit margin ({profit_margin:.1f}%) is sub-optimal")
        if risk_level != "Low Risk":
            reasons.append(f"risk level is '{risk_level}'")
        if score < 75:
            reasons.append(f"business score ({score}/100) requires tuning")
            
        reason_str = ", ".join(reasons)
        rationale = f"Product has baseline commercial potential, but key parameters should be optimized prior to full rollout because {reason_str}."

    return {
        "decision": decision,
        "badge_color": badge_color,
        "rationale": rationale
    }
