"""
Badge Components for AURIX.
Provides various badge styles for risk levels, status, and more.
"""

from ui.styles.css_builder import get_current_theme


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


def priority_badge(priority: str) -> str:
    """Render a priority badge."""
    priority_map = {
        "URGENT": "danger",
        "HIGH": "danger",
        "MEDIUM": "warning",
        "LOW": "success"
    }
    badge_level = priority_map.get(priority.upper(), "low")
    return render_badge(priority, badge_level)


def custom_badge(text: str, bg_color: str, text_color: str = "white") -> str:
    """Render a custom colored badge."""
    return f'<span class="badge" style="background:{bg_color};color:{text_color};">{text}</span>'
