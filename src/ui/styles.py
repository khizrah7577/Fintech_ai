"""Scoped FinWise sage / cream theme — avoid painting every Streamlit widget."""

from __future__ import annotations

import streamlit as st

from src.config import COLORS


def inject_global_styles() -> None:
    c = COLORS
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
  font-family: 'Source Sans 3', sans-serif;
  color: {c['text']};
}}

.stApp {{
  background:
    radial-gradient(ellipse 80% 50% at 0% 0%, {c['light_sage']}88 0%, transparent 55%),
    radial-gradient(ellipse 60% 40% at 100% 0%, #efe6d6 0%, transparent 50%),
    {c['bg']};
}}

[data-testid="stHeader"] {{
  background: rgba(245, 244, 237, 0.75);
}}

/* Sidebar — branded, not global * color override */
section[data-testid="stSidebar"] {{
  background: linear-gradient(185deg, {c['sidebar']} 0%, #0f332e 100%);
  border-right: 1px solid rgba(163, 184, 161, 0.25);
}}
section[data-testid="stSidebar"] .fw-side-brand {{
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.85rem;
  font-weight: 700;
  color: #F8F5ED;
  margin: 0;
  letter-spacing: -0.02em;
}}
section[data-testid="stSidebar"] .fw-side-sub {{
  color: {c['sage']};
  font-size: 0.82rem;
  margin: 0.2rem 0 1rem 0;
}}
section[data-testid="stSidebar"] .fw-side-disclaimer {{
  color: #d5e2d4;
  font-size: 0.75rem;
  line-height: 1.4;
  opacity: 0.9;
}}
section[data-testid="stSidebar"] label {{
  color: #E7EFE8 !important;
}}
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stCaption {{
  color: #dce8db !important;
}}
section[data-testid="stSidebar"] div[data-baseweb="radio"] label p {{
  color: #E7EFE8 !important;
}}

.fw-page-title {{
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(1.9rem, 3.5vw, 2.6rem);
  font-weight: 700;
  color: {c['primary']};
  margin: 0 0 0.25rem 0;
  letter-spacing: -0.02em;
  line-height: 1.15;
}}
.fw-page-sub {{
  color: {c['muted']};
  margin: 0 0 1rem 0;
  font-size: 1.02rem;
}}

.fw-disclaimer {{
  background: {c['light_sage']};
  border-left: 3px solid {c['primary']};
  border-radius: 0 10px 10px 0;
  padding: 0.7rem 1rem;
  color: {c['text']};
  font-size: 0.88rem;
  margin: 0.5rem 0 1.1rem 0;
}}

.fw-card {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 14px;
  padding: 1.1rem 1.2rem;
  box-shadow: 0 10px 28px rgba(24, 61, 54, 0.06);
}}

.fw-metric-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.85rem;
  margin: 0.5rem 0 1rem 0;
}}
.fw-metric {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 14px;
  padding: 0.9rem 1rem;
  box-shadow: 0 8px 20px rgba(24, 61, 54, 0.05);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}}
@media (prefers-reduced-motion: no-preference) {{
  .fw-metric:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 26px rgba(24, 61, 54, 0.09);
  }}
}}
.fw-metric .label {{
  color: {c['muted']};
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
.fw-metric .value {{
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.7rem;
  font-weight: 700;
  color: {c['primary']};
  margin-top: 0.2rem;
}}
.fw-metric .delta {{
  font-size: 0.82rem;
  color: {c['secondary']};
  margin-top: 0.15rem;
}}

.fw-risk-LOW {{ color: {c['success']}; font-weight: 700; }}
.fw-risk-MEDIUM {{ color: {c['warning']}; font-weight: 700; }}
.fw-risk-HIGH {{ color: {c['danger']}; font-weight: 700; }}

.fw-empty {{
  background: linear-gradient(145deg, {c['cream']}, {c['light_sage']});
  border: 1px dashed {c['sage']};
  border-radius: 16px;
  padding: 2rem 1.5rem;
  text-align: center;
  color: {c['text']};
}}
.fw-empty h3 {{
  font-family: 'Cormorant Garamond', Georgia, serif;
  color: {c['primary']};
  margin-bottom: 0.4rem;
}}

/* Welcome / landing illustration */
.fw-welcome-wrap {{
  min-height: 70vh;
  display: flex;
  align-items: stretch;
}}
.fw-welcome-card {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 18px;
  padding: 1.75rem 1.6rem;
  box-shadow: 0 16px 40px rgba(18, 63, 56, 0.08);
}}
.fw-illus {{
  position: relative;
  height: 100%;
  min-height: 420px;
  border-radius: 22px;
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 30%, {c['sage']}55, transparent 40%),
    radial-gradient(circle at 80% 20%, {c['warm']}44, transparent 35%),
    linear-gradient(160deg, {c['primary']} 0%, #1f5a4e 45%, {c['secondary']} 100%);
}}
.fw-illus .orb {{
  position: absolute;
  border-radius: 50%;
  background: rgba(247, 245, 237, 0.12);
  border: 1px solid rgba(247, 245, 237, 0.2);
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
  background: rgba(248, 245, 237, 0.95);
  color: {c['primary']};
  border-radius: 12px;
  padding: 0.7rem 0.9rem;
  box-shadow: 0 10px 24px rgba(0,0,0,0.12);
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
  background: radial-gradient(circle at 40% 40%, {c['sage']}, transparent 70%);
  opacity: 0.55;
}}

.fw-chat-user {{
  background: {c['primary']};
  color: #F8F5ED;
  border-radius: 14px 14px 4px 14px;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0 0.4rem 15%;
}}
.fw-chat-ai {{
  background: {c['card']};
  border: 1px solid {c['border']};
  color: {c['text']};
  border-radius: 14px 14px 14px 4px;
  padding: 0.75rem 1rem;
  margin: 0.4rem 15% 0.4rem 0;
}}

div[data-testid="stMetric"] {{
  background: {c['card']};
  border: 1px solid {c['border']};
  border-radius: 14px;
  padding: 0.75rem 1rem;
}}
</style>
        """,
        unsafe_allow_html=True,
    )
