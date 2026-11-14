"""Premium light fintech theme with top navigation — navy / emerald / mint."""

from __future__ import annotations

import streamlit as st

from finwise.config import COLORS


def inject_global_styles() -> None:
    c = COLORS
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
  font-family: 'DM Sans', sans-serif;
  color: {c['text']};
}}

.stApp {{
  background:
    radial-gradient(ellipse 60% 35% at 100% 0%, rgba(6,182,212,0.08) 0%, transparent 50%),
    radial-gradient(ellipse 50% 30% at 0% 0%, rgba(16,185,129,0.07) 0%, transparent 45%),
    {c['bg']};
}}

[data-testid="stHeader"] {{ background: transparent; }}

/* Hide default sidebar chrome — top nav is primary */
section[data-testid="stSidebar"] {{
  display: none !important;
}}
[data-testid="stSidebarCollapsedControl"] {{
  display: none !important;
}}
.stApp > header {{
  background: transparent;
}}

/* Top navigation */
.fw-topnav {{
  position: sticky;
  top: 0;
  z-index: 100;
  margin: -1rem -1rem 1.25rem -1rem;
  padding: 0.85rem 1.5rem;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid {c['border']};
  box-shadow: 0 4px 24px rgba(11, 31, 58, 0.04);
}}
.fw-topnav-inner {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
}}
.fw-brand {{
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
}}
.fw-logo-mark {{
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, {c['navy']} 0%, {c['emerald']} 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  font-size: 0.95rem;
  letter-spacing: -0.02em;
}}
.fw-brand-name {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  font-size: 1.15rem;
  color: {c['navy']};
  letter-spacing: -0.03em;
}}
.fw-brand-name span {{
  color: {c['emerald']};
}}
.fw-nav-links {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  align-items: center;
}}
.fw-nav-chip {{
  font-size: 0.82rem;
  font-weight: 600;
  color: {c['muted']};
  padding: 0.45rem 0.75rem;
  border-radius: 999px;
  border: 1px solid transparent;
  transition: all 0.15s ease;
  white-space: nowrap;
}}
.fw-nav-chip.active {{
  color: {c['navy']};
  background: {c['mint']};
  border-color: #A7F3D0;
}}
.fw-profile {{
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.35rem 0.65rem 0.35rem 0.35rem;
  border-radius: 999px;
  border: 1px solid {c['border']};
  background: #fff;
}}
.fw-avatar {{
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, {c['cyan']}, {c['emerald']});
  color: #fff;
  font-size: 0.7rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.fw-profile-meta {{
  font-size: 0.75rem;
  color: {c['muted']};
  line-height: 1.2;
}}
.fw-profile-meta strong {{
  display: block;
  color: {c['navy']};
  font-size: 0.8rem;
}}

.fw-page-title {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: clamp(1.6rem, 2.8vw, 2.1rem);
  font-weight: 800;
  color: {c['navy']};
  margin: 0 0 0.2rem 0;
  letter-spacing: -0.03em;
}}
.fw-page-sub {{
  color: {c['muted']};
  margin: 0 0 1.1rem 0;
  font-size: 0.98rem;
}}

.fw-disclaimer {{
  background: linear-gradient(90deg, {c['mint']}, #F0FDFA);
  border: 1px solid #A7F3D0;
  border-left: 3px solid {c['emerald']};
  border-radius: 12px;
  padding: 0.7rem 1rem;
  color: {c['text']};
  font-size: 0.84rem;
  margin: 0.35rem 0 1rem 0;
}}

.fw-kpi {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 18px;
  padding: 1.05rem 1.15rem;
  box-shadow: 0 8px 28px rgba(11, 31, 58, 0.045);
  height: 100%;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}}
@media (prefers-reduced-motion: no-preference) {{
  .fw-kpi:hover {{
    transform: translateY(-3px);
    box-shadow: 0 14px 34px rgba(11, 31, 58, 0.08);
  }}
}}
.fw-kpi .kpi-top {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.55rem;
}}
.fw-kpi .kpi-label {{
  color: {c['muted']};
  font-size: 0.74rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
.fw-kpi .kpi-icon {{
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: {c['mint']};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}}
.fw-kpi .kpi-value {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.55rem;
  font-weight: 800;
  color: {c['navy']};
  letter-spacing: -0.02em;
}}
.fw-kpi .kpi-delta {{
  margin-top: 0.35rem;
  font-size: 0.78rem;
  font-weight: 600;
}}
.fw-kpi .kpi-delta.pos {{ color: {c['positive']}; }}
.fw-kpi .kpi-delta.neg {{ color: {c['negative']}; }}
.fw-kpi .kpi-delta.neu {{ color: {c['muted']}; }}

.fw-card {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 18px;
  padding: 1.15rem 1.25rem;
  box-shadow: 0 8px 28px rgba(11, 31, 58, 0.04);
  margin-bottom: 1rem;
}}
.fw-card h3, .fw-section-title {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: {c['navy']};
  margin: 0 0 0.75rem 0;
}}

