"""Reusable UI fragments and chart helpers."""

from __future__ import annotations

from typing import Any

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from finwise.config import (
    CATEGORY_ICONS,
    COLORS,
    EDUCATIONAL_DISCLAIMER,
    EXPENSE_CATEGORIES,
    health_band_label,
)
from finwise.utils import format_money


def page_header(title: str, subtitle: str = "") -> None:
    st.markdown(f'<h1 class="fw-page-title">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="fw-page-sub">{subtitle}</p>', unsafe_allow_html=True)


def disclaimer_banner() -> None:
    st.markdown(
        f'<div class="fw-disclaimer">{EDUCATIONAL_DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


def empty_state(title: str, body: str) -> None:
    st.markdown(
        f'<div class="fw-empty"><h3>{title}</h3><p>{body}</p></div>',
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, icon: str, delta: str = "", tone: str = "neu") -> None:
    st.markdown(
        f"""
        <div class="fw-kpi">
          <div class="kpi-top">
            <div class="kpi-label">{label}</div>
            <div class="kpi-icon">{icon}</div>
          </div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {tone}">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(risk: str) -> None:
    level = (risk or "MEDIUM").upper()
    st.markdown(
        f'<span class="fw-risk-{level}" style="font-size:1.35rem;">{level}</span>',
        unsafe_allow_html=True,
    )


def score_band_caption(score: int) -> str:
    return f"{score}/100 — {health_band_label(score)}"


def _chart_layout(fig, height: int = 320):
    fig.update_layout(
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=COLORS["text"],
        font_family="DM Sans",
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def expense_pie(results: dict[str, Any]):
    labels = {k: label for k, label in EXPENSE_CATEGORIES}
    rows = [
        {"Category": labels.get(k, k), "Amount": v}
        for k, v in (results.get("expense_breakdown") or {}).items()
        if v > 0
    ]
    if not rows:
        return None
    fig = px.pie(
        rows,
        names="Category",
        values="Amount",
        hole=0.55,
        color_discrete_sequence=[
            COLORS["navy"],
            COLORS["emerald"],
            COLORS["cyan"],
            COLORS["accent"],
            COLORS["warm"],
            "#0EA5E9",
            "#8B5CF6",
            "#14B8A6",
            "#64748B",
        ],
    )
    return _chart_layout(fig, 340)


def income_vs_expense_chart(results: dict[str, Any]):
    symbol = results.get("symbol", "$")
    fig = go.Figure(
        data=[
            go.Bar(
                name="Income",
                x=["This month"],
                y=[results.get("monthly_income", 0)],
                marker_color=COLORS["emerald"],
                text=[format_money(results.get("monthly_income", 0), symbol)],
                textposition="auto",
            ),
            go.Bar(
                name="Expenses",
                x=["This month"],
                y=[results.get("total_expenses", 0)],
                marker_color=COLORS["negative"],
                text=[format_money(results.get("total_expenses", 0), symbol)],
                textposition="auto",
            ),
            go.Bar(
                name="Savings",
                x=["This month"],
                y=[results.get("savings", 0)],
                marker_color=COLORS["cyan"],
                text=[format_money(results.get("savings", 0), symbol)],
                textposition="auto",
            ),
        ]
    )
    fig.update_layout(barmode="group", yaxis_title=f"Amount ({symbol})")
    return _chart_layout(fig, 320)


def cashflow_gauge(results: dict[str, Any]):
    util = min(100.0, float(results.get("budget_utilization") or results.get("expense_ratio") or 0))
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=util,
            number={"suffix": "%"},
            title={"text": "Budget utilization"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": COLORS["emerald"]},
                "steps": [
                    {"range": [0, 60], "color": COLORS["mint"]},
                    {"range": [60, 85], "color": "#FEF3C7"},
                    {"range": [85, 100], "color": "#FEE2E2"},
                ],
                "threshold": {
                    "line": {"color": COLORS["negative"], "width": 3},
                    "value": 90,
                },
            },
        )
    )
    return _chart_layout(fig, 280)


def category_bars(results: dict[str, Any]):
    labels = {k: label for k, label in EXPENSE_CATEGORIES}
    rows = [
        {"Category": labels.get(k, k), "Amount": v}
        for k, v in (results.get("expense_breakdown") or {}).items()
        if v > 0
    ]
    if not rows:
        return None
    fig = px.bar(
        rows,
        x="Amount",
        y="Category",
        orientation="h",
        color="Amount",
        color_continuous_scale=["#D1FAE5", COLORS["emerald"], COLORS["navy"]],
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="")
    return _chart_layout(fig, 360)


def health_score_ring(score: int, title: str = "Health score"):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": COLORS["navy"]},
                "steps": [
                    {"range": [0, 40], "color": "#FEE2E2"},
                    {"range": [40, 60], "color": "#FEF3C7"},
                    {"range": [60, 80], "color": "#D1FAE5"},
                    {"range": [80, 100], "color": "#A7F3D0"},
                ],
            },
        )
    )
    return _chart_layout(fig, 280)


def overview_metrics(results: dict[str, Any]) -> None:
    sym = results.get("symbol", "$")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card(
            "Total Income",
            format_money(results["monthly_income"], sym),
            "💰",
            "This month's inflow",
            "neu",
        )
    with c2:
        kpi_card(
            "Total Expenses",
            format_money(results["total_expenses"], sym),
            "📉",
            f"{results['expense_ratio']:.1f}% of income",
            "neg" if results["expense_ratio"] > 80 else "neu",
        )
    with c3:
        rem = results["remaining_income"]
        kpi_card(
            "Current Balance",
            format_money(rem, sym),
            "⚖️",
            "surplus" if rem >= 0 else "deficit",
            "pos" if rem >= 0 else "neg",
        )
    with c4:
        kpi_card(
            "Total Savings",
            format_money(results["savings"], sym),
            "🏦",
            f"{results['savings_ratio']:.1f}% savings rate",
            "pos" if results["savings_ratio"] >= 10 else "neu",
        )


def build_transactions_from_results(results: dict[str, Any]) -> list[dict[str, Any]]:
    """Derive a transaction-like list from the monthly snapshot (no invented history)."""
    labels = {k: v for k, v in EXPENSE_CATEGORIES}
    sym = results.get("symbol", "$")
    rows: list[dict[str, Any]] = [
        {
            "id": "income",
            "category": "income",
            "label": "Monthly income",
            "type": "income",
            "amount": results.get("monthly_income", 0),
            "icon": CATEGORY_ICONS.get("income", "💰"),
            "symbol": sym,
        }
    ]
    for key, amount in (results.get("expense_breakdown") or {}).items():
        if amount <= 0:
            continue
        rows.append(
            {
                "id": key,
                "category": key,
                "label": labels.get(key, key),
                "type": "expense",
                "amount": amount,
                "icon": CATEGORY_ICONS.get(key, "📦"),
                "symbol": sym,
            }
        )
    if results.get("savings", 0) > 0:
        rows.append(
            {
                "id": "savings",
                "category": "savings",
                "label": "Monthly savings",
                "type": "income",
                "amount": results.get("savings", 0),
                "icon": CATEGORY_ICONS.get("savings", "🏦"),
                "symbol": sym,
            }
        )
    return rows
