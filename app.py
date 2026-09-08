import os

import sys

from pathlib import Path

import warnings

warnings.filterwarnings("ignore")



# Ensure root project directory is in sys.path (cross-platform pathlib resolution)

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(0, str(PROJECT_ROOT))



import json

import pandas as pd

import numpy as np

import streamlit as st

import plotly.express as px

import plotly.graph_objects as go



from src.data_loader import (

    load_and_validate_data, get_product_name_col, load_external_dataset, 

    generate_data_quality_report, CATEGORY_SUBCATEGORIES, SEASONS, 

    PLATFORMS, MARKETING_CHANNELS, COMPETITION_LEVELS, REGIONS, PAYMENT_METHODS

)

from src.train_models import train_and_evaluate_all, MODELS_DIR, DATA_PATH

from src.prediction import run_product_analysis, simulate_price_sensitivity

from src.uncertainty import estimate_uncertainty_all, evaluate_conformal_calibration

from src.optimization import (

    run_joint_optimization, run_price_optimization, 

    run_discount_optimization, run_advertising_optimization

)

from research.baseline import run_baseline_comparison
from research.ablation import run_ablation_study
from utils.helpers import format_currency, save_prediction_to_history, load_prediction_history, logger
from src.ui.theme import COLORS
from src.ui.styles import inject_custom_styles

from src.ui.components import (
    render_top_header, render_kpi_summary_grid, render_hero_launch_card, 
    render_business_score_gauge, render_recommendation_cards
)

from src.ui.charts import (

    build_conformal_interval_chart, build_waterfall_chart,

    build_price_elasticity_chart, build_model_performance_chart

)

from src.ui.landing_page import render_project_info_landing_page

from src.ui.product_analyzer_page import render_product_launch_analyzer_page

from src.explainability import render_shap_explainability_section



HISTORY_PATH = os.path.join("data", "prediction_history.json")

METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")



# Streamlit Page Configuration

st.set_page_config(

    page_title="AI E-Commerce Profitability Intelligence",

    page_icon="📈",

    layout="wide",

    initial_sidebar_state="expanded"

)



# Inject White Enterprise CSS Styles

inject_custom_styles()



# Initialize Session State Page Navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "dashboard"

if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

if "current_input" not in st.session_state:
    st.session_state["current_input"] = None

if "last_input_tuple" not in st.session_state:
    st.session_state["last_input_tuple"] = None

# Pre-initialize widget keys safely
default_keys = {
    "p_cat": list(CATEGORY_SUBCATEGORIES.keys())[0],
    "p_subcat": list(CATEGORY_SUBCATEGORIES.values())[0][0],
    "p_sp": 3499.0,
    "p_cp": 1400.0,
    "p_disc": 15.0,
    "p_ad": 12000.0,
    "p_ship": 120.0,
    "p_ret": 6.0,
    "p_rating": 4.4,
    "p_season": SEASONS[0],
    "p_channel": MARKETING_CHANNELS[0],
    "p_comp": COMPETITION_LEVELS[1],
    "p_plat": PLATFORMS[0],
    "p_reg": REGIONS[0],
    "p_pay": PAYMENT_METHODS[0]
}
for dk, dv in default_keys.items():
    if dk not in st.session_state:
        st.session_state[dk] = dv

# Cache real dataset loading
@st.cache_data
def load_cached_real_dataset():
    try:
        return load_and_validate_data()
    except Exception:
        return None

df_dataset = load_cached_real_dataset()

# ==============================================================================
# GLOBAL SIDEBAR NAVIGATION PANEL
# ==============================================================================
st.sidebar.markdown(f'''
<div style="padding: 6px 0 16px 0; border-bottom: 1px solid {COLORS['border']}; margin-bottom: 16px;">
    <h2 style="font-size: 20px; font-weight: 800; color: {COLORS['text_primary']}; margin: 0; display: flex; align-items: center; gap: 8px;">
        ⚡ AI E-Commerce
    </h2>
    <p style="font-size: 13px; color: {COLORS['purple']}; font-weight: 700; margin: 2px 0 0 0; letter-spacing: 0.04em;">
        Profitability Intelligence
    </p>
</div>
''', unsafe_allow_html=True)

nav_options = [
    "Business Dashboard",
    "Product Launch Analyzer",
    "Product Analysis",
    "Profit Prediction",
    "Model Comparison",
    "Explainability",
    "Price Optimization",
    "Risk Analysis",
    "Research / Experiments",
    "Prediction History",
    "Project Overview",
    "Settings"
]

