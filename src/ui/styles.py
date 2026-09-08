import streamlit as st
from src.ui.theme import COLORS

def inject_custom_styles():
    """
    Injects Sky Blue Enterprise SaaS CSS styles for Streamlit application.
    Soft Sky Blue main canvas (#F0F9FF), pure white elevated cards (#FFFFFF),
    sky blue sidebar (#E0F2FE), subtle sky borders (#BAE6FD), dark navy typography (#0F172A),
    and sky blue primary accents (#0284C7).
    """
    css = f"""
    <style>
    /* Main Canvas Background (Soft Sky Blue) & Base Typography */
    .stApp {{
        background-color: #F0F9FF !important;
        color: {COLORS['text_primary']} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}
    
    /* Sidebar Navigation Panel Styling (Sky Blue Tint) */
    section[data-testid="stSidebar"] {{
        background-color: #E0F2FE !important;
        border-right: 1px solid #BAE6FD !important;
        box-shadow: 2px 0 12px rgba(2, 132, 199, 0.05) !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS['text_primary']} !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {{
        background-color: #E0F2FE !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 4px !important;
        color: #0369A1 !important;
        font-weight: 600 !important;
        transition: all 0.15s ease !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
        background-color: #BAE6FD !important;
        color: #0284C7 !important;
    }}

    /* Top Enterprise Application Header */
    .top-header-container {{
        background-color: #FFFFFF;
        border: 1px solid #BAE6FD;
        border-radius: 12px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.06);
    }}
    .top-header-title {{
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: {COLORS['text_primary']};
        margin: 0 0 6px 0;
    }}
    .top-header-subtitle {{
        font-size: 14px;
        color: {COLORS['text_secondary']};
        margin: 0;
    }}
    .status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #E0F2FE;
        color: #0284C7;
        border: 1px solid #BAE6FD;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
    }}

    /* Streamlit KPI Metric Cards Transformation */
    div[data-testid="stMetric"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #BAE6FD !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.05) !important;
    }}
    div[data-testid="stMetric"] label {{
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: {COLORS['text_secondary']} !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        font-size: 24px !important;
        font-weight: 800 !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* Executive Hero Launch Decision Card */
    .hero-decision-card {{
        border-radius: 14px;
        padding: 26px 30px;
        margin-bottom: 24px;
        border-left: 6px solid;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.06);
        background-color: #FFFFFF;
    }}
    .hero-launch {{
        border-left-color: {COLORS['positive']};
        border: 1px solid #BAE6FD;
        border-left: 6px solid {COLORS['positive']};
        background: linear-gradient(135deg, {COLORS['positive_bg']} 0%, #FFFFFF 100%);
    }}
    .hero-modify {{
        border-left-color: {COLORS['warning']};
        border: 1px solid #BAE6FD;
        border-left: 6px solid {COLORS['warning']};
        background: linear-gradient(135deg, {COLORS['warning_bg']} 0%, #FFFFFF 100%);
    }}
    .hero-nolaunch {{
        border-left-color: {COLORS['negative']};
        border: 1px solid #BAE6FD;
        border-left: 6px solid {COLORS['negative']};
        background: linear-gradient(135deg, {COLORS['negative_bg']} 0%, #FFFFFF 100%);
    }}
    
    /* Elevated White Metric & Component Cards */
    .premium-card {{
        background-color: #FFFFFF;
        border: 1px solid #BAE6FD;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.05);
    }}
    .card-label {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {COLORS['text_secondary']};
        margin-bottom: 8px;
    }}
    .card-value {{
        font-size: 26px;
        font-weight: 800;
        color: {COLORS['text_primary']};
    }}
    .card-subtext {{
        font-size: 12px;
        color: {COLORS['text_muted']};
        margin-top: 6px;
    }}

    /* Section Header Titles */
    .section-header-title {{
        font-size: 17px;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: {COLORS['text_primary']};
        border-bottom: 2px solid #BAE6FD;
        padding-bottom: 8px;
        margin-top: 22px;
        margin-bottom: 18px;
    }}

    /* Recommendation Cards */
    .recommendation-card {{
        background-color: #FFFFFF;
        border: 1px solid #BAE6FD;
        border-left: 4px solid {COLORS['primary']};
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.04);
    }}
    .rec-category {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: {COLORS['primary']};
        letter-spacing: 0.08em;
    }}
    .rec-text {{
        font-size: 14px;
        font-weight: 600;
        color: {COLORS['text_primary']};
        margin-top: 4px;
    }}
    
    /* Primary CTA Button (Sky Blue Accent) */
    div.stButton > button[type="primary"] {{
        background-color: #0284C7 !important;
        border: 1px solid #0369A1 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3) !important;
        transition: all 0.2s ease !important;
    }}
    div.stButton > button[type="primary"]:hover {{
        background-color: #0369A1 !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.45) !important;
        transform: translateY(-1px) !important;
    }}

    /* Secondary Buttons */
    div.stButton > button:not([type="primary"]) {{
        background-color: #FFFFFF !important;
        border: 1px solid #BAE6FD !important;
        color: {COLORS['text_primary']} !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(2, 132, 199, 0.03) !important;
    }}
    div.stButton > button:not([type="primary"]):hover {{
        border-color: #0284C7 !important;
        color: #0284C7 !important;
        background-color: #E0F2FE !important;
    }}

    /* Streamlit Tabs Styling */
    div[data-baseweb="tab-list"] {{
        gap: 8px !important;
    }}
    div[data-baseweb="tab"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #BAE6FD !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        color: #0369A1 !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="tab"][aria-selected="true"] {{
        border-color: #0284C7 !important;
        color: #0284C7 !important;
        background-color: #E0F2FE !important;
    }}

    /* Hide Streamlit default branding footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
