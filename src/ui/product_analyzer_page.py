"""
Page 3: Product Launch Analyzer Module
Simple Business-Facing Product Profitability & Launch Analysis Screen.
Uses existing trained ML models and production prediction pipeline (run_product_analysis).
"""

import os
import streamlit as st
import pandas as pd
from src.prediction import run_product_analysis
from src.optimization import run_joint_optimization
from src.ui.theme import COLORS
from src.ui.components import render_hero_launch_card, render_business_score_gauge, render_recommendation_cards
from src.ui.charts import build_conformal_interval_chart
from utils.helpers import save_prediction_to_history

HISTORY_PATH = os.path.join("data", "prediction_history.json")

def render_product_launch_analyzer_page():
    """
    Renders Page 3: Product Launch Analyzer.
    Allows business users to input product details and evaluate launch potential
    using the existing trained ML model pipeline and prescriptive optimizer.
    """
    st.markdown(f'''
    <div style="text-align:center; padding: 24px 20px 18px 20px; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; margin-bottom:24px; box-shadow: 0 4px 20px rgba(0,0,0,0.03);">
        <span style="font-size:12px; font-weight:700; color:#2563EB; text-transform:uppercase; letter-spacing:0.1em; background:#EFF6FF; padding:4px 14px; border-radius:9999px; border:1px solid rgba(37,99,235,0.3);">BUSINESS LAUNCH EVALUATOR</span>
        <h1 style="font-size:28px; font-weight:800; color:#0F172A; margin:10px 0 6px 0; letter-spacing:-0.02em;">
            🚀 PRODUCT LAUNCH ANALYZER
        </h1>
        <p style="font-size:14px; color:#475569; max-width:750px; margin:0 auto; line-height:1.5;">
            Enter your product commercial details to evaluate business potential, demand, revenue, profit margin, risk rating, and launch recommendation using our trained AI models.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    # 1. USER INPUT FORM
    with st.form("product_launch_analyzer_form", clear_on_submit=False):
        st.markdown("<div class='section-header-title'>📦 PRODUCT COMMERCIAL INFORMATION</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            prod_name = st.text_input("Product Name", value="Smart LED Study Lamp", placeholder="e.g. Smart LED Study Lamp")
            quantity = st.number_input("Target Quantity / Order Volume (Units)", min_value=1, value=500, step=10)
            
        with c2:
            selling_price = st.number_input("Selling Price ($ / ₹)", min_value=0.01, value=149.0, step=5.0)
            cost_price = st.number_input("Cost Price / COGS ($ / ₹)", min_value=0.01, value=85.0, step=5.0)
            discount_pct = st.slider("Discount (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)

        with c3:
            adv_cost = st.number_input("Advertising Budget ($ / ₹)", min_value=0.0, value=200.0, step=50.0)
            ship_cost = st.number_input("Shipping Cost ($ / ₹)", min_value=0.0, value=15.0, step=2.0)

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        btn_submit = st.form_submit_button("ANALYZE PRODUCT →", type="primary", use_container_width=True)

    # Soft warning if Cost Price > Selling Price
    if cost_price > selling_price:
        st.warning(f"⚠️ **Cost Price Alert**: Cost Price (${cost_price:,.2f}) exceeds Selling Price (${selling_price:,.2f}), which creates an immediate unit-level loss.")

    # 2. FORM VALIDATION & PREDICTION EXECUTION
    if btn_submit:
        # Input Validation Rules
        if not prod_name or not prod_name.strip():
            st.error("🚨 **Validation Error**: Product Name cannot be empty. Please provide a valid product name.")
            return

        if quantity <= 0:
            st.error("🚨 **Validation Error**: Quantity must be greater than 0.")
            return

        if selling_price <= 0:
            st.error("🚨 **Validation Error**: Selling Price must be greater than 0.")
            return

        if cost_price <= 0:
            st.error("🚨 **Validation Error**: Cost Price must be greater than 0.")
            return

        if not (0.0 <= discount_pct <= 100.0):
            st.error("🚨 **Validation Error**: Discount % must be between 0 and 100.")
            return

        if adv_cost < 0:
            st.error("🚨 **Validation Error**: Advertising Cost cannot be negative.")
            return

        if ship_cost < 0:
            st.error("🚨 **Validation Error**: Shipping Cost cannot be negative.")
            return

        # Prepare exact input payload expected by existing run_product_analysis pipeline
        input_payload = {
            "product_name": prod_name.strip(),
            "selling_price": float(selling_price),
            "cost_price": float(cost_price),
            "discount_percent": float(discount_pct),
            "shipping_cost": float(ship_cost),
            "advertising_cost": float(adv_cost),
            "quantity": int(quantity)
        }

        with st.spinner("Analyzing product using trained ML models... Calculating risk & launch decision..."):
            # Execute EXISTING production prediction pipeline
            res = run_product_analysis(input_payload)

            # Adjust predicted profit if explicit advertising budget was provided
            if adv_cost > 0:
                raw_profit = res["predicted_profit"]
                adj_profit = raw_profit - adv_cost
                res["predicted_profit"] = adj_profit
                
                # Recalculate profit margin safely
                rev = res["predicted_revenue"]
                if rev > 0:
                    res["profit_margin"] = round((adj_profit / rev) * 100.0, 2)
                else:
                    res["profit_margin"] = 0.0

            st.session_state["analyzer_result"] = res
            st.session_state["analyzer_input"] = input_payload
            
            # Save completed prediction to history
            save_prediction_to_history(res, HISTORY_PATH)

    # 3. PREDICTION OUTPUT DISPLAY
    if "analyzer_result" in st.session_state and st.session_state["analyzer_result"] is not None:
        res = st.session_state["analyzer_result"]
        inp = st.session_state["analyzer_input"]
        
        st.markdown("---")
        st.markdown(f"<div class='section-header-title'>📊 PRODUCT BUSINESS ANALYSIS &nbsp;|&nbsp; <b>{res['product_name']}</b></div>", unsafe_allow_html=True)
        
        # Metric KPI Cards
        k1, k2, k3, k4, k5 = st.columns(5)
        
        with k1:
            st.metric("Predicted Demand", f"{res['predicted_demand']:,} units")
        with k2:
            st.metric("Predicted Revenue", f"${res['predicted_revenue']:,.2f}")
        with k3:
            st.metric("Predicted Profit", f"${res['predicted_profit']:,.2f}")
        with k4:
            rev = res['predicted_revenue']
            if rev > 0:
                st.metric("Profit Margin", f"{res['profit_margin']:.1f}%")
            else:
                st.metric("Profit Margin", "N/A")
                st.caption("Profit margin unavailable because predicted revenue is zero.")
        with k5:
            risk_lvl = res["risk_analysis"]["risk_level"]
            st.metric("Risk Rating", risk_lvl)

        st.markdown("---")

        # Hero Launch Decision Card
        render_hero_launch_card(
            decision_res=res["launch_decision"],
            risk_res=res["risk_analysis"],
            profit_val=res["predicted_profit"],
            score_val=res["business_score"]["score"]
        )

        st.markdown("---")

        # Business Score & Conformal Uncertainty Range
        b_col1, b_col2 = st.columns(2)
        
        with b_col1:
            fig_gauge, breakdown = render_business_score_gauge(res["business_score"])
            st.plotly_chart(fig_gauge, use_container_width=True)

        with b_col2:
            unc = res.get("uncertainty", {})
            prof_unc = unc.get("profit", {})
            st.markdown("### 🎲 90% Conformal Prediction Range")
            fig_unc = build_conformal_interval_chart(
                point_val=res['predicted_profit'],
                lower_val=prof_unc.get('lower_bound', 0.0),
                upper_val=prof_unc.get('upper_bound', 0.0),
                title="90% Prediction Interval ($)"
            )
            st.plotly_chart(fig_unc, use_container_width=True)
            st.caption(f"Expected Profit: **${res['predicted_profit']:,.2f}** &nbsp;|&nbsp; 90% Interval: **${prof_unc.get('lower_bound', 0.0):,.2f}** to **${prof_unc.get('upper_bound', 0.0):,.2f}**")

        st.markdown("---")

        # Actionable Recommendations & Business Conclusion
        render_recommendation_cards(res["recommendations"])

        st.markdown("<div class='section-header-title'>📝 BUSINESS CONCLUSION</div>", unsafe_allow_html=True)
        st.info(res["conclusion"])

        # ======================================================================
        # NEW SECTION: RECOMMENDED PRODUCT STRATEGY
        # ======================================================================
        st.markdown("---")
        st.markdown("<div class='section-header-title'>🎯 RECOMMENDED PRODUCT STRATEGY</div>", unsafe_allow_html=True)

        with st.spinner("Executing prescriptive optimization for your product..."):
            opt_data = run_joint_optimization(inp, run_product_analysis, objective="Maximize Profit")

        if opt_data and "comparison" in opt_data:
            comp = opt_data["comparison"]
            cur_s = comp["current"]
            opt_s = comp["optimized"]
            imp = comp["improvement"]
            
            user_prod_name = inp.get("product_name", "Smart Product")
            user_cp = float(inp.get("cost_price", 40.0))
            user_adv = float(inp.get("advertising_cost", 0.0))
            user_ship = float(inp.get("shipping_cost", 10.0))

            # 1. Recommended Product Strategy Card
            st.markdown(f'''
            <div class="premium-card" style="border-left:5px solid #2563EB; background:linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%);">
                <div class="card-label" style="color:#2563EB;">RECOMMENDED STRATEGY FOR: <b style="color:#0F172A;">{user_prod_name}</b></div>
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:16px; margin-top:12px;">
                    <div>
                        <span style="font-size:11px; color:#475569;">PRODUCT NAME</span><br>
                        <b style="font-size:15px; color:#0F172A;">{user_prod_name}</b>
                    </div>
                    <div>
                        <span style="font-size:11px; color:#475569;">RECOMMENDED QUANTITY</span><br>
                        <b style="font-size:15px; color:#2563EB;">{opt_s['predicted_demand']:,} units</b>
                    </div>
                    <div>
                        <span style="font-size:11px; color:#475569;">RECOMMENDED SELLING PRICE</span><br>
                        <b style="font-size:15px; color:#047857;">${opt_s['price']:,.2f}</b>
                    </div>
                    <div>
                        <span style="font-size:11px; color:#475569;">RECOMMENDED COST PRICE</span><br>
                        <b style="font-size:15px; color:#0F172A;">${user_cp:,.2f}</b>
                    </div>
                    <div>
                        <span style="font-size:11px; color:#475569;">RECOMMENDED DISCOUNT</span><br>
                        <b style="font-size:15px; color:#2563EB;">{opt_s['discount']:.1f}%</b>
                    </div>
                    <div>
                        <span style="font-size:11px; color:#475569;">RECOMMENDED ADVERTISING COST</span><br>
                        <b style="font-size:15px; color:#0F172A;">${user_adv:,.2f}</b>
                    </div>
                    <div>
                        <span style="font-size:11px; color:#475569;">RECOMMENDED SHIPPING COST</span><br>
                        <b style="font-size:15px; color:#0F172A;">${user_ship:,.2f}</b>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            # 2. WHY THIS STRATEGY IS RECOMMENDED
            st.markdown("<h4 style='font-size:15px; font-weight:700; color:#0F172A; margin:16px 0 10px 0;'>💡 WHY THIS STRATEGY IS RECOMMENDED</h4>", unsafe_allow_html=True)
            
            reasons = []
            if imp["profit_change"] > 0:
                reasons.append(f"Expected Net Profit increases by <b>+${imp['profit_change']:,.2f}</b> (+{imp['profit_change_pct']:.1f}% lift).")
            if imp["margin_change"] > 0:
                reasons.append(f"Profit Margin expands by <b>+{imp['margin_change']:.1f}%</b> under the recommended price and discount point.")
            if imp["revenue_change"] > 0:
                reasons.append(f"Expected Revenue increases by <b>+${imp['revenue_change']:,.2f}</b> due to higher customer demand volume.")
            if imp["business_score_change"] > 0:
                reasons.append(f"Overall Business Score improves by <b>+{imp['business_score_change']} pts</b> (from {cur_s['business_score']} to {opt_s['business_score']} / 100).")
            if opt_s["risk_level"] != cur_s["risk_level"]:
                reasons.append(f"Commercial Risk Rating shifts from <b>{cur_s['risk_level']}</b> to <b>{opt_s['risk_level']}</b>.")

            if not reasons:
                reasons.append("The current strategy is already near-optimal for your commercial configuration.")

            reason_html = "".join([f"<li style='margin-bottom:6px; color:#0F172A;'>• {r}</li>" for r in reasons])
            st.markdown(f'''
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:16px 20px; box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                <ul style="margin:0; padding-left:16px; font-size:14px; line-height:1.6; list-style-type:none;">
                    {reason_html}
                </ul>
            </div>
            ''', unsafe_allow_html=True)

            # 3. CURRENT VS RECOMMENDED STRATEGY COMPARISON
            st.markdown("<h4 style='font-size:15px; font-weight:700; color:#0F172A; margin:20px 0 10px 0;'>⚖️ CURRENT VS RECOMMENDED STRATEGY COMPARISON</h4>", unsafe_allow_html=True)
            
            c_m1, c_m2, c_m3, c_m4 = st.columns(4)
            with c_m1:
                st.metric("Expected Profit Lift", f"${opt_s['expected_profit']:,.2f}", delta=f"${imp['profit_change']:,.2f}")
            with c_m2:
                st.metric("Profit Lift %", f"+{imp['profit_change_pct']:.1f}%", delta=f"{imp['profit_change_pct']:.1f}%")
            with c_m3:
                st.metric("Margin Change", f"{opt_s['profit_margin']:.1f}%", delta=f"{imp['margin_change']:.1f}%")
            with c_m4:
                st.metric("Business Score Delta", f"{opt_s['business_score']} / 100", delta=f"{imp['business_score_change']:+d} pts")

            # Side-by-side comparison table
            comp_table_data = [
                {
                    "Metric / Input": "Selling Price",
                    "Current Strategy": f"${cur_s['price']:,.2f}",
                    "Recommended Strategy": f"${opt_s['price']:,.2f}",
                    "Delta / Impact": f"${opt_s['price'] - cur_s['price']:,.2f}"
                },
                {
                    "Metric / Input": "Cost Price",
                    "Current Strategy": f"${user_cp:,.2f}",
                    "Recommended Strategy": f"${user_cp:,.2f}",
                    "Delta / Impact": "$0.00 (Fixed Input)"
                },
                {
                    "Metric / Input": "Discount %",
                    "Current Strategy": f"{cur_s['discount']:.1f}%",
                    "Recommended Strategy": f"{opt_s['discount']:.1f}%",
                    "Delta / Impact": f"{opt_s['discount'] - cur_s['discount']:.1f}%"
                },
                {
                    "Metric / Input": "Advertising Budget",
                    "Current Strategy": f"${user_adv:,.2f}",
                    "Recommended Strategy": f"${user_adv:,.2f}",
                    "Delta / Impact": "$0.00 (Fixed Budget)"
                },
                {
                    "Metric / Input": "Shipping Cost",
                    "Current Strategy": f"${user_ship:,.2f}",
                    "Recommended Strategy": f"${user_ship:,.2f}",
                    "Delta / Impact": "$0.00 (Fixed Input)"
                },
                {
                    "Metric / Input": "Predicted Demand",
                    "Current Strategy": f"{cur_s['predicted_demand']:,} units",
                    "Recommended Strategy": f"{opt_s['predicted_demand']:,} units",
                    "Delta / Impact": f"{opt_s['predicted_demand'] - cur_s['predicted_demand']:+,} units"
                },
                {
                    "Metric / Input": "Expected Revenue",
                    "Current Strategy": f"${cur_s['expected_revenue']:,.2f}",
                    "Recommended Strategy": f"${opt_s['expected_revenue']:,.2f}",
                    "Delta / Impact": f"${imp['revenue_change']:,.2f}"
                },
                {
                    "Metric / Input": "Expected Profit",
                    "Current Strategy": f"${cur_s['expected_profit']:,.2f}",
                    "Recommended Strategy": f"${opt_s['expected_profit']:,.2f}",
                    "Delta / Impact": f"${imp['profit_change']:,.2f}"
                },
                {
                    "Metric / Input": "Profit Margin",
                    "Current Strategy": f"{cur_s['profit_margin']:.1f}%",
                    "Recommended Strategy": f"{opt_s['profit_margin']:.1f}%",
                    "Delta / Impact": f"{imp['margin_change']:+.1f}%"
                },
                {
                    "Metric / Input": "Risk Rating",
                    "Current Strategy": cur_s['risk_level'],
                    "Recommended Strategy": opt_s['risk_level'],
                    "Delta / Impact": "Low Risk Retained" if cur_s['risk_level'] == opt_s['risk_level'] else f"{cur_s['risk_level']} → {opt_s['risk_level']}"
                },
                {
                    "Metric / Input": "Business Score",
                    "Current Strategy": f"{cur_s['business_score']} / 100",
                    "Recommended Strategy": f"{opt_s['business_score']} / 100",
                    "Delta / Impact": f"{imp['business_score_change']:+d} pts"
                }
            ]
            df_comp_table = pd.DataFrame(comp_table_data)
            st.dataframe(df_comp_table, hide_index=True, use_container_width=True)