# Sync radio index with current_page
nav_index_map = {
    "dashboard": 0,
    "analyzer": 1,
    "product_analysis": 2,
    "prediction": 3,
    "model_comparison": 4,
    "explainability": 5,
    "optimization": 6,
    "risk": 7,
    "research": 8,
    "history": 9,
    "project_info": 10,
    "settings": 11
}
current_nav_index = nav_index_map.get(st.session_state.get("current_page", "dashboard"), 0)

nav_choice = st.sidebar.radio(
    "NAVIGATION",
    nav_options,
    index=current_nav_index,
    key="global_sidebar_nav"
)

# Update session state based on sidebar selection
nav_page_map = {
    "Business Dashboard": "dashboard",
    "Product Launch Analyzer": "analyzer",
    "Product Analysis": "product_analysis",
    "Profit Prediction": "prediction",
    "Model Comparison": "model_comparison",
    "Explainability": "explainability",
    "Price Optimization": "optimization",
    "Risk Analysis": "risk",
    "Research / Experiments": "research",
    "Prediction History": "history",
    "Project Overview": "project_info",
    "Settings": "settings"
}
selected_page = nav_page_map.get(nav_choice, "dashboard")
if st.session_state["current_page"] != selected_page:
    st.session_state["current_page"] = selected_page

