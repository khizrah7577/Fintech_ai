"""Financial Insights derived from calculations + AI JSON."""

from __future__ import annotations

import streamlit as st

from src.config import EXPENSE_CATEGORIES, health_band_label
from src.ui.components import disclaimer_banner, empty_state, page_header, risk_badge
from src.utils import format_money


def render_insights() -> None:
    page_header(
        "Financial Insights",
        "Observations from your Python metrics and the latest AI analysis.",
    )
    disclaimer_banner()

    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")
    if not results:
        empty_state(
            "No insights yet",
            "Submit your finances on the Financial Analysis page first.",
        )
        return

    sym = results.get("symbol", "$")
    labels = {k: v for k, v in EXPENSE_CATEGORIES}
    highest = results.get("highest_expense")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Savings ratio", f"{results['savings_ratio']:.1f}%")
    c2.metric("Expense ratio", f"{results['expense_ratio']:.1f}%")
    c3.metric("Debt burden", f"{results['debt_burden']:.1f}%")
    if highest:
        c4.metric(
            "Highest expense",
            f"{labels.get(highest['category'], highest['category'])}",
            delta=format_money(highest["amount"], sym),
        )
    else:
        c4.metric("Highest expense", "—")

    st.markdown("### Health & risk")
    s1, s2 = st.columns(2)
    with s1:
        st.write(
            f"Python preliminary score: **{results['preliminary_score']}/100** "
            f"({health_band_label(results['preliminary_score'])})"
        )
    with s2:
        if analysis:
            st.write(
                f"AI health score: **{analysis['financial_health_score']}/100** "
                f"({health_band_label(analysis['financial_health_score'])})"
            )
            risk_badge(analysis["risk_level"])
        else:
            st.info("AI risk insights appear after analysis.")

    if analysis:
        st.markdown("### Spending observations")
        for item in analysis.get("spending_analysis") or []:
            st.markdown(
                f"**{item.get('category', 'Category')}** — {item.get('observation', '')}"
            )
            if item.get("recommendation"):
                st.caption(f"Suggestion: {item['recommendation']}")

        st.markdown("### Financial priorities")
        for i, p in enumerate(analysis.get("top_priorities") or [], 1):
            st.markdown(f"{i}. {p}")

        st.markdown("### Savings opportunities")
        for tip in analysis.get("savings_strategy") or []:
            st.markdown(f"- {tip}")

        st.markdown("### Practical improvements")
        for tip in analysis.get("budget_recommendations") or []:
            st.markdown(f"- {tip}")
    else:
        st.warning("Run AI analysis to unlock spending observations and priorities.")

    # Python-side opportunities even without AI
    st.markdown("### Calculated opportunities")
    if results["remaining_income"] < 0:
        st.error(
            f"Expenses exceed income by {format_money(abs(results['remaining_income']), sym)}. "
            "Prioritise cutting non-essentials and reviewing debt payments."
        )
    elif results["remaining_income"] == 0:
        st.warning("Zero remaining income — try trimming one discretionary category to create surplus.")
    if results["debt_burden"] >= 20:
        st.warning(
            f"Debt payments are {results['debt_burden']:.1f}% of income — "
            "consider a debt-reduction focus if that matches your goal."
        )
    if results["savings_ratio"] < 10 and results["monthly_income"] > 0:
        st.info("Educational tip: building toward a 10–20% savings ratio strengthens resilience.")

    disclaimer_banner()
