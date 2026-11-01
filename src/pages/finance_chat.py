"""Conversational AI Finance Assistant grounded in user data."""

from __future__ import annotations

import html

import streamlit as st

from src.chains import answer_finance_question, build_llm
from src.session import effective_api_key, has_api_key
from src.ui.components import disclaimer_banner, empty_state, page_header
from src.utils import friendly_error

SUGGESTIONS = [
    "Where does most of my money go?",
    "How much can I save next month?",
    "Why is my financial health score low?",
    "How can I reduce my expenses?",
    "How much should I allocate to each category?",
    "Explain my financial risk level.",
    "Summarize my monthly financial situation.",
]


def render_finance_chat() -> None:
    page_header(
        "AI Finance Assistant",
        "Ask questions about your submitted numbers — educational answers only.",
    )
    disclaimer_banner()

    results = st.session_state.get("results")
    analysis = st.session_state.get("analysis")

    if not results:
        empty_state(
            "No financial snapshot yet",
            "Complete Financial Analysis first so the assistant can use your real figures.",
        )
        if st.button("Go to Financial Analysis"):
            st.session_state.page = "analysis"
            st.rerun()
        return

    if not has_api_key():
        st.error("Configure an OpenAI API key in Settings before chatting.")
        return

    top = st.columns([3, 1])
    with top[1]:
        if st.button("New conversation", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

    st.caption("Suggested prompts")
    scols = st.columns(2)
    for i, prompt in enumerate(SUGGESTIONS):
        if scols[i % 2].button(prompt, key=f"sug_{i}", use_container_width=True):
            _ask(prompt, results, analysis)

    for idx, msg in enumerate(st.session_state.chat_messages):
        role = msg["role"]
        css = "fw-chat-user" if role == "user" else "fw-chat-ai"
        safe = html.escape(msg["content"]).replace("\n", "<br>")
        st.markdown(f'<div class="{css}">{safe}</div>', unsafe_allow_html=True)
        if role == "assistant":
            st.download_button(
                "Download reply",
                data=msg["content"],
                file_name=f"finwise_reply_{idx}.txt",
                mime="text/plain",
                key=f"dl_reply_{idx}",
            )

    question = st.chat_input("Ask about your budget…")
    if question:
        _ask(question, results, analysis)


def _ask(question: str, results: dict, analysis: dict | None) -> None:
    st.session_state.chat_messages.append({"role": "user", "content": question})
    with st.spinner("Thinking…"):
        try:
            llm = build_llm(
                api_key=effective_api_key(),
                model=st.session_state.model_name,
                temperature=st.session_state.temperature,
                streaming=False,
            )
            answer = answer_finance_question(
                question, results, analysis, llm=llm
            )
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as exc:  # noqa: BLE001
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": friendly_error(exc)}
            )
    st.rerun()
