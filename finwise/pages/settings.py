"""Settings — API, model, cache, reset."""

from __future__ import annotations

import streamlit as st

from finwise.cache_manager import configure_cache, describe_cache_modes, get_active_backend
from finwise.chains import test_api_connection
from finwise.config import (
    APP_NAME,
    APP_SUBTITLE,
    CACHE_OPTIONS,
    DISCLAIMER_COMPACT,
    OPENAI_API_KEY,
    SQLITE_CACHE_PATH,
    SUPPORTED_MODELS,
    mask_api_key,
)
from finwise.session import effective_api_key, reset_session_data
from finwise.ui.components import disclaimer_banner, page_header
from finwise.utils import friendly_error


def render_settings() -> None:
    page_header("Settings", "API configuration, model controls, and session tools.")
    disclaimer_banner()

    st.markdown('<div class="fw-card">', unsafe_allow_html=True)
    st.markdown("##### OpenAI API")
    st.write(f"`.env` / secrets key: `{mask_api_key(OPENAI_API_KEY)}`")

    show = st.toggle("Show session API key", value=st.session_state.show_api_key)
    st.session_state.show_api_key = show
    st.session_state.session_api_key = st.text_input(
        "Session API key (runtime)",
        value=st.session_state.session_api_key,
        type="default" if show else "password",
        help="Stored only in Streamlit session state for this browser session.",
    )

    models = list(dict.fromkeys([st.session_state.model_name, *SUPPORTED_MODELS]))
    st.session_state.model_name = st.selectbox(
        "Model",
        models,
        index=models.index(st.session_state.model_name)
        if st.session_state.model_name in models
        else 0,
    )
    st.session_state.temperature = st.slider(
        "Creativity / temperature",
        0.0,
        1.0,
        float(st.session_state.temperature),
        0.05,
    )

    t1, t2 = st.columns(2)
    with t1:
        if st.button("Test API connection", use_container_width=True):
            ok, msg = test_api_connection(
                api_key=effective_api_key() or None,
                model=st.session_state.model_name,
            )
            st.session_state.connection_status = (
                f"✅ {msg}" if ok else f"❌ {friendly_error(Exception(msg))}"
            )
    with t2:
        status = "Key present" if effective_api_key() else "No key configured"
        st.metric("Connection", status)

    if st.session_state.get("connection_status"):
        st.info(st.session_state.connection_status)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="fw-card">', unsafe_allow_html=True)
    st.markdown("##### LLM cache")
    labels = list(CACHE_OPTIONS.keys())
    current_backend = st.session_state.cache_backend
    current_label = next(
        (lab for lab, val in CACHE_OPTIONS.items() if val == current_backend),
        labels[0],
    )
    choice = st.radio("Cache backend", labels, index=labels.index(current_label))
    st.session_state.cache_backend = CACHE_OPTIONS[choice]
    try:
        msg = configure_cache(st.session_state.cache_backend)
        st.caption(msg)
    except Exception as exc:  # noqa: BLE001
        st.warning(str(exc)[:200])
    modes = describe_cache_modes()
    st.write(f"- Memory: {modes['memory']}")
    st.write(f"- SQLite: {modes['sqlite']}")
    st.caption(f"Active: `{get_active_backend()}` · DB: `{SQLITE_CACHE_PATH}`")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("##### Session")
    if not st.session_state.confirm_reset:
        if st.button("Reset session…", use_container_width=True):
            st.session_state.confirm_reset = True
            st.rerun()
    else:
        st.warning(
            "Clears analysis, chat, and form memory. "
            "Does **not** delete SQLite cache or your `.env` key."
        )
        c1, c2 = st.columns(2)
        if c1.button("Confirm reset", type="primary", use_container_width=True):
            reset_session_data()
            st.success("Session cleared.")
            st.rerun()
        if c2.button("Cancel", use_container_width=True):
            st.session_state.confirm_reset = False
            st.rerun()

    if st.button("Return to welcome / change API key", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.write(f"**{APP_NAME}**")
    st.caption(APP_SUBTITLE)
    st.caption(DISCLAIMER_COMPACT)
