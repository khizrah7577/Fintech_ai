"""Central Streamlit session-state helpers."""

from __future__ import annotations

import streamlit as st

from src.config import DEFAULT_TEMPERATURE, OPENAI_API_KEY, OPENAI_MODEL


def init_session() -> None:
    defaults = {
        "authenticated": False,
        "page": "dashboard",
        "results": None,
        "analysis": None,
        "stream_text": None,
        "pending_stream": False,
        "message_demo": None,
        "chat_messages": [],
        "form_defaults": {},
        "budget_targets": None,
        "savings_target": None,
        "session_api_key": "",
        "model_name": OPENAI_MODEL,
        "temperature": DEFAULT_TEMPERATURE,
        "cache_backend": "memory",
        "show_api_key": False,
        "connection_status": "",
        "confirm_reset": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def effective_api_key() -> str:
    override = (st.session_state.get("session_api_key") or "").strip()
    if override:
        return override
    return (OPENAI_API_KEY or "").strip()


def has_api_key() -> bool:
    return bool(effective_api_key())


def reset_session_data() -> None:
    """Clear analysis/chat/form state. Does NOT delete SQLite cache or .env."""
    st.session_state.results = None
    st.session_state.analysis = None
    st.session_state.stream_text = None
    st.session_state.pending_stream = False
    st.session_state.message_demo = None
    st.session_state.chat_messages = []
    st.session_state.budget_targets = None
    st.session_state.savings_target = None
    st.session_state.form_defaults = {}
    st.session_state.confirm_reset = False
