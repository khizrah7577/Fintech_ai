"""Modern fintech SaaS theme — navy sidebar, clean cards, scoped CSS only."""

from __future__ import annotations

import streamlit as st

from finwise.config import COLORS


def inject_global_styles() -> None:
    c = COLORS
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Instrument+Sans:wght@500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
  font-family: 'DM Sans', sans-serif;
  color: {c['text']};
}}

.stApp {{
  background:
    radial-gradient(ellipse 70% 40% at 100% -10%, rgba(27,77,255,0.08) 0%, transparent 50%),
    radial-gradient(ellipse 50% 30% at 0% 0%, rgba(99,102,241,0.06) 0%, transparent 45%),
    {c['bg']};
}}

[data-testid="stHeader"] {{
  background: rgba(244, 246, 249, 0.85);
  backdrop-filter: blur(8px);
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, {c['sidebar']} 0%, {c['sidebar_soft']} 55%, #0A1020 100%);
  border-right: 1px solid rgba(148, 163, 184, 0.12);
}}
section[data-testid="stSidebar"] .fw-side-brand {{
  font-family: 'Instrument Sans', 'DM Sans', sans-serif;
  font-size: 1.55rem;
  font-weight: 700;
  color: #F8FAFC;
  margin: 0;
  letter-spacing: -0.03em;
}}
section[data-testid="stSidebar"] .fw-side-sub {{
  color: #94A3B8;
  font-size: 0.78rem;
  margin: 0.25rem 0 1rem 0;
  line-height: 1.35;
}}
section[data-testid="stSidebar"] .fw-nav-active {{
  display: block;
  background: rgba(27, 77, 255, 0.22);
  border: 1px solid rgba(59, 130, 246, 0.35);
  border-radius: 10px;
  padding: 0.55rem 0.75rem;
  color: #E0E7FF !important;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.35rem;
}}
section[data-testid="stSidebar"] .fw-side-disclaimer {{
  color: #94A3B8;
  font-size: 0.72rem;
  line-height: 1.4;
}}
section[data-testid="stSidebar"] label {{
  color: #CBD5E1 !important;
}}
section[data-testid="stSidebar"] div[data-baseweb="radio"] label p {{
  color: #E2E8F0 !important;
}}
section[data-testid="stSidebar"] .stCaption {{
  color: #94A3B8 !important;
}}
section[data-testid="stSidebar"] .stButton > button {{
  background: rgba(27, 77, 255, 0.15);
  color: #E0E7FF !important;
  border: 1px solid rgba(59, 130, 246, 0.35);
  border-radius: 10px;
  font-weight: 600;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
  background: rgba(27, 77, 255, 0.28);
  border-color: {c['secondary']};
}}

.fw-page-title {{
  font-family: 'Instrument Sans', 'DM Sans', sans-serif;
  font-size: clamp(1.75rem, 3vw, 2.35rem);
  font-weight: 700;
  color: {c['primary_dark']};
  margin: 0 0 0.2rem 0;
  letter-spacing: -0.03em;
  line-height: 1.15;
}}
.fw-page-sub {{
  color: {c['muted']};
  margin: 0 0 1rem 0;
  font-size: 1rem;
}}

.fw-disclaimer {{
  background: linear-gradient(90deg, #EEF2FF, #F8FAFC);
  border-left: 3px solid {c['primary']};
  border-radius: 0 12px 12px 0;
  padding: 0.75rem 1rem;
  color: {c['text']};
  font-size: 0.86rem;
  margin: 0.4rem 0 1.1rem 0;
  border: 1px solid {c['border']};
  border-left-width: 3px;
}}

.fw-card {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 16px;
  padding: 1.15rem 1.25rem;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}}

.fw-metric {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 16px;
  padding: 1rem 1.1rem;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}}
