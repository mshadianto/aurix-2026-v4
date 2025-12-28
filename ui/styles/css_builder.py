"""
CSS Builder for AURIX.
Generates dynamic CSS based on current theme.
"""

import streamlit as st
from typing import Dict
from app.constants import COLORS


def get_current_theme() -> Dict[str, str]:
    """Get current theme colors based on session state."""
    theme_name = st.session_state.get('theme', 'dark')
    return COLORS.get(theme_name, COLORS['dark'])


def inject_css():
    """Inject complete CSS styles into the page."""
    t = get_current_theme()
    is_dark = st.session_state.get('theme', 'dark') == 'dark'
    
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ===== GLOBAL ===== */
* {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

.stApp {{
    background: {t['bg']};
}}

/* ===== HIDE STREAMLIT DEFAULTS ===== */
#MainMenu, footer, header {{visibility: hidden;}}
.block-container {{padding: 2rem 3rem 3rem 3rem; max-width: 1400px;}}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {{
    background: {t['sidebar_bg']};
    border-right: 1px solid {t['border']};
}}

section[data-testid="stSidebar"] .stRadio label {{
    color: {t['text']} !important;
}}

section[data-testid="stSidebar"] .stRadio label:hover {{
    background: {t['card_hover']};
    border-radius: 8px;
}}

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4, h5, h6 {{
    color: {t['text']} !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}}

h1 {{ font-size: 2rem !important; }}
h2 {{ font-size: 1.5rem !important; margin-bottom: 1.5rem !important; }}
h3 {{ font-size: 1.125rem !important; }}

p, span, li, td, th, label {{
    color: {t['text_secondary']} !important;
}}

/* Light mode text visibility fix */
div[data-testid="stMarkdownContainer"] div {{
    color: {t['text']} !important;
}}

div[data-testid="stMarkdownContainer"] .metric-label,
div[data-testid="stMarkdownContainer"] .pro-card-header {{
    color: {t['text_muted']} !important;
}}

a {{
    color: {t['primary']} !important;
    text-decoration: none !important;
}}

a:hover {{
    color: {t['primary_hover']} !important;
}}

/* ===== CARDS ===== */
.pro-card {{
    background: {t['card']};
    border: 1px solid {t['border']};
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}}

.pro-card:hover {{
    border-color: {t['primary']};
    box-shadow: 0 4px 12px {'rgba(0,0,0,0.3)' if is_dark else 'rgba(0,0,0,0.08)'};
}}

.pro-card-header {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {t['text_muted']} !important;
    margin-bottom: 0.5rem;
}}

.pro-card-value {{
    font-size: 2rem;
    font-weight: 700;
    color: {t['text']} !important;
    line-height: 1.2;
}}

/* ===== METRICS ===== */
.metric-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}}

@media (max-width: 1024px) {{
    .metric-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

.metric-card {{
    background: {t['card']};
    border: 1px solid {t['border']};
    border-radius: 12px;
    padding: 1.25rem;
    text-align: left;
}}

.metric-label {{
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {t['text_muted']} !important;
    margin-bottom: 0.5rem;
}}

.metric-value {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {t['text']} !important;
}}

.metric-change {{
    font-size: 0.75rem;
    margin-top: 0.25rem;
}}

.metric-change.positive {{ color: {t['success']} !important; }}
.metric-change.negative {{ color: {t['danger']} !important; }}

/* ===== BADGES ===== */
.badge {{
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}}

.badge-high, .badge-critical, .badge-danger {{
    background: {'rgba(239,68,68,0.15)' if is_dark else 'rgba(220,38,38,0.1)'};
    color: {t['danger']} !important;
    border: 1px solid {'rgba(239,68,68,0.3)' if is_dark else 'rgba(220,38,38,0.2)'};
}}

.badge-medium, .badge-warning {{
    background: {'rgba(245,158,11,0.15)' if is_dark else 'rgba(217,119,6,0.1)'};
    color: {t['warning']} !important;
    border: 1px solid {'rgba(245,158,11,0.3)' if is_dark else 'rgba(217,119,6,0.2)'};
}}

.badge-low, .badge-success {{
    background: {'rgba(16,185,129,0.15)' if is_dark else 'rgba(5,150,105,0.1)'};
    color: {t['success']} !important;
    border: 1px solid {'rgba(16,185,129,0.3)' if is_dark else 'rgba(5,150,105,0.2)'};
}}

.badge-open {{
    background: {'rgba(245,158,11,0.15)' if is_dark else 'rgba(217,119,6,0.1)'};
    color: {t['warning']} !important;
}}

.badge-closed {{
    background: {'rgba(16,185,129,0.15)' if is_dark else 'rgba(5,150,105,0.1)'};
    color: {t['success']} !important;
}}

/* ===== BUTTONS ===== */
.stButton > button {{
    background: {t['primary']} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.625rem 1.25rem !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    transition: all 0.2s ease !important;
}}

.stButton > button:hover {{
    background: {t['primary_hover']} !important;
    box-shadow: 0 4px 12px {'rgba(59,130,246,0.4)' if is_dark else 'rgba(37,99,235,0.3)'} !important;
}}

/* ===== INPUTS ===== */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {{
    background: {t['bg_secondary']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
    color: {t['text']} !important;
}}

.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {t['primary']} !important;
    box-shadow: 0 0 0 2px {'rgba(59,130,246,0.2)' if is_dark else 'rgba(37,99,235,0.15)'} !important;
}}

