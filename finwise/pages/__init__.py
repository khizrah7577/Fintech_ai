"""FinWise AI page renderers."""

from finwise.pages.analytics import render_analytics
from finwise.pages.budget_planner import render_budget_planner
from finwise.pages.dashboard import render_dashboard
from finwise.pages.finance_chat import render_finance_chat
from finwise.pages.reports import render_reports
from finwise.pages.settings import render_settings
from finwise.pages.transactions import render_transactions
from finwise.pages.welcome import render_welcome

PAGE_RENDERERS = {
    "dashboard": render_dashboard,
    "transactions": render_transactions,
    "budget": render_budget_planner,
    "analytics": render_analytics,
    "chat": render_finance_chat,
    "reports": render_reports,
    "settings": render_settings,
}

__all__ = ["PAGE_RENDERERS", "render_welcome"]
