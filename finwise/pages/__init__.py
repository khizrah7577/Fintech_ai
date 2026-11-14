"""FinWise AI page renderers."""

from finwise.pages.budget_planner import render_budget_planner
from finwise.pages.dashboard import render_dashboard
from finwise.pages.finance_chat import render_finance_chat
from finwise.pages.financial_analysis import render_financial_analysis
from finwise.pages.insights import render_insights
from finwise.pages.reports import render_reports
from finwise.pages.settings import render_settings
from finwise.pages.welcome import render_welcome

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
