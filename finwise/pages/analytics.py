"""Financial Analytics — rich charts from real snapshot + AI JSON."""

from __future__ import annotations

import streamlit as st

from finwise.config import health_band_label
from finwise.ui.components import (
    cashflow_gauge,
    category_bars,
    disclaimer_banner,
    empty_state,
    expense_pie,
    health_score_ring,
    income_vs_expense_chart,
    overview_metrics,
    page_header,
    risk_badge,
    score_band_caption,
)


def render_analytics() -> None:
    page_header(
        "Financial Analytics",
        "Monthly analysis from your saved snapshot — charts use actual calculated values.",
    )
    disclaimer_banner()

    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")
    if not results:
        empty_state(
            "No analytics yet",
            "Save a monthly snapshot under Transactions first.",
        )
        return

    overview_metrics(results)

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Savings ratio", f"{results['savings_ratio']:.1f}%")
    a2.metric("Expense ratio", f"{results['expense_ratio']:.1f}%")
    a3.metric("Debt burden", f"{results['debt_burden']:.1f}%")
    a4.metric("Python score", f"{results['preliminary_score']}/100")

    st.markdown("### Cash flow & mix")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(income_vs_expense_chart(results), use_container_width=True)
    with c2:
        pie = expense_pie(results)
        if pie:
            st.plotly_chart(pie, use_container_width=True)

    st.markdown("### Performance gauges")
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(cashflow_gauge(results), use_container_width=True)
    with g2:
        st.plotly_chart(
            health_score_ring(results["preliminary_score"], "Python health"),
            use_container_width=True,
        )
    with g3:
        if analysis:
            st.plotly_chart(
                health_score_ring(analysis["financial_health_score"], "AI health"),
                use_container_width=True,
            )
        else:
            st.info("AI score appears after AI analysis.")

    bars = category_bars(results)
    if bars:
        st.markdown("### Category-wise spending")
        st.plotly_chart(bars, use_container_width=True)

    st.markdown("### Health & risk")
    st.write(
        f"Python preliminary score: **{score_band_caption(results['preliminary_score'])}**"
    )
    if analysis:
        st.write(
            f"AI health score: **{score_band_caption(analysis['financial_health_score'])}**"
        )
        risk_badge(analysis["risk_level"])
        st.markdown("#### Spending observations")
        for item in analysis.get("spending_analysis") or []:
            st.markdown(
                f"**{item.get('category', 'Category')}** — {item.get('observation', '')}"
            )
            if item.get("recommendation"):
                st.caption(f"Suggestion: {item['recommendation']}")
        st.markdown("#### Priorities")
        for i, p in enumerate(analysis.get("top_priorities") or [], 1):
            st.markdown(f"{i}. {p}")
    else:
        st.warning("Run AI analysis from Transactions to unlock AI insights.")

    st.caption(
        "Period: current monthly snapshot only — no fabricated annual history. "
        f"Goal: {results.get('financial_goal')} · Band: "
        f"{health_band_label(analysis['financial_health_score'] if analysis else results['preliminary_score'])}"
    )