.fw-empty {{
  background: linear-gradient(145deg, #FFFFFF, {c['mint']});
  border: 1px dashed #6EE7B7;
  border-radius: 18px;
  padding: 2.2rem 1.5rem;
  text-align: center;
}}
.fw-empty h3 {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  color: {c['navy']};
  margin-bottom: 0.35rem;
}}

.fw-welcome-card {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 22px;
  padding: 1.85rem 1.7rem;
  box-shadow: 0 18px 40px rgba(11, 31, 58, 0.06);
}}
.fw-illus {{
  position: relative;
  min-height: 420px;
  border-radius: 22px;
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 30%, rgba(16,185,129,0.35), transparent 40%),
    radial-gradient(circle at 80% 20%, rgba(6,182,212,0.28), transparent 35%),
    linear-gradient(160deg, {c['navy']} 0%, #0F3D3A 55%, #0B1F3A 100%);
}}
.fw-illus .orb {{
  position: absolute;
  border-radius: 50%;
  background: rgba(248,250,252,0.08);
  border: 1px solid rgba(248,250,252,0.12);
}}
.fw-illus .orb-a {{ width: 150px; height: 150px; top: 12%; left: 10%; }}
.fw-illus .orb-b {{ width: 90px; height: 90px; top: 55%; right: 18%; }}
.fw-illus .orb-c {{ width: 50px; height: 50px; bottom: 18%; left: 35%; }}
@media (prefers-reduced-motion: no-preference) {{
  .fw-illus .orb-a {{ animation: fw-float 7s ease-in-out infinite; }}
  .fw-illus .orb-b {{ animation: fw-float 5.5s ease-in-out infinite reverse; }}
}}
@keyframes fw-float {{
  0%, 100% {{ transform: translateY(0); }}
  50% {{ transform: translateY(-12px); }}
}}
.fw-float-card {{
  position: absolute;
  background: rgba(255,255,255,0.96);
  color: {c['navy']};
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
  border-radius: 50%;
  background: radial-gradient(circle at 40% 40%, rgba(16,185,129,0.45), transparent 70%);
  opacity: 0.55;
}}

.fw-chat-user {{
  background: linear-gradient(135deg, {c['navy']}, {c['emerald']});
  color: #F8FAFC;
  border-radius: 16px 16px 4px 16px;
  padding: 0.85rem 1.05rem;
  margin: 0.45rem 0 0.45rem 18%;
}}
.fw-chat-ai {{
  background: {c['card']};
  border: 1px solid {c['border']};
  color: {c['text']};
  border-radius: 16px 16px 16px 4px;
  padding: 0.85rem 1.05rem;
  margin: 0.45rem 18% 0.45rem 0;
}}

.fw-tx-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid {c['border']};
}}
.fw-tx-left {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
}}
.fw-tx-icon {{
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: {c['mint']};
  display: flex;
  align-items: center;
  justify-content: center;
}}
.fw-tx-amt.expense {{ color: {c['negative']}; font-weight: 700; }}
.fw-tx-amt.income {{ color: {c['positive']}; font-weight: 700; }}

.fw-risk-LOW {{ color: {c['positive']}; font-weight: 700; }}
.fw-risk-MEDIUM {{ color: {c['warning']}; font-weight: 700; }}
.fw-risk-HIGH {{ color: {c['negative']}; font-weight: 700; }}

div[data-testid="stMetric"] {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 16px;
  padding: 0.85rem 1rem;
}}

.stButton > button[kind="primary"],
.stFormSubmitButton > button {{
  background: linear-gradient(135deg, {c['navy']}, {c['emerald']}) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
}}

/* Compact nav button row under brand */
div[data-testid="stHorizontalBlock"] button {{
  border-radius: 999px !important;
}}

@media (max-width: 768px) {{
  .fw-topnav {{ margin: -1rem -0.5rem 1rem -0.5rem; padding: 0.75rem 1rem; }}
  .fw-chat-user, .fw-chat-ai {{ margin-left: 0; margin-right: 0; }}
  .fw-illus {{ min-height: 280px; }}
}}
</style>
        """,
        unsafe_allow_html=True,
    )
