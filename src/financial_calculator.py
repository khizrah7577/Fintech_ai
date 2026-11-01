"""Deterministic financial maths — no AI calls."""

from __future__ import annotations

from typing import Any

from src.config import BUDGET_GUIDELINES, EXPENSE_CATEGORIES


def safe_ratio(numerator: float, denominator: float) -> float:
    """Return percentage ratio; guard divide-by-zero when income is 0."""
    if denominator <= 0:
        return 0.0
    return (numerator / denominator) * 100.0


def validate_inputs(
    monthly_income: float,
    expenses: dict[str, float],
    savings: float,
) -> list[str]:
    """Return a list of validation warnings/errors (empty = ok)."""
    issues: list[str] = []
    try:
        income = float(monthly_income)
    except (TypeError, ValueError):
        return ["Monthly income must be a number."]

    if income < 0:
        issues.append("Monthly income cannot be negative.")
    if income == 0:
        issues.append("Income is zero — ratios will be 0% and scores will be limited.")

    try:
        sav = float(savings)
    except (TypeError, ValueError):
        issues.append("Savings must be a number.")
        sav = 0.0
    if sav < 0:
        issues.append("Savings cannot be negative.")

    for key, label in EXPENSE_CATEGORIES:
        raw = expenses.get(key, 0)
        try:
            val = float(raw)
        except (TypeError, ValueError):
            issues.append(f"{label} must be a number.")
            continue
        if val < 0:
            issues.append(f"{label} cannot be negative.")

    if income > 0 and sav > income * 2:
        issues.append(
            "Savings are unusually high relative to monthly income — "
            "confirm the figure is this month's contribution, not total wealth."
        )
    return issues


def calculate_financials(
    monthly_income: float,
    expenses: dict[str, float],
    savings: float,
) -> dict[str, Any]:
    """
    Compute totals, ratios, and a rule-based preliminary score (0–100).

    Required formulas:
      total_expenses = sum(all expense categories)
      remaining_income = monthly_income - total_expenses
      savings_ratio = (savings / monthly_income) * 100 if income > 0 else 0
      expense_ratio = (total_expenses / monthly_income) * 100 if income > 0 else 0

    Same inputs always produce the same outputs.
    """
    expense_values = {k: max(0.0, float(v or 0)) for k, v in expenses.items()}
    # Ensure all known categories exist
    for key, _ in EXPENSE_CATEGORIES:
        expense_values.setdefault(key, 0.0)

    income = max(0.0, float(monthly_income or 0))
    savings_amt = max(0.0, float(savings or 0))

    total_expenses = sum(expense_values.values())
    remaining_income = income - total_expenses
    savings_ratio = (savings_amt / income) * 100 if income > 0 else 0.0
    expense_ratio = (total_expenses / income) * 100 if income > 0 else 0.0

    debt = float(expense_values.get("loan_debt", 0) or 0)
    debt_burden = safe_ratio(debt, income) if income > 0 else (100.0 if debt > 0 else 0.0)

    preliminary_score = compute_preliminary_score(
        savings_ratio=savings_ratio,
        remaining_income=remaining_income,
        income=income,
        expense_ratio=expense_ratio,
        debt_burden=debt_burden,
    )

    ranked = sorted(expense_values.items(), key=lambda x: x[1], reverse=True)
    top_categories = [{"category": k, "amount": v} for k, v in ranked if v > 0]
    highest = top_categories[0] if top_categories else None

    budget_util = min(100.0, expense_ratio) if income > 0 else 0.0
    savings_progress = min(100.0, savings_ratio / 20.0 * 100.0) if income > 0 else 0.0

    return {
        "monthly_income": income,
        "expenses": expense_values,
        "total_expenses": round(total_expenses, 2),
        "remaining_income": round(remaining_income, 2),
        "savings": savings_amt,
        "savings_ratio": round(savings_ratio, 2),
        "expense_ratio": round(expense_ratio, 2),
        "debt_burden": round(debt_burden, 2),
        "preliminary_score": preliminary_score,
        "top_categories": top_categories,
        "highest_expense": highest,
        "budget_utilization": round(budget_util, 2),
        "savings_progress_to_20pct": round(savings_progress, 2),
        "expense_breakdown": expense_values,
    }


