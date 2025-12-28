"""
Dashboard Page for AURIX.
Main overview page showing key metrics and insights.
"""

import streamlit as st
import random
from datetime import datetime
from typing import Dict, List

from ui.styles.css_builder import get_current_theme
from ui.components import (
    render_page_header,
    render_footer,
    render_metric_card,
    render_metric_grid,
    render_stat_card,
    render_list_item,
    risk_badge,
    render_progress_bar,
    render_alert
)
from data.seeds import AUDIT_UNIVERSE, KRI_INDICATORS
from services.visitor_service import get_visitor_stats, track_page_view


def render():
    """Render the dashboard page."""
    t = get_current_theme()
    
    # Track page view
    track_page_view("Dashboard")
    
    # Welcome Banner
    _render_welcome_banner(t)
    
    # Quick Stats
    _render_quick_stats(t)
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    _render_quick_actions(t)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        _render_risk_heatmap(t)
        st.markdown("<br>", unsafe_allow_html=True)
        _render_audit_universe(t)
    
    with col2:
        _render_kri_alerts(t)
        st.markdown("<br>", unsafe_allow_html=True)
        _render_recent_activity(t)
        st.markdown("<br>", unsafe_allow_html=True)
        _render_system_health(t)
    
    # Visitor Analytics
    st.markdown("<br><br>", unsafe_allow_html=True)
    _render_visitor_analytics(t)
    
    # Footer
    render_footer()


