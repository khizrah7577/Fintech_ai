"""Application settings, form options, and environment loading."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

APP_NAME = "FinWise AI"
APP_SUBTITLE = "AI-Powered Personal Financial Analysis and Smart Budget Assistant"
APP_TAGLINE = "Clarity for your month — then plan the next one."

# Exact educational disclaimer (assignment + product requirement)
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
SQLITE_CACHE_PATH = str(ROOT_DIR / "finwise_llm_cache.db")

HEALTH_BANDS = [
    (80, 100, "Strong", "strong"),
    (60, 79, "Generally healthy", "healthy"),
    (40, 59, "Needs improvement", "improve"),
    (0, 39, "High attention", "attention"),
]

# Sage + earth palette
COLORS = {
    "bg": "#F5F4ED",
    "sidebar": "#123F38",
    "primary": "#174A40",
    "secondary": "#668A75",
    "sage": "#A3B8A1",
    "light_sage": "#E7EFE8",
    "cream": "#F8F5ED",
    "card": "#FFFFFF",
    "text": "#183D36",
    "muted": "#68776E",
    "border": "#DCE5DC",
    "warm": "#B89C78",
    "danger": "#A94442",
    "warning": "#8A6D3B",
    "success": "#2E6B4F",
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

# Suggested 50/30/20-style educational allocation (needs / wants / savings)
# Mapped loosely onto categories for the Budget Planner defaults.
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
    # Remaining ~10% intended for savings target
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
