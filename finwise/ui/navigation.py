"""Horizontal top navigation for FinWise AI."""

from __future__ import annotations

import streamlit as st

from finwise.config import APP_NAME, NAV_PAGES, mask_api_key
from finwise.session import effective_api_key


def render_top_nav() -> None:
    """Brand bar + active page indicator. Routing uses Streamlit buttons below."""
    labels = {k: v for k, v in NAV_PAGES}
    current = st.session_state.get("page", "dashboard")
    chips = []
    for key, label in NAV_PAGES:
        active = "active" if key == current else ""
        chips.append(f'<span class="fw-nav-chip {active}">{label}</span>')

    key_status = "Connected" if effective_api_key() else "No key"
    masked = mask_api_key(effective_api_key()) if effective_api_key() else "Paste key in Settings"

    st.markdown(
        f"""
        <div class="fw-topnav">
          <div class="fw-topnav-inner">
            <div class="fw-brand">
              <div class="fw-logo-mark">F</div>
              <div class="fw-brand-name">{APP_NAME.split()[0]} <span>AI</span></div>
            </div>
            <div class="fw-nav-links">{''.join(chips)}</div>
            <div class="fw-profile">
              <div class="fw-avatar">FW</div>
              <div class="fw-profile-meta">
                <strong>Workspace</strong>
                {key_status} · {masked}
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Interactive routing (Streamlit-compatible)
    cols = st.columns(len(NAV_PAGES))
    for i, (key, label) in enumerate(NAV_PAGES):
        with cols[i]:
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if key == current else "secondary",
            ):
                st.session_state.page = key
                st.rerun()

    st.caption(
        f"Active: **{labels.get(current, current)}** · "
        "Educational prototype — not financial advice."
    )
