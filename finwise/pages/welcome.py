"""Welcome screen — collect OpenAI API key at runtime (no secrets required)."""

from __future__ import annotations

import streamlit as st

from finwise.config import APP_NAME, APP_SUBTITLE, DISCLAIMER_COMPACT, OPENAI_MODEL
from finwise.session import effective_api_key
from finwise.utils import friendly_error


def render_welcome() -> None:
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="fw-welcome-card">
              <p style="font-family:'Instrument Sans','DM Sans',sans-serif;font-size:2.35rem;
                 font-weight:700;color:#0F1C3F;margin:0;letter-spacing:-0.03em;">{APP_NAME}</p>
              <p style="color:#64748B;margin:0.35rem 0 1.2rem 0;">{APP_SUBTITLE}</p>
              <p style="color:#0F172A;line-height:1.55;">
                Welcome to FinWise AI — paste your OpenAI API key below to start.
                The key stays in this browser session only and is never written to the repo.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown("#### Enter your OpenAI API key")
        st.caption(
            "Required at runtime. Optional: also set `OPENAI_API_KEY` in Streamlit Secrets "
            "or a local `.env` so you can leave this blank."
        )

        show = st.toggle("Show API key", value=False, key="welcome_show_key")
        key_input = st.text_input(
            "OpenAI API key",
            type="default" if show else "password",
            value=st.session_state.get("session_api_key", ""),
            placeholder="sk-…",
            help="Stored only in Streamlit session state for this visit.",
        )

        model = st.selectbox(
            "Model",
            list(
                dict.fromkeys(
                    [st.session_state.get("model_name", OPENAI_MODEL), OPENAI_MODEL, "gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"]
                )
            ),
            index=0,
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Test connection", use_container_width=True):
                st.session_state.session_api_key = key_input.strip()
                if not effective_api_key():
                    st.session_state.connection_status = "❌ Paste an API key first."
                else:
                    try:
                        from finwise.chains import test_api_connection

                        ok, msg = test_api_connection(
                            api_key=effective_api_key(),
                            model=model,
                        )
                        st.session_state.connection_status = (
                            f"✅ {msg}" if ok else f"❌ {friendly_error(Exception(msg))}"
                        )
                    except Exception as exc:  # noqa: BLE001
                        st.session_state.connection_status = f"❌ {friendly_error(exc)}"
        with c2:
            if st.button("Enter FinWise AI", type="primary", use_container_width=True):
                st.session_state.session_api_key = key_input.strip()
                st.session_state.model_name = model
                if not effective_api_key():
                    st.error("Paste your OpenAI API key above to continue.")
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
2. Create a secret key (`sk-…`).
3. Paste it above and click **Enter FinWise AI**.
4. Do not commit keys to GitHub.
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
                Runtime API key
                <span class="mini">Session-only · not stored in Git</span>
              </div>
              <div class="fw-float-card b">
                Educational AI insights
                <span class="mini">LangChain · Structured JSON</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
