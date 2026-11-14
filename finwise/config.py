"""Application settings, form options, and environment loading."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _secret_or_env(name: str, default: str = "") -> str:
    """Prefer Streamlit Cloud secrets, then environment / .env.

    Never crash when secrets.toml is missing — Streamlit raises on bare
    `st.secrets` access when no secrets are configured.
    """
    env_val = (os.getenv(name, default) or default).strip()
    try:
        from streamlit import runtime

        if not runtime.exists():
            return env_val
        import streamlit as st

        # Any access to st.secrets can raise if no secrets are configured.
        try:
            value = st.secrets[name]  # type: ignore[index]
        except Exception:
            return env_val
        if value is not None and str(value).strip():
            return str(value).strip()
    except Exception:
        pass
    return env_val


def refresh_secrets_from_streamlit() -> None:
    """Reload API settings after Streamlit is running (optional)."""
    global OPENAI_API_KEY, OPENAI_MODEL
    OPENAI_API_KEY = _secret_or_env("OPENAI_API_KEY", OPENAI_API_KEY)
    OPENAI_MODEL = _secret_or_env("OPENAI_MODEL", OPENAI_MODEL) or "gpt-4o-mini"


OPENAI_API_KEY = _secret_or_env("OPENAI_API_KEY", "")
OPENAI_MODEL = _secret_or_env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini"

APP_NAME = "FinWise AI"
APP_SUBTITLE = "AI-Powered Personal Financial Analysis and Smart Budget Assistant"
APP_TAGLINE = "Clarity for your month — then plan the next one."

EDUCATIONAL_DISCLAIMER = (
    "Educational prototype only. FinWise AI does not provide guaranteed investment "
    "advice, execute financial transactions, or connect to real bank accounts. "
    "Insights are for informational purposes only. Consult a qualified financial "
    "professional before making money decisions."
)
DISCLAIMER_COMPACT = (
    "Educational prototype only — not financial advice. No bank connections or guaranteed outcomes."
)

EXPENSE_CATEGORIES = [
    ("housing", "Housing / Rent"),
    ("food", "Food & Groceries"),
    ("transportation", "Transportation"),
    ("utilities", "Utilities"),
    ("education", "Education"),
    ("healthcare", "Healthcare"),
    ("entertainment", "Entertainment"),
    ("loan_debt", "Loan / Debt"),
    ("other", "Other"),
]

FINANCIAL_GOALS = [
    "Save money",
    "Emergency fund",
    "Pay off debt",
    "Vacation",
    "Start a business",
    "Improve budgeting",
]

CURRENCIES = [
    ("USD", "$"),
    ("EUR", "€"),
    ("GBP", "£"),
    ("PKR", "Rs"),
    ("INR", "₹"),
    ("AED", "AED"),
]

CACHE_OPTIONS = {
    "In-memory (fast, session only)": "memory",
    "SQLite (persists across restarts)": "sqlite",
}

SUPPORTED_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4.1-mini",
    "gpt-4.1",
    "gpt-3.5-turbo",
]

DEFAULT_TEMPERATURE = 0.3

# Prefer temp dir on Streamlit Cloud (safer write permissions)
SQLITE_CACHE_PATH = str(Path(tempfile.gettempdir()) / "finwise_llm_cache.db")

HEALTH_BANDS = [
    (80, 100, "Strong", "strong"),
    (60, 79, "Generally healthy", "healthy"),
    (40, 59, "Needs improvement", "improve"),
    (0, 39, "High attention", "attention"),
]

# Modern fintech SaaS palette — navy / charcoal / blue accents
COLORS = {
    "bg": "#F4F6F9",
    "sidebar": "#0B1220",
    "sidebar_soft": "#121A2B",
    "primary": "#1B4DFF",
    "primary_dark": "#0F1C3F",
    "secondary": "#3B82F6",
    "accent": "#6366F1",
    "sage": "#94A3B8",
    "light_sage": "#E8EEF7",
    "cream": "#F8FAFC",
    "card": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#64748B",
    "border": "#E2E8F0",
    "warm": "#F59E0B",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "success": "#10B981",
    "positive": "#059669",
    "negative": "#DC2626",
}

NAV_PAGES = [
    ("dashboard", "Home / Dashboard"),
    ("analysis", "Financial Analysis"),
    ("chat", "AI Finance Assistant"),
    ("budget", "Budget Planner"),
    ("insights", "Financial Insights"),
    ("reports", "Reports"),
    ("settings", "Settings"),
]

BUDGET_GUIDELINES = {
    "housing": 0.30,
    "food": 0.12,
    "transportation": 0.10,
    "utilities": 0.06,
    "education": 0.04,
    "healthcare": 0.05,
    "entertainment": 0.08,
    "loan_debt": 0.10,
    "other": 0.05,
}


def currency_symbol(code: str) -> str:
    for c, symbol in CURRENCIES:
        if c == code:
            return symbol
    return code


def health_band_label(score: int) -> str:
    for low, high, label, _ in HEALTH_BANDS:
        if low <= score <= high:
            return label
    return "Unknown"


def mask_api_key(key: str) -> str:
    if not key:
        return "(not set)"
    if len(key) <= 8:
        return "••••••••"
    return f"{key[:4]}…{key[-4:]}"
