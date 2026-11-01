"""Main assignment workflow — inputs, Python calc, LLMChain, JSON, streaming."""

from __future__ import annotations

import streamlit as st

from src.chains import (
    build_llm,
    run_message_demo,
    run_structured_analysis,
    stream_recommendations,
)
from src.config import (
    CURRENCIES,
    FINANCIAL_GOALS,
    currency_symbol,
    health_band_label,
)
from src.financial_calculator import calculate_financials, validate_inputs
from src.session import effective_api_key, has_api_key
from src.ui.components import (
    disclaimer_banner,
    expense_pie,
    overview_metrics,
    page_header,
    risk_badge,
    score_band_caption,
)
from src.utils import friendly_error


def render_financial_analysis() -> None:
    page_header(
        "Financial Analysis",
        "Enter your month → Python computes ratios → LangChain returns structured insights.",
    )
    disclaimer_banner()

    defaults = st.session_state.get("form_defaults") or {}

    with st.form("finwise_analysis_form", clear_on_submit=False):
        st.markdown("### 1. Income and savings")
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
            currency_code = st.selectbox(
                "Currency",
                [c[0] for c in CURRENCIES],
                index=max(
                    0,
                    [c[0] for c in CURRENCIES].index(defaults.get("currency", "USD"))
                    if defaults.get("currency", "USD") in [c[0] for c in CURRENCIES]
                    else 0,
                ),
            )

        st.markdown("### 2. Monthly expense breakdown")
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

        st.markdown("### 3. Financial goals and options")
        g1, g2 = st.columns(2)
        with g1:
            goals = FINANCIAL_GOALS
            g_default = defaults.get("financial_goal", goals[0])
            g_idx = goals.index(g_default) if g_default in goals else 0
            financial_goal = st.selectbox("Financial goal", goals, index=g_idx)
        with g2:
            show_message_demo = st.checkbox(
                "Show LangChain System / Human / AI message demo",
                value=False,
            )

        submitted = st.form_submit_button(
            "Analyse My Finances",
            type="primary",
            use_container_width=True,
        )

    if submitted:
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
        issues = validate_inputs(monthly_income, expenses, savings)
        for issue in issues:
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

        if not has_api_key():
            st.error("Add an OpenAI API key in Settings or `.env` before AI analysis.")
        else:
            with st.spinner("Running LLMChain analysis…"):
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
                    if show_message_demo:
                        demo_line = (
                            f"Income {symbol}{monthly_income:,.0f}, "
                            f"expenses {symbol}{calc['total_expenses']:,.0f}, "
                            f"goal: {financial_goal}."
                        )
                        st.session_state.message_demo = run_message_demo(llm, demo_line)
                    st.success("Analysis complete. Dashboard updated.")
                except Exception as exc:  # noqa: BLE001
                    st.session_state.pending_stream = False
                    st.error(friendly_error(exc))

    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")

    if results:
        st.markdown("---")
        st.markdown("### Financial overview (Python)")
        overview_metrics(results)
        st.caption(
            f"Expense ratio **{results['expense_ratio']:.1f}%** · "
            f"Debt burden **{results['debt_burden']:.1f}%** · "
            f"Python score **{results['preliminary_score']}/100** "
            f"({health_band_label(results['preliminary_score'])})"
        )
        pie = expense_pie(results)
        if pie:
            st.plotly_chart(pie, use_container_width=True)

    if analysis:
        st.markdown("### AI financial analysis")
        st.info(analysis["financial_summary"])
        a1, a2, a3 = st.columns(3)
        with a1:
            st.caption("AI financial health score")
            st.subheader(score_band_caption(analysis["financial_health_score"]))
            st.progress(analysis["financial_health_score"] / 100)
        with a2:
            st.caption("Python preliminary score")
            st.subheader(score_band_caption(results["preliminary_score"]))
            st.progress(results["preliminary_score"] / 100)
        with a3:
            st.caption("Risk level")
            risk_badge(analysis["risk_level"])

        tabs = st.tabs(
            [
                "Spending analysis",
                "Top priorities",
                "Budget tips",
                "Savings strategy",
                "Next-month plan",
            ]
        )
        with tabs[0]:
            for item in analysis.get("spending_analysis") or []:
                with st.expander(item.get("category") or "Category", expanded=False):
                    st.write(item.get("observation", ""))
                    st.markdown(f"**Recommendation:** {item.get('recommendation', '')}")
        with tabs[1]:
            for i, p in enumerate(analysis.get("top_priorities") or [], 1):
                st.markdown(f"**{i}.** {p}")
        with tabs[2]:
            for tip in analysis.get("budget_recommendations") or []:
                st.markdown(f"- {tip}")
        with tabs[3]:
            for tip in analysis.get("savings_strategy") or []:
                st.markdown(f"- {tip}")
        with tabs[4]:
            for step in analysis.get("next_month_action_plan") or []:
                st.markdown(f"- {step}")

        st.markdown("### Personalized recommendation")
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

        if st.session_state.get("message_demo"):
            with st.expander("LangChain message objects demo"):
                demo = st.session_state.message_demo
                st.markdown("**SystemMessage**")
                st.code(demo["system"])
                st.markdown("**HumanMessage**")
                st.code(demo["human"])
                st.markdown("**AIMessage**")
                st.code(demo["ai"])

        with st.expander("Raw structured JSON"):
            clean = {k: v for k, v in analysis.items() if not str(k).startswith("_")}
            st.json(clean)

        disclaimer_banner()
