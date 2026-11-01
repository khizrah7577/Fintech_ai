"""Welcome / API configuration landing screen."""

from __future__ import annotations

import streamlit as st

from src.chains import test_api_connection
from src.config import APP_NAME, APP_SUBTITLE, DISCLAIMER_COMPACT, OPENAI_API_KEY, OPENAI_MODEL
from src.session import effective_api_key
from src.utils import friendly_error


def render_welcome() -> None:
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="fw-welcome-card">
              <p style="font-family:'Cormorant Garamond',Georgia,serif;font-size:2.4rem;
                 font-weight:700;color:#174A40;margin:0;letter-spacing:-0.02em;">{APP_NAME}</p>
              <p style="color:#68776E;margin:0.35rem 0 1.2rem 0;">{APP_SUBTITLE}</p>
              <p style="color:#183D36;line-height:1.55;">
                Welcome to FinWise AI — enter your monthly numbers, get deterministic
                Python insights, then educational AI guidance powered by LangChain.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown("#### Connect with OpenAI")
        st.caption(
            "Uses your `.env` key if present. You may also paste a session key below "
            "(stored only in Streamlit session state)."
        )

        env_ready = bool(OPENAI_API_KEY)
        if env_ready:
            st.success("`.env` API key detected — you can continue without pasting a key.")
        else:
            st.warning("No `.env` key found. Paste an OpenAI API key to continue.")

        show = st.toggle("Show API key", value=False, key="welcome_show_key")
        key_input = st.text_input(
            "OpenAI API key (optional override)",
            type="default" if show else "password",
            value=st.session_state.get("session_api_key", ""),
            placeholder="sk-…",
            help="Session-scoped override. Leave blank to use .env.",
        )

        model = st.selectbox(
            "Model",
            [OPENAI_MODEL, "gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
            index=0,
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Test connection", use_container_width=True):
                st.session_state.session_api_key = key_input.strip()
                ok, msg = test_api_connection(
                    api_key=effective_api_key() or None,
                    model=model,
                )
                if ok:
                    st.session_state.connection_status = f"✅ {msg}"
                else:
                    st.session_state.connection_status = f"❌ {friendly_error(Exception(msg))}"
        with c2:
            if st.button("Enter FinWise AI", type="primary", use_container_width=True):
                st.session_state.session_api_key = key_input.strip()
                st.session_state.model_name = model
                if not effective_api_key():
                    st.error("Add an API key in `.env` or paste one above.")
                else:
                    st.session_state.authenticated = True
                    st.session_state._welcome_seen = True
                    st.session_state.page = "dashboard"
                    st.rerun()

        if st.session_state.get("connection_status"):
            st.info(st.session_state.connection_status)

        st.caption(DISCLAIMER_COMPACT)
        with st.expander("How to get an API key"):
            st.markdown(
                """
1. Create an account at [platform.openai.com](https://platform.openai.com).
2. Create a secret key.
3. Copy `.env.example` to `.env` and set `OPENAI_API_KEY=…`, **or** paste the key above for this session.
4. Never commit `.env` or share your key.
                """
            )

    with right:
        st.markdown(
            """
            <div class="fw-illus">
              <div class="orb orb-a"></div>
              <div class="orb orb-b"></div>
              <div class="orb orb-c"></div>
              <div class="fw-botanic"></div>
              <div class="fw-float-card a">
                Monthly clarity
                <span class="mini">Income · Expenses · Savings</span>
              </div>
              <div class="fw-float-card b">
                Educational AI insights
                <span class="mini">LangChain · Structured JSON</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
