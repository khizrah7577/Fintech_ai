"""
FinWise AI — Streamlit entrypoint.
Run:  streamlit run app.py

Premium top-nav fintech UI. Boots without API key (welcome screen).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Avoid clash with Streamlit Cloud mount path /mount/src
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

from finwise.config import APP_NAME, refresh_secrets_from_streamlit
from finwise.session import init_session
from finwise.ui.styles import inject_global_styles

st.set_page_config(
    page_title=f"{APP_NAME} | Smart Budget Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

try:
    refresh_secrets_from_streamlit()
except Exception:
    pass

init_session()
inject_global_styles()

try:
    from finwise.cache_manager import configure_cache

    configure_cache(st.session_state.cache_backend)
except Exception as exc:  # noqa: BLE001
    st.session_state["_cache_warning"] = str(exc)[:200]

if not st.session_state.authenticated:
    from finwise.pages.welcome import render_welcome

    render_welcome()
    st.stop()

from finwise.pages import PAGE_RENDERERS  # noqa: E402
from finwise.ui.navigation import render_top_nav  # noqa: E402

render_top_nav()

# Migrate old page keys if needed
if st.session_state.page in {"analysis", "insights"}:
    st.session_state.page = "analytics" if st.session_state.page == "insights" else "transactions"

renderer = PAGE_RENDERERS.get(st.session_state.page, PAGE_RENDERERS["dashboard"])
renderer()
