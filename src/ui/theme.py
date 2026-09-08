"""
Centralized Theme & Semantic Color System
Premium Dark Investment Dashboard Palette
"""

COLORS = {
    "primary": "#C58BB9",        # Soft Lavender / Pink Primary Accent
    "primary_hover": "#D7A6CA",  # Accent Hover
    "primary_dark": "#9A658E",   # Deep Lavender
    "primary_light": "#1C1820",  # Secondary Card Tint
    "background_main": "#08070A",# Primary Background (Almost-Black)
    "sidebar_bg": "#0D0B10",     # Dark Sidebar
    "card_bg": "#151217",        # Dark Charcoal Card Surface
    "card_secondary": "#1C1820",   # Secondary Card Surface
    "input_bg": "#100E13",       # Input Field Background
    "border": "#3A303B",         # Subtle Charcoal/Lavender Border
    "muted_purple": "#806A7D",   # Muted Purple Accent
    "text_primary": "#F5F0F5",   # Crisp Light Typography
    "text_secondary": "#A9A1AA", # Muted Gray-Purple Secondary Text
    "text_muted": "#806A7D",     # Muted Text
    "positive": "#4FC58A",       # Success / Profit Green
    "positive_bg": "#0E2419",    # Dark Green Tint
    "warning": "#D6B36A",        # Warm Gold / Warning
    "warning_bg": "#241D0E",     # Dark Gold Tint
    "negative": "#D96570",       # Loss / Negative Red
    "negative_bg": "#261114",    # Dark Red Tint
    "neutral": "#806A7D"         # Neutral Purple Slate
}

DECISION_CONFIG = {
    "🟢 LAUNCH": {
        "badge_class": "badge-launch",
        "bg_color": "#0E2419",
        "border_color": "#4FC58A",
        "text_color": "#4FC58A",
        "icon": "🟢",
        "label": "COMMERCIAL LAUNCH APPROVED"
    },
    "🟡 LAUNCH WITH MODIFICATIONS": {
        "badge_class": "badge-modify",
        "bg_color": "#241D0E",
        "border_color": "#D6B36A",
        "text_color": "#D6B36A",
        "icon": "🟡",
        "label": "MODIFY COMMERCIAL STRATEGY"
    },
    "🔴 DO NOT LAUNCH": {
        "badge_class": "badge-nolaunch",
        "bg_color": "#261114",
        "border_color": "#D96570",
        "text_color": "#D96570",
        "icon": "🔴",
        "label": "DO NOT LAUNCH"
    }
}

