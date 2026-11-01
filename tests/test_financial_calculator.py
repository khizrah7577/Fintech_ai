"""Deterministic tests for the five assignment scenarios (no API)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.financial_calculator import calculate_financials, infer_risk_from_metrics
from src.prompts import ANALYSIS_PROMPT
from src.utils import parse_analysis_json


def _base_expenses(**overrides):
    data = {
        "housing": 0.0,
        "food": 0.0,
        "transportation": 0.0,
        "utilities": 0.0,
        "education": 0.0,
        "healthcare": 0.0,
        "entertainment": 0.0,
        "loan_debt": 0.0,
        "other": 0.0,
    }
    data.update(overrides)
    return data


def test_scenario_1_strong_surplus():
    # Income 8000, expenses ~2000
    expenses = _base_expenses(
        housing=900, food=400, transportation=200, utilities=150,
        education=50, healthcare=100, entertainment=100, loan_debt=50, other=50,
    )
    r = calculate_financials(8000, expenses, savings=1500)
    assert r["total_expenses"] == 2000
    assert r["remaining_income"] == 6000
    assert r["preliminary_score"] >= 70
    assert infer_risk_from_metrics(r) == "LOW"


def test_scenario_2_overspend():
    # Income 2000, expenses ~2600 → remaining -600, expense ratio 130%
    expenses = _base_expenses(
        housing=1000, food=500, transportation=300, utilities=200,
        education=100, healthcare=100, entertainment=200, loan_debt=100, other=100,
    )
    r = calculate_financials(2000, expenses, savings=0)
    assert r["total_expenses"] == 2600
    assert r["remaining_income"] == -600
    assert abs(r["expense_ratio"] - 130.0) < 0.01
    assert r["preliminary_score"] < 50
    assert infer_risk_from_metrics(r) == "HIGH"


def test_scenario_3_high_debt():
    expenses = _base_expenses(
        housing=1000, food=400, transportation=200, utilities=150,
        education=50, healthcare=100, entertainment=100, loan_debt=2500, other=50,
    )
    r = calculate_financials(5000, expenses, savings=200)
    assert r["debt_burden"] == 50.0
    assert infer_risk_from_metrics(r) in {"MEDIUM", "HIGH"}


def test_scenario_4_strong_savings_ratio():
    expenses = _base_expenses(
        housing=1000, food=400, transportation=200, utilities=150,
        education=50, healthcare=100, entertainment=100, loan_debt=100, other=100,
    )
    r = calculate_financials(4000, expenses, savings=1200)
    assert abs(r["savings_ratio"] - 30.0) < 0.01
    assert r["preliminary_score"] >= 60


def test_scenario_5_zero_remaining():
    expenses = _base_expenses(
        housing=1200, food=500, transportation=300, utilities=200,
        education=100, healthcare=150, entertainment=150, loan_debt=300, other=100,
    )
    r = calculate_financials(3000, expenses, savings=0)
    assert r["total_expenses"] == 3000
    assert r["remaining_income"] == 0
    assert abs(r["expense_ratio"] - 100.0) < 0.01
    assert infer_risk_from_metrics(r) in {"MEDIUM", "HIGH"}


def test_zero_income_guard():
    r = calculate_financials(0, _base_expenses(housing=100), savings=10)
    assert r["savings_ratio"] == 0
    assert r["expense_ratio"] == 0


def test_prompt_variables():
    required = {
        "monthly_income",
        "total_expenses",
        "remaining_income",
        "savings",
        "savings_ratio",
        "expense_ratio",
        "financial_goal",
        "expense_breakdown",
    }
    assert required == set(ANALYSIS_PROMPT.input_variables)


def test_json_parser():
    raw = """
    ```json
    {
      "financial_summary": "ok",
      "financial_health_score": 88,
      "spending_analysis": [{"category": "food", "observation": "a", "recommendation": "b"}],
      "risk_level": "low",
      "top_priorities": ["one"],
      "budget_recommendations": ["two"],
      "savings_strategy": ["three"],
      "next_month_action_plan": ["four"]
    }
    ```
    """
    data = parse_analysis_json(raw)
    assert data["financial_health_score"] == 88
    assert data["risk_level"] == "LOW"


if __name__ == "__main__":
    test_scenario_1_strong_surplus()
    test_scenario_2_overspend()
    test_scenario_3_high_debt()
    test_scenario_4_strong_savings_ratio()
    test_scenario_5_zero_remaining()
    test_zero_income_guard()
    test_prompt_variables()
    test_json_parser()
    print("All calculator / parser tests passed.")
