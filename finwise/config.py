"""Application settings, form options, and environment loading."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _secret_or_env(name: str, default: str = "") -> str:
    """Prefer Streamlit Cloud secrets, then environment / .env."""
    env_val = (os.getenv(name, default) or default).strip()
    try:
        from streamlit import runtime

        if not runtime.exists():
            return env_val
        import streamlit as st

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
    global OPENAI_API_KEY, OPENAI_MODEL
    OPENAI_API_KEY = _secret_or_env("OPENAI_API_KEY", OPENAI_API_KEY)
    OPENAI_MODEL = _secret_or_env("OPENAI_MODEL", OPENAI_MODEL) or "gpt-4o-mini"


OPENAI_API_KEY = _secret_or_env("OPENAI_API_KEY", "")
OPENAI_MODEL = _secret_or_env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini"

APP_NAME = "FinWise AI"
APP_SUBTITLE = "AI-Powered Personal Financial Analysis and Smart Budget Assistant"
APP_TAGLINE = "Intelligence for every dollar you earn and spend."

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

CATEGORY_ICONS = {
    "housing": "🏠",
    "food": "🛒",
    "transportation": "🚗",
    "utilities": "💡",
    "education": "📚",
    "healthcare": "❤️",
    "entertainment": "🎬",
    "loan_debt": "💳",
    "other": "📦",
    "income": "💰",
    "savings": "🏦",
}

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
SQLITE_CACHE_PATH = str(Path(tempfile.gettempdir()) / "finwise_llm_cache.db")

HEALTH_BANDS = [
    (80, 100, "Strong", "strong"),
    (60, 79, "Generally healthy", "healthy"),
    (40, 59, "Needs improvement", "improve"),
    (0, 39, "High attention", "attention"),
]

# Premium light fintech — navy + emerald + mint/cyan
COLORS = {
    "bg": "#F7FAFC",
    "surface": "#FFFFFF",
    "navy": "#0B1F3A",
    "navy_soft": "#132B4D",
    "primary": "#0F766E",
    "primary_dark": "#0B1F3A",
    "emerald": "#059669",
    "mint": "#D1FAE5",
    "cyan": "#06B6D4",
    "secondary": "#0D9488",
    "accent": "#14B8A6",
    "sage": "#94A3B8",
    "light_sage": "#ECFDF5",
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
    "sidebar": "#0B1F3A",
    "sidebar_soft": "#132B4D",
}

# Horizontal top navigation (primary)
NAV_PAGES = [
    ("dashboard", "Dashboard"),
    ("transactions", "Transactions"),
    ("budget", "Budget Planner"),
    ("analytics", "Financial Analytics"),
    ("chat", "AI Financial Advisor"),
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
