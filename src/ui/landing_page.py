"""
Professional Project Information Landing Page (Page 1)
Premium Dark Investment Dashboard UI Theme
"""

import streamlit as st
from src.ui.theme import COLORS

def render_project_info_landing_page(df_dataset):
    """
    Renders Page 1: Professional Project Information & Research Landing Screen.
    Uses dynamic dataset stats from df_dataset.
    """
    # 1. Main Header Title
    st.markdown(f'''
    <div style="text-align:center; padding: 30px 20px 20px 20px; background:#151217; border:1px solid #3A303B; border-radius:14px; margin-bottom:24px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
        <span style="font-size:12px; font-weight:700; color:#C58BB9; text-transform:uppercase; letter-spacing:0.1em; background:rgba(197,139,185,0.12); padding:4px 14px; border-radius:9999px; border:1px solid rgba(197,139,185,0.3);">RESEARCH-GRADE DECISION INTELLIGENCE SYSTEM</span>
        <h1 style="font-size:32px; font-weight:800; color:#F5F0F5; margin:14px 0 8px 0; letter-spacing:-0.02em;">
            AI-BASED E-COMMERCE PRODUCT PROFITABILITY & BUSINESS DECISION INTELLIGENCE SYSTEM
        </h1>
        <p style="font-size:15px; color:#A9A1AA; max-width:850px; margin:0 auto; line-height:1.6;">
            An AI-powered predictive and prescriptive framework for e-commerce product profitability, risk assessment and business decision-making.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    # 2. Project Overview & Problem Statement
    col_ov, col_ps = st.columns(2)
    
    with col_ov:
        st.markdown(f'''
        <div class="premium-card" style="height:100%;">
            <div class="card-label" style="color:#C58BB9;">📌 PROJECT OVERVIEW</div>
            <p style="font-size:14px; color:#F5F0F5; line-height:1.6; margin:6px 0 0 0;">
                An AI-based decision intelligence system designed to help e-commerce businesses evaluate a product before launch or promotion by predicting net profit, quantifying prediction uncertainty, assessing business risk, and identifying profit-maximizing pricing and discount strategies.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col_ps:
        st.markdown(f'''
        <div class="premium-card" style="height:100%;">
            <div class="card-label" style="color:#C58BB9;">⚠️ PROBLEM STATEMENT</div>
            <p style="font-size:14px; color:#F5F0F5; line-height:1.6; margin:6px 0 0 0;">
                E-commerce businesses must make product decisions under uncertainty. Traditional approaches fail to integrate machine learning profit predictions with prediction uncertainty quantification, multi-factor risk scoring, business suitability scoring, strategy optimization, and risk-aware launch decisions.
            </p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # 3. Research Objectives (6 Cards Grid)
    st.markdown("<div class='section-header-title'>🎯 RESEARCH OBJECTIVES</div>", unsafe_allow_html=True)
    
    obj_col1, obj_col2 = st.columns(2)
    
    with obj_col1:
        st.markdown(f'''
        <div class="premium-card">
            <div class="card-label" style="color:#C58BB9;">OBJECTIVE 1 &nbsp;|&nbsp; PROFIT PREDICTION MODELS</div>
            <p style="font-size:13px; color:#F5F0F5; margin:4px 0 0 0;">Develop machine-learning profit regression models for predicting e-commerce product profitability using pre-sale features.</p>
        </div>
        <div class="premium-card">
            <div class="card-label" style="color:#C58BB9;">OBJECTIVE 2 &nbsp;|&nbsp; INTEGRATED DECISION FRAMEWORK</div>
            <p style="font-size:13px; color:#F5F0F5; margin:4px 0 0 0;">Develop an integrated framework for estimating profit margin, 0-100 business score, and product-level commercial potential.</p>
        </div>
        <div class="premium-card">
            <div class="card-label" style="color:#C58BB9;">OBJECTIVE 3 &nbsp;|&nbsp; UNCERTAINTY QUANTIFICATION</div>
            <p style="font-size:13px; color:#F5F0F5; margin:4px 0 0 0;">Incorporate split conformal prediction uncertainty to quantify interval bounds and downside loss probability P(Profit < 0).</p>
        </div>
        ''', unsafe_allow_html=True)

    with obj_col2:
        st.markdown(f'''
        <div class="premium-card">
            <div class="card-label" style="color:#C58BB9;">OBJECTIVE 4 &nbsp;|&nbsp; PRESCRIPTIVE OPTIMIZATION</div>
            <p style="font-size:13px; color:#F5F0F5; margin:4px 0 0 0;">Develop a prescriptive optimization framework for identifying profit-maximizing price and discount strategies.</p>
        </div>
        <div class="premium-card">
            <div class="card-label" style="color:#C58BB9;">OBJECTIVE 5 &nbsp;|&nbsp; EXPERIMENTAL EVALUATION</div>
            <p style="font-size:13px; color:#F5F0F5; margin:4px 0 0 0;">Evaluate the proposed framework against baseline approaches and conduct ablation experiments across 6 configurations.</p>
        </div>
        <div class="premium-card">
            <div class="card-label" style="color:#C58BB9;">OBJECTIVE 6 &nbsp;|&nbsp; DECISION-SUPPORT DASHBOARD</div>
            <p style="font-size:13px; color:#F5F0F5; margin:4px 0 0 0;">Develop an interactive decision-support dashboard that converts ML profit predictions into risk-aware launch decisions and recommendations.</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # 4. Proposed Framework Visual Diagram
    st.markdown("<div class='section-header-title'>🔄 PROPOSED DECISION FRAMEWORK ARCHITECTURE</div>", unsafe_allow_html=True)
    st.markdown(f'''
    <div style="background:#151217; border:1px solid #3A303B; border-radius:12px; padding:20px; text-align:center; box-shadow:0 4px 16px rgba(0,0,0,0.3);">
        <div style="display:flex; justify-content:center; align-items:center; flex-wrap:wrap; gap:10px; font-size:12px; font-weight:700;">
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:8px 12px; border-radius:8px; border:1px solid rgba(197,139,185,0.3);">PRODUCT INPUT</span>
            <span style="color:#A9A1AA;">→</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:8px 12px; border-radius:8px; border:1px solid rgba(197,139,185,0.3);">DATA QUALITY & LEAKAGE CHECK</span>
            <span style="color:#A9A1AA;">→</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:8px 12px; border-radius:8px; border:1px solid rgba(197,139,185,0.3);">PROFIT PREDICTION MODEL (XGBOOST/CATBOOST/RF)</span>
            <span style="color:#A9A1AA;">→</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:8px 12px; border-radius:8px; border:1px solid rgba(197,139,185,0.3);">CONFORMAL PROFIT UNCERTAINTY</span>
        </div>
        <div style="margin:12px 0 4px 0; color:#A9A1AA; font-size:16px;">↓</div>
        <div style="display:flex; justify-content:center; align-items:center; flex-wrap:wrap; gap:10px; font-size:12px; font-weight:700;">
            <span style="background:rgba(79,197,138,0.12); color:#4FC58A; padding:8px 12px; border-radius:8px; border:1px solid rgba(79,197,138,0.3);">BUSINESS RECOMMENDATIONS</span>
            <span style="color:#A9A1AA;">←</span>
            <span style="background:rgba(79,197,138,0.12); color:#4FC58A; padding:8px 12px; border-radius:8px; border:1px solid rgba(79,197,138,0.3);">LAUNCH DECISION</span>
            <span style="color:#A9A1AA;">←</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:8px 12px; border-radius:8px; border:1px solid rgba(197,139,185,0.3);">PRESCRIPTIVE OPTIMIZATION</span>
            <span style="color:#A9A1AA;">←</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:8px 12px; border-radius:8px; border:1px solid rgba(197,139,185,0.3);">0-100 BUSINESS SCORE</span>
            <span style="color:#A9A1AA;">←</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:8px 12px; border-radius:8px; border:1px solid rgba(197,139,185,0.3);">RISK ANALYSIS</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


    st.markdown("---")

    # 5. ML Models & Data Source Statistics
    col_m, col_d = st.columns(2)
    
    with col_m:
        st.markdown("<div class='section-header-title'>🤖 MODELS EVALUATED</div>", unsafe_allow_html=True)
        st.markdown(f'''
        <div class="premium-card">
            <ul style="margin:0; padding-left:20px; font-size:14px; color:#F5F0F5; line-height:1.8;">
                <li>Multiple Linear Regression</li>
                <li>Random Forest Regressor</li>
                <li>XGBoost Regressor</li>
                <li>LightGBM Regressor</li>
                <li>CatBoost Regressor</li>
                <li>Artificial Neural Network (ANN)</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

    with col_d:
        st.markdown("<div class='section-header-title'>📊 DATA SOURCE STATISTICS</div>", unsafe_allow_html=True)
        if df_dataset is not None:
            num_rows = f"{len(df_dataset):,}"
            num_cols = f"{len(df_dataset.columns)}"
            sha256 = df_dataset.attrs.get("sha256", "cfff9e65bb9e...")[:16]
            st.markdown(f'''
            <div class="premium-card">
                <div style="font-size:13px; color:#A9A1AA; margin-bottom:4px;">DATASET NAME: <b style="color:#F5F0F5;">Global E-Commerce Sales Dataset | 2021–2024</b></div>
                <div style="font-size:13px; color:#A9A1AA; margin-bottom:4px;">DATASET TYPE: <b style="color:#4FC58A; background:rgba(79,197,138,0.15); padding:2px 6px; border-radius:4px;">REAL-WORLD DATA</b></div>
                <div style="font-size:13px; color:#A9A1AA; margin-bottom:4px;">TRANSACTION RECORDS: <b style="color:#F5F0F5;">{num_rows}</b></div>
                <div style="font-size:13px; color:#A9A1AA; margin-bottom:4px;">COLUMNS / FEATURES: <b style="color:#F5F0F5;">{num_cols}</b></div>
                <div style="font-size:11px; color:#A9A1AA; margin-top:6px;">SHA-256 HASH: <code style="background:#1C1820; color:#C58BB9; padding:2px 6px; border-radius:4px;">{sha256}...</code></div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.info("Dataset information will be available after the dataset is loaded.")

    st.markdown("---")

    # 6. Research Components & Tech Stack
    col_c, col_t = st.columns(2)
    
    with col_c:
        st.markdown("<div class='section-header-title'>🔬 RESEARCH COMPONENTS</div>", unsafe_allow_html=True)
        st.markdown(f'''
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">Demand & Profit Prediction</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">Split Conformal Uncertainty</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">Multi-Factor Risk Engine</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">0-100 Business Scoring</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">Prescriptive Optimization</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">What-If Simulator</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">Baseline System Evaluation</span>
            <span style="background:rgba(197,139,185,0.12); color:#C58BB9; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(197,139,185,0.3);">Ablation Experiments (A - F)</span>
            <span style="background:rgba(79,197,138,0.12); color:#4FC58A; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid rgba(79,197,138,0.3);">Real-World Dataset Support</span>
        </div>
        ''', unsafe_allow_html=True)

    with col_t:
        st.markdown("<div class='section-header-title'>🛠️ TECHNOLOGY STACK</div>", unsafe_allow_html=True)
        st.markdown(f'''
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">Python 3.12</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">Pandas</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">NumPy</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">Scikit-learn</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">XGBoost</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">LightGBM</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">CatBoost</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">Streamlit</span>
            <span style="background:#1C1820; color:#F5F0F5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; border:1px solid #3A303B;">Plotly</span>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # 7. Research Note & Primary CTA Button
    st.caption("ℹ️ **Research Note**: Research-oriented system using reproducible machine-learning experiments, real-world data support, prediction uncertainty, prescriptive optimization, baseline comparison, and ablation analysis.")
    
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    
    btn_next = st.button("NEXT → EXPLORE BUSINESS DASHBOARD", use_container_width=True, type="primary")
    if btn_next:
        st.session_state["current_page"] = "dashboard"
        st.rerun()
