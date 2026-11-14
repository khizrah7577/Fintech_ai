"""Shared monthly financial snapshot form + AI analysis trigger."""

from __future__ import annotations

import streamlit as st

from finwise.chains import (
    build_llm,
    run_message_demo,
    run_structured_analysis,
    stream_recommendations,
)
from finwise.config import CURRENCIES, FINANCIAL_GOALS, currency_symbol
from finwise.financial_calculator import calculate_financials, validate_inputs
from finwise.session import effective_api_key, has_api_key
from finwise.utils import friendly_error


def render_snapshot_form(*, show_ai: bool = True) -> None:
    """Collect income/expenses and optionally run LangChain analysis."""
    defaults = st.session_state.get("form_defaults") or {}

    with st.form("finwise_snapshot_form", clear_on_submit=False):
        st.markdown("##### Income & savings")
        c1, c2, c3 = st.columns(3)
        with c1:
            monthly_income = st.number_input(
                "Monthly income",
                min_value=0.0,
                value=float(defaults.get("monthly_income", 5000.0)),
                step=100.0,
            )
        with c2:
            savings = st.number_input(
                "Current monthly savings",
                min_value=0.0,
                value=float(defaults.get("savings", 500.0)),
                step=50.0,
            )
        with c3:
            codes = [c[0] for c in CURRENCIES]
            currency_code = st.selectbox(
                "Currency",
                codes,
                index=codes.index(defaults["currency"])
                if defaults.get("currency") in codes
                else 0,
            )

        st.markdown("##### Expense categories")
        with st.expander("Housing & essentials", expanded=True):
            e1, e2, e3 = st.columns(3)
            housing = e1.number_input(
                "Housing / Rent", min_value=0.0,
                value=float(defaults.get("housing", 1500.0)), step=50.0,
            )
            food = e2.number_input(
                "Food & Groceries", min_value=0.0,
                value=float(defaults.get("food", 400.0)), step=25.0,
            )
            utilities = e3.number_input(
                "Utilities", min_value=0.0,
                value=float(defaults.get("utilities", 150.0)), step=10.0,
            )
        with st.expander("Mobility, health & learning", expanded=True):
            e4, e5, e6 = st.columns(3)
            transportation = e4.number_input(
                "Transportation", min_value=0.0,
                value=float(defaults.get("transportation", 200.0)), step=20.0,
            )
            healthcare = e5.number_input(
                "Healthcare", min_value=0.0,
                value=float(defaults.get("healthcare", 100.0)), step=10.0,
            )
            education = e6.number_input(
                "Education", min_value=0.0,
                value=float(defaults.get("education", 50.0)), step=10.0,
            )
        with st.expander("Lifestyle & obligations", expanded=True):
            e7, e8, e9 = st.columns(3)
            entertainment = e7.number_input(
                "Entertainment", min_value=0.0,
                value=float(defaults.get("entertainment", 150.0)), step=10.0,
            )
            loan_debt = e8.number_input(
                "Loan / Debt", min_value=0.0,
                value=float(defaults.get("loan_debt", 300.0)), step=25.0,
            )
            other = e9.number_input(
                "Other", min_value=0.0,
                value=float(defaults.get("other", 100.0)), step=10.0,
            )

        goals = FINANCIAL_GOALS
        g_default = defaults.get("financial_goal", goals[0])
        financial_goal = st.selectbox(
            "Financial goal",
            goals,
            index=goals.index(g_default) if g_default in goals else 0,
        )
        run_ai = st.checkbox("Also run AI analysis after save", value=show_ai)
        show_demo = st.checkbox("Show LangChain message demo", value=False)

        submitted = st.form_submit_button(
            "Save snapshot & calculate",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    expenses = {
        "housing": housing,
        "food": food,
        "transportation": transportation,
        "utilities": utilities,
        "education": education,
        "healthcare": healthcare,
        "entertainment": entertainment,
        "loan_debt": loan_debt,
        "other": other,
    }
    for issue in validate_inputs(monthly_income, expenses, savings):
        st.warning(issue)

    symbol = currency_symbol(currency_code)
    calc = calculate_financials(monthly_income, expenses, savings)
    st.session_state.form_defaults = {
        "monthly_income": monthly_income,
        "savings": savings,
        "currency": currency_code,
        "financial_goal": financial_goal,
        **expenses,
    }
    st.session_state.results = {
        **calc,
        "financial_goal": financial_goal,
        "currency": currency_code,
        "symbol": symbol,
    }
    st.session_state.analysis = None
    st.session_state.stream_text = None
    st.session_state.message_demo = None
    st.session_state.pending_stream = False
    st.session_state.budget_targets = None
    st.success("Snapshot saved. Python metrics updated.")

    if not run_ai:
        return
    if not has_api_key():
        st.error("Add an OpenAI API key on the welcome screen or in Settings for AI analysis.")
        return

    with st.spinner("Running AI analysis…"):
        try:
            llm = build_llm(
                api_key=effective_api_key(),
                model=st.session_state.model_name,
                temperature=st.session_state.temperature,
                streaming=False,
            )
            analysis = run_structured_analysis(st.session_state.results, llm=llm)
            st.session_state.analysis = analysis
            st.session_state.pending_stream = True
            if show_demo:
                demo_line = (
                    f"Income {symbol}{monthly_income:,.0f}, "
                    f"expenses {symbol}{calc['total_expenses']:,.0f}, "
                    f"goal: {financial_goal}."
                )
                st.session_state.message_demo = run_message_demo(llm, demo_line)
            st.success("AI analysis complete.")
        except Exception as exc:  # noqa: BLE001
            st.session_state.pending_stream = False
            st.error(friendly_error(exc))


def render_streaming_block() -> None:
    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")
    if not (results and analysis):
        return
    st.markdown("##### Personalized recommendation")
    if st.session_state.get("pending_stream") and has_api_key():
        try:
            stream_llm = build_llm(
                api_key=effective_api_key(),
                model=st.session_state.model_name,
                temperature=st.session_state.temperature,
                streaming=True,
            )
            stream_inputs = {
                **results,
                "financial_health_score": analysis["financial_health_score"],
                "risk_level": analysis["risk_level"],
            }
            chunks: list[str] = []

            def _gen():
                for piece in stream_recommendations(stream_llm, stream_inputs):
                    chunks.append(piece)
                    yield piece

            st.write_stream(_gen())
            st.session_state.stream_text = "".join(chunks)
        except Exception as exc:  # noqa: BLE001
            st.error(friendly_error(exc))
        finally:
            st.session_state.pending_stream = False
    elif st.session_state.get("stream_text"):
        st.write(st.session_state.stream_text)