def compute_preliminary_score(
    *,
    savings_ratio: float,
    remaining_income: float,
    income: float,
    expense_ratio: float,
    debt_burden: float,
) -> int:
    """
    Weighted 0–100 heuristic (Python only — not from the LLM):
    - Savings habit ............. 30 pts
    - Leftover / cash-flow ...... 30 pts
    - Expense ratio ............. 25 pts
    - Debt burden ............... 15 pts
    """
    if savings_ratio >= 20:
        savings_pts = 30.0
    elif savings_ratio >= 10:
        savings_pts = 22.0
    elif savings_ratio >= 5:
        savings_pts = 14.0
    elif savings_ratio > 0:
        savings_pts = 8.0
    else:
        savings_pts = 0.0

    if income <= 0:
        leftover_pts = 0.0 if remaining_income <= 0 else 10.0
    else:
        leftover_pct = (remaining_income / income) * 100.0
        if leftover_pct >= 20:
            leftover_pts = 30.0
        elif leftover_pct >= 10:
            leftover_pts = 24.0
        elif leftover_pct >= 0:
            leftover_pts = 16.0
        elif leftover_pct >= -10:
            leftover_pts = 6.0
        else:
            leftover_pts = 0.0

    if expense_ratio <= 50:
        expense_pts = 25.0
    elif expense_ratio <= 70:
        expense_pts = 20.0
    elif expense_ratio <= 90:
        expense_pts = 12.0
    elif expense_ratio <= 100:
        expense_pts = 6.0
    else:
        expense_pts = 0.0

    if debt_burden <= 10:
        debt_pts = 15.0
    elif debt_burden <= 20:
        debt_pts = 11.0
    elif debt_burden <= 35:
        debt_pts = 6.0
    elif debt_burden <= 50:
        debt_pts = 3.0
    else:
        debt_pts = 0.0

    score = int(round(savings_pts + leftover_pts + expense_pts + debt_pts))
    return max(0, min(100, score))


def recommend_budget_allocation(monthly_income: float) -> dict[str, float]:
    """Educational category limits based on guideline shares of income."""
    income = max(0.0, float(monthly_income or 0))
    return {
        key: round(income * share, 2) for key, share in BUDGET_GUIDELINES.items()
    }


def recalculate_budget(
    monthly_income: float,
    current_expenses: dict[str, float],
    targets: dict[str, float],
    savings_target: float,
) -> dict[str, Any]:
    """Compare current spend vs adjustable category targets."""
    income = max(0.0, float(monthly_income or 0))
    current = {k: max(0.0, float(v or 0)) for k, v in current_expenses.items()}
    planned = {k: max(0.0, float(v or 0)) for k, v in targets.items()}
    sav_target = max(0.0, float(savings_target or 0))

    total_current = sum(current.values())
    total_planned = sum(planned.values())
    remaining_after_plan = income - total_planned - sav_target

    warnings: list[str] = []
    for key, label in EXPENSE_CATEGORIES:
        cur = current.get(key, 0.0)
        tgt = planned.get(key, 0.0)
        if cur > tgt > 0:
            warnings.append(
                f"{label}: spending {cur:.2f} exceeds target {tgt:.2f}."
            )
    if remaining_after_plan < 0:
        warnings.append(
            "Planned expenses + savings target exceed monthly income."
        )
    if income > 0 and sav_target / income < 0.10:
        warnings.append(
            "Educational tip: many planners aim for ~10–20% toward savings."
        )

    return {
        "monthly_income": income,
        "total_current_expenses": round(total_current, 2),
        "total_planned_expenses": round(total_planned, 2),
        "savings_target": round(sav_target, 2),
        "remaining_after_plan": round(remaining_after_plan, 2),
        "targets": planned,
        "current": current,
        "warnings": warnings,
        "overspend_categories": [
            k
            for k, _ in EXPENSE_CATEGORIES
            if current.get(k, 0) > planned.get(k, 0) > 0
            or (current.get(k, 0) > planned.get(k, 0) and planned.get(k, 0) == 0 and current.get(k, 0) > 0)
        ],
    }


def infer_risk_from_metrics(calc: dict[str, Any]) -> str:
    """Rule-based educational risk hint (complements AI risk_level)."""
    if calc["remaining_income"] < 0 or calc["expense_ratio"] > 110:
        return "HIGH"
    if calc["debt_burden"] >= 35 or calc["expense_ratio"] >= 95:
        return "HIGH"
    if calc["debt_burden"] >= 20 or calc["expense_ratio"] >= 80 or calc["remaining_income"] == 0:
        return "MEDIUM"
    if calc["preliminary_score"] >= 70:
        return "LOW"
    return "MEDIUM"
