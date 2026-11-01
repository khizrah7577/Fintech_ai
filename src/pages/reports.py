"""Monthly financial report export (CSV / PDF)."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from src.ui.components import disclaimer_banner, empty_state, overview_metrics, page_header, risk_badge
from src.utils import build_csv_report, build_pdf_report, friendly_error


def render_reports() -> None:
    page_header(
        "Reports",
        "Current-analysis summary only — no fabricated historical months.",
    )
    disclaimer_banner()

    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")

    if not results:
        empty_state(
            "Nothing to report yet",
            "Complete an analysis first. Reports cover the current session snapshot only.",
        )
        return

    st.info(
        "This report reflects your **current** FinWise analysis only. "
        "Month-to-month history is not stored."
    )

    overview_metrics(results)
    if analysis:
        st.write(f"**Summary:** {analysis.get('financial_summary', '')}")
        st.write(
            f"**AI score:** {analysis.get('financial_health_score')}/100 · "
            f"**Python score:** {results.get('preliminary_score')}/100"
        )
        risk_badge(analysis.get("risk_level", "MEDIUM"))
        st.markdown("**Recommendations**")
        for tip in analysis.get("budget_recommendations") or []:
            st.markdown(f"- {tip}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    csv_data = build_csv_report(results, analysis)
    st.download_button(
        "Download CSV report",
        data=csv_data,
        file_name=f"finwise_report_{stamp}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    try:
        pdf_bytes = build_pdf_report(
            results, analysis, symbol=results.get("symbol", "$")
        )
        st.download_button(
            "Download PDF report",
            data=pdf_bytes,
            file_name=f"finwise_report_{stamp}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as exc:  # noqa: BLE001
        st.warning(friendly_error(exc))

    if st.session_state.get("stream_text"):
        with st.expander("Streamed recommendation letter"):
            st.write(st.session_state.stream_text)

    disclaimer_banner()
