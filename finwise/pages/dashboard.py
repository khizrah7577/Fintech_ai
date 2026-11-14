"""Premium financial overview dashboard."""

from __future__ import annotations

import streamlit as st

from finwise.config import APP_NAME, health_band_label
from finwise.ui.components import (
    cashflow_gauge,
    category_bars,
    disclaimer_banner,
    empty_state,
    expense_pie,
    health_score_ring,
    income_vs_expense_chart,
    kpi_card,
    overview_metrics,
    page_header,
    risk_badge,
)


def render_dashboard() -> None:
    page_header(
        f"Welcome to {APP_NAME}",
        "Your calm monthly overview — built from your numbers, not guesswork.",
    )
    disclaimer_banner()

    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")

    q1, q2, q3, q4 = st.columns(4)
    if q1.button("Update snapshot", use_container_width=True):
        st.session_state.page = "transactions"
        st.rerun()
    if q2.button("Open analytics", use_container_width=True):
        st.session_state.page = "analytics"
        st.rerun()
    if q3.button("Ask AI advisor", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()
    if q4.button("View reports", use_container_width=True):
        st.session_state.page = "reports"
        st.rerun()

    if not results:
        empty_state(
            "Start your financial snapshot",
            "Go to Transactions, enter income and expenses, then save. "
            "Your dashboard will fill with live KPIs and charts.",
        )
        return

    overview_metrics(results)

    c5, c6 = st.columns(2)
    with c5:
        kpi_card(
            "Budget utilization",
            f"{results.get('budget_utilization', results['expense_ratio']):.1f}%",
            "📊",
            f"Expense ratio {results['expense_ratio']:.1f}%",
            "neg" if results["expense_ratio"] > 90 else "neu",
        )
    with c6:
        score = (
            analysis["financial_health_score"]
            if analysis
            else results["preliminary_score"]
        )
        kpi_card(
            "Financial health score",
            f"{score}/100",
            "💚",
            health_band_label(score)
            + (" · AI" if analysis else " · Python"),
            "pos" if score >= 60 else "neg",
        )

    st.markdown('<div class="fw-card">', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.markdown('<p class="fw-section-title">Income vs expenses</p>', unsafe_allow_html=True)
        st.plotly_chart(income_vs_expense_chart(results), use_container_width=True)
    with right:
        st.markdown('<p class="fw-section-title">Expense distribution</p>', unsafe_allow_html=True)
        pie = expense_pie(results)
        if pie:
            st.plotly_chart(pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.plotly_chart(cashflow_gauge(results), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.plotly_chart(
            health_score_ring(results["preliminary_score"], "Python score"),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with g3:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        if analysis:
            st.plotly_chart(
                health_score_ring(analysis["financial_health_score"], "AI score"),
                use_container_width=True,
            )
            risk_badge(analysis["risk_level"])
        else:
            st.info("Run AI analysis from Transactions to unlock the AI health score.")
        st.markdown("</div>", unsafe_allow_html=True)

    bars = category_bars(results)
    if bars:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<p class="fw-section-title">Category-wise spending</p>', unsafe_allow_html=True)
        st.plotly_chart(bars, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if analysis:
        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.markdown('<p class="fw-section-title">Latest AI insight</p>', unsafe_allow_html=True)
        st.info(analysis.get("financial_summary", ""))
        st.markdown("</div>", unsafe_allow_html=True)
