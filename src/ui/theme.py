"""
Centralized Theme & Semantic Color System
Premium FinTech AI Business Dashboard Palette
"""

COLORS = {
    "primary": "#B56CFF",         # Primary Accent Purple
    "primary_hover": "#D7A8FF",   # Accent Hover Light Purple
    "primary_gradient": "linear-gradient(135deg, #B56CFF 0%, #E8A5D8 100%)", # Purple/Pink Gradient
    "purple": "#B56CFF",          # Core Purple
    "purple_light": "#D7A8FF",    # Light Purple
    "pink_accent": "#E8A5D8",     # Soft Pink Accent
    "background_main": "#08070B", # Deep Canvas Background
    "background_alt": "#0D0B12",  # Alternate Canvas Tint
    "sidebar_bg": "#0A090D",      # Deep Sidebar Background
    "card_bg": "#141119",         # Elevated Charcoal Card Surface
    "card_secondary": "#1B1721",  # Secondary Card Surface
    "input_bg": "#141119",        # Input Field Background
    "border": "#2D2736",          # Subtle Border
    "border_glow": "rgba(181, 108, 255, 0.35)", # Subtle Purple Border Glow
    "text_primary": "#F7F4F8",    # Crisp White / Off-White Typography
    "text_secondary": "#A9A2AF",  # Muted Secondary Gray-Purple Text
    "text_muted": "#7E7785",      # Muted Caption Text
    "positive": "#35D49A",        # Success / Profit Green
    "positive_bg": "#0C2B1F",     # Dark Green Surface Tint
    "warning": "#F4C95D",         # Warm Gold / Warning
    "warning_bg": "#2A2210",      # Dark Gold Surface Tint
    "negative": "#FF5C70",        # Loss / Negative Red
    "negative_bg": "#2B1116",     # Dark Red Surface Tint
    "neutral": "#7E7785"          # Slate Neutral
}

DECISION_CONFIG = {
    "🟢 LAUNCH": {
        "badge_class": "badge-launch",
        "bg_color": "#0C2B1F",
        "border_color": "#35D49A",
        "text_color": "#35D49A",
        "icon": "🟢",
        "label": "COMMERCIAL LAUNCH APPROVED"
    },
    "🟡 LAUNCH WITH MODIFICATIONS": {
        "badge_class": "badge-modify",
        "bg_color": "#2A2210",
        "border_color": "#F4C95D",
        "text_color": "#F4C95D",
        "icon": "🟡",
        "label": "MODIFY COMMERCIAL STRATEGY"
    },
    "🔴 DO NOT LAUNCH": {
        "badge_class": "badge-nolaunch",
        "bg_color": "#2B1116",
        "border_color": "#FF5C70",
        "text_color": "#FF5C70",
        "icon": "🔴",
        "label": "DO NOT LAUNCH"
    }
}

