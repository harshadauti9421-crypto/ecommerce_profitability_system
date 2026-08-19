def generate_business_recommendations(
    selling_price,
    cost_price,
    discount_percent,
    advertising_cost,
    shipping_cost,
    return_rate,
    product_rating,
    predicted_demand,
    predicted_revenue,
    predicted_profit,
    profit_margin
):
    """
    Generate dynamic, contextual, actionable business recommendations based on product parameters.
    No irrelevant recommendations displayed.
    """
    recommendations = []
    
    # 1. Pricing & Markup Check
    markup = selling_price / max(cost_price, 0.01)
    if markup < 1.4:
        recommendations.append(
            f"💡 **Pricing Markup Tuning**: Current markup is low ({markup:.2f}x). Consider increasing selling price or negotiating lower COGS with suppliers to elevate gross margins."
        )

    # 2. Discount Optimization
    if discount_percent > 30.0:
        recommendations.append(
            f"🏷️ **Discount Optimization**: Discount of {discount_percent:.1f}% is high. Reducing discount by 5-10% can significantly improve overall profit margin without severely impacting conversion rate."
        )

    # 3. Shipping Expense Management
    if selling_price > 0 and (shipping_cost / selling_price) > 0.15:
        recommendations.append(
            f"🚚 **Shipping Logistics Optimization**: Shipping cost accounts for {(shipping_cost/selling_price)*100:.1f}% of retail price. Explore multi-warehouse fulfillment, bulk shipping contracts, or setting a minimum order threshold."
        )

    # 4. Advertising Budget ROAS
    if predicted_revenue > 0:
        ad_ratio = (advertising_cost / predicted_revenue) * 100.0
        if ad_ratio > 30.0:
            recommendations.append(
                f"📢 **Ad Spend Efficiency**: Advertising represents {ad_ratio:.1f}% of projected revenue. Reallocate ad spend towards high-intent channels (e.g., Search Ads, Influencers) to lower customer acquisition cost (CAC)."
            )

    # 5. Reverse Logistics & Return Management
    if return_rate > 10.0:
        recommendations.append(
            f"📦 **Return Mitigation**: Expected return rate is high ({return_rate:.1f}%). Enhance product description, add detailed size guides/high-res media, and conduct quality assurance checks to curb return claims."
        )

    # 6. Inventory Planning
    if predicted_demand >= 1000:
        recommendations.append(
            f"🏭 **Inventory Preparedness**: High demand projection ({predicted_demand:,} units). Secure adequate safety inventory with suppliers to prevent stockouts during peak promotional windows."
        )
    elif predicted_demand < 200:
        recommendations.append(
            "🎯 **Niche Marketing & Demand Generation**: Demand projection is conservative. Run targeted pilot campaigns or offer bundled promotions to test initial market traction before committing to large production runs."
        )

    # 7. Customer Satisfaction & Rating
    if product_rating < 3.8:
        recommendations.append(
            f"⭐ **Quality Improvement**: Average rating ({product_rating}★) is below benchmark. Address negative customer feedback in packaging, durability, or delivery speed to protect long-term brand equity."
        )
        
    # Default fallback recommendation if none triggered
    if not recommendations:
        recommendations.append(
            "✅ **Maintain Strategy**: Current parameters are balanced. Maintain ongoing monitoring of competitor pricing and advertising performance post-launch."
        )
        
    return recommendations

def generate_business_conclusion(
    product_name,
    predicted_demand,
    predicted_revenue,
    predicted_profit,
    profit_margin,
    risk_level,
    business_score,
    launch_decision,
    top_recommendation
):
    """
    Generate dynamic natural language executive summary paragraph.
    """
    decision_text = launch_decision["decision"].replace("🟢 ", "").replace("🟡 ", "").replace("🔴 ", "")
    rev_fmt = f"₹{predicted_revenue:,.0f}" if predicted_revenue >= 0 else f"-₹{abs(predicted_revenue):,.0f}"
    prof_fmt = f"₹{predicted_profit:,.0f}" if predicted_profit >= 0 else f"-₹{abs(predicted_profit):,.0f}"
    
    conclusion = (
        f"The product **'{product_name}'** has received a Business Score of **{business_score['score']}/100** ({business_score['label']}) "
        f"with a **{risk_level}** risk profile. Model projections estimate a customer demand of **{predicted_demand:,} units**, "
        f"generating an expected revenue of **{rev_fmt}** and net profit of **{prof_fmt}** (Profit Margin: **{profit_margin:.1f}%**). "
        f"Based on financial and risk modeling, the executive launch decision is **{decision_text}**. "
        f"The primary recommended action is: {top_recommendation}"
    )
    return conclusion
