def generate_business_recommendations(
    selling_price,
    cost_price,
    discount_percent,
    advertising_cost,
    shipping_cost,
    return_rate,
    product_rating,
    predicted_profit=0.0,
    profit_margin=0.0,
    *args, **kwargs
):
    """
    Generate dynamic, contextual, actionable business recommendations based on product profit & unit economics parameters.
    No demand prediction dependence.
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
            f"🏷️ **Discount Optimization**: Discount of {discount_percent:.1f}% is high. Reducing discount by 5-10% can significantly improve overall profit margin without compromising unit margin."
        )

    # 3. Shipping Expense Management
    if selling_price > 0 and (shipping_cost / selling_price) > 0.15:
        recommendations.append(
            f"🚚 **Shipping Logistics Optimization**: Shipping cost accounts for {(shipping_cost/selling_price)*100:.1f}% of retail price. Explore multi-warehouse fulfillment or bulk shipping contracts."
        )

    # 4. Profitability & Margin Optimization
    if profit_margin < 15.0 and profit_margin > 0:
        recommendations.append(
            f"📈 **Profit Margin Expansion**: Profit margin ({profit_margin:.1f}%) is sub-optimal. Adjust pricing or streamline fulfillment expenses to reach a minimum 20% target margin."
        )
    elif predicted_profit <= 0:
        recommendations.append(
            "🔴 **Profit Deficit Alert**: The product is projected to operate at a net financial loss. Re-evaluate unit cost price, retail price, and discount structure prior to commercial commitment."
        )

    # 5. Reverse Logistics & Return Management
    if return_rate > 10.0:
        recommendations.append(
            f"📦 **Return Mitigation**: Expected return rate is high ({return_rate:.1f}%). Enhance product description, add detailed size guides/high-res media, and conduct quality assurance checks to curb return claims."
        )

    # 6. Customer Satisfaction & Rating
    if product_rating < 3.8:
        recommendations.append(
            f"⭐ **Quality Improvement**: Average rating ({product_rating}★) is below benchmark. Address negative customer feedback in packaging, durability, or delivery speed to protect long-term brand equity."
        )
        
    # Default fallback recommendation if none triggered
    if not recommendations:
        recommendations.append(
            "✅ **Maintain Strategy**: Current parameters are balanced. Maintain ongoing monitoring of competitor pricing and profitability post-launch."
        )
        
    return recommendations

def generate_business_conclusion(
    product_name,
    predicted_profit,
    profit_margin,
    risk_level,
    business_score,
    launch_decision,
    top_recommendation,
    *args, **kwargs
):
    """
    Generate dynamic natural language executive summary paragraph for PROFIT PREDICTION.
    """
    decision_text = launch_decision["decision"].replace("🟢 ", "").replace("🟡 ", "").replace("🔴 ", "")
    prof_fmt = f"₹{predicted_profit:,.2f}" if predicted_profit >= 0 else f"-₹{abs(predicted_profit):,.2f}"
    
    conclusion = (
        f"The product **'{product_name}'** has received a Business Score of **{business_score['score']}/100** ({business_score['label']}) "
        f"with a **{risk_level}** risk profile. Model projections estimate an expected net profit of **{prof_fmt}** "
        f"(Profit Margin: **{profit_margin:.1f}%**). "
        f"Based on financial and risk modeling, the executive launch decision is **{decision_text}**. "
        f"The primary recommended action is: {top_recommendation}"
    )
    return conclusion

