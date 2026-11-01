# FinWise AI — Assignment Compliance Report

Generated after implementation and automated testing of deterministic modules.

## Rubric mapping (100 marks)

| Criterion | Marks | Status | Evidence |
|-----------|------:|--------|----------|
| Streamlit UI and UX | 15 | **Implemented** | Multi-page sage UI (`app.py`, `src/pages/*`, `src/ui/*`). Welcome screen, dashboard, forms, charts, disclaimers. Visual QA in browser not run in this session. |
| Financial calculations | 10 | **Implemented + tested** | `src/financial_calculator.py`; `tests/test_financial_calculator.py` — all 5 scenarios passed. |
| ChatOpenAI integration | 10 | **Implemented** | `src/chains.py` → `build_llm()` / `ChatOpenAI`. Live API call depends on valid `.env` key (not invoked in CI-style test). |
| PromptTemplate | 10 | **Implemented + tested** | `ANALYSIS_PROMPT` with required 8 variables (asserted in tests). |
| ChatPromptTemplate + messages | 10 | **Implemented** | `ANALYSIS_CHAT_TEMPLATE`, `NARRATIVE_CHAT_TEMPLATE`; optional System/Human/AI demo on Analysis page. |
| LLMChain | 10 | **Implemented** | `build_analysis_chain()` + `run_structured_analysis()` using LangChain 0.3 `LLMChain`. |
| Structured JSON output | 10 | **Implemented + tested** | Exact schema in `prompts.py`; `parse_analysis_json` validated in tests. |
| Streaming | 10 | **Implemented** | `stream_recommendations()` + `st.write_stream` on Analysis page. Live stream requires API. |
| Caching | 10 | **Implemented** | `InMemoryCache` + `SQLiteCache` via `set_llm_cache`; Settings toggle; reuse-safe across reruns. |
| Code quality & docs | 5 | **Implemented** | Modular `src/`, README, `.env.example`, compliance doc, tests. |

## Five scenarios (Python)

| # | Result | Verified |
|---|--------|----------|
| 1 Income 8000 / expenses 2000 | Remaining 6000; score ≥70; LOW risk | Pass |
| 2 Income 2000 / expenses 2600 | Remaining −600; expense ratio 130%; HIGH | Pass |
| 3 Income 5000 / debt 2500 | Debt burden 50%; MEDIUM/HIGH | Pass |
| 4 Income 4000 / savings 1200 | Savings ratio 30%; score ≥60 | Pass |
| 5 Income 3000 / expenses 3000 | Remaining 0; expense ratio 100% | Pass |

## Live OpenAI integrations

Not exercised in automated tests (avoids spending tokens / leaking keys). Untested live paths:

- End-to-end `LLMChain` invoke with a real model  
- Real `st.write_stream` typing effect  
- Chat assistant replies  
- Settings “Test connection” against OpenAI  

**How to verify live:** set `.env` → `streamlit run app.py` → Financial Analysis → Analyse My Finances.

## Design / product extras (beyond rubric)

- Welcome / API configuration screen  
- AI Finance Assistant chat  
- Budget Planner with adjustable targets  
- Insights + Reports (CSV/PDF)  
- Session API-key override + confirmed reset  

These do **not** replace assignment requirements; they wrap them.
