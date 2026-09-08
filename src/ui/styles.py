import streamlit as st
from src.ui.theme import COLORS

def inject_custom_styles():
    """
    Injects Premium Dark Investment Dashboard CSS styles for Streamlit application.
    Almost-black canvas (#08070A) with dark purple radial glow, dark charcoal elevated cards (#151217),
    dark sidebar (#0D0B10), subtle purple-charcoal borders (#3A303B), crisp typography (#F5F0F5),
    soft lavender accents (#C58BB9), success profit green (#4FC58A), and loss red (#D96570).
    """
    css = f"""
    <style>
    /* Main Canvas Background (Almost-Black with Subtle Top Radial Glow) & Base Typography */
    .stApp {{
        background-color: {COLORS['background_main']} !important;
        background-image: radial-gradient(circle at 50% -10%, #1E1724 0%, #08070A 65%) !important;
        color: {COLORS['text_primary']} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}

    /* Global Headings & Markdown Text */
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, span, label {{
        color: {COLORS['text_primary']} !important;
    }}
    .stCaption, caption, small {{
        color: {COLORS['text_secondary']} !important;
    }}
    
    /* Sidebar Navigation Panel Styling (Dark Investment Theme) */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['sidebar_bg']} !important;
        border-right: 1px solid {COLORS['border']} !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4) !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS['text_primary']} !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 5px !important;
        color: {COLORS['text_secondary']} !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
        background-color: {COLORS['card_secondary']} !important;
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Top Enterprise Application Header Container */
    .top-header-container {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
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
        background-color: {COLORS['card_secondary']};
        color: {COLORS['primary']};
        border: 1px solid {COLORS['border']};
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
    }}

    /* Streamlit KPI Metric Cards Transformation */
    div[data-testid="stMetric"] {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 16px !important;
        padding: 18px 22px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
    }}
    div[data-testid="stMetric"] label {{
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: {COLORS['text_secondary']} !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        font-size: 26px !important;
        font-weight: 800 !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* Executive Hero Launch Decision Card */
    .hero-decision-card {{
        border-radius: 16px;
        padding: 26px 30px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        background-color: {COLORS['card_bg']};
    }}
    .hero-launch {{
        border: 1px solid {COLORS['positive']};
        border-left: 6px solid {COLORS['positive']};
        background: linear-gradient(135deg, {COLORS['positive_bg']} 0%, {COLORS['card_bg']} 100%);
    }}
    .hero-modify {{
        border: 1px solid {COLORS['warning']};
        border-left: 6px solid {COLORS['warning']};
        background: linear-gradient(135deg, {COLORS['warning_bg']} 0%, {COLORS['card_bg']} 100%);
    }}
    .hero-nolaunch {{
        border: 1px solid {COLORS['negative']};
        border-left: 6px solid {COLORS['negative']};
        background: linear-gradient(135deg, {COLORS['negative_bg']} 0%, {COLORS['card_bg']} 100%);
    }}
    
    /* Elevated Dark Charcoal Metric & Component Cards */
    .premium-card {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }}
    .card-label {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
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
        letter-spacing: 0.02em;
        color: {COLORS['text_primary']};
        border-bottom: 1px solid {COLORS['border']};
        padding-bottom: 10px;
        margin-top: 24px;
        margin-bottom: 20px;
    }}

    /* Recommendation Cards */
    .recommendation-card {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-left: 4px solid {COLORS['primary']};
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
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
        margin-top: 6px;
    }}

    /* Dark Input Controls (Text Inputs, Number Inputs, Selectboxes, Textareas) */
    input, textarea, select, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: {COLORS['input_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text_primary']} !important;
        border-radius: 10px !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: {COLORS['muted_purple']} !important;
    }}
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 12px rgba(197, 139, 185, 0.3) !important;
    }}
    div[data-baseweb="popover"], div[data-baseweb="menu"], div[role="listbox"] {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
    }}
    div[data-baseweb="option"] {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text_primary']} !important;
    }}
    div[data-baseweb="option"]:hover, div[data-baseweb="option"][aria-selected="true"] {{
        background-color: {COLORS['card_secondary']} !important;
        color: {COLORS['primary']} !important;
    }}

    /* Form Container Boxes */
    .input-group-box {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }}
    .input-group-header {{
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        color: {COLORS['primary']};
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }}
    
    /* Primary CTA Buttons (Lavender Pink Accent) */
    div.stButton > button[type="primary"] {{
        background-color: {COLORS['primary']} !important;
        border: 1px solid {COLORS['primary_hover']} !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        box-shadow: 0 0 16px rgba(197, 139, 185, 0.35) !important;
        transition: all 0.2s ease !important;
    }}
    div.stButton > button[type="primary"]:hover {{
        background-color: {COLORS['primary_hover']} !important;
        box-shadow: 0 0 22px rgba(215, 166, 202, 0.5) !important;
        transform: translateY(-1px) !important;
        color: #FFFFFF !important;
    }}

    /* Secondary Buttons & Top Nav Buttons */
    div.stButton > button:not([type="primary"]) {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text_secondary']} !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
    }}
    div.stButton > button:not([type="primary"]):hover {{
        border-color: {COLORS['muted_purple']} !important;
        color: {COLORS['text_primary']} !important;
        background-color: {COLORS['card_secondary']} !important;
    }}

    /* Streamlit Tabs Styling */
    div[data-baseweb="tab-list"] {{
        background-color: transparent !important;
        gap: 8px !important;
    }}
    div[data-baseweb="tab"] {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: {COLORS['text_secondary']} !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="tab"][aria-selected="true"] {{
        border-color: {COLORS['primary']} !important;
        color: #FFFFFF !important;
        background-color: {COLORS['primary']} !important;
        box-shadow: 0 0 14px rgba(197, 139, 185, 0.35) !important;
    }}

    /* Expanders & DataFrames */
    div[data-testid="stExpander"] {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 14px !important;
    }}
    div[data-testid="stExpander"] details summary {{
        color: {COLORS['text_primary']} !important;
        background-color: {COLORS['card_bg']} !important;
    }}
    div[data-testid="stDataFrame"], .stDataFrame {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
    }}

    /* Top Navigation Bar Container */
    .top-nav-bar-container {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        padding: 10px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }}

    /* Hide Streamlit default branding footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