@media (prefers-reduced-motion: no-preference) {{
  .fw-metric:hover {{
    transform: translateY(-3px);
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
  }}
}}
.fw-metric .label {{
  color: {c['muted']};
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}
.fw-metric .value {{
  font-family: 'Instrument Sans', 'DM Sans', sans-serif;
  font-size: 1.55rem;
  font-weight: 700;
  color: {c['primary_dark']};
  margin-top: 0.25rem;
}}
.fw-metric .delta {{
  font-size: 0.8rem;
  color: {c['secondary']};
  margin-top: 0.2rem;
}}
.fw-metric .delta.pos {{ color: {c['positive']}; }}
.fw-metric .delta.neg {{ color: {c['negative']}; }}

.fw-risk-LOW {{ color: {c['positive']}; font-weight: 700; }}
.fw-risk-MEDIUM {{ color: {c['warning']}; font-weight: 700; }}
.fw-risk-HIGH {{ color: {c['negative']}; font-weight: 700; }}

.fw-empty {{
  background: linear-gradient(145deg, #FFFFFF, #EEF2FF);
  border: 1px dashed #C7D2FE;
  border-radius: 18px;
  padding: 2.2rem 1.5rem;
  text-align: center;
  color: {c['text']};
}}
.fw-empty h3 {{
  font-family: 'Instrument Sans', sans-serif;
  color: {c['primary_dark']};
  margin-bottom: 0.4rem;
}}

.fw-welcome-card {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 20px;
  padding: 1.85rem 1.7rem;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}}
.fw-illus {{
  position: relative;
  height: 100%;
  min-height: 420px;
  border-radius: 22px;
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 30%, rgba(59,130,246,0.35), transparent 40%),
    radial-gradient(circle at 80% 20%, rgba(99,102,241,0.3), transparent 35%),
    linear-gradient(160deg, #0B1220 0%, #121A2B 45%, #1E293B 100%);
}}
.fw-illus .orb {{
  position: absolute;
  border-radius: 50%;
  background: rgba(248, 250, 252, 0.08);
  border: 1px solid rgba(248, 250, 252, 0.12);
}}
.fw-illus .orb-a {{ width: 160px; height: 160px; top: 12%; left: 10%; }}
.fw-illus .orb-b {{ width: 90px; height: 90px; top: 55%; right: 18%; }}
.fw-illus .orb-c {{ width: 50px; height: 50px; bottom: 18%; left: 35%; }}
@media (prefers-reduced-motion: no-preference) {{
  .fw-illus .orb-a {{ animation: fw-float 7s ease-in-out infinite; }}
  .fw-illus .orb-b {{ animation: fw-float 5.5s ease-in-out infinite reverse; }}
  .fw-illus .orb-c {{ animation: fw-float 6.2s ease-in-out infinite; }}
}}
@keyframes fw-float {{
  0%, 100% {{ transform: translateY(0); }}
  50% {{ transform: translateY(-12px); }}
}}
.fw-float-card {{
  position: absolute;
  background: rgba(255,255,255,0.96);
  color: {c['primary_dark']};
  border-radius: 14px;
  padding: 0.75rem 0.95rem;
  box-shadow: 0 12px 28px rgba(0,0,0,0.18);
  font-size: 0.85rem;
  font-weight: 600;
}}
.fw-float-card.a {{ top: 22%; right: 12%; }}
.fw-float-card.b {{ bottom: 22%; left: 12%; }}
.fw-float-card .mini {{
  display: block;
  font-size: 0.72rem;
  color: {c['muted']};
  font-weight: 500;
  margin-top: 0.15rem;
}}
.fw-botanic {{
  position: absolute;
  bottom: -20px;
  right: -10px;
  width: 180px;
  height: 180px;
  border-radius: 50% 50% 40% 60%;
  background: radial-gradient(circle at 40% 40%, rgba(59,130,246,0.45), transparent 70%);
  opacity: 0.55;
}}

.fw-chat-user {{
  background: linear-gradient(135deg, {c['primary']}, {c['accent']});
  color: #F8FAFC;
  border-radius: 16px 16px 4px 16px;
  padding: 0.85rem 1.05rem;
  margin: 0.45rem 0 0.45rem 18%;
  box-shadow: 0 8px 18px rgba(27, 77, 255, 0.18);
}}
.fw-chat-ai {{
  background: {c['card']};
  border: 1px solid {c['border']};
  color: {c['text']};
  border-radius: 16px 16px 16px 4px;
  padding: 0.85rem 1.05rem;
  margin: 0.45rem 18% 0.45rem 0;
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
}}

div[data-testid="stMetric"] {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 16px;
  padding: 0.85rem 1rem;
}}

.stButton > button[kind="primary"],
.stFormSubmitButton > button {{
  background: linear-gradient(135deg, {c['primary']}, {c['accent']}) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  box-shadow: 0 8px 20px rgba(27, 77, 255, 0.22);
}}

@media (max-width: 768px) {{
  .fw-chat-user, .fw-chat-ai {{ margin-left: 0; margin-right: 0; }}
  .fw-illus {{ min-height: 280px; }}
}}
</style>
        """,
        unsafe_allow_html=True,
    )
