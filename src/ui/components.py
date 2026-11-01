"""Reusable Streamlit UI fragments."""

from __future__ import annotations

from typing import Any

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config import COLORS, EDUCATIONAL_DISCLAIMER, EXPENSE_CATEGORIES, health_band_label
from src.utils import format_money


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


def metric_card_row(items: list[dict[str, str]]) -> None:
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            delta = item.get("delta", "")
            delta_html = f'<div class="delta">{delta}</div>' if delta else ""
            st.markdown(
                f"""
                <div class="fw-metric">
                  <div class="label">{item.get('label','')}</div>
                  <div class="value">{item.get('value','')}</div>
                  {delta_html}
                </div>
                """,
                unsafe_allow_html=True,
            )


def risk_badge(risk: str) -> None:
    level = (risk or "MEDIUM").upper()
    st.markdown(
        f'<span class="fw-risk-{level}" style="font-size:1.4rem;">{level}</span>',
        unsafe_allow_html=True,
    )


def score_band_caption(score: int) -> str:
    return f"{score}/100 — {health_band_label(score)}"


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
        hole=0.48,
        color_discrete_sequence=[
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["sage"],
            COLORS["warm"],
            "#8FAE9B",
            "#4F7568",
            "#C4B59A",
            "#2F5D52",
            "#9BB8A8",
        ],
    )
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=COLORS["text"],
        legend_title_text="",
        height=340,
    )
    return fig


def income_vs_expense_chart(results: dict[str, Any]):
    symbol = results.get("symbol", "$")
    fig = go.Figure(
        data=[
            go.Bar(
                name="Income",
                x=["Monthly"],
                y=[results.get("monthly_income", 0)],
                marker_color=COLORS["primary"],
            ),
            go.Bar(
                name="Expenses",
                x=["Monthly"],
                y=[results.get("total_expenses", 0)],
                marker_color=COLORS["warm"],
            ),
            go.Bar(
                name="Savings",
                x=["Monthly"],
                y=[results.get("savings", 0)],
                marker_color=COLORS["sage"],
            ),
        ]
    )
    fig.update_layout(
        barmode="group",
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=COLORS["text"],
        yaxis_title=f"Amount ({symbol})",
        height=320,
        legend=dict(orientation="h"),
    )
    return fig


def overview_metrics(results: dict[str, Any]) -> None:
    sym = results.get("symbol", "$")
    metric_card_row(
        [
            {
                "label": "Monthly income",
                "value": format_money(results["monthly_income"], sym),
            },
            {
                "label": "Total expenses",
                "value": format_money(results["total_expenses"], sym),
            },
            {
                "label": "Remaining",
                "value": format_money(results["remaining_income"], sym),
                "delta": "surplus" if results["remaining_income"] >= 0 else "deficit",
            },
            {
                "label": "Current savings",
                "value": format_money(results["savings"], sym),
                "delta": f"{results['savings_ratio']:.1f}% of income",
            },
        ]
    )
