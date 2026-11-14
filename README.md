# FinWise AI

**AI-Powered Personal Financial Analysis and Smart Budget Assistant**

Premium Streamlit fintech app with horizontal top navigation, KPI dashboards, analytics, budget planner, AI advisor, and reports.

> Educational prototype only. Not financial advice.

**GitHub:** https://github.com/khizrah7577/Fintech_ai

## Pages (top navigation)

1. Dashboard  
2. Transactions (monthly snapshot + transaction list)  
3. Budget Planner  
4. Financial Analytics  
5. AI Financial Advisor  
6. Reports (CSV / PDF)  
7. Settings  

## Run locally

```powershell
cd D:\langchain\Fintech_ai
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Paste your OpenAI API key on the welcome screen (session-only).

## Streamlit Cloud

- Repo: `khizrah7577/Fintech_ai`
- Branch: `main`
- Main file: `app.py`
- Python: **3.12**
- Secrets optional (`OPENAI_API_KEY`) — runtime key also supported

## Package layout

Application code lives in `finwise/` (not `src/`) to avoid Streamlit Cloud’s `/mount/src` path conflict.