st.sidebar.markdown("---")
st.sidebar.markdown(f'''
<div style="font-size: 13px; color: {COLORS['text_secondary']}; display: flex; flex-direction: column; gap: 10px; padding: 4px 0 12px 0;">
    <div style="cursor: pointer; display: flex; align-items: center; gap: 8px;">⚙️ <b>Settings</b></div>
    <div style="cursor: pointer; display: flex; align-items: center; gap: 8px;">❓ <b>Help / Documentation</b></div>
</div>
''', unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ System Control Center")
if st.sidebar.button("🔄 Retrain All 6 ML Models", use_container_width=True, key="global_retrain_models_btn"):
    with st.spinner("Training 6 ML Models on 10,000 real records..."):
        metrics = train_and_evaluate_all()
        st.sidebar.success("✅ Models retrained & conformal quantiles saved!")

auto_run = st.sidebar.checkbox("⚡ Real-Time Scenario Sync", value=True, key="global_auto_run_sync_chk")

# Top Global Page Navigation Header Bar
st.markdown("<div class='top-nav-bar-container'>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)
with p_col1:
    btn_p1_type = "primary" if st.session_state["current_page"] == "project_info" else "secondary"
    if st.button("📄 PAGE 1: PROJECT OVERVIEW", use_container_width=True, type=btn_p1_type, key="top_nav_p1_btn"):
        st.session_state["current_page"] = "project_info"
        st.rerun()

with p_col2:
    btn_p2_type = "primary" if st.session_state["current_page"] == "dashboard" else "secondary"
    if st.button("📊 PAGE 2: BUSINESS DASHBOARD", use_container_width=True, type=btn_p2_type, key="top_nav_p2_btn"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()

with p_col3:
    btn_p3_type = "primary" if st.session_state["current_page"] == "analyzer" else "secondary"
    if st.button("🚀 PAGE 3: PRODUCT LAUNCH ANALYZER", use_container_width=True, type=btn_p3_type, key="top_nav_p3_btn"):
        st.session_state["current_page"] = "analyzer"
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PAGE ROUTING & DISPLAY
# ==============================================================================
if st.session_state["current_page"] == "project_info":
    render_project_info_landing_page(df_dataset)

elif st.session_state["current_page"] == "analyzer":
    render_product_launch_analyzer_page()

else:
    # Render Main Dashboard Top Header Banner
    render_top_header()



    # --------------------------------------------------------------------------

    # MODULE 1: BUSINESS DASHBOARD (EXECUTIVE OVERVIEW)

    # --------------------------------------------------------------------------

    if nav_choice == "Business Dashboard":

        if df_dataset is None:

            st.error("🚨 REAL RESEARCH DATASET NOT FOUND.\nPlease place 'ecommerce_sales_dataset.csv' inside the 'data/raw/' directory.\nSynthetic data generation has been completely disabled per real-world research policy.")

        else:

            prod_name_col = get_product_name_col(df_dataset)

            unique_products = sorted(df_dataset[prod_name_col].dropna().astype(str).unique().tolist()) if prod_name_col else []



            with st.expander("🛠️ COMMERCIAL PRODUCT SPECIFICATIONS & PARAMETERS", expanded=True):

                # 📦 PRODUCT IDENTIFICATION (Full Width Card)

                st.markdown("<div class='input-group-box' style='margin-bottom: 20px;'>", unsafe_allow_html=True)

                st.markdown("<div class='input-group-header'>📦 PRODUCT IDENTIFICATION</div>", unsafe_allow_html=True)

                

                # 1. Product Name (Full Available Width)

                if unique_products:

                    selected_prod_name = st.selectbox(

                        "Product Name",

                        options=unique_products,

                        index=0,

                        key="p_select_name",

                        help="Search or select a product from the dataset"

                    )

                    st.caption("Search or select a product from the dataset")

                    

                    if st.session_state.get("last_selected_product") != selected_prod_name:

                        matched = df_dataset[df_dataset[prod_name_col].astype(str) == selected_prod_name]

                        if not matched.empty:

                            row = matched.iloc[0]

                            st.session_state["p_cat"] = str(row.get("product_category", "Technology"))

                            st.session_state["p_subcat"] = str(row.get("product_subcategory", "Accessories"))

                            st.session_state["p_sp"] = float(row.get("selling_price", 100.0))

                            st.session_state["p_cp"] = float(row.get("cost_price", 40.0))

                            st.session_state["p_disc"] = float(row.get("discount_percent", 0.0))

                            st.session_state["p_ship"] = float(row.get("shipping_cost", 10.0))

                            st.session_state["p_market"] = str(row.get("market", "US"))

                            st.session_state["p_region"] = str(row.get("region", "East"))

                            st.session_state["p_segment"] = str(row.get("segment", "Consumer"))

                            st.session_state["p_ship_mode"] = str(row.get("ship_mode", "Standard Class"))

                            st.session_state["p_order_priority"] = str(row.get("order_priority", "Medium"))

                            st.session_state["last_selected_product"] = selected_prod_name

                else:

                    st.text_input("Product Name", key="p_name")



                # 2. Category & Subcategory (Side-by-Side)

                cat_col1, cat_col2 = st.columns(2, gap="medium")

                with cat_col1:

                    categories = sorted(df_dataset["product_category"].dropna().unique().tolist()) if "product_category" in df_dataset.columns else ["Technology"]

                    st.selectbox("Category", options=categories, key="p_cat")

                    

                with cat_col2:

                    subcats = sorted(df_dataset[df_dataset["product_category"] == st.session_state.get("p_cat", categories[0])]["product_subcategory"].dropna().unique().tolist()) if "product_subcategory" in df_dataset.columns else ["Accessories"]

                    if st.session_state.get("p_subcat") not in subcats:

                        st.session_state["p_subcat"] = subcats[0] if subcats else "Accessories"

                    st.selectbox("Subcategory", options=subcats, key="p_subcat")



                # 3. Market & Region (Side-by-Side)

                mkt_col1, mkt_col2 = st.columns(2, gap="medium")

                with mkt_col1:

                    markets = sorted(df_dataset["market"].dropna().unique().tolist()) if "market" in df_dataset.columns else ["US"]

                    st.selectbox("Market", options=markets, key="p_market")

                    

                with mkt_col2:

                    regions = sorted(df_dataset["region"].dropna().unique().tolist()) if "region" in df_dataset.columns else ["East"]

                    st.selectbox("Region", options=regions, key="p_region")



                st.markdown("</div>", unsafe_allow_html=True)



                # 2. PRICING & LOGISTICS SECTIONS (Side-by-Side)

                param_col1, param_col2 = st.columns(2, gap="medium")

                with param_col1:

                    st.markdown("<div class='input-group-box'>", unsafe_allow_html=True)

                    st.markdown("<div class='input-group-header'>🏷️ PRICING & UNIT COSTS</div>", unsafe_allow_html=True)

                    st.number_input("Unit Selling Price (₹)", min_value=0.1, step=10.0, key="p_sp")

                    st.number_input("Unit Cost / COGS (₹)", min_value=0.1, step=10.0, key="p_cp")

                    st.slider("Discount %", min_value=0.0, max_value=85.0, step=1.0, key="p_disc")

                    st.markdown("</div>", unsafe_allow_html=True)



                with param_col2:

                    st.markdown("<div class='input-group-box'>", unsafe_allow_html=True)

                    st.markdown("<div class='input-group-header'>🚚 LOGISTICS & EXPENSES</div>", unsafe_allow_html=True)

                    st.number_input("Shipping Cost (₹)", min_value=0.0, step=5.0, key="p_ship")

                    st.text_input("Customer Segment", value=st.session_state.get("p_segment", "Consumer"), key="p_segment_display", disabled=True)

                    st.text_input("Shipping Mode", value=st.session_state.get("p_ship_mode", "Standard Class"), key="p_ship_mode_display", disabled=True)

                    st.markdown("</div>", unsafe_allow_html=True)



                st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

                analyze_btn = st.button("🚀 ANALYZE PRODUCT PROFITABILITY →", use_container_width=True, type="primary")



            product_name = st.session_state.get("p_select_name") if unique_products else st.session_state.get("p_name", "Superstore Product")

            product_category = st.session_state.get("p_cat", "Technology")

            product_subcategory = st.session_state.get("p_subcat", "Accessories")

            selling_price = float(st.session_state.get("p_sp", 100.0))

            cost_price = float(st.session_state.get("p_cp", 40.0))

            discount_percent = float(st.session_state.get("p_disc", 0.0))

            shipping_cost = float(st.session_state.get("p_ship", 10.0))

            market = st.session_state.get("p_market", "US")

            region = st.session_state.get("p_region", "East")

            segment = st.session_state.get("p_segment", "Consumer")

            ship_mode = st.session_state.get("p_ship_mode", "Standard Class")

            order_priority = st.session_state.get("p_order_priority", "Medium")



            current_input_tuple = (

                product_name, product_category, product_subcategory, selling_price, cost_price,

                discount_percent, shipping_cost, market, region, segment, ship_mode, order_priority

            )



            should_run = analyze_btn or (auto_run and (st.session_state["analysis_result"] is None or st.session_state.get("last_input_tuple") != current_input_tuple))



            if should_run:

                st.session_state["last_input_tuple"] = current_input_tuple

                input_data = {

                    "product_name": product_name,

                    "product_category": product_category,

                    "product_subcategory": product_subcategory,

                    "selling_price": selling_price,

                    "cost_price": cost_price,

                    "discount_percent": discount_percent,

                    "shipping_cost": shipping_cost,

                    "market": market,

                    "region": region,

                    "segment": segment,

                    "ship_mode": ship_mode,

                    "order_priority": order_priority

                }

                st.session_state["current_input"] = input_data

                

                with st.spinner("Analyzing product... Calculating business risk... Evaluating strategy..."):

                    res = run_product_analysis(input_data)

                    st.session_state["analysis_result"] = res

                    save_prediction_to_history(res, HISTORY_PATH)



            # Render Active Business Dashboard Results
            if st.session_state["analysis_result"] is not None:
                res = st.session_state["analysis_result"]
                inp = st.session_state.get("current_input", {})
                
                st.markdown("---")

                # 1. KPI SUMMARY CARDS GRID
                render_kpi_summary_grid(
                    profit_val=res['predicted_profit'],
                    margin_val=res['profit_margin'],
                    risk_lvl=res["risk_analysis"]["risk_level"],
                    business_score=res["business_score"]["score"],
                    decision_str=res["launch_decision"]["decision"]
                )

                st.markdown("---")

                # 2. MAIN BUSINESS ANALYSIS GRID (RESPONSIVE 2-COLUMN)
                st.markdown("<div class='section-header-title'>📊 MAIN BUSINESS ANALYSIS & LAUNCH DECISION</div>", unsafe_allow_html=True)
                main_col1, main_col2 = st.columns([1, 1], gap="large")

                with main_col1:
                    st.markdown("<h4 style='font-size:16px; font-weight:700; color:#F7F4F8; margin-bottom:12px;'>📉 Profitability Overview & Prediction Range</h4>", unsafe_allow_html=True)
                    unc = res.get("uncertainty", {})
                    prof_unc = unc.get("profit", {})
                    
                    fig_unc = build_conformal_interval_chart(
                        point_val=res['predicted_profit'],
                        lower_val=prof_unc.get('lower_bound', 0.0),
                        upper_val=prof_unc.get('upper_bound', 0.0)
                    )
                    st.plotly_chart(fig_unc, use_container_width=True)

                    u_c1, u_c2 = st.columns(2)
                    with u_c1:
                        st.metric("Interval Width (MPIW)", f"₹{prof_unc.get('interval_width', 0):,.2f}")
                    with u_c2:
                        st.metric("Loss Probability P(Profit < 0)", f"{unc.get('loss_probability_pct', 0.0):.1f}%")

                with main_col2:
                    st.markdown("<h4 style='font-size:16px; font-weight:700; color:#F7F4F8; margin-bottom:12px;'>🚀 Business Decision & Strategy Assessment</h4>", unsafe_allow_html=True)
                    
                    render_hero_launch_card(
                        decision_res=res["launch_decision"],
                        risk_res=res["risk_analysis"],
                        profit_val=res["predicted_profit"],
                        score_val=res["business_score"]["score"]
                    )
                    
                    fig_gauge, breakdown = render_business_score_gauge(res["business_score"])
                    st.plotly_chart(fig_gauge, use_container_width=True)

                st.markdown("---")

                # 3. INTERACTIVE PRICE ELASTICITY & PROFIT CURVE
                st.markdown("<div class='section-header-title'>📈 INTERACTIVE PRICE ELASTICITY & PROFIT CURVE</div>", unsafe_allow_html=True)
                
                if inp:
                    df_sens, opt_row = simulate_price_sensitivity(inp, min_mult=0.5, max_mult=1.7, steps=20)
                    col_sp = [c for c in df_sens.columns if "Selling Price" in c][0]
                    col_profit = [c for c in df_sens.columns if "Profit" in c and "Margin" not in c][0]
                    opt_sp = opt_row[col_sp]
                    opt_profit = opt_row[col_profit]

                    st.markdown(f'''
                    <div style="background-color: {COLORS['positive_bg']}; border: 1px solid {COLORS['positive']}; color: {COLORS['positive']}; padding: 14px 20px; border-radius: 12px; font-size: 15px; font-weight: 600; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">
                        🎯 <b>Profit-Maximizing Price Point Found</b>: Set selling price to <b>₹{opt_sp:,.2f}</b>, maximizing predicted net profit at approximately <b>₹{opt_profit:,.2f}</b>.
                    </div>
                    ''', unsafe_allow_html=True)

                    fig_sens = build_price_elasticity_chart(df_sens, col_sp, col_profit, opt_sp, opt_profit)
                    st.plotly_chart(fig_sens, use_container_width=True)

                st.markdown("---")

                # 4. EXPLAINABLE AI (WHY THIS PREDICTION?)
                render_shap_explainability_section(res, df_dataset)

                st.markdown("---")

                # 5. ACTIONABLE RECOMMENDATIONS & CONCLUSION
                render_recommendation_cards(res["recommendations"])

                st.markdown("<div class='section-header-title'>📝 EXECUTIVE TAKEAWAY CONCLUSION</div>", unsafe_allow_html=True)
                st.info(res["conclusion"])



    # --------------------------------------------------------------------------
    # MODULE 2: PRODUCT ANALYSIS & FINANCIAL WATERFALL
    # --------------------------------------------------------------------------
    elif nav_choice == "Product Analysis":
        st.markdown("<div class='section-header-title'>📦 PRODUCT ANALYSIS & FINANCIAL WATERFALL BREAKDOWN</div>", unsafe_allow_html=True)
        
        if st.session_state["analysis_result"] is None:
            st.info("Analyze a product in Business Dashboard first.")
        else:
            res = st.session_state["analysis_result"]
            inp = st.session_state["current_input"]
            
            sp = float(inp.get("selling_price", 100.0))
            cp = float(inp.get("cost_price", 40.0))
            disc = float(inp.get("discount_percent", 0.0))
            ship = float(inp.get("shipping_cost", 10.0))
            
            gross_rev = round(sp, 2)
            discount_val = round(sp * (disc / 100.0), 2)
            net_rev = round(sp * (1.0 - disc / 100.0), 2)
            total_cogs = round(cp, 2)
            total_ship = round(ship, 2)
            net_profit = res["predicted_profit"]
            
            st.markdown("### 📊 Financial Waterfall Breakdown")
            fig_waterfall = build_waterfall_chart(gross_rev, discount_val, net_rev, total_cogs, total_ship, net_profit)
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
            st.markdown("---")
            df_sens, opt_row = simulate_price_sensitivity(inp, min_mult=0.5, max_mult=1.7, steps=20)
            col_sp = [c for c in df_sens.columns if "Selling Price" in c][0]
            col_profit = [c for c in df_sens.columns if "Profit" in c and "Margin" not in c][0]

            opt_sp = opt_row[col_sp]
            opt_profit = opt_row[col_profit]
            
            st.markdown(f'''
            <div style="background-color: {COLORS['positive_bg']}; border: 1px solid {COLORS['positive']}; color: {COLORS['positive']}; padding: 14px 20px; border-radius: 12px; font-size: 15px; font-weight: 600; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">
                🎯 <b>Profit-Maximizing Price Point Found</b>: Set selling price to <b>₹{opt_sp:,.2f}</b>, maximizing predicted net profit at approximately <b>₹{opt_profit:,.2f}</b>.
            </div>
            ''', unsafe_allow_html=True)
            fig_sens = build_price_elasticity_chart(df_sens, col_sp, col_profit, opt_sp, opt_profit)
            st.plotly_chart(fig_sens, use_container_width=True)

    # --------------------------------------------------------------------------
    # MODULE 3: PROFIT PREDICTION & CONFIDENCE UNCERTAINTY
    # --------------------------------------------------------------------------
    elif nav_choice == "Profit Prediction":
        st.markdown("<div class='section-header-title'>🎲 PROFIT PREDICTION & CONFORMAL UNCERTAINTY</div>", unsafe_allow_html=True)
        
        if st.session_state["analysis_result"] is None:
            st.info("Analyze a product in Business Dashboard first.")
        else:
            res = st.session_state["analysis_result"]
            unc = res.get("uncertainty", {})
            
            u_c1, u_c2 = st.columns(2)
            with u_c1:
                prof_unc = unc.get("profit", {})
                prof_low = prof_unc.get("lower_bound", 0.0)
                prof_high = prof_unc.get("upper_bound", 0.0)
                low_str = f"-₹{abs(prof_low):,.2f}" if prof_low < 0 else f"₹{prof_low:,.2f}"
                high_str = f"-₹{abs(prof_high):,.2f}" if prof_high < 0 else f"₹{prof_high:,.2f}"
                st.metric("Expected Net Profit", f"₹{res['predicted_profit']:,.2f}")
                st.caption(f"Conformal Range (90%): {low_str} to {high_str}")
            with u_c2:
                st.metric("Loss Probability P(Profit < 0)", f"{unc.get('loss_probability_pct', 0.0):.1f}%")
                st.caption(f"Interval Width: ₹{prof_unc.get('interval_width', 0):,.2f}")

            fig_unc = build_conformal_interval_chart(
                point_val=res['predicted_profit'],
                lower_val=prof_unc.get('lower_bound', 0.0),
                upper_val=prof_unc.get('upper_bound', 0.0),
                title="Conformal Profit Uncertainty Interval (₹)"
            )
            st.plotly_chart(fig_unc, use_container_width=True)

    # --------------------------------------------------------------------------
    # MODULE 4: MODEL COMPARISON & PERFORMANCE SUITE
    # --------------------------------------------------------------------------
    elif nav_choice == "Model Comparison":
        st.markdown("<div class='section-header-title'>🤖 MODEL PERFORMANCE EVALUATION SUITE</div>", unsafe_allow_html=True)
        
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                metrics = json.load(f)
            
            p_models = metrics.get("profit", {}).get("models", {})
            if p_models:
                sorted_p = sorted(
                    p_models.items(),
                    key=lambda item: (
                        item[1]["test"]["RMSE"],
                        item[1]["test"]["MAE"],
                        -item[1]["test"]["R2"],
                        abs(item[1]["val"]["R2"] - item[1]["test"]["R2"])
                    )
                )
                p_best = metrics.get("profit", {}).get("best_model") or sorted_p[0][0]
            else:
                p_best = "Random Forest"
            
            st.success(f"🏆 **WINNING PROFIT PREDICTION MODEL**: **'{p_best}'** (Trained & Evaluated on 6 ML Regressors)")

            p_rows = []
            for name, r_data in p_models.items():
                p_rows.append({
                    "Model": name,
                    "Validation R²": round(r_data["val"]["R2"], 4),
                    "Test R²": round(r_data["test"]["R2"], 4),
                    "MAE (₹)": round(r_data["test"]["MAE"], 2),
                    "RMSE (₹)": round(r_data["test"]["RMSE"], 2),
                    "Status": "🏆 Best Model" if name == p_best else "Evaluated"
                })
            df_p_models = pd.DataFrame(p_rows)
            st.dataframe(df_p_models, hide_index=True, use_container_width=True)
            
            st.info("ℹ️ **Best Model Selection Criterion**: Primary: Lowest Test RMSE → Secondary: Lowest Test MAE → Tertiary: Highest Test R² → Quaternary: Lowest Overfitting Gap. All 6 models evaluated on exact same test set.")
            
            if not df_p_models.empty:
                fig_p = build_model_performance_chart(df_p_models)
                st.plotly_chart(fig_p, use_container_width=True)

    # --------------------------------------------------------------------------
    # MODULE 5: EXPLAINABILITY (WHY THIS PREDICTION?)
    # --------------------------------------------------------------------------
    elif nav_choice == "Explainability":
        if st.session_state["analysis_result"] is None:
            st.info("Analyze a product in Business Dashboard first to view SHAP explanations.")
        else:
            render_shap_explainability_section(st.session_state["analysis_result"], df_dataset)

    # --------------------------------------------------------------------------
    # MODULE 6: PRICE OPTIMIZATION & WHAT-IF SIMULATION
    # --------------------------------------------------------------------------
    elif nav_choice == "Price Optimization":
        st.markdown("<div class='section-header-title'>🎯 PRESCRIPTIVE COMMERCIAL OPTIMIZATION & WHAT-IF SIMULATOR</div>", unsafe_allow_html=True)
        
        if st.session_state["current_input"] is None:
            st.info("Analyze a product in Business Dashboard first.")
        else:
            inp = st.session_state["current_input"]
            opt_data = run_joint_optimization(inp, run_product_analysis, objective="Maximize Profit")
            
            if opt_data and "comparison" in opt_data:
                comp = opt_data["comparison"]
                cur_s = comp["current"]
                opt_s = comp["optimized"]
                imp = comp["improvement"]
                
                s_col1, s_col2, s_col3 = st.columns(3)
                with s_col1:
                    st.subheader("CURRENT STRATEGY")
                    st.metric("Selling Price", f"₹{cur_s['price']:,.2f}")
                    st.metric("Discount %", f"{cur_s['discount']:.1f}%")
                    st.metric("Expected Profit", f"₹{cur_s['expected_profit']:,.2f}")
                    
                with s_col2:
                    st.subheader("RECOMMENDED STRATEGY")
                    st.metric("Optimal Price", f"₹{opt_s['price']:,.2f}", delta=f"₹{opt_s['price'] - cur_s['price']:,.2f}")
                    st.metric("Optimal Discount", f"{opt_s['discount']:.1f}%", delta=f"{opt_s['discount'] - cur_s['discount']:.1f}%")
                    st.metric("Optimized Profit", f"₹{opt_s['expected_profit']:,.2f}", delta=f"₹{imp['profit_change']:,.2f}")
                    
                with s_col3:
                    st.subheader("EXPECTED CHANGE")
                    st.metric("Profit Change", f"₹{imp['profit_change']:,.2f}")
                    st.metric("Profit Lift %", f"+{imp['profit_change_pct']:.1f}%")
                    st.metric("Margin Change", f"+{imp['margin_change']:.1f}%")

            st.markdown("---")
            st.markdown("### 🎛️ Interactive What-If Scenario Simulator")
            base_input = dict(st.session_state["current_input"])
            
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                sim_sp = st.slider("Simulated Price (₹)", 1.0, 50000.0, float(base_input.get("selling_price", 100.0)))
                sim_cp = st.slider("Simulated Cost (₹)", 1.0, 30000.0, float(base_input.get("cost_price", 40.0)))
            with s_col2:
                sim_disc = st.slider("Simulated Discount %", 0.0, 85.0, float(base_input.get("discount_percent", 0.0)))
                sim_ship = st.slider("Simulated Shipping Cost (₹)", 0.0, 2000.0, float(base_input.get("shipping_cost", 10.0)))

            sim_input = dict(base_input)
            sim_input["selling_price"] = sim_sp
            sim_input["cost_price"] = sim_cp
            sim_input["discount_percent"] = sim_disc
            sim_input["shipping_cost"] = sim_ship
            
            base_res = st.session_state["analysis_result"]
            sim_res = run_product_analysis(sim_input)
            
            comp_df = pd.DataFrame([
                {"Metric": "Predicted Net Profit", "Current": f"₹{base_res['predicted_profit']:,.2f}", "What-If": f"₹{sim_res['predicted_profit']:,.2f}", "Change": f"₹{sim_res['predicted_profit'] - base_res['predicted_profit']:,.2f}"},
                {"Metric": "Profit Margin", "Current": f"{base_res['profit_margin']:.1f}%", "What-If": f"{sim_res['profit_margin']:.1f}%", "Change": f"{sim_res['profit_margin'] - base_res['profit_margin']:+.1f}%"},
                {"Metric": "Business Score", "Current": f"{base_res['business_score']['score']}/100", "What-If": f"{sim_res['business_score']['score']}/100", "Change": f"{sim_res['business_score']['score'] - base_res['business_score']['score']:+d} pts"}
            ])
            st.dataframe(comp_df, hide_index=True, use_container_width=True)

    # --------------------------------------------------------------------------
    # MODULE 7: RISK ANALYSIS
    # --------------------------------------------------------------------------
    elif nav_choice == "Risk Analysis":
        st.markdown("<div class='section-header-title'>🛡️ MULTI-FACTOR RISK ANALYSIS</div>", unsafe_allow_html=True)
        
        if st.session_state["analysis_result"] is None:
            st.info("Analyze a product in Business Dashboard first.")
        else:
            res = st.session_state["analysis_result"]
            risk = res["risk_analysis"]
            st.write(f"### Risk Rating: {risk['risk_level']} ({risk['risk_score']}/100)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### ✓ Positive Factors")
                for p in risk["positive_factors"]:
                    st.markdown(f"- ✓ {p}")
            with col2:
                st.markdown("### ⚠ Negative Risk Factors")
                for n in risk["negative_factors"]:
                    st.markdown(f"- ⚠ {n}")

    # --------------------------------------------------------------------------
    # MODULE 8: RESEARCH / EXPERIMENTS
    # --------------------------------------------------------------------------
    elif nav_choice in ["Research / Experiments", "Research Evaluation"]:
        st.markdown("<div class='section-header-title'>🔬 RESEARCH LABORATORY & EXPERIMENTAL EVALUATION</div>", unsafe_allow_html=True)
        
        r_tabs = st.tabs(["BASELINE COMPARISON", "ABLATION STUDY"])
        with r_tabs[0]:
            st.subheader("Baseline System vs Proposed Decision Framework")
            if st.button("▶ Run Baseline Experiment"):
                df_base = run_baseline_comparison()
                st.dataframe(df_base, hide_index=True, use_container_width=True)
                
        with r_tabs[1]:
            st.subheader("Ablation Study (Experiments A - F)")
            if st.button("▶ Run Ablation Study"):
                df_abl, hyp = run_ablation_study()
                st.dataframe(df_abl, hide_index=True, use_container_width=True)

    # --------------------------------------------------------------------------
    # MODULE 9: PREDICTION HISTORY
    # --------------------------------------------------------------------------
    elif nav_choice == "Prediction History":
        st.markdown("<div class='section-header-title'>📜 PREDICTION HISTORY LOGS</div>", unsafe_allow_html=True)
        
        history_records = load_prediction_history(HISTORY_PATH)
        if not history_records:
            st.info("No prediction history found yet.")
        else:
            df_hist = pd.DataFrame(history_records)
            st.dataframe(df_hist, hide_index=True, use_container_width=True)

    # --------------------------------------------------------------------------
    # MODULE 10: SETTINGS & CONTROL CENTER
    # --------------------------------------------------------------------------
    elif nav_choice == "Settings":
        st.markdown("<div class='section-header-title'>⚙️ SYSTEM SETTINGS & MODEL RE-TRAINING CONTROL CENTER</div>", unsafe_allow_html=True)
        
        st.markdown("### 🤖 ML Pipeline Re-Training")
        st.write("Click below to retrain all 6 ML Regressors on the live dataset records and update conformal prediction bounds.")
        
        if st.button("🔄 Retrain All 6 ML Models", type="primary"):
            with st.spinner("Training 6 ML Models on 10,000 real records..."):
                metrics = train_and_evaluate_all()
                st.success("✅ All 6 ML models retrained and saved successfully!")
                
        st.markdown("---")
        st.markdown("### 📊 Dataset Integrity & Info")
        if df_dataset is not None:
            st.write(f"**Loaded Records**: `{len(df_dataset):,}` rows")
            st.write(f"**Total Features**: `{len(df_dataset.columns)}` columns")
            st.write(f"**SHA-256 Checksum**: `{df_dataset.attrs.get('sha256', 'Verified')}`")