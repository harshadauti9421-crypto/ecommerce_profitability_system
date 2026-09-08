import streamlit as st
import plotly.graph_objects as go
from src.ui.theme import COLORS, DECISION_CONFIG

def render_top_header(dataset_name="Global Superstore 2016", num_records="51,290", sha256_hash="cfff9e65bb9e..."):
    """
    Render Clean Top Header for FinTech AI Business Dashboard.
    Left: Business Dashboard title & subtitle.
    Right: Notification icon, Settings icon, User profile, and Ask AI pill button.
    """
    st.markdown(f'''
    <div class="top-header-container">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
            <div>
                <h1 class="top-header-title">Business Dashboard</h1>
                <p class="top-header-subtitle">AI-powered profitability and business decision intelligence</p>
            </div>
            <div class="header-utilities">
                <div class="header-icon-btn" title="Notifications">🔔</div>
                <div class="header-icon-btn" title="Settings">⚙️</div>
                <div class="header-icon-btn" title="User Profile">👤</div>
                <div class="ask-ai-btn" title="Ask AI Decision Intelligence">
                    <span>✨</span> <b>Ask AI</b>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_kpi_summary_grid(profit_val, margin_val, risk_lvl, business_score, decision_str=""):
    """
    Renders Top 4–5 Dynamic KPI Summary Cards grid for FinTech AI Dashboard.
    Visual Hierarchy: Icon, uppercase label, large dynamic value, status indicator.
    """
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="card-label">💰 PREDICTED NET PROFIT</div>
            <div class="kpi-value" style="color:{COLORS['positive'] if profit_val >= 0 else COLORS['negative']};">
                ₹{profit_val:,.2f}
            </div>
            <div style="font-size:12px; color:{COLORS['positive'] if profit_val >= 0 else COLORS['negative']}; font-weight:600; margin-top:4px;">
                {"↑ Positive Net Return" if profit_val >= 0 else "↓ Downside Net Loss"}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    with k2:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="card-label">📈 PROFIT MARGIN</div>
            <div class="kpi-value" style="color:{COLORS['purple']};">
                {margin_val:.1f}%
            </div>
            <div style="font-size:12px; color:{COLORS['text_secondary']}; font-weight:600; margin-top:4px;">
                Pre-sale Margin Estimate
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with k3:
        risk_color = COLORS['positive'] if "Low" in risk_lvl else (COLORS['warning'] if "Moderate" in risk_lvl or "Medium" in risk_lvl else COLORS['negative'])
        st.markdown(f'''
        <div class="kpi-card">
            <div class="card-label">🛡️ RISK RATING</div>
            <div class="kpi-value" style="color:{risk_color};">
                {risk_lvl}
            </div>
            <div style="font-size:12px; color:{COLORS['text_secondary']}; font-weight:600; margin-top:4px;">
                Multi-Factor Risk Assessment
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with k4:
        score_color = COLORS['positive'] if business_score >= 80 else (COLORS['purple'] if business_score >= 65 else COLORS['warning'])
        st.markdown(f'''
        <div class="kpi-card">
            <div class="card-label">⭐ BUSINESS SCORE</div>
            <div class="kpi-value" style="color:{score_color};">
                {business_score} <span style="font-size:14px; color:{COLORS['text_secondary']};">/ 100</span>
            </div>
            <div style="font-size:12px; color:{COLORS['text_secondary']}; font-weight:600; margin-top:4px;">
                Commercial Potential Rating
            </div>
        </div>
        ''', unsafe_allow_html=True)

def render_hero_launch_card(decision_res, risk_res, profit_val=0.0, score_val=0):
    """
    Render Executive Hero Launch Decision Card (🟢 LAUNCH / 🟡 MODIFY / 🔴 DO NOT LAUNCH)
    along with Business Score, Risk, and Expected Profit in FinTech AI Theme.
    """
    decision = decision_res.get("decision", "🔴 DO NOT LAUNCH")
    config = DECISION_CONFIG.get(decision, DECISION_CONFIG["🔴 DO NOT LAUNCH"])
    
    border_col = config['border_color']
    bg_tint = config['bg_color']
    
    st.markdown(f'''
    <div style="background-color:{COLORS['card_bg']}; border:1px solid {border_col}; border-left:6px solid {border_col}; border-radius:16px; padding:24px 28px; margin-bottom:24px; box-shadow:0 4px 20px rgba(0,0,0,0.4);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
            <div>
                <span style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:{config['text_color']};">COMMERCIAL LAUNCH DECISION</span>
                <h2 style="font-size:30px; font-weight:800; margin:4px 0 0 0; color:{COLORS['text_primary']}; display:flex; align-items:center; gap:12px;">
                    <span>{config['icon']}</span> {decision.replace("🟢 ", "").replace("🟡 ", "").replace("🔴 ", "")}
                </h2>
            </div>
            <div style="display:flex; gap:16px; background-color:{COLORS['card_secondary']}; border:1px solid {COLORS['border']}; padding:12px 20px; border-radius:12px; text-align:center; box-shadow:0 4px 16px rgba(0,0,0,0.3);">
                <div>
                    <span style="font-size:11px; font-weight:600; color:{COLORS['text_secondary']};">EXPECTED PROFIT</span><br>
                    <span style="font-size:18px; font-weight:800; color:{COLORS['positive'] if profit_val >= 0 else COLORS['negative']};">₹{profit_val:,.2f}</span>
                </div>
                <div style="border-left:1px solid {COLORS['border']}; padding-left:16px;">
                    <span style="font-size:11px; font-weight:600; color:{COLORS['text_secondary']};">BUSINESS SCORE</span><br>
                    <span style="font-size:18px; font-weight:800; color:{COLORS['purple']};">{score_val} / 100</span>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_business_score_gauge(score_res):
    """Render Radial Business Score Gauge (0 - 100) for FinTech Theme Background."""
    score = score_res.get("score", 0)
    label = score_res.get("label", "Moderate")
    breakdown = score_res.get("breakdown", {})
    
    if score >= 80:
        score_color = COLORS["positive"]
    elif score >= 65:
        score_color = COLORS["purple"]
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
            'bgcolor': COLORS['card_bg'],
            'bordercolor': COLORS['border'],
            'steps': [
                {'range': [0, 50], 'color': COLORS['negative_bg']},
                {'range': [50, 65], 'color': COLORS['warning_bg']},
                {'range': [65, 80], 'color': COLORS['card_secondary']},
                {'range': [80, 100], 'color': COLORS['positive_bg']}
            ]
        }
    ))
    fig_gauge.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg']
    )
    
    return fig_gauge, breakdown

def render_recommendation_cards(recommendations):
    """Render Actionable AI Recommendation Cards grouped by category for FinTech Theme."""
    st.markdown("<div class='section-header-title'>💡 AI BUSINESS RECOMMENDATION</div>", unsafe_allow_html=True)
    
    for i, r in enumerate(recommendations):
        category = "PRICING & STRATEGY" if "price" in r.lower() or "discount" in r.lower() else ("OPERATIONS & FULFILLMENT" if "ship" in r.lower() or "cost" in r.lower() else "RISK MITIGATION")
        st.markdown(f'''
        <div class="recommendation-card">
            <div class="rec-category">RECOMMENDATION #{i+1} &nbsp;|&nbsp; {category}</div>
            <div class="rec-text" style="font-size:14px; font-weight:600; color:{COLORS['text_primary']}; margin-top:6px;">💡 {r}</div>
        </div>
        ''', unsafe_allow_html=True)


