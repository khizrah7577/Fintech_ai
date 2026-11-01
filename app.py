"""
FinWise AI — Streamlit entrypoint.
Run:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from src.cache_manager import configure_cache
from src.config import (
    APP_NAME,
    APP_SUBTITLE,
    DISCLAIMER_COMPACT,
    NAV_PAGES,
)
from src.pages import PAGE_RENDERERS, render_welcome
from src.session import init_session
from src.ui.styles import inject_global_styles

st.set_page_config(
    page_title=f"{APP_NAME} | Smart Budget Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()
inject_global_styles()

# Register cache once per backend choice (safe across reruns)
configure_cache(st.session_state.cache_backend)

if not st.session_state.authenticated:
    render_welcome()
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f'<p class="fw-side-brand">{APP_NAME}</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="fw-side-sub">{APP_SUBTITLE}</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    labels = [label for _, label in NAV_PAGES]
    keys = [key for key, _ in NAV_PAGES]
    try:
        current_idx = keys.index(st.session_state.page)
    except ValueError:
        current_idx = 0

    choice = st.radio("Navigate", labels, index=current_idx, label_visibility="collapsed")
    st.session_state.page = keys[labels.index(choice)]

    st.markdown("---")
    st.markdown(
        f'<p class="fw-side-disclaimer">{DISCLAIMER_COMPACT}</p>',
        unsafe_allow_html=True,
    )
    st.caption("Model: " + str(st.session_state.model_name))
    if st.button("Back to welcome"):
        st.session_state.authenticated = False
        st.rerun()

# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------
renderer = PAGE_RENDERERS.get(st.session_state.page, PAGE_RENDERERS["dashboard"])
renderer()