/* ===== TABLES ===== */
.pro-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.875rem;
}}

.pro-table th {{
    background: {t['bg_secondary']};
    color: {t['text_muted']} !important;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid {t['border']};
}}

.pro-table td {{
    padding: 0.875rem 1rem;
    border-bottom: 1px solid {t['border']};
    color: {t['text_secondary']} !important;
}}

.pro-table tr:hover td {{
    background: {t['card_hover']};
}}

/* ===== ALERTS ===== */
.alert-box {{
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid;
    margin: 1rem 0;
}}

.alert-danger {{
    background: {'rgba(239,68,68,0.1)' if is_dark else 'rgba(220,38,38,0.05)'};
    border-color: {t['danger']};
    color: {t['danger']} !important;
}}

.alert-warning {{
    background: {'rgba(245,158,11,0.1)' if is_dark else 'rgba(217,119,6,0.05)'};
    border-color: {t['warning']};
    color: {t['warning']} !important;
}}

.alert-success {{
    background: {'rgba(16,185,129,0.1)' if is_dark else 'rgba(5,150,105,0.05)'};
    border-color: {t['success']};
    color: {t['success']} !important;
}}

/* ===== LIST ITEMS ===== */
.list-item {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.875rem 0;
    border-bottom: 1px solid {t['border']};
}}

.list-item:last-child {{
    border-bottom: none;
}}

.list-item-title {{
    font-weight: 500;
    color: {t['text']} !important;
}}

.list-item-subtitle {{
    font-size: 0.8rem;
    color: {t['text_muted']} !important;
}}

/* ===== PROGRESS BAR ===== */
.progress-bar {{
    width: 100%;
    height: 8px;
    background: {t['border']};
    border-radius: 4px;
    overflow: hidden;
    margin: 0.5rem 0;
}}

.progress-fill {{
    height: 100%;
    background: {t['primary']};
    transition: width 0.3s ease;
}}

/* ===== STAT CARD ===== */
.stat-card {{
    background: {t['card']};
    border: 1px solid {t['border']};
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}}

.stat-icon {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

.stat-value {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {t['text']} !important;
}}

.stat-label {{
    font-size: 0.75rem;
    color: {t['text_muted']} !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.25rem;
}}

/* ===== SECTION TITLE ===== */
.section-title {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {t['text_muted']} !important;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid {t['border']};
}}

/* ===== LOGO ===== */
.logo-container {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1.25rem;
    border-bottom: 1px solid {t['border']};
    margin-bottom: 1rem;
}}

.logo-text {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: {t['text']} !important;
}}

.logo-tagline {{
    font-size: 0.65rem;
    color: {t['text_muted']} !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}

/* ===== CHAT ===== */
.chat-user {{
    background: {t['primary']};
    color: white !important;
    padding: 1rem;
    border-radius: 12px 12px 4px 12px;
    margin: 0.5rem 0;
    margin-left: 15%;
}}

.chat-ai {{
    background: {t['card']};
    border: 1px solid {t['border']};
    padding: 1rem;
    border-radius: 12px 12px 12px 4px;
    margin: 0.5rem 0;
    margin-right: 15%;
}}

/* ===== FOOTER ===== */
.pro-footer {{
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
    border-top: 1px solid {t['border']};
}}

.footer-brand {{
    font-size: 1rem;
    font-weight: 700;
    color: {t['text']} !important;
    margin-bottom: 0.25rem;
}}

.footer-tagline {{
    font-size: 0.75rem;
    color: {t['text_muted']} !important;
    margin-bottom: 1rem;
}}

.footer-disclaimer {{
    background: {'rgba(245,158,11,0.1)' if is_dark else 'rgba(217,119,6,0.05)'};
    border: 1px solid {'rgba(245,158,11,0.2)' if is_dark else 'rgba(217,119,6,0.15)'};
    border-radius: 8px;
    padding: 1rem;
    font-size: 0.75rem;
    color: {t['text_muted']} !important;
    max-width: 800px;
    margin: 0 auto 1rem auto;
    text-align: left;
}}

/* ===== KRI GAUGE ===== */
.kri-gauge {{
    width: 100%;
    height: 120px;
    position: relative;
    margin: 1rem 0;
}}

.kri-gauge-bg {{
    width: 100%;
    height: 15px;
    background: linear-gradient(to right, {t['success']}, {t['warning']}, {t['danger']});
    border-radius: 10px;
    position: relative;
}}

.kri-gauge-pointer {{
    width: 4px;
    height: 30px;
    background: {t['text']};
    position: absolute;
    top: -7.5px;
    transform: translateX(-2px);
}}

.kri-gauge-value {{
    text-align: center;
    margin-top: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: {t['text']} !important;
}}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}

::-webkit-scrollbar-track {{
    background: {t['bg']};
}}

::-webkit-scrollbar-thumb {{
    background: {t['border']};
    border-radius: 3px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {t['text_muted']};
}}
</style>
"""
    
    st.markdown(css, unsafe_allow_html=True)


def get_color(color_name: str) -> str:
    """Get a specific color from current theme."""
    t = get_current_theme()
    return t.get(color_name, "#000000")
