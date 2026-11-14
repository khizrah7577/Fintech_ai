"""
FinWise AI — Streamlit entrypoint.
Run:  streamlit run app.py

Boots without an API key. Users paste OPENAI_API_KEY on the welcome screen.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Streamlit Cloud mounts repos under /mount/src/<repo>.
# Package is named `finwise` (not `src`) to avoid clashing with /mount/src.
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

from finwise.config import (
    APP_NAME,
    APP_SUBTITLE,
    DISCLAIMER_COMPACT,
    NAV_PAGES,
    refresh_secrets_from_streamlit,
)
from finwise.session import init_session
from finwise.ui.styles import inject_global_styles

st.set_page_config(
    page_title=f"{APP_NAME} | Smart Budget Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Optional secrets — must never crash if secrets.toml is absent
try:
    refresh_secrets_from_streamlit()
except Exception:
    pass

init_session()
inject_global_styles()

# Cache is optional; failure must not block the welcome / runtime-key flow
try:
    from finwise.cache_manager import configure_cache

    configure_cache(st.session_state.cache_backend)
except Exception as exc:  # noqa: BLE001
    st.session_state["_cache_warning"] = str(exc)[:200]

if not st.session_state.authenticated:
    from finwise.pages.welcome import render_welcome

    render_welcome()
    st.stop()

# Heavy page imports only after the user has entered the app
from finwise.pages import PAGE_RENDERERS  # noqa: E402

with st.sidebar:
    st.markdown(f'<p class="fw-side-brand">{APP_NAME}</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="fw-side-sub">{APP_SUBTITLE}</p>',
        unsafe_allow_html=True,
    )
    st.caption("Professional financial clarity")
    st.markdown("---")

    labels = [label for _, label in NAV_PAGES]
    keys = [key for key, _ in NAV_PAGES]
    try:
        current_idx = keys.index(st.session_state.page)
    except ValueError:
        current_idx = 0

    choice = st.radio("Navigate", labels, index=current_idx, label_visibility="collapsed")
    st.session_state.page = keys[labels.index(choice)]
    st.markdown(
        f'<div class="fw-nav-active">● {choice}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        f'<p class="fw-side-disclaimer">{DISCLAIMER_COMPACT}</p>',
        unsafe_allow_html=True,
    )
    st.caption("Model: " + str(st.session_state.model_name))
    if st.button("Change API key / welcome", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

renderer = PAGE_RENDERERS.get(st.session_state.page, PAGE_RENDERERS["dashboard"])
renderer()
