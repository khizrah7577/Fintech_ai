"""FinWise AI page renderers."""

from src.pages.budget_planner import render_budget_planner
from src.pages.dashboard import render_dashboard
from src.pages.finance_chat import render_finance_chat
from src.pages.financial_analysis import render_financial_analysis
from src.pages.insights import render_insights
from src.pages.reports import render_reports
from src.pages.settings import render_settings
from src.pages.welcome import render_welcome

PAGE_RENDERERS = {
    "dashboard": render_dashboard,
    "analysis": render_financial_analysis,
    "chat": render_finance_chat,
    "budget": render_budget_planner,
    "insights": render_insights,
    "reports": render_reports,
    "settings": render_settings,
}

__all__ = ["PAGE_RENDERERS", "render_welcome"]
