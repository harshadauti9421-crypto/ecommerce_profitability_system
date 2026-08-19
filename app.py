import os
import sys

# Ensure root project directory is in sys.path for Streamlit Cloud and deployment environments
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_and_validate_data, get_product_name_col, CATEGORY_SUBCATEGORIES, SEASONS, PLATFORMS, MARKETING_CHANNELS, COMPETITION_LEVELS, REGIONS, PAYMENT_METHODS
from src.train_models import train_and_evaluate_all, MODELS_DIR, DATA_PATH
from src.prediction import run_product_analysis, simulate_price_sensitivity
from src.explainability import explain_prediction_shap
from utils.helpers import format_currency, save_prediction_to_history, load_prediction_history, logger

HISTORY_PATH = os.path.join("data", "prediction_history.json")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI E-Commerce Profitability & Business Decision System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Business Dashboard CSS Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E293B 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        text-align: center;
        transition: transform 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 0.4rem;
    }
    .badge-launch {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1.3rem;
        display: inline-block;
        border: 2px solid #86EFAC;
    }
    .badge-modify {
        background-color: #FEF9C3;
        color: #A16207;
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1.3rem;
        display: inline-block;
        border: 2px solid #FDE047;
    }
    .badge-reject {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1.3rem;
        display: inline-block;
        border: 2px solid #FCA5A5;
    }
    </style>
