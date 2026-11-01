"""Home / Dashboard page."""

from __future__ import annotations

import streamlit as st

from src.config import APP_NAME, health_band_label
from src.ui.components import (
    disclaimer_banner,
    empty_state,
    expense_pie,
    income_vs_expense_chart,
    overview_metrics,
    page_header,
    risk_badge,
    score_band_caption,
)


def render_dashboard() -> None:
    page_header(
        f"Welcome to {APP_NAME}",
        "Your calm monthly overview — built from your numbers, not guesswork.",
    )
    disclaimer_banner()

    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")

    if not results:
        empty_state(
            "Start your financial snapshot",
            "Go to Financial Analysis, enter income and expenses, then run Analyse My Finances. "
            "Your dashboard will fill with live metrics, charts, and AI insights.",
        )
        if st.button("Go to Financial Analysis", type="primary"):
            st.session_state.page = "analysis"
            st.rerun()
        return

    overview_metrics(results)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.caption("Python preliminary score")
        st.subheader(score_band_caption(results["preliminary_score"]))
        st.progress(results["preliminary_score"] / 100)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.caption("AI financial health score")
        if analysis:
            st.subheader(score_band_caption(analysis["financial_health_score"]))
            st.progress(analysis["financial_health_score"] / 100)
        else:
            st.info("Run AI analysis to unlock this score.")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.caption("Risk level")
        if analysis:
            risk_badge(analysis["risk_level"])
        else:
            st.write("—")
        st.caption(f"Goal: {results.get('financial_goal', '—')}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    left, right = st.columns(2)
    with left:
        st.markdown("##### Income vs expenses")
        st.plotly_chart(income_vs_expense_chart(results), use_container_width=True)
    with right:
        st.markdown("##### Expense category breakdown")
        pie = expense_pie(results)
        if pie:
            st.plotly_chart(pie, use_container_width=True)
        else:
            st.caption("No expense amounts entered.")

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("##### Savings progress (toward 20% educational target)")
        st.progress(min(1.0, results.get("savings_progress_to_20pct", 0) / 100))
        st.caption(f"Current savings ratio: {results['savings_ratio']:.1f}%")
    with s2:
        st.markdown("##### Budget utilization")
        st.progress(min(1.0, results.get("budget_utilization", 0) / 100))
        st.caption(f"Expense ratio: {results['expense_ratio']:.1f}% of income")

    if analysis:
        st.markdown("##### Recent analysis")
        st.info(analysis.get("financial_summary", ""))
        st.caption(
            f"Bands — {health_band_label(analysis['financial_health_score'])} · "
            f"Risk {analysis.get('risk_level')}"
        )

    n1, n2, n3 = st.columns(3)
    if n1.button("Open AI Assistant", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()
    if n2.button("Budget Planner", use_container_width=True):
        st.session_state.page = "budget"
        st.rerun()
    if n3.button("Downloadable Reports", use_container_width=True):
        st.session_state.page = "reports"
        st.rerun()
