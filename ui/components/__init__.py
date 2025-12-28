"""
Reusable UI Components for AURIX.
Contains badges, cards, headers, footers, and other common components.
"""

import streamlit as st
from typing import Optional, Union
from ui.styles.css_builder import get_current_theme


# ============================================
# Badges
# ============================================

def render_badge(text: str, level: str) -> str:
    """
    Render a badge with appropriate styling.
    
    Args:
        text: Badge text
        level: Badge level (high, medium, low, success, warning, danger, open, closed)
    
    Returns:
        HTML string for the badge
    """
    return f'<span class="badge badge-{level.lower()}">{text}</span>'


def risk_badge(level: str) -> str:
    """Render a risk level badge."""
    level_upper = level.upper()
    level_map = {
        "HIGH": "danger",
        "MEDIUM": "warning",
        "LOW": "success",
        "CRITICAL": "danger"
    }
    badge_level = level_map.get(level_upper, "low")
    return render_badge(level_upper, badge_level)


def status_badge(status: str) -> str:
    """Render a status badge."""
    status_map = {
        "OPEN": "warning",
        "IN PROGRESS": "warning",
        "CLOSED": "success",
        "OVERDUE": "danger",
        "ACTIVE": "success",
        "INACTIVE": "low"
    }
    badge_level = status_map.get(status.upper(), "low")
    return render_badge(status, badge_level)


# ============================================
# Cards
# ============================================

def render_metric_card(label: str, value: str, change: str = None, change_type: str = "positive", icon: str = None) -> str:
    """
    Render a metric card.
    
    Args:
        label: Metric label
        value: Metric value
        change: Optional change indicator (e.g., "+5%")
        change_type: "positive" or "negative"
        icon: Optional icon emoji
    
    Returns:
        HTML string for the metric card
    """
    t = get_current_theme()
    change_color = t['success'] if change_type == 'positive' else t['danger']
    change_html = ""
    if change:
        change_html = f'<div style="font-size:0.75rem;margin-top:0.25rem;color:{change_color} !important;">{change}</div>'
    
    icon_html = f'<span style="margin-right:0.5rem;">{icon}</span>' if icon else ''
    
    return f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;">
        <div style="font-size:0.75rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:{t['text_muted']} !important;margin-bottom:0.5rem;">{icon_html}{label}</div>
        <div style="font-size:1.75rem;font-weight:700;color:{t['text']} !important;">{value}</div>
        {change_html}
    </div>
    '''


def render_stat_card(icon: str, value: Union[str, int], label: str, color: str = None) -> str:
    """
    Render a stat card with icon.
    
    Args:
        icon: Emoji or icon
        value: Stat value
        label: Stat label
        color: Optional color override
    
    Returns:
        HTML string for the stat card
    """
    t = get_current_theme()
    value_color = color if color else t['text']
    
    return f'''
    <div class="stat-card">
        <div class="stat-icon">{icon}</div>
        <div class="stat-value" style="color:{value_color};">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    '''


def render_info_card(title: str, content: str, icon: str = "ℹ️") -> str:
    """Render an info card."""
    t = get_current_theme()
    
    return f'''
    <div class="pro-card" style="padding:1rem;">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
            <span style="font-size:1.25rem;">{icon}</span>
            <strong style="color:{t['text']} !important;">{title}</strong>
        </div>
        <div style="color:{t['text_secondary']} !important;font-size:0.9rem;">
            {content}
        </div>
    </div>
    '''


def render_list_item(title: str, subtitle: str = "", badge: str = None) -> str:
    """Render a list item with optional badge."""
    t = get_current_theme()
    badge_html = badge if badge else ""
    
    return f'''
    <div class="list-item">
        <div>
            <div class="list-item-title">{title}</div>
            <div class="list-item-subtitle">{subtitle}</div>
        </div>
        {badge_html}
    </div>
    '''


# ============================================
# Headers & Footers
# ============================================

def render_page_header(title: str, subtitle: str = ""):
    """Render a page header."""
    t = get_current_theme()
    
    subtitle_html = f'<span style="font-size:0.8rem;color:{t["text_muted"]} !important;">{subtitle}</span>' if subtitle else ''
    
    st.markdown(f'''
    <div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 0;margin-bottom:1.5rem;border-bottom:1px solid {t['border']};">
        <div>
            <h2 style="margin:0;color:{t['text']} !important;">{title}</h2>
            {subtitle_html}
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_footer():
    """Render the application footer."""
    from app.constants import APP_NAME, APP_VERSION, APP_AUTHOR, APP_YEAR
    
    st.markdown(f'''
    <div class="pro-footer">
        <div class="footer-brand">🛡️ {APP_NAME}</div>
        <div class="footer-tagline">Intelligent Audit. Elevated Assurance.</div>
        <div style="margin-bottom:1rem;">
            <a href="https://github.com/mshadianto" target="_blank" style="margin:0 0.75rem;font-size:0.8rem;">GitHub</a>
            <a href="https://linkedin.com/in/mshadianto" target="_blank" style="margin:0 0.75rem;font-size:0.8rem;">LinkedIn</a>
            <a href="https://mshadianto.id" target="_blank" style="margin:0 0.75rem;font-size:0.8rem;">Website</a>
        </div>
        <div class="footer-disclaimer">
            <strong>⚠️ Disclaimer:</strong> Platform AURIX adalah alat bantu untuk Internal Auditor dan bukan pengganti professional judgment.
            Hasil analisis AI harus divalidasi oleh auditor yang kompeten. Developer tidak bertanggung jawab atas keputusan yang diambil berdasarkan output platform ini.
        </div>
        <div style="font-size:0.7rem;color:#64748b;">© {APP_YEAR} {APP_AUTHOR}. All Rights Reserved. | {APP_NAME} v{APP_VERSION}</div>
    </div>
    ''', unsafe_allow_html=True)


