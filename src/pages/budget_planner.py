"""Budget Planner — educational targets vs current spending."""

from __future__ import annotations

import streamlit as st

from src.config import EXPENSE_CATEGORIES
from src.financial_calculator import recalculate_budget, recommend_budget_allocation
from src.ui.components import disclaimer_banner, empty_state, page_header
from src.utils import format_money


def render_budget_planner() -> None:
    page_header(
        "Budget Planner",
        "Compare your current spend with adjustable educational category targets.",
    )
    disclaimer_banner()

    results = st.session_state.get("results")
    if not results:
        empty_state(
            "Need a financial snapshot",
            "Run Financial Analysis first so we can plan against your real income.",
        )
        return

    sym = results.get("symbol", "$")
    income = results["monthly_income"]
    current = results.get("expense_breakdown") or {}

    if st.session_state.budget_targets is None:
        st.session_state.budget_targets = recommend_budget_allocation(income)
    if st.session_state.savings_target is None:
        st.session_state.savings_target = round(income * 0.10, 2)

    st.markdown("### Snapshot")
    m1, m2, m3 = st.columns(3)
    m1.metric("Monthly income", format_money(income, sym))
    m2.metric("Current expenses", format_money(results["total_expenses"], sym))
    m3.metric("Remaining (actual)", format_money(results["remaining_income"], sym))

    st.markdown("### Adjust category targets")
    st.caption("Defaults follow an educational guideline mix — edit freely and recalculate.")
    targets = dict(st.session_state.budget_targets)
    cols = st.columns(3)
    for i, (key, label) in enumerate(EXPENSE_CATEGORIES):
        with cols[i % 3]:
            targets[key] = st.number_input(
                label,
                min_value=0.0,
                value=float(targets.get(key, 0.0)),
                step=25.0,
                key=f"budget_tgt_{key}",
            )

    savings_target = st.number_input(
        "Savings target",
        min_value=0.0,
        value=float(st.session_state.savings_target),
        step=25.0,
    )

    if st.button("Recalculate budget", type="primary"):
        st.session_state.budget_targets = targets
        st.session_state.savings_target = savings_target

    plan = recalculate_budget(
        income,
        current,
        st.session_state.budget_targets,
        st.session_state.savings_target,
    )

    st.markdown("### Planned results")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Planned expenses", format_money(plan["total_planned_expenses"], sym))
    p2.metric("Savings target", format_money(plan["savings_target"], sym))
    p3.metric("Remaining after plan", format_money(plan["remaining_after_plan"], sym))
    p4.metric("Current expenses", format_money(plan["total_current_expenses"], sym))

    st.markdown("### Category check")
    for key, label in EXPENSE_CATEGORIES:
        cur = plan["current"].get(key, 0)
        tgt = plan["targets"].get(key, 0)
        over = cur > tgt
        line = f"**{label}** — current {format_money(cur, sym)} · target {format_money(tgt, sym)}"
        if over:
            st.warning(line + " · overspending")
        else:
            st.success(line)

    if plan["warnings"]:
        st.markdown("### Warnings")
        for w in plan["warnings"]:
            st.warning(w)

    disclaimer_banner()
