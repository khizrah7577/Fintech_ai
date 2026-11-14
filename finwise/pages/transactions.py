"""Transaction-style view of the monthly snapshot + data entry."""

from __future__ import annotations

import streamlit as st

from finwise.pages.snapshot_form import render_snapshot_form, render_streaming_block
from finwise.ui.components import (
    build_transactions_from_results,
    disclaimer_banner,
    empty_state,
    page_header,
)
from finwise.utils import format_money


def render_transactions() -> None:
    page_header(
        "Transactions",
        "Enter your monthly snapshot, then review income and category spending as transactions.",
    )
    disclaimer_banner()

    tab_list, tab_add = st.tabs(["Transaction list", "Update monthly snapshot"])

    with tab_add:
        st.markdown(
            "Save your income and expenses here. Figures come from **your inputs** — "
            "no fabricated bank history."
        )
        render_snapshot_form(show_ai=True)
        render_streaming_block()
        if st.session_state.get("message_demo"):
            with st.expander("LangChain message objects demo"):
                demo = st.session_state.message_demo
                st.markdown("**SystemMessage**")
                st.code(demo["system"])
                st.markdown("**HumanMessage**")
                st.code(demo["human"])
                st.markdown("**AIMessage**")
                st.code(demo["ai"])

    with tab_list:
        results = st.session_state.get("results")
        if not results:
            empty_state(
                "No transactions yet",
                "Use the Update monthly snapshot tab to enter income and expenses.",
            )
            return

        rows = build_transactions_from_results(results)
        search = st.text_input("Search category", "")
        ftype = st.selectbox("Type", ["All", "Income", "Expense"])
        sort = st.selectbox("Sort by", ["Amount (high → low)", "Amount (low → high)", "Name"])

        filtered = rows
        if search.strip():
            q = search.strip().lower()
            filtered = [r for r in filtered if q in r["label"].lower() or q in r["category"]]
        if ftype == "Income":
            filtered = [r for r in filtered if r["type"] == "income"]
        elif ftype == "Expense":
            filtered = [r for r in filtered if r["type"] == "expense"]

        if sort.startswith("Amount (high"):
            filtered = sorted(filtered, key=lambda r: r["amount"], reverse=True)
        elif sort.startswith("Amount (low"):
            filtered = sorted(filtered, key=lambda r: r["amount"])
        else:
            filtered = sorted(filtered, key=lambda r: r["label"])

        st.markdown('<div class="fw-card">', unsafe_allow_html=True)
        st.caption(
            f"Showing {len(filtered)} items from your current monthly snapshot "
            f"(goal: {results.get('financial_goal', '—')})."
        )
        for r in filtered:
            amt = format_money(r["amount"], r["symbol"])
            sign = "+" if r["type"] == "income" else "−"
            cls = "income" if r["type"] == "income" else "expense"
            st.markdown(
                f"""
                <div class="fw-tx-row">
                  <div class="fw-tx-left">
                    <div class="fw-tx-icon">{r['icon']}</div>
                    <div>
                      <strong>{r['label']}</strong><br/>
                      <span style="color:#64748B;font-size:0.8rem;">{r['type'].title()}</span>
                    </div>
                  </div>
                  <div class="fw-tx-amt {cls}">{sign}{amt}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