# ============================================
# Alerts
# ============================================

def render_alert(message: str, alert_type: str = "info") -> str:
    """
    Render an alert box.
    
    Args:
        message: Alert message
        alert_type: "danger", "warning", "success", or "info"
    
    Returns:
        HTML string for the alert
    """
    return f'''
    <div class="alert-box alert-{alert_type}">
        {message}
    </div>
    '''


# ============================================
# Progress & Gauges
# ============================================

def render_progress_bar(value: int, max_value: int = 100, color: str = None) -> str:
    """Render a progress bar."""
    t = get_current_theme()
    bar_color = color if color else t['primary']
    percentage = (value / max_value * 100) if max_value > 0 else 0
    
    return f'''
    <div class="progress-bar">
        <div class="progress-fill" style="width:{percentage}%;background:{bar_color};"></div>
    </div>
    '''


def render_kri_gauge(value: float, threshold: float, unit: str, good_direction: str = "lower") -> str:
    """
    Render a KRI gauge visualization.
    
    Args:
        value: Current value
        threshold: Threshold value
        unit: Unit of measurement
        good_direction: "lower", "higher", or "optimal"
    
    Returns:
        HTML string for the gauge
    """
    t = get_current_theme()
    
    # Calculate position
    if threshold == 0:
        max_val = max(value * 2, 10)
        position = min(value / max_val * 100, 100) if max_val > 0 else 0
    else:
        max_val = threshold * 1.5
        position = min(value / max_val * 100, 100)
    
    # Determine status color
    if threshold == 0:
        if value == 0:
            status_color = t['success']
        elif value <= 2:
            status_color = t['warning']
        else:
            status_color = t['danger']
    elif good_direction == "lower":
        if value <= threshold * 0.8:
            status_color = t['success']
        elif value <= threshold:
            status_color = t['warning']
        else:
            status_color = t['danger']
    elif good_direction == "higher":
        if value >= threshold:
            status_color = t['success']
        elif value >= threshold * 0.9:
            status_color = t['warning']
        else:
            status_color = t['danger']
    else:  # optimal
        if abs(value - threshold) <= threshold * 0.1:
            status_color = t['success']
        elif abs(value - threshold) <= threshold * 0.2:
            status_color = t['warning']
        else:
            status_color = t['danger']
    
    return f'''
    <div class="kri-gauge">
        <div class="kri-gauge-bg">
            <div class="kri-gauge-pointer" style="left: {position}%;"></div>
        </div>
        <div class="kri-gauge-value" style="color: {status_color};">
            {value}{unit}
        </div>
        <div style="text-align: center; font-size: 0.75rem; color: {t['text_muted']};">
            Threshold: {threshold}{unit}
        </div>
    </div>
    '''


# ============================================
# Section Helpers
# ============================================

def render_section_title(title: str):
    """Render a section title."""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def render_metric_grid(metrics: list):
    """
    Render a grid of metric cards using Streamlit columns.
    
    Args:
        metrics: List of dicts with keys: label, value, change (optional), change_type (optional)
    """
    t = get_current_theme()
    cols = st.columns(len(metrics))
    
    for col, m in zip(cols, metrics):
        with col:
            change_color = t['success'] if m.get('change_type', 'positive') == 'positive' else t['danger']
            change_html = ""
            if m.get('change'):
                change_html = f'<div style="font-size:0.75rem;margin-top:0.25rem;color:{change_color};">{m["change"]}</div>'
            
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
                <div style="font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:{t['text_muted']};margin-bottom:0.5rem;">{m['label']}</div>
                <div style="font-size:1.75rem;font-weight:700;color:{t['text']};line-height:1.2;">{m['value']}</div>
                {change_html}
            </div>
            ''', unsafe_allow_html=True)