""", unsafe_allow_html=True)

def check_models_exist():
    """Verify whether trained model artifacts exist."""
    required = [
        os.path.join(MODELS_DIR, "preprocessing_pipeline.pkl"),
        os.path.join(MODELS_DIR, "best_demand_model.pkl"),
        os.path.join(MODELS_DIR, "best_profit_model.pkl"),
        METRICS_PATH
    ]
    return all(os.path.exists(p) for p in required)

# Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "current_input" not in st.session_state:
    st.session_state["current_input"] = None

# Sidebar Controls
st.sidebar.title("🎮 Business Controls")
st.sidebar.markdown("---")

if not check_models_exist():
    st.sidebar.warning("⚠️ Trained models missing.")
    if st.sidebar.button("⚙️ Train All 4 ML Models"):
        with st.spinner("Training models on 43,893 records..."):
            try:
                train_and_evaluate_all()
                st.sidebar.success("✅ Models trained successfully!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Training failed: {str(e)}")

# Sidebar Quick Mode Toggle
auto_run = st.sidebar.checkbox("⚡ Live Recalculation Mode", value=True, help="Automatically update predictions when inputs change")

# Main Navigation Tabs
tabs = st.tabs([
    "💼 Business Model Dashboard", 
    "📊 Financial P&L & Waterfall", 
    "📈 Price Elasticity & Sensitivity",
    "🤖 Model Performance (4 ML Models)", 
    "💡 SHAP Explainable AI", 
    "🎛️ Interactive What-If Simulator", 
    "🚀 Launch Decision"
])

# ==============================================================================
# TAB 1: BUSINESS MODEL DASHBOARD (MAIN INPUT & EXECUTIVE BANNER)
# ==============================================================================
with tabs[0]:
    st.markdown('<div class="main-header">Interactive E-Commerce Business Intelligence System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Real-time Machine Learning prediction, risk analysis, scoring, and business decision dashboard.</div>', unsafe_allow_html=True)

    # Cached dataset loading for searchable product dropdown
    @st.cache_data
    def load_cached_dataset():
        if os.path.exists(DATA_PATH):
            return load_and_validate_data(DATA_PATH)
        return None

    df_dataset = load_cached_dataset()
    prod_name_col = get_product_name_col(df_dataset) if df_dataset is not None else None

    if df_dataset is not None and not df_dataset.empty and prod_name_col:
        unique_products = sorted(df_dataset[prod_name_col].dropna().astype(str).unique().tolist())
    else:
        unique_products = []

    with st.expander("🛠️ **Product & Commercial Inputs** (Click to expand/collapse)", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if unique_products:
                selected_prod_name = st.selectbox(
                    "Product Name (🔍 Search or Select from Dataset)",
                    options=unique_products,
                    index=0,
                    key="p_select_name"
                )
                product_name = selected_prod_name
                
                # Auto-populate default values when a new product is selected from dataset
                if st.session_state.get("last_selected_product") != selected_prod_name:
                    matched = df_dataset[df_dataset[prod_name_col].astype(str) == selected_prod_name]
                    if not matched.empty:
                        row = matched.iloc[0]
                        cat_val = str(row["product_category"]) if str(row["product_category"]) in CATEGORY_SUBCATEGORIES else list(CATEGORY_SUBCATEGORIES.keys())[0]
                        subcats_val = CATEGORY_SUBCATEGORIES.get(cat_val, [])
                        subcat_val = str(row["product_subcategory"]) if str(row["product_subcategory"]) in subcats_val else (subcats_val[0] if subcats_val else "")
                        
                        st.session_state["p_cat"] = cat_val
                        st.session_state["p_subcat"] = subcat_val
                        st.session_state["p_sp"] = float(row["selling_price"])
                        st.session_state["p_cp"] = float(row["cost_price"])
                        st.session_state["p_disc"] = float(row["discount_percent"])
                        st.session_state["p_ad"] = float(row["advertising_cost"])
                        st.session_state["p_ship"] = float(row["shipping_cost"])
                        st.session_state["p_ret"] = float(row["return_rate"])
                        st.session_state["p_rating"] = float(row["product_rating"])
                        st.session_state["p_season"] = str(row["season"]) if str(row["season"]) in SEASONS else SEASONS[0]
                        st.session_state["p_channel"] = str(row["marketing_channel"]) if str(row["marketing_channel"]) in MARKETING_CHANNELS else MARKETING_CHANNELS[0]
                        st.session_state["p_comp"] = str(row["competition_level"]) if str(row["competition_level"]) in COMPETITION_LEVELS else COMPETITION_LEVELS[0]
                        st.session_state["p_plat"] = str(row["platform"]) if str(row["platform"]) in PLATFORMS else PLATFORMS[0]
                        st.session_state["p_reg"] = str(row["region"]) if str(row["region"]) in REGIONS else REGIONS[0]
                        st.session_state["p_pay"] = str(row["payment_method"]) if str(row["payment_method"]) in PAYMENT_METHODS else PAYMENT_METHODS[0]
                        st.session_state["last_selected_product"] = selected_prod_name
            else:
                st.warning("⚠️ Dataset missing or product name column not found. Using manual entry mode.")
                product_name = st.text_input("Product Name", value="Custom E-Commerce Product", key="p_name")

            # Render What-If inputs (pre-filled with selected product defaults, editable by user)
            product_category = st.selectbox("Category", options=list(CATEGORY_SUBCATEGORIES.keys()), key="p_cat")
            subcats = CATEGORY_SUBCATEGORIES.get(product_category, list(CATEGORY_SUBCATEGORIES.values())[0])
            
            # Ensure subcategory stays valid if category is changed
            current_subcat = st.session_state.get("p_subcat", subcats[0])
            subcat_idx = subcats.index(current_subcat) if current_subcat in subcats else 0
            product_subcategory = st.selectbox("Subcategory", options=subcats, index=subcat_idx, key="p_subcat")
            
            selling_price = st.number_input("Selling Price (₹)", min_value=1.0, value=st.session_state.get("p_sp", 3499.0), step=50.0, key="p_sp")
            cost_price = st.number_input("Cost Price / COGS (₹)", min_value=1.0, value=st.session_state.get("p_cp", 1400.0), step=50.0, key="p_cp")

        with col2:
            discount_percent = st.slider("Discount %", min_value=0.0, max_value=80.0, value=st.session_state.get("p_disc", 15.0), step=1.0, key="p_disc")
            advertising_cost = st.number_input("Advertising Budget (₹)", min_value=0.0, value=st.session_state.get("p_ad", 12000.0), step=500.0, key="p_ad")
            shipping_cost = st.number_input("Shipping Cost per Unit (₹)", min_value=0.0, value=st.session_state.get("p_ship", 120.0), step=10.0, key="p_ship")
            return_rate = st.slider("Expected Return Rate %", min_value=0.0, max_value=40.0, value=st.session_state.get("p_ret", 6.0), step=0.5, key="p_ret")
            product_rating = st.slider("Product Rating (Stars)", min_value=1.0, max_value=5.0, value=st.session_state.get("p_rating", 4.4), step=0.1, key="p_rating")

        with col3:
            season = st.selectbox("Launch Season / Event", options=SEASONS, key="p_season")
            marketing_channel = st.selectbox("Marketing Channel", options=MARKETING_CHANNELS, key="p_channel")
            competition_level = st.selectbox("Competition Level", options=COMPETITION_LEVELS, key="p_comp")
            platform = st.selectbox("Platform", options=PLATFORMS, key="p_plat")
            region = st.selectbox("Region", options=REGIONS, key="p_reg")
            payment_method = st.selectbox("Payment Method", options=PAYMENT_METHODS, key="p_pay")

        analyze_btn = st.button("🚀 ANALYZE PRODUCT BUSINESS MODEL", use_container_width=True, type="primary")

    # Determine input signature to detect real-time changes
    current_input_tuple = (
        product_name, product_category, product_subcategory, selling_price, cost_price,
        discount_percent, advertising_cost, shipping_cost, return_rate, product_rating,
        season, marketing_channel, competition_level, platform, region, payment_method
    )

    # Run analysis logic if button clicked OR auto_run enabled
    should_run = analyze_btn or (auto_run and (st.session_state["analysis_result"] is None or st.session_state.get("last_input_tuple") != current_input_tuple))

    if should_run:
        if not check_models_exist():
            st.error("⚠️ Models are missing. Click '⚙️ Train All 4 ML Models' in the sidebar first.")
        else:
            st.session_state["last_input_tuple"] = current_input_tuple
            input_data = {
                "product_name": product_name,
                "product_category": product_category,
                "product_subcategory": product_subcategory,
                "selling_price": selling_price,
                "cost_price": cost_price,
                "discount_percent": discount_percent,
                "advertising_cost": advertising_cost,
                "shipping_cost": shipping_cost,
                "return_rate": return_rate,
                "product_rating": product_rating,
                "season": season,
                "marketing_channel": marketing_channel,
                "competition_level": competition_level,
                "platform": platform,
                "region": region,
                "payment_method": payment_method
            }
            try:
                res = run_product_analysis(input_data)
                st.session_state["analysis_result"] = res
                st.session_state["current_input"] = input_data
                
                # Save run to local history
                save_record = {
                    "product_name": product_name,
                    "category": product_category,
                    "selling_price": selling_price,
                    "cost_price": cost_price,
                    "predicted_demand": res["predicted_demand"],
                    "predicted_revenue": res["predicted_revenue"],
                    "predicted_profit": res["predicted_profit"],
                    "profit_margin": res["profit_margin"],
                    "risk_level": res["risk_analysis"]["risk_level"],
                    "business_score": res["business_score"]["score"],
                    "launch_decision": res["launch_decision"]["decision"]
                }
                save_prediction_to_history(save_record, HISTORY_PATH)
            except Exception as e:
                st.error(f"Execution error: {str(e)}")

    # Render Dashboard Results
    if st.session_state["analysis_result"] is not None:
        res = st.session_state["analysis_result"]
        st.markdown("---")

        # 1. Executive Banner & Decision Badge
        dec = res["launch_decision"]
        score = res["business_score"]
        risk = res["risk_analysis"]
        
        banner_col1, banner_col2, banner_col3 = st.columns([2, 1, 1])
        
        with banner_col1:
            st.markdown(f"### Product: **{res['product_name']}**")
            badge_class = "badge-launch" if dec["badge_color"] == "green" else ("badge-modify" if dec["badge_color"] == "orange" else "badge-reject")
            st.markdown(f'<div class="{badge_class}">{dec["decision"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**Decision Rationale:** {dec['rationale']}")
            
        with banner_col2:
            # Interactive Business Score Gauge using Plotly
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score["score"],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Business Score", 'font': {'size': 18}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1},
                    'bar': {'color': "#1E293B"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 49], 'color': '#FEE2E2'},
                        {'range': [49, 64], 'color': '#FEF9C3'},
                        {'range': [64, 79], 'color': '#DBEAFE'},
                        {'range': [79, 100], 'color': '#DCFCE7'}
                    ],
                }
            ))
            fig_gauge.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with banner_col3:
            st.metric("Risk Profile", risk["risk_level"], delta=f"Score: {risk['risk_score']}/100", delta_color="inverse")
            st.metric("Target Category", res["product_name"] if len(res["product_name"]) < 15 else "E-Commerce", delta=product_category)

        st.markdown("---")

        # 2. Key Predictions Metric Cards
        st.subheader("💰 Machine Learning Predictions")
        k1, k2, k3, k4 = st.columns(4)
        
        with k1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Predicted Demand</div>
                    <div class="metric-value">{res['predicted_demand']:,} units</div>
                </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Predicted Revenue</div>
                    <div class="metric-value">{format_currency(res['predicted_revenue'])}</div>
                </div>
            """, unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Predicted Profit</div>
                    <div class="metric-value">{format_currency(res['predicted_profit'])}</div>
                </div>
            """, unsafe_allow_html=True)

        with k4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Profit Margin</div>
                    <div class="metric-value">{res['profit_margin']:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Dynamic Risk Factors & Score Breakdown Table
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            st.subheader("🔍 Dynamic Risk Factor Breakdown")
            if risk["positive_factors"]:
                st.markdown("**Positive Growth Drivers:**")
                for pos in risk["positive_factors"]:
                    st.markdown(f"- ✅ {pos}")
            if risk["negative_factors"]:
                st.markdown("**Negative Risk Drivers:**")
                for neg in risk["negative_factors"]:
                    st.markdown(f"- ⚠️ {neg}")

        with r_col2:
            st.subheader("🎯 Business Score Breakdown")
            breakdown = score["breakdown"]
            df_score = pd.DataFrame(list(breakdown.items()), columns=["Pillar Component", "Points Earned"])
            fig_score_bar = px.bar(
                df_score, 
                x="Points Earned", 
                y="Pillar Component", 
                orientation="h",
                text="Points Earned",
                color="Points Earned",
                color_continuous_scale="Blues"
            )
            fig_score_bar.update_layout(height=230, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
            st.plotly_chart(fig_score_bar, use_container_width=True)

        st.markdown("---")

        # 4. Business Recommendations & Executive Conclusion
        st.subheader("💡 Actionable Business Recommendations")
        for rec in res["recommendations"]:
            st.markdown(rec)

        st.markdown("---")
        st.subheader("📝 Executive Summary")
        st.info(res["conclusion"])

# ==============================================================================
# TAB 2: FINANCIAL P&L & WATERFALL CHART
# ==============================================================================
with tabs[1]:
    st.markdown('<div class="main-header">Interactive Financial P&L Statement & Waterfall</div>', unsafe_allow_html=True)
    st.markdown("Detailed breakdown of gross revenue, COGS, shipping, advertising, return losses, and net profit.")

    if st.session_state["analysis_result"] is None:
        st.info("Analyze a product in Tab 1 first to view financial P&L breakdown.")
    else:
        res = st.session_state["analysis_result"]
        inp = st.session_state["current_input"]
        
        demand = res["predicted_demand"]
        sp = float(inp["selling_price"])
        cp = float(inp["cost_price"])
        disc = float(inp["discount_percent"])
        ad = float(inp["advertising_cost"])
        ship = float(inp["shipping_cost"])
        ret = float(inp["return_rate"])
        
        gross_rev = round(sp * demand, 2)
        discount_val = round(gross_rev * (disc / 100.0), 2)
        net_rev = res["predicted_revenue"]
        
        total_cogs = round(cp * demand, 2)
        total_ship = round(ship * demand, 2)
        return_loss = round((ret / 100.0) * demand * (cp * 0.25 + ship * 0.5), 2)
        net_profit = res["predicted_profit"]
        
        # Interactive Plotly Waterfall Chart
        fig_waterfall = go.Figure(go.Waterfall(
            name="Financial P&L",
            orientation="v",
            measure=["relative", "relative", "total", "relative", "relative", "relative", "relative", "total"],
            x=["Gross Revenue", "Discounts (-)", "Net Revenue", "COGS (-)", "Shipping Costs (-)", "Ad Budget (-)", "Return Loss (-)", "Net Profit (=)"],
            textposition="outside",
            text=[f"₹{gross_rev:,.0f}", f"-₹{discount_val:,.0f}", f"₹{net_rev:,.0f}", f"-₹{total_cogs:,.0f}", f"-₹{total_ship:,.0f}", f"-₹{ad:,.0f}", f"-₹{return_loss:,.0f}", f"₹{net_profit:,.0f}"],
            y=[gross_rev, -discount_val, 0, -total_cogs, -total_ship, -ad, -return_loss, 0],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#EF4444"}},
            increasing={"marker": {"color": "#10B981"}},
            totals={"marker": {"color": "#3B82F6"}}
        ))
        
        fig_waterfall.update_layout(
            title="Interactive Revenue-to-Profit Waterfall Breakdown (₹)",
            showlegend=False,
            height=450
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Dynamic Profit & Loss (P&L) Statement Table")
        
        pnl_data = [
            {"Line Item": "Gross Revenue", "Per Unit (₹)": f"₹{sp:,.2f}", "Total Batch (₹)": format_currency(gross_rev), "% of Net Revenue": f"{(gross_rev/net_rev)*100:.1f}%" if net_rev>0 else "0%"},
            {"Line Item": "Discounts Given (-)", "Per Unit (₹)": f"₹{sp*(disc/100):,.2f}", "Total Batch (₹)": format_currency(-discount_val), "% of Net Revenue": f"-{disc:.1f}%"},
            {"Line Item": "Net Realized Revenue", "Per Unit (₹)": f"₹{sp*(1-disc/100):,.2f}", "Total Batch (₹)": format_currency(net_rev), "% of Net Revenue": "100.0%"},
            {"Line Item": "Cost of Goods Sold (COGS) (-)", "Per Unit (₹)": f"₹{cp:,.2f}", "Total Batch (₹)": format_currency(-total_cogs), "% of Net Revenue": f"-{(total_cogs/net_rev)*100:.1f}%" if net_rev>0 else "0%"},
            {"Line Item": "Freight & Shipping Expense (-)", "Per Unit (₹)": f"₹{ship:,.2f}", "Total Batch (₹)": format_currency(-total_ship), "% of Net Revenue": f"-{(total_ship/net_rev)*100:.1f}%" if net_rev>0 else "0%"},
            {"Line Item": "Advertising & Marketing Spend (-)", "Per Unit (₹)": f"₹{ad/demand:,.2f}" if demand>0 else "₹0", "Total Batch (₹)": format_currency(-ad), "% of Net Revenue": f"-{(ad/net_rev)*100:.1f}%" if net_rev>0 else "0%"},
            {"Line Item": "Reverse Logistics & Return Loss (-)", "Per Unit (₹)": f"₹{return_loss/demand:,.2f}" if demand>0 else "₹0", "Total Batch (₹)": format_currency(-return_loss), "% of Net Revenue": f"-{(return_loss/net_rev)*100:.1f}%" if net_rev>0 else "0%"},
            {"Line Item": "Net Operating Profit (=)", "Per Unit (₹)": f"₹{net_profit/demand:,.2f}" if demand>0 else "₹0", "Total Batch (₹)": format_currency(net_profit), "% of Net Revenue": f"{res['profit_margin']:.1f}%"}
        ]
        
        st.dataframe(pd.DataFrame(pnl_data), hide_index=True, use_container_width=True)

# ==============================================================================
# TAB 3: PRICE ELASTICITY & SENSITIVITY CURVE
# ==============================================================================
with tabs[2]:
    st.markdown('<div class="main-header">Price Elasticity & Profit Optimization Curve</div>', unsafe_allow_html=True)
    st.markdown("Simulate how demand, revenue, and profit shift across different price points to discover the **Optimal Retail Price**.")

    if st.session_state["current_input"] is None:
        st.info("Analyze a product in Tab 1 first to generate price elasticity curves.")
    else:
        inp = st.session_state["current_input"]
        
        with st.spinner("Simulating price sensitivity across price range..."):
            df_sens, opt_row = simulate_price_sensitivity(inp, min_mult=0.5, max_mult=1.7, steps=20)
            
        opt_sp = opt_row["Selling Price (₹)"]
        opt_profit = opt_row["Predicted Profit (₹)"]
        opt_demand = opt_row["Predicted Demand (Units)"]
        
        st.success(f"🎯 **Profit-Maximizing Price Point Found**: Setting price to **₹{opt_sp:,.0f}** optimizes net profit to **{format_currency(opt_profit)}** at an estimated demand of **{opt_demand:,} units**.")
        
        # Dual-axis Plotly Curve: Price vs Profit & Demand
        fig_sens = go.Figure()
        
        # Profit Line
        fig_sens.add_trace(go.Scatter(
            x=df_sens["Selling Price (₹)"],
            y=df_sens["Predicted Profit (₹)"],
            name="Predicted Profit (₹)",
            line=dict(color="#10B981", width=3),
            mode="lines+markers"
        ))
        
        # Demand Line on secondary Y axis
        fig_sens.add_trace(go.Scatter(
            x=df_sens["Selling Price (₹)"],
            y=df_sens["Predicted Demand (Units)"],
            name="Predicted Demand (Units)",
            line=dict(color="#3B82F6", width=3, dash="dash"),
            mode="lines+markers",
            yaxis="y2"
        ))
        
        # Optimal Price Highlight Marker
        fig_sens.add_trace(go.Scatter(
            x=[opt_sp],
            y=[opt_profit],
            name="Optimal Price Marker",
            marker=dict(size=14, color="#F59E0B", symbol="star"),
            mode="markers"
        ))
        
        fig_sens.update_layout(
            title="Interactive Price Elasticity: Selling Price vs Profit & Demand",
            xaxis=dict(title=dict(text="Selling Price (₹)")),
            yaxis=dict(title=dict(text="Predicted Profit (₹)", font=dict(color="#10B981")), tickfont=dict(color="#10B981")),
            yaxis2=dict(title=dict(text="Predicted Demand (Units)", font=dict(color="#3B82F6")), tickfont=dict(color="#3B82F6"), overlaying="y", side="right"),
            height=480,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_sens, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📊 Price Sensitivity Grid Data")
        st.dataframe(df_sens, hide_index=True, use_container_width=True)

# ==============================================================================
# TAB 4: MODEL PERFORMANCE (6 ML MODELS)
# ==============================================================================
with tabs[3]:
    st.markdown('<div class="main-header">Machine Learning Model Evaluation Suite</div>', unsafe_allow_html=True)
    st.markdown("Dynamic evaluation metrics ($R^2$, MAE, RMSE, MAPE) computed on hold-out Test dataset.")
    
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)

        for target_key in ["demand", "profit"]:
            st.subheader(f"📌 Target Variable: {target_key.upper()} Models Comparison")
            best_model_name = metrics_data[target_key]["best_model"]
            st.success(f"🏆 Winning Model Selected: **{best_model_name}**")
            
            model_records = []
            models_dict = metrics_data[target_key]["models"]
            for m_name, m_eval in models_dict.items():
                test_m = m_eval["test"]
                model_records.append({
                    "Model": m_name,
                    "R² Score": test_m["R2"],
                    "MAE": test_m["MAE"],
                    "RMSE": test_m["RMSE"],
                    "MAPE (%)": test_m["MAPE"]
                })
                
            df_metrics = pd.DataFrame(model_records).sort_values(by="R² Score", ascending=False)
            st.dataframe(df_metrics, hide_index=True, use_container_width=True)
            
            # Interactive Plotly Bar Chart of R2 Scores
            fig_m = px.bar(
                df_metrics, 
                x="R² Score", 
                y="Model", 
                orientation="h", 
                text="R² Score",
                color="R² Score",
                color_continuous_scale="Viridis",
                title=f"Test R² Accuracy Across All 6 Regression Models ({target_key.capitalize()})"
            )
            fig_m.update_layout(height=320)
            st.plotly_chart(fig_m, use_container_width=True)
            st.markdown("---")
    else:
        st.info("No model metrics found. Please train models from sidebar.")

# ==============================================================================
# TAB 5: SHAP EXPLAINABLE AI
# ==============================================================================
with tabs[4]:
    st.markdown('<div class="main-header">Explainable AI (SHAP Explanations)</div>', unsafe_allow_html=True)
    st.markdown("Transparent feature attribution explaining **why** the ML model predicted this exact profit outcome.")
    
    if st.session_state["analysis_result"] is None:
        st.warning("Analyze a product in Tab 1 first to generate SHAP explanations.")
    else:
        X_input_df = st.session_state["analysis_result"]["X_input"]
        
        with st.spinner("Computing SHAP feature contributions..."):
            try:
                fig_global, fig_local, df_exp = explain_prediction_shap(X_input_df, model_type="profit")
                
                exp_col1, exp_col2 = st.columns(2)
                with exp_col1:
                    st.subheader("1. Local Feature Contribution (This Product)")
                    st.pyplot(fig_local)
                with exp_col2:
                    st.subheader("2. Global Model Feature Importance")
                    st.pyplot(fig_global)
                    
                st.markdown("---")
                st.subheader("Feature Impact Breakdown Table")
                st.dataframe(df_exp, hide_index=True, use_container_width=True)
            except Exception as e:
                st.error(f"SHAP evaluation error: {str(e)}")

# ==============================================================================
# TAB 6: INTERACTIVE WHAT-IF SIMULATOR
# ==============================================================================
with tabs[5]:
    st.markdown('<div class="main-header">Interactive What-If Business Simulator</div>', unsafe_allow_html=True)
    st.markdown("Simulate commercial strategy shifts and compare deltas in profit, demand, revenue, risk, and business score.")

    if st.session_state["current_input"] is None:
        st.info("Analyze a product in Tab 1 first to populate base parameters into the What-If Simulator.")
    else:
        base_input = dict(st.session_state["current_input"])
        
        st.subheader("🎛️ Adjust What-If Scenario Parameters")
        s_col1, s_col2, s_col3 = st.columns(3)
        
        with s_col1:
            sim_sp = st.slider("Simulated Selling Price (₹)", min_value=100.0, max_value=20000.0, value=float(base_input["selling_price"]), step=50.0)
            sim_cp = st.slider("Simulated Cost Price (₹)", min_value=50.0, max_value=15000.0, value=float(base_input["cost_price"]), step=50.0)
            
        with s_col2:
            sim_disc = st.slider("Simulated Discount %", min_value=0.0, max_value=80.0, value=float(base_input["discount_percent"]), step=1.0)
            sim_ad = st.slider("Simulated Ad Budget (₹)", min_value=0.0, max_value=100000.0, value=float(base_input["advertising_cost"]), step=1000.0)

        with s_col3:
            sim_ship = st.slider("Simulated Shipping Cost (₹)", min_value=0.0, max_value=1000.0, value=float(base_input["shipping_cost"]), step=10.0)
            sim_ret = st.slider("Simulated Return Rate %", min_value=0.0, max_value=40.0, value=float(base_input["return_rate"]), step=0.5)

        sim_input = dict(base_input)
        sim_input["selling_price"] = sim_sp
        sim_input["cost_price"] = sim_cp
        sim_input["discount_percent"] = sim_disc
        sim_input["advertising_cost"] = sim_ad
        sim_input["shipping_cost"] = sim_ship
        sim_input["return_rate"] = sim_ret
        
        base_res = st.session_state["analysis_result"]
        sim_res = run_product_analysis(sim_input)
        
        st.markdown("---")
        st.subheader("📊 Dynamic Scenario Comparison & Deltas")
        
        # Interactive Side-by-Side Comparison Metrics
        comp_df = pd.DataFrame([
            {
                "Metric": "Predicted Demand",
                "Current Scenario": f"{base_res['predicted_demand']:,} units",
                "Modified Scenario": f"{sim_res['predicted_demand']:,} units",
                "Delta": f"{sim_res['predicted_demand'] - base_res['predicted_demand']:,} units"
            },
            {
                "Metric": "Predicted Revenue",
                "Current Scenario": format_currency(base_res["predicted_revenue"]),
                "Modified Scenario": format_currency(sim_res["predicted_revenue"]),
                "Delta": format_currency(sim_res["predicted_revenue"] - base_res["predicted_revenue"])
            },
            {
                "Metric": "Predicted Profit",
                "Current Scenario": format_currency(base_res["predicted_profit"]),
                "Modified Scenario": format_currency(sim_res["predicted_profit"]),
                "Delta": format_currency(sim_res["predicted_profit"] - base_res["predicted_profit"])
            },
            {
                "Metric": "Profit Margin",
                "Current Scenario": f"{base_res['profit_margin']:.1f}%",
                "Modified Scenario": f"{sim_res['profit_margin']:.1f}%",
                "Delta": f"{sim_res['profit_margin'] - base_res['profit_margin']:+.1f}%"
            },
            {
                "Metric": "Business Score",
                "Current Scenario": f"{base_res['business_score']['score']} / 100",
                "Modified Scenario": f"{sim_res['business_score']['score']} / 100",
                "Delta": f"{sim_res['business_score']['score'] - base_res['business_score']['score']:+d} pts"
            },
            {
                "Metric": "Risk Level",
                "Current Scenario": base_res["risk_analysis"]["risk_level"],
                "Modified Scenario": sim_res["risk_analysis"]["risk_level"],
                "Delta": "Shift" if base_res["risk_analysis"]["risk_level"] != sim_res["risk_analysis"]["risk_level"] else "Unchanged"
            },
            {
                "Metric": "Launch Decision",
                "Current Scenario": base_res["launch_decision"]["decision"],
                "Modified Scenario": sim_res["launch_decision"]["decision"],
                "Delta": "Shift" if base_res["launch_decision"]["decision"] != sim_res["launch_decision"]["decision"] else "Unchanged"
            }
        ])
        
        st.dataframe(comp_df, hide_index=True, use_container_width=True)

        # Plotly Bar Chart comparing Current vs Modified Financials
        fig_comp = go.Figure(data=[
            go.Bar(name='Current Scenario', x=['Revenue', 'Profit'], y=[base_res['predicted_revenue'], base_res['predicted_profit']], marker_color='#3B82F6'),
            go.Bar(name='Modified Scenario', x=['Revenue', 'Profit'], y=[sim_res['predicted_revenue'], sim_res['predicted_profit']], marker_color='#10B981')
        ])
        fig_comp.update_layout(barmode='group', title="Interactive Scenario Comparison: Revenue & Profit (₹)", height=350)
        st.plotly_chart(fig_comp, use_container_width=True)

# ==============================================================================
# TAB 7: LAUNCH DECISION DASHBOARD
# ==============================================================================
with tabs[6]:
    st.markdown('<div class="main-header">🚀 Executive Product Launch Decision Engine</div>', unsafe_allow_html=True)
    st.markdown("Automated strategic business decision, model confidence evaluation, key driver breakdown, recommendations, and executive conclusion.")

    if st.session_state["analysis_result"] is None:
        st.info("Analyze a product in Tab 1 (or Tab 6) first to generate the Launch Decision evaluation.")
    else:
        res = st.session_state["analysis_result"]
        inp = st.session_state["current_input"]

        # ----------------------------------------------------------------------
        # 1. LAUNCH DECISION
        # ----------------------------------------------------------------------
        st.subheader("1. Launch Decision")
        
        dec_info = res["launch_decision"]
        decision_str = dec_info["decision"]
        rationale = dec_info["rationale"]
        
        # Display Decision Card with Visual Emphasis
        border_color = '#10B981' if 'LAUNCH' in decision_str and 'NOT' not in decision_str and 'MODIFICATIONS' not in decision_str else '#F59E0B' if 'MODIFICATIONS' in decision_str else '#EF4444'
        st.markdown(f'''
        <div style="background-color: #1E293B; border-left: 6px solid {border_color}; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="margin:0; font-size: 1.8rem; color: #FFFFFF;">
                Final Decision: <span style="color: {border_color}; font-weight: bold;">{decision_str}</span>
            </h2>
            <p style="margin-top: 10px; font-size: 1.05rem; color: #CBD5E1;">
                <strong>Strategic Rationale:</strong> {rationale}
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Supporting Executive Metrics Cards
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        col_d1.metric("Predicted Revenue", format_currency(res["predicted_revenue"]))
        col_d2.metric("Predicted Profit", format_currency(res["predicted_profit"]), delta=f"{res['profit_margin']:.1f}% Margin")
        col_d3.metric("Business Score", f"{res['business_score']['score']} / 100", delta=res['business_score'].get('label', 'Score'))
        col_d4.metric("Risk Level", res["risk_analysis"]["risk_level"])

        st.markdown("---")

        # ----------------------------------------------------------------------
        # 2. BEST MODEL
        # ----------------------------------------------------------------------
        st.subheader("2. Best Model")
        
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                metrics_data = json.load(f)
                
            best_profit_model_name = metrics_data["profit"]["best_model"]
            best_demand_model_name = metrics_data["demand"]["best_model"]
            profit_model_metrics = metrics_data["profit"]["models"][best_profit_model_name]["test"]
            demand_model_metrics = metrics_data["demand"]["models"][best_demand_model_name]["test"]
            
            st.markdown(f"**Actual best-performing model**: `{best_profit_model_name}` *(Selected dynamically based on Validation R² optimization for Profit target)*")
            
            # Display actual performance evaluation metrics
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric("R² Score", f"{profit_model_metrics['R2']:.4f}")
            m_col2.metric("MAE", format_currency(profit_model_metrics['MAE']))
            m_col3.metric("RMSE", format_currency(profit_model_metrics['RMSE']))
            m_col4.metric("MAPE", f"{profit_model_metrics.get('MAPE', 0):.1f}%")
            
            with st.expander("ℹ️ **Demand Target Winning Model Details**"):
                st.write(f"Best Demand Model: **{best_demand_model_name}** | Test R²: {demand_model_metrics['R2']:.4f} | Test MAE: {demand_model_metrics['MAE']:.1f} units")
        else:
            st.warning("Model metrics file missing. Please train models first.")

        st.markdown("---")

        # ----------------------------------------------------------------------
        # 3. KEY REASONS
        # ----------------------------------------------------------------------
        st.subheader("3. Key Reasons")
        st.markdown("Most important positive and negative factors driving the product performance and risk assessment.")
        
        key_pos, key_neg = st.columns(2)
        
        with key_pos:
            st.markdown("#### 🟢 Positive Factors")
            pos_factors = list(res["risk_analysis"]["positive_factors"])
            
            try:
                fig_g, fig_l, df_shap = explain_prediction_shap(res["X_input"], model_type="profit")
                if not df_shap.empty:
                    top_shap_pos = df_shap[df_shap["Impact"] > 0].head(3)
                    for _, row in top_shap_pos.iterrows():
                        feat_name = str(row['Feature']).replace('_', ' ').title()
                        pos_factors.append(f"Strong positive ML impact from **{feat_name}**")
            except Exception:
                pass
                
            if pos_factors:
                unique_pos = list(dict.fromkeys(pos_factors))
                for factor in unique_pos:
                    st.markdown(f"- ✅ {factor}")
            else:
                st.markdown("- No major positive drivers identified.")

        with key_neg:
            st.markdown("#### 🔴 Negative Factors")
            neg_factors = list(res["risk_analysis"]["negative_factors"])
            
            try:
                if 'df_shap' in locals() and not df_shap.empty:
                    top_shap_neg = df_shap[df_shap["Impact"] < 0].head(3)
                    for _, row in top_shap_neg.iterrows():
                        feat_name = str(row['Feature']).replace('_', ' ').title()
                        neg_factors.append(f"Negative ML drag from **{feat_name}**")
            except Exception:
                pass

            if neg_factors:
                unique_neg = list(dict.fromkeys(neg_factors))
                for factor in unique_neg:
                    st.markdown(f"- ⚠️ {factor}")
            else:
                st.markdown("- ✅ No major negative risk drivers detected.")

        st.markdown("---")

        # ----------------------------------------------------------------------
        # 4. RECOMMENDATIONS
        # ----------------------------------------------------------------------
        st.subheader("4. Recommendations")
        st.markdown("Contextually generated optimization steps for this specific product analysis:")
        
        recs = res["recommendations"]
        if recs:
            for rec in recs:
                st.markdown(rec)
        else:
            st.markdown("- Product parameters are well-optimized; maintain current commercial strategy.")

        st.markdown("---")

        # ----------------------------------------------------------------------
        # 5. CONCLUSION
        # ----------------------------------------------------------------------
        st.subheader("5. Conclusion")
        st.info(res["conclusion"])
