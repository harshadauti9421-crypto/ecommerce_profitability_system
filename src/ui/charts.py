"""
Interactive Light White Enterprise Plotly Chart Engine
"""

import plotly.express as px
import plotly.graph_objects as go
from src.ui.theme import COLORS

def build_conformal_interval_chart(point_val, lower_val, upper_val, title="90% Conformal Profit Interval ($)"):
    """
    Builds an interactive Plotly range/dumbbell chart displaying Lower Bound, Point Estimate, and Upper Bound.
    """
    fig = go.Figure()

    # Horizontal Connecting Range Line
    fig.add_trace(go.Scatter(
        x=[lower_val, upper_val],
        y=["Expected Profit", "Expected Profit"],
        mode="lines",
        line=dict(color=COLORS["primary"], width=6),
        name="90% Prediction Interval",
        hoverinfo="skip"
    ))

    # Lower Bound Marker
    fig.add_trace(go.Scatter(
        x=[lower_val],
        y=["Expected Profit"],
        mode="markers+text",
        marker=dict(color=COLORS["warning"], size=16, symbol="line-ns-open", line=dict(width=3)),
        text=[f"Lower: ${lower_val:,.2f}"],
        textposition="bottom center",
        name="90% Lower Bound",
        hovertemplate="<b>90% Lower Bound</b>: $%{x:,.2f}<extra></extra>"
    ))

    # Point Estimate Marker
    fig.add_trace(go.Scatter(
        x=[point_val],
        y=["Expected Profit"],
        mode="markers+text",
        marker=dict(color=COLORS["positive"], size=18, symbol="diamond"),
        text=[f"Point Estimate: ${point_val:,.2f}"],
        textposition="top center",
        name="Point Estimate",
        hovertemplate="<b>Point Estimate (ML Winner)</b>: $%{x:,.2f}<extra></extra>"
    ))

    # Upper Bound Marker
    fig.add_trace(go.Scatter(
        x=[upper_val],
        y=["Expected Profit"],
        mode="markers+text",
        marker=dict(color=COLORS["primary"], size=16, symbol="line-ns-open", line=dict(width=3)),
        text=[f"Upper: ${upper_val:,.2f}"],
        textposition="bottom center",
        name="90% Upper Bound",
        hovertemplate="<b>90% Upper Bound</b>: $%{x:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(color=COLORS["text_primary"], size=16, weight="bold")),
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["card_bg"],
        height=200,
        margin=dict(l=30, r=30, t=50, b=30),
        xaxis=dict(
            title=dict(text="Net Profit ($)", font=dict(color=COLORS["text_secondary"])),
            tickfont=dict(color=COLORS["text_secondary"]),
            gridcolor="#F1F5F9",
            zerolinecolor=COLORS["border"]
        ),
        yaxis=dict(
            tickfont=dict(color=COLORS["text_primary"], size=13, weight="bold"),
            gridcolor="#F1F5F9"
        ),
        showlegend=False
    )
    return fig

def build_waterfall_chart(gross_rev, discount_val, net_rev, total_cogs, total_ship, net_profit):
    """Financial P&L Waterfall Chart with White Enterprise Theme."""
    fig = go.Figure(go.Waterfall(
        name="P&L",
        orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "total"],
        x=["Gross Revenue", "Discounts (-)", "Net Revenue", "COGS (-)", "Shipping Costs (-)", "Net Profit (=)"],
        textposition="outside",
        text=[f"${gross_rev:,.2f}", f"-${discount_val:,.2f}", f"${net_rev:,.2f}", f"-${total_cogs:,.2f}", f"-${total_ship:,.2f}", f"${net_profit:,.2f}"],
        y=[gross_rev, -discount_val, 0, -total_cogs, -total_ship, 0],
        connector={"line": {"color": COLORS["border"]}},
        decreasing={"marker": {"color": COLORS["negative"]}},
        increasing={"marker": {"color": COLORS["positive"]}},
        totals={"marker": {"color": COLORS["primary"]}}
    ))
    fig.update_layout(
        title=dict(text="Financial Waterfall Breakdown ($)", font=dict(color=COLORS["text_primary"], size=16, weight="bold")),
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["card_bg"],
        font=dict(color=COLORS["text_primary"]),
        height=420,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(gridcolor="#F1F5F9", tickfont=dict(color=COLORS["text_secondary"])),
        yaxis=dict(gridcolor="#F1F5F9", tickfont=dict(color=COLORS["text_secondary"]))
    )
    return fig

def build_price_elasticity_chart(df_sens, col_sp, col_profit, opt_sp, opt_profit, *args, **kwargs):
    """Price Sensitivity & Profit Curve Chart with White Enterprise Theme."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sens[col_sp], y=df_sens[col_profit],
        name="Predicted Net Profit (₹)",
        line=dict(color=COLORS["positive"], width=3),
        mode="lines+markers"
    ))
    if "Profit Margin (%)" in df_sens.columns:
        fig.add_trace(go.Scatter(
            x=df_sens[col_sp], y=df_sens["Profit Margin (%)"],
            name="Profit Margin (%)",
            line=dict(color=COLORS["primary"], width=3, dash="dash"),
            mode="lines+markers",
            yaxis="y2"
        ))
    fig.add_trace(go.Scatter(
        x=[opt_sp], y=[opt_profit],
        name="Optimal Price Marker",
        marker=dict(size=14, color=COLORS["warning"], symbol="star"),
        mode="markers"
    ))
    fig.update_layout(
        title=dict(text="Interactive Price Sensitivity & Net Profit Curve", font=dict(color=COLORS["text_primary"], size=16, weight="bold")),
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["card_bg"],
        font=dict(color=COLORS["text_primary"]),
        xaxis=dict(title=dict(text="Selling Price (₹)", font=dict(color=COLORS["text_secondary"])), gridcolor="#F1F5F9", tickfont=dict(color=COLORS["text_secondary"])),
        yaxis=dict(title=dict(text="Predicted Profit (₹)", font=dict(color=COLORS["positive"])), gridcolor="#F1F5F9", tickfont=dict(color=COLORS["positive"])),
        yaxis2=dict(title=dict(text="Profit Margin (%)", font=dict(color=COLORS["primary"])), tickfont=dict(color=COLORS["primary"]), overlaying="y", side="right"),
        height=460,
        hovermode="x unified"
    )
    return fig


def build_model_performance_chart(df_models):
    """6 ML Model Test R² Comparison Chart with White Enterprise Theme."""
    x_col = "Model" if "Model" in df_models.columns else ("Model Name" if "Model Name" in df_models.columns else df_models.columns[0])
    fig = px.bar(
        df_models, x=x_col, y="Test R²", color="Status",
        title="6 ML Models Test R² Evaluation Comparison",
        color_discrete_map={"🏆 Best Model": COLORS["positive"], "Evaluated": COLORS["primary"]}
    )
    fig.update_layout(
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["card_bg"],
        font=dict(color=COLORS["text_primary"]),
        xaxis=dict(gridcolor="#F1F5F9", tickfont=dict(color=COLORS["text_secondary"])),
        yaxis=dict(gridcolor="#F1F5F9", tickfont=dict(color=COLORS["text_secondary"])),
        height=380
    )
    return fig