def _render_welcome_banner(t: dict):
    """Render welcome banner."""
    st.markdown(f'''
    <div class="pro-card" style="background: linear-gradient(135deg, {t['primary']} 0%, {t['accent']} 100%); border: none; margin-bottom: 2rem;">
        <div style="color: white; text-align: center; padding: 1rem 0;">
            <h1 style="margin: 0; font-size: 2rem; color: white !important;">🛡️ Welcome to AURIX</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.95; color: white !important;">
                Intelligent Audit. Elevated Assurance. | v4.0 Enterprise
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def _render_quick_stats(t: dict):
    """Render quick statistics."""
    findings = st.session_state.get('findings', [])
    open_findings = len([f for f in findings if f.get('status') == 'Open'])
    high_findings = len([f for f in findings if f.get('rating') == 'HIGH'])
    active_rules = len([r for r in st.session_state.get('continuous_audit_rules', []) if r.get('active', False)])
    doc_count = len(st.session_state.get('documents', []))
    wp_count = len(st.session_state.get('working_papers', []))
    
    metrics = [
        {"label": "Audit Universe", "value": "36 Areas", "change": "6 categories"},
        {
            "label": "Open Findings", 
            "value": str(open_findings), 
            "change": f"{high_findings} critical" if high_findings > 0 else "All clear",
            "change_type": "negative" if high_findings > 0 else "positive"
        },
        {"label": "CA Monitoring", "value": f"{active_rules} Active", "change": "18 rules available"},
        {"label": "Documents", "value": str(doc_count), "change": f"{wp_count} working papers"},
    ]
    
    render_metric_grid(metrics)


def _render_quick_actions(t: dict):
    """Render quick action buttons."""
    cols = st.columns(4)
    
    actions = [
        ("📝", "Findings", f"{len([f for f in st.session_state.get('findings', []) if f.get('status') == 'Open'])} open"),
        ("📊", "Analytics", "6 tools ready"),
        ("📈", "KRI Monitor", "24 indicators"),
        ("🚨", "Fraud Scan", "60+ red flags"),
    ]
    
    for col, (icon, title, subtitle) in zip(cols, actions):
        with col:
            st.markdown(f'''
            <div style="background:{t['card']}; border:1px solid {t['border']}; border-radius:8px; padding:1rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:600; color:{t['text']}; margin-bottom:0.25rem;">{title}</div>
                <div style="font-size:0.75rem; color:{t['text_muted']};">{subtitle}</div>
            </div>
            ''', unsafe_allow_html=True)


def _render_risk_heatmap(t: dict):
    """Render risk heatmap."""
    st.markdown("### 🔥 Risk Heat Map")
    
    for cat, areas in AUDIT_UNIVERSE.items():
        high_risk = random.randint(0, 2)
        medium_risk = random.randint(1, 3)
        low_risk = len(areas) - high_risk - medium_risk
        total = len(areas)
        
        high_pct = (high_risk / total) * 100
        medium_pct = (medium_risk / total) * 100
        low_pct = (low_risk / total) * 100
        
        st.markdown(f'''
        <div style="background:{t['card']}; border:1px solid {t['border']}; border-radius:12px; padding:1rem; margin-bottom:0.75rem;">
            <div style="margin-bottom:0.5rem;">
                <strong style="color:{t['text']};">{cat}</strong>
                <span style="float:right; color:{t['text_muted']}; font-size:0.85rem;">
                    {total} areas
                </span>
            </div>
            <div style="display:flex; height:8px; border-radius:4px; overflow:hidden; background:{t['border']};">
                <div style="width:{high_pct}%; background:{t['danger']};"></div>
                <div style="width:{medium_pct}%; background:{t['warning']};"></div>
                <div style="width:{low_pct}%; background:{t['success']};"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:0.5rem; font-size:0.75rem;">
                <span style="color:{t['danger']};">■ {high_risk} High</span>
                <span style="color:{t['warning']};">■ {medium_risk} Medium</span>
                <span style="color:{t['success']};">■ {low_risk} Low</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_audit_universe(t: dict):
    """Render audit universe details."""
    st.markdown("### 📂 Audit Universe Details")
    
    for cat, areas in AUDIT_UNIVERSE.items():
        with st.expander(f"{cat} ({len(areas)} areas)", expanded=False):
            for area in areas:
                risk = random.choice(['HIGH', 'MEDIUM', 'LOW'])
                badge_html = risk_badge(risk)
                st.markdown(f'''
                <div class="list-item">
                    <div>
                        <div class="list-item-title">{area}</div>
                        <div class="list-item-subtitle">{cat}</div>
                    </div>
                    {badge_html}
                </div>
                ''', unsafe_allow_html=True)


def _render_kri_alerts(t: dict):
    """Render KRI alerts panel."""
    st.markdown("### ⚠️ KRI Alerts")
    
    alerts = [
        ("NPL Ratio", "5.54%", "DANGER", "Credit Risk"),
        ("LCR", "93.42%", "WARNING", "Liquidity Risk"),
        ("System Downtime", "2.3h", "WARNING", "Operational Risk"),
    ]
    
    for name, value, status, category in alerts:
        badge_html = risk_badge(status)
        
        st.markdown(f'''
        <div style="background:{t['card']}; border:1px solid {t['border']}; border-radius:12px; padding:0.875rem; margin-bottom:0.5rem;">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div style="flex:1;">
                    <div style="font-weight:600; color:{t['text']};">{name}</div>
                    <div style="font-size:0.75rem; color:{t['text_muted']};">{category}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.25rem; font-weight:700; color:{t['text']};">{value}</div>
                    {badge_html}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_recent_activity(t: dict):
    """Render recent activity panel."""
    st.markdown("### 📰 Recent Activity")
    
    activities = [
        ("2 hours ago", "KRI threshold breach", "📈", t['danger']),
        ("5 hours ago", "3 fraud flags detected", "🚨", t['warning']),
        ("1 day ago", "CA rule triggered", "🔄", t['accent']),
        ("2 days ago", "Working paper created", "📄", t['success']),
        ("3 days ago", "Audit completed", "✅", t['success']),
    ]
    
    for time, desc, icon, color in activities:
        st.markdown(f'''
        <div style="background:{t['card']}; border:1px solid {t['border']}; border-radius:12px; padding:0.75rem; margin-bottom:0.5rem; border-left:3px solid {color};">
            <div style="font-size:0.7rem; color:{t['text_muted']}; margin-bottom:0.25rem;">
                {icon} {time}
            </div>
            <div style="color:{t['text']}; font-size:0.85rem; font-weight:500;">
                {desc}
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_system_health(t: dict):
    """Render system health panel."""
    st.markdown("### 💚 System Health")
    
    health_items = [
        ("Data Analytics", 98, t['success']),
        ("CA Monitoring", 100, t['success']),
        ("Document Processing", 87, t['warning']),
        ("AI Assistant", 95, t['success']),
    ]
    
    for name, health, color in health_items:
        st.markdown(f'''
        <div style="background:{t['card']}; border:1px solid {t['border']}; border-radius:12px; padding:0.75rem; margin-bottom:0.5rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                <span style="font-size:0.85rem; color:{t['text']};">{name}</span>
                <span style="font-size:0.85rem; font-weight:600; color:{color};">{health}%</span>
            </div>
            {render_progress_bar(health, 100, color)}
        </div>
        ''', unsafe_allow_html=True)


def _render_visitor_analytics(t: dict):
    """Render visitor analytics section."""
    st.markdown("## 👥 Platform Analytics")
    
    stats = get_visitor_stats()
    
    if stats:
        cols = st.columns(4)
        
        metrics = [
            (f"{stats['total_visits']:,}", "Total Visits", t['accent']),
            (f"{stats['unique_visitors']:,}", "Unique Visitors", t['success']),
            (f"{stats['total_page_views']:,}", "Page Views", t['primary']),
            (f"{stats['avg_session_duration'] // 60}m {stats['avg_session_duration'] % 60}s", "Avg Session", t['warning']),
        ]
        
        for col, (value, label, color) in zip(cols, metrics):
            with col:
                st.markdown(f'''
                <div style="background:{t['card']}; border:1px solid {t['border']}; border-radius:12px; text-align:center; padding:1.5rem;">
                    <div style="font-size:2rem; color:{color}; font-weight:700;">{value}</div>
                    <div style="font-size:0.85rem; color:{t['text_muted']}; margin-top:0.5rem;">{label}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Show mock data indicator if applicable
        if stats.get('is_mock', False):
            st.info("📊 Showing demo data. Connect database for real analytics.")
