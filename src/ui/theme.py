"""
Centralized Theme & Semantic Color System
Sky Blue Enterprise AI Business Intelligence Palette
"""

COLORS = {
    "primary": "#0284C7",        # Sky Blue Primary Accent (Sky 600)
    "primary_dark": "#0369A1",   # Deep Sky Blue (Sky 700)
    "primary_light": "#E0F2FE",  # Soft Sky Blue Tint (Sky 100)
    "background_light": "#F0F9FF",# Soft Sky Blue Main Canvas Background (Sky 50)
    "card_bg": "#FFFFFF",        # Pure White Elevated Card Surface
    "sidebar_bg": "#E0F2FE",     # Light Sky Blue Sidebar (Sky 100)
    "border": "#BAE6FD",         # Subtle Sky Slate Border (Sky 200)
    "text_primary": "#0F172A",   # Deep Slate 900 / Dark Navy
    "text_secondary": "#0369A1", # Muted Sky Navy
    "text_muted": "#64748B",     # Dimmed Slate 400
    "positive": "#10B981",       # Emerald Green
    "positive_bg": "#ECFDF5",    # Soft Green Tint
    "warning": "#F59E0B",        # Amber Gold
    "warning_bg": "#FFFBEB",    # Soft Amber Tint
    "negative": "#EF4444",       # Rose Red
    "negative_bg": "#FEF2F2",    # Soft Red Tint
    "neutral": "#64748B"         # Slate 500
}

DECISION_CONFIG = {
    "🟢 LAUNCH": {
        "badge_class": "badge-launch",
        "bg_color": "#ECFDF5",
        "border_color": "#10B981",
        "text_color": "#047857",
        "icon": "🟢",
        "label": "COMMERCIAL LAUNCH APPROVED"
    },
    "🟡 LAUNCH WITH MODIFICATIONS": {
        "badge_class": "badge-modify",
        "bg_color": "#FFFBEB",
        "border_color": "#F59E0B",
        "text_color": "#B45309",
        "icon": "🟡",
        "label": "MODIFY COMMERCIAL STRATEGY"
    },
    "🔴 DO NOT LAUNCH": {
        "badge_class": "badge-nolaunch",
        "bg_color": "#FEF2F2",
        "border_color": "#EF4444",
        "text_color": "#B91C1C",
        "icon": "🔴",
        "label": "DO NOT LAUNCH"
    }
}
