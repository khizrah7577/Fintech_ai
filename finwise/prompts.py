"""Prompt templates, system safety rules, and JSON schema for FinWise AI."""

from __future__ import annotations

import json

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

JSON_SCHEMA = {
    "financial_summary": "",
    "financial_health_score": 0,
    "spending_analysis": [
        {"category": "", "observation": "", "recommendation": ""}
    ],
    "risk_level": "",
    "top_priorities": [],
    "budget_recommendations": [],
    "savings_strategy": [],
    "next_month_action_plan": [],
}

# Escape braces so PromptTemplate does not treat JSON keys as variables.
JSON_SCHEMA_TEXT = json.dumps(JSON_SCHEMA, indent=2).replace("{", "{{").replace("}", "}}")

SYSTEM_SAFETY = """You are FinWise AI, an educational personal-finance assistant.
You help users understand their monthly numbers and suggest budgeting improvements.

HARD RULES (never break these):
- You provide educational information only — never guaranteed investment advice.
- Do not claim any financial outcome is certain or guaranteed.
- Do not encourage illegal activity or reckless debt.
- Do not invent account balances or transactions the user did not provide.
- Do not pretend you have access to bank accounts or external transactions.
- Be clear, practical, and kind. Use the user's currency and goal.
- Always remind (briefly) that this is educational and a professional can help further.

Financial health score bands (educational only):
- 80–100: Strong
- 60–79: Generally healthy
- 40–59: Needs improvement
- Below 40: High attention

Risk level must be one of: LOW, MEDIUM, HIGH.
"""

# Reusable single-string PromptTemplate with required variables
ANALYSIS_PROMPT = PromptTemplate(
    input_variables=[
        "monthly_income",
        "total_expenses",
        "remaining_income",
        "savings",
        "savings_ratio",
        "expense_ratio",
        "financial_goal",
        "expense_breakdown",
    ],
    template=(
        "Analyse this monthly financial snapshot for educational budgeting insights.\n\n"
        "Monthly income: {monthly_income}\n"
        "Total expenses: {total_expenses}\n"
        "Remaining income: {remaining_income}\n"
        "Current savings (this month): {savings}\n"
        "Savings ratio (%): {savings_ratio}\n"
        "Expense ratio (%): {expense_ratio}\n"
        "Financial goal: {financial_goal}\n"
        "Expense breakdown (JSON): {expense_breakdown}\n\n"
        "Return ONLY valid JSON matching this exact schema (no markdown fences):\n"
        f"{JSON_SCHEMA_TEXT}\n\n"
        "Fill spending_analysis with one object per significant expense category. "
        "Use realistic educational recommendations aligned with the goal. "
        "financial_health_score must be an integer 0–100."
    ),
)

# System + Human ChatPromptTemplate
ANALYSIS_CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_SAFETY),
        (
            "human",
            "Here is my monthly financial data. Produce structured educational insights.\n\n"
            "Monthly income: {monthly_income}\n"
            "Total expenses: {total_expenses}\n"
            "Remaining income: {remaining_income}\n"
            "Current savings: {savings}\n"
            "Savings ratio (%): {savings_ratio}\n"
            "Expense ratio (%): {expense_ratio}\n"
            "Financial goal: {financial_goal}\n"
            "Expense breakdown: {expense_breakdown}\n\n"
            "Respond with ONLY valid JSON (no code fences) matching:\n"
            f"{JSON_SCHEMA_TEXT}",
        ),
    ]
)

# Narrative streaming recommendations
NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_SAFETY
            + "\nWrite a short, warm, educational recommendation letter (3–5 short paragraphs). "
            "Do not use JSON. End with one clear next step and a brief educational disclaimer.",
        ),
        (
            "human",
            "Write personalized budgeting recommendations for:\n"
            "Goal: {financial_goal}\n"
            "Income: {monthly_income} | Expenses: {total_expenses} | "
            "Remaining: {remaining_income} | Savings: {savings}\n"
            "Savings ratio: {savings_ratio}% | Expense ratio: {expense_ratio}%\n"
            "Breakdown: {expense_breakdown}\n"
            "Python preliminary score: {preliminary_score}/100\n"
            "AI health score (from prior analysis): {financial_health_score}/100 | "
            "Risk: {risk_level}\n",
        ),
    ]
)

CHAT_SYSTEM = (
    SYSTEM_SAFETY
    + "\nAnswer the user's question using ONLY the financial snapshot provided. "
    "Prefer exact Python-calculated figures from the snapshot. "
    "Keep answers concise (short paragraphs or bullets). Markdown is allowed."
)

CHAT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", CHAT_SYSTEM),
        (
            "human",
            "Financial snapshot (trusted Python calculations):\n{financial_context}\n\n"
            "User question: {question}",
        ),
    ]
)

MESSAGE_DEMO_SYSTEM = (
    "You are FinWise AI. Briefly confirm you understand the user's numbers "
    "and that your role is educational only. One or two sentences."
)
