import streamlit as st
from src.ui.theme import COLORS

def inject_custom_styles():
    """
    Injects Premium FinTech AI Business Dashboard CSS styles for Streamlit application.
    Deep canvas (#08070B) with purple radial glow, elevated charcoal cards (#141119),
    deep sidebar (#0A090D), purple/pink gradient pill active nav (#B56CFF -> #E8A5D8),
    white typography (#F7F4F8), success profit green (#35D49A), and loss red (#FF5C70).
    """
    css = f"""
    <style>
    /* Main Canvas Background & Typography */
    .stApp {{
        background-color: {COLORS['background_main']} !important;
        background-image: radial-gradient(circle at 50% -10%, #1E1230 0%, #08070B 75%) !important;
        color: {COLORS['text_primary']} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}

    /* Global Headings & Text */
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, span, label {{
        color: {COLORS['text_primary']} !important;
    }}
    .stCaption, caption, small {{
        color: {COLORS['text_secondary']} !important;
    }}

    /* Premium Fixed Left Sidebar Panel */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['sidebar_bg']} !important;
        border-right: 1px solid {COLORS['border']} !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5) !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Sidebar Navigation Items (Purple/Pink Gradient Active Pill) */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 12px !important;
        padding: 11px 16px !important;
        margin-bottom: 6px !important;
        color: {COLORS['text_secondary']} !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease-in-out !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
        background-color: {COLORS['card_secondary']} !important;
        color: {COLORS['text_primary']} !important;
        border-color: {COLORS['border_glow']} !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] {{
        background: linear-gradient(135deg, {COLORS['purple']} 0%, {COLORS['pink_accent']} 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 16px rgba(181, 108, 255, 0.4) !important;
        font-weight: 700 !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] span {{
        color: #FFFFFF !important;
    }}

    /* Top Dashboard Header Container */
    .top-header-container {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
    }}
    .top-header-title {{
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: {COLORS['text_primary']};
        margin: 0 0 4px 0;
    }}
    .top-header-subtitle {{
        font-size: 14px;
        color: {COLORS['text_secondary']};
        margin: 0;
    }}

    /* Header Utility Bar (Icons & Ask AI Pill) */
    .header-utilities {{
        display: flex;
        align-items: center;
        gap: 12px;
        justify-content: flex-end;
    }}
    .header-icon-btn {{
        background-color: {COLORS['card_secondary']};
        border: 1px solid {COLORS['border']};
        color: {COLORS['text_primary']};
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    .header-icon-btn:hover {{
        border-color: {COLORS['purple']};
        box-shadow: 0 0 12px {COLORS['border_glow']};
    }}
    .ask-ai-btn {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['purple']};
        color: {COLORS['text_primary']};
        padding: 8px 18px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 0 14px rgba(181, 108, 255, 0.3);
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    .ask-ai-btn:hover {{
        box-shadow: 0 0 20px rgba(181, 108, 255, 0.5);
        transform: translateY(-1px);
    }}

    /* Dynamic KPI Summary Cards */
    div[data-testid="stMetric"], .kpi-card {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    div[data-testid="stMetric"]:hover, .kpi-card:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(181, 108, 255, 0.2) !important;
        border-color: {COLORS['border_glow']} !important;
    }}
    div[data-testid="stMetric"] label, .kpi-label {{
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: {COLORS['text_secondary']} !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"], .kpi-value {{
        font-size: 26px !important;
        font-weight: 800 !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* Elevated Dark Charcoal Cards */
    .premium-card {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .premium-card:hover {{
        border-color: {COLORS['border_glow']};
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
        border-left: 4px solid {COLORS['purple']};
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }}
    .rec-category {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: {COLORS['purple']};
        letter-spacing: 0.08em;
    }}

    /* Dark Input Controls */
    input, textarea, select, div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text_primary']} !important;
        border-radius: 10px !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: {COLORS['text_muted']} !important;
    }}
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {{
        border-color: {COLORS['purple']} !important;
        box-shadow: 0 0 14px {COLORS['border_glow']} !important;
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
        color: {COLORS['purple']} !important;
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
        color: {COLORS['purple']};
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }}

    /* Primary CTA Buttons (Purple/Pink Gradient Accent) */
    div.stButton > button[type="primary"] {{
        background: linear-gradient(135deg, {COLORS['purple']} 0%, {COLORS['pink_accent']} 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 18px rgba(181, 108, 255, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }}
    div.stButton > button[type="primary"]:hover {{
        box-shadow: 0 6px 24px rgba(181, 108, 255, 0.6) !important;
        transform: translateY(-1px) !important;
        color: #FFFFFF !important;
    }}

    /* Secondary Buttons */
    div.stButton > button:not([type="primary"]) {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid rgba(181, 108, 255, 0.4) !important;
        color: {COLORS['text_primary']} !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.2s ease !important;
    }}
    div.stButton > button:not([type="primary"]):hover {{
        border-color: {COLORS['purple']} !important;
        color: {COLORS['purple_light']} !important;
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
        border-color: {COLORS['purple']} !important;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, {COLORS['purple']} 0%, {COLORS['pink_accent']} 100%) !important;
        box-shadow: 0 4px 16px rgba(181, 108, 255, 0.35) !important;
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
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }}

    /* Hide Streamlit default branding footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


