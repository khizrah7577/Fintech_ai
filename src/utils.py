"""Safe JSON parsing, money helpers, and report export utilities."""

from __future__ import annotations

import csv
import io
import json
import re
from datetime import datetime
from typing import Any

REQUIRED_KEYS = {
    "financial_summary",
    "financial_health_score",
    "spending_analysis",
    "risk_level",
    "top_priorities",
    "budget_recommendations",
    "savings_strategy",
    "next_month_action_plan",
}


def strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def extract_json_object(text: str) -> str | None:
    cleaned = strip_code_fences(text)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return cleaned[start : end + 1]


def parse_analysis_json(raw: str | Any) -> dict[str, Any]:
    """
    Parse LLM JSON safely. Raises ValueError with a clear message on failure.
    Normalizes types for the dashboard — never crashes the UI if callers catch.
    """
    if isinstance(raw, dict):
        data = raw
    else:
        text = str(raw or "").strip()
        if not text:
            raise ValueError("Empty model response — cannot parse JSON.")
        candidate = extract_json_object(text) or strip_code_fences(text)
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON from model: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Model JSON root must be an object.")

    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"JSON missing keys: {sorted(missing)}")

    score = data.get("financial_health_score", 0)
    try:
        score = int(round(float(score)))
    except (TypeError, ValueError):
        score = 0
    data["financial_health_score"] = max(0, min(100, score))

    risk = str(data.get("risk_level", "MEDIUM")).strip().upper()
    if risk not in {"LOW", "MEDIUM", "HIGH"}:
        risk = "MEDIUM"
    data["risk_level"] = risk

    data["financial_summary"] = str(data.get("financial_summary") or "").strip()
    data["spending_analysis"] = _normalize_spending(data.get("spending_analysis"))
    data["top_priorities"] = _as_str_list(data.get("top_priorities"))
    data["budget_recommendations"] = _as_str_list(data.get("budget_recommendations"))
    data["savings_strategy"] = _as_str_list(data.get("savings_strategy"))
    data["next_month_action_plan"] = _as_str_list(data.get("next_month_action_plan"))

    return data


def _normalize_spending(value: Any) -> list[dict[str, str]]:
    items = _as_list(value)
    out: list[dict[str, str]] = []
    for item in items:
        if isinstance(item, dict):
            out.append(
                {
                    "category": str(item.get("category", "")).strip(),
                    "observation": str(item.get("observation", "")).strip(),
                    "recommendation": str(item.get("recommendation", "")).strip(),
                }
            )
        else:
            out.append(
                {
                    "category": "General",
                    "observation": str(item),
                    "recommendation": "",
                }
            )
    return out


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _as_str_list(value: Any) -> list[str]:
    items = _as_list(value)
    return [str(x).strip() for x in items if str(x).strip()]


def format_money(amount: float, symbol: str) -> str:
    sign = "-" if amount < 0 else ""
    return f"{sign}{symbol}{abs(amount):,.2f}"


def friendly_error(exc: Exception) -> str:
    """User-facing error without secrets or stack traces."""
    msg = str(exc).lower()
    raw = str(exc)
    if "api key" in msg or "authentication" in msg or "401" in msg:
        return "API authentication failed. Check your OpenAI API key in Settings."
    if "rate limit" in msg or "429" in msg:
        return "OpenAI rate limit reached. Wait a moment and try again."
    if "timeout" in msg or "connection" in msg or "network" in msg:
        return "Network problem talking to OpenAI. Check your connection and retry."
    if "model" in msg and ("not found" in msg or "does not exist" in msg):
        return "Selected model is unavailable. Choose another model in Settings."
    if "invalid json" in msg or "missing keys" in msg or "empty model" in msg:
        return f"Could not read AI JSON response: {raw}"
    # Truncate unknown errors; never echo full keys
    cleaned = re.sub(r"sk-[A-Za-z0-9_-]+", "sk-***", raw)
    return f"Something went wrong: {cleaned[:240]}"


def build_csv_report(results: dict[str, Any], analysis: dict[str, Any] | None) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["FinWise AI Monthly Report"])
    writer.writerow(["Generated", datetime.now().isoformat(timespec="seconds")])
    writer.writerow([])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Monthly income", results.get("monthly_income")])
    writer.writerow(["Total expenses", results.get("total_expenses")])
    writer.writerow(["Remaining income", results.get("remaining_income")])
    writer.writerow(["Savings", results.get("savings")])
    writer.writerow(["Savings ratio %", results.get("savings_ratio")])
    writer.writerow(["Expense ratio %", results.get("expense_ratio")])
    writer.writerow(["Debt burden %", results.get("debt_burden")])
    writer.writerow(["Python preliminary score", results.get("preliminary_score")])
    if analysis:
        writer.writerow(["AI health score", analysis.get("financial_health_score")])
        writer.writerow(["Risk level", analysis.get("risk_level")])
        writer.writerow(["Summary", analysis.get("financial_summary")])
    writer.writerow([])
    writer.writerow(["Category", "Amount"])
    for k, v in (results.get("expense_breakdown") or {}).items():
        writer.writerow([k, v])
    if analysis:
        writer.writerow([])
        writer.writerow(["Top priorities"])
        for p in analysis.get("top_priorities") or []:
            writer.writerow([p])
        writer.writerow([])
        writer.writerow(["Budget recommendations"])
        for p in analysis.get("budget_recommendations") or []:
            writer.writerow([p])
    return buf.getvalue()


def build_pdf_report(
    results: dict[str, Any],
    analysis: dict[str, Any] | None,
    symbol: str = "$",
) -> bytes:
    """Lightweight PDF via reportlab if available; otherwise raise clear error."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError(
            "PDF export requires reportlab. Install with: pip install reportlab"
        ) from exc

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - inch

    def line(text: str, size: int = 11, gap: float = 16) -> None:
        nonlocal y
        if y < inch:
            c.showPage()
            y = height - inch
        c.setFont("Helvetica", size)
        c.drawString(inch, y, text[:110])
        y -= gap

    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, y, "FinWise AI — Monthly Financial Summary")
    y -= 22
    line(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 9, 14)
    line("Educational prototype only — not financial advice.", 9, 18)
    line(f"Income: {format_money(results.get('monthly_income', 0), symbol)}")
    line(f"Expenses: {format_money(results.get('total_expenses', 0), symbol)}")
    line(f"Remaining: {format_money(results.get('remaining_income', 0), symbol)}")
    line(f"Savings: {format_money(results.get('savings', 0), symbol)}")
    line(f"Python score: {results.get('preliminary_score')}/100")
    if analysis:
        line(f"AI score: {analysis.get('financial_health_score')}/100")
        line(f"Risk: {analysis.get('risk_level')}")
        y -= 6
        line("Summary:", 11, 14)
        for chunk in _wrap(str(analysis.get("financial_summary") or ""), 90):
            line(chunk, 10, 13)
        y -= 4
        line("Priorities:", 11, 14)
        for p in analysis.get("top_priorities") or []:
            line(f"- {p}", 10, 13)
    c.save()
    return buffer.getvalue()


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]
