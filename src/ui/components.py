import streamlit as st
import plotly.graph_objects as go
from src.ui.theme import COLORS, DECISION_CONFIG

def render_top_header(dataset_name="Global Superstore 2016", num_records="51,290", sha256_hash="cfff9e65bb9e..."):
    """Render Modern Enterprise SaaS top header banner with live dataset status badge."""
    st.markdown(f'''
    <div class="top-header-container">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
            <div>
                <h1 class="top-header-title">AI E-COMMERCE PROFITABILITY INTELLIGENCE</h1>
                <p class="top-header-subtitle">AI-powered product profitability & business decision intelligence</p>
                <div class="status-pill">
                    <span>●</span> REAL-WORLD DATA &nbsp;|&nbsp; {dataset_name} ({num_records} transaction records)
                </div>
            </div>
            <div style="text-align:right;">
                <span style="font-size:11px; color:#64748B; font-weight:600;">DATASET SHA-256</span><br>
                <code style="font-size:11px; background:#F8FAFC; padding:3px 8px; border-radius:6px; border:1px solid #E2E8F0; color:#2563EB; font-weight:700;">{sha256_hash[:16]}...</code>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_hero_launch_card(decision_res, risk_res, profit_val=0.0, score_val=0):
    """
    Render Executive Hero Launch Decision Card (🟢 LAUNCH / 🟡 MODIFY / 🔴 DO NOT LAUNCH)
    along with Business Score, Risk, and Expected Profit.
    """
    decision = decision_res.get("decision", "🔴 DO NOT LAUNCH")
    config = DECISION_CONFIG.get(decision, DECISION_CONFIG["🔴 DO NOT LAUNCH"])
    
    card_class = "hero-launch" if "🟢" in decision else ("hero-modify" if "🟡" in decision else "hero-nolaunch")
    
    st.markdown(f'''
    <div class="hero-decision-card {card_class}">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px; margin-bottom:0;">
            <div>
                <span style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:{config['text_color']};">COMMERCIAL LAUNCH RECOMMENDATION</span>
                <h2 style="font-size:30px; font-weight:800; margin:4px 0 0 0; color:{COLORS['text_primary']}; display:flex; align-items:center; gap:12px;">
                    <span>{config['icon']}</span> {decision.replace("🟢 ", "").replace("🟡 ", "").replace("🔴 ", "")}
                </h2>
            </div>
            <div style="display:flex; gap:16px; background-color:#FFFFFF; border:1px solid {config['border_color']}; padding:12px 20px; border-radius:10px; text-align:center; box-shadow:0 2px 8px rgba(15,23,42,0.03);">
                <div>
                    <span style="font-size:11px; font-weight:600; color:{COLORS['text_secondary']};">EXPECTED PROFIT</span><br>
                    <span style="font-size:18px; font-weight:800; color:{COLORS['positive']};">${profit_val:,.2f}</span>
                </div>
                <div style="border-left:1px solid #E2E8F0; padding-left:16px;">
                    <span style="font-size:11px; font-weight:600; color:{COLORS['text_secondary']};">BUSINESS SCORE</span><br>
                    <span style="font-size:18px; font-weight:800; color:{COLORS['primary']};">{score_val} / 100</span>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_business_score_gauge(score_res):
    """Render Radial Business Score Gauge (0 - 100) for Light White Enterprise Background."""
    score = score_res.get("score", 0)
    label = score_res.get("label", "Moderate")
    breakdown = score_res.get("breakdown", {})
    
    if score >= 80:
        score_color = COLORS["positive"]
    elif score >= 65:
        score_color = COLORS["primary"]
    elif score >= 50:
        score_color = COLORS["warning"]
    else:
        score_color = COLORS["negative"]
        
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Business Score ({label})", 'font': {'size': 15, 'color': COLORS['text_primary'], 'weight': 'bold'}},
        number={'suffix': "/100", 'font': {'size': 26, 'color': score_color, 'weight': 'bold'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': COLORS['border']},
            'bar': {'color': score_color, 'thickness': 0.3},
            'bgcolor': "#FFFFFF",
            'bordercolor': COLORS['border'],
            'steps': [
                {'range': [0, 50], 'color': '#FEF2F2'},
                {'range': [50, 65], 'color': '#FFFBEB'},
                {'range': [65, 80], 'color': '#EFF6FF'},
                {'range': [80, 100], 'color': '#ECFDF5'}
            ]
        }
    ))
    fig_gauge.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )
    
    return fig_gauge, breakdown

def render_recommendation_cards(recommendations):
    """Render Actionable AI Recommendation Cards grouped by category for Light Enterprise Theme."""
    st.markdown("<div class='section-header-title'>💡 AI BUSINESS ACTION PLAN</div>", unsafe_allow_html=True)
    
    for i, r in enumerate(recommendations):
        category = "PRICING & STRATEGY" if "price" in r.lower() or "discount" in r.lower() else ("OPERATIONS & FULFILLMENT" if "ship" in r.lower() or "cost" in r.lower() else "RISK MITIGATION")
        st.markdown(f'''
        <div class="recommendation-card">
            <div class="rec-category">RECOMMENDATION #{i+1} &nbsp;|&nbsp; {category}</div>
            <div class="rec-text">💡 {r}</div>
        </div>
        ''', unsafe_allow_html=True)
