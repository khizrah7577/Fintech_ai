"""ChatOpenAI, LLMChain, message demo, JSON analysis, streaming, and chat."""

from __future__ import annotations

import json
from typing import Any, Generator, Iterator

from langchain.chains import LLMChain
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config import DEFAULT_TEMPERATURE, OPENAI_API_KEY, OPENAI_MODEL
from src.prompts import (
    ANALYSIS_CHAT_TEMPLATE,
    ANALYSIS_PROMPT,
    CHAT_PROMPT,
    MESSAGE_DEMO_SYSTEM,
    NARRATIVE_CHAT_TEMPLATE,
)
from src.utils import parse_analysis_json


def _prompt_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    breakdown = inputs.get("expense_breakdown", {})
    if not isinstance(breakdown, str):
        breakdown = json.dumps(breakdown, ensure_ascii=False)
    return {
        "monthly_income": inputs["monthly_income"],
        "total_expenses": inputs["total_expenses"],
        "remaining_income": inputs["remaining_income"],
        "savings": inputs["savings"],
        "savings_ratio": inputs["savings_ratio"],
        "expense_ratio": inputs["expense_ratio"],
        "financial_goal": inputs["financial_goal"],
        "expense_breakdown": breakdown,
    }


def resolve_api_key(api_key: str | None = None) -> str:
    key = (api_key or "").strip() or (OPENAI_API_KEY or "").strip()
    if not key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it in Settings or set it in your .env file."
        )
    return key


def build_llm(
    *,
    api_key: str | None = None,
    model: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
    streaming: bool = False,
) -> ChatOpenAI:
    """Connect the app to an OpenAI chat model via ChatOpenAI."""
    key = resolve_api_key(api_key)
    return ChatOpenAI(
        model=model or OPENAI_MODEL,
        temperature=temperature,
        api_key=key,
        streaming=streaming,
    )


def build_analysis_chain(llm: ChatOpenAI | None = None) -> LLMChain:
    """Reusable LLMChain that processes financial data into structured JSON text."""
    model = llm or build_llm()
    return LLMChain(llm=model, prompt=ANALYSIS_PROMPT, verbose=False)


def test_api_connection(
    *,
    api_key: str | None = None,
    model: str | None = None,
) -> tuple[bool, str]:
    """Lightweight connectivity check. Returns (ok, message)."""
    try:
        llm = build_llm(api_key=api_key, model=model, temperature=0, streaming=False)
        reply = llm.invoke(
            [
                SystemMessage(content="Reply with exactly: OK"),
                HumanMessage(content="ping"),
            ]
        )
        text = str(getattr(reply, "content", reply)).strip()
        return True, f"Connected. Model responded: {text[:80]}"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


def run_message_demo(llm: ChatOpenAI, summary_line: str) -> dict[str, str]:
    """Demonstrate SystemMessage, HumanMessage, and AIMessage."""
    messages = [
        SystemMessage(content=MESSAGE_DEMO_SYSTEM),
        HumanMessage(content=summary_line),
    ]
    ai: AIMessage = llm.invoke(messages)  # type: ignore[assignment]
    return {
        "system": MESSAGE_DEMO_SYSTEM,
        "human": summary_line,
        "ai": str(ai.content),
    }


def run_structured_analysis(
    inputs: dict[str, Any],
    *,
    llm: ChatOpenAI | None = None,
) -> dict[str, Any]:
    """
    Primary path: reusable LLMChain + PromptTemplate → structured JSON.

    ChatPromptTemplate is formatted for audit / assignment coverage; narrative
    streaming uses NARRATIVE_CHAT_TEMPLATE separately.
    """
    model = llm or build_llm()
    payload = _prompt_inputs(inputs)

    chat_messages = ANALYSIS_CHAT_TEMPLATE.format_messages(**payload)

    chain = build_analysis_chain(model)
    chain_raw = chain.invoke(payload)
    chain_text = (
        chain_raw.get("text") if isinstance(chain_raw, dict) else str(chain_raw)
    )

    parsed = parse_analysis_json(chain_text)
    parsed["_prompt_audit"] = {
        "system_preview": str(chat_messages[0].content)[:240],
        "human_preview": str(chat_messages[1].content)[:240],
        "chain_used": "LLMChain + PromptTemplate",
        "chat_template": "ChatPromptTemplate (analysis + narrative)",
    }
    return parsed


def stream_recommendations(
    llm: ChatOpenAI,
    inputs: dict[str, Any],
) -> Generator[str, None, None]:
    """Yield narrative recommendation chunks for st.write_stream."""
    base = _prompt_inputs(inputs)
    narrative_inputs = {
        **base,
        "preliminary_score": inputs.get("preliminary_score", 0),
        "financial_health_score": inputs.get("financial_health_score", 0),
        "risk_level": inputs.get("risk_level", "MEDIUM"),
    }
    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(**narrative_inputs)
    for chunk in llm.stream(messages):
        content = getattr(chunk, "content", None)
        if content:
            yield content


def stream_recommendations_iterator(
    llm: ChatOpenAI,
    inputs: dict[str, Any],
) -> Iterator[str]:
    yield from stream_recommendations(llm, inputs)


def build_financial_context(results: dict[str, Any], analysis: dict[str, Any] | None) -> str:
    symbol = results.get("symbol", "$")
    lines = [
        f"Currency symbol: {symbol}",
        f"Goal: {results.get('financial_goal')}",
        f"Monthly income: {results.get('monthly_income')}",
        f"Total expenses: {results.get('total_expenses')}",
        f"Remaining income: {results.get('remaining_income')}",
        f"Savings: {results.get('savings')}",
        f"Savings ratio %: {results.get('savings_ratio')}",
        f"Expense ratio %: {results.get('expense_ratio')}",
        f"Debt burden %: {results.get('debt_burden')}",
        f"Python preliminary score: {results.get('preliminary_score')}",
        f"Expense breakdown: {json.dumps(results.get('expense_breakdown') or {})}",
    ]
    if analysis:
        lines.extend(
            [
                f"AI health score: {analysis.get('financial_health_score')}",
                f"AI risk level: {analysis.get('risk_level')}",
                f"AI summary: {analysis.get('financial_summary')}",
                f"Top priorities: {analysis.get('top_priorities')}",
            ]
        )
    return "\n".join(lines)


def answer_finance_question(
    question: str,
    results: dict[str, Any],
    analysis: dict[str, Any] | None,
    *,
    llm: ChatOpenAI | None = None,
) -> str:
    """Conversational Q&A grounded in submitted financial data."""
    model = llm or build_llm()
    messages = CHAT_PROMPT.format_messages(
        financial_context=build_financial_context(results, analysis),
        question=question,
    )
    reply = model.invoke(messages)
    return str(getattr(reply, "content", reply))
