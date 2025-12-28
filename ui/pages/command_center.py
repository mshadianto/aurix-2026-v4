"""
Command Center Module for AURIX.
Real-time monitoring dashboard with alerts and KPIs.
"""

import streamlit as st
from datetime import datetime, timedelta
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the command center page."""
    t = get_current_theme()
    
    render_page_header(
        "🎛️ Command Center",
        "Real-time audit monitoring and operational dashboard"
    )
    
    # Auto-refresh indicator
    now_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">'
        '<div style="display:flex;align-items:center;gap:0.5rem;">'
        '<div style="width:10px;height:10px;background:#22c55e;border-radius:50%;"></div>'
        '<span style="color:#22c55e;font-size:0.85rem;font-weight:600;">LIVE</span>'
        '<span style="color:' + t['text_muted'] + ';font-size:0.8rem;">• Last updated: ' + now_time + '</span>'
        '</div>'
        '<div style="font-size:0.8rem;color:' + t['text_muted'] + ';">'
        '🔄 Auto-refresh: 30s'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Key metrics banner
    _render_key_metrics(t)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        _render_activity_feed(t)
        st.markdown("<br>", unsafe_allow_html=True)
        _render_performance_gauges(t)
    
    with col2:
        _render_alerts_panel(t)
        st.markdown("<br>", unsafe_allow_html=True)
        _render_team_status(t)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom section
    _render_monitoring_grid(t)
    
    render_footer()


def _render_key_metrics(t: dict):
    """Render key metrics banner."""
    metrics = [
        {"label": "Active Audits", "value": "12", "change": "+2", "trend": "up", "icon": "📋"},
        {"label": "Open Issues", "value": "47", "change": "-5", "trend": "down", "icon": "⚠️"},
        {"label": "Overdue Actions", "value": "8", "change": "+3", "trend": "up", "icon": "🔴"},
        {"label": "Team Utilization", "value": "87%", "change": "+5%", "trend": "up", "icon": "👥"},
        {"label": "AI Queries Today", "value": "156", "change": "+42", "trend": "up", "icon": "🤖"},
        {"label": "Documents Processed", "value": "324", "change": "+78", "trend": "up", "icon": "📁"},
    ]
    
    cols = st.columns(6)
    
    for col, m in zip(cols, metrics):
        trend_color = t['success'] if (m['trend'] == 'down' and 'Overdue' in m['label']) or (m['trend'] == 'up' and 'Overdue' not in m['label']) else t['danger']
        if 'Overdue' in m['label']:
            trend_color = t['danger'] if m['trend'] == 'up' else t['success']
        
        trend_icon = "📈" if m['trend'] == 'up' else "📉"
        
        with col:
            html = (
                '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:16px;padding:1rem;text-align:center;">'
                '<div style="font-size:1.5rem;margin-bottom:0.25rem;">' + m['icon'] + '</div>'
                '<div style="font-size:1.5rem;font-weight:700;color:' + t['text'] + ';">' + m['value'] + '</div>'
                '<div style="font-size:0.7rem;color:' + t['text_muted'] + ';margin-bottom:0.25rem;">' + m['label'] + '</div>'
                '<div style="font-size:0.7rem;color:' + trend_color + ';font-weight:600;">'
                + trend_icon + ' ' + m['change'] +
                '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)


def _render_activity_feed(t: dict):
    """Render real-time activity feed."""
    st.markdown("### 📡 Live Activity Feed")
    
    activities = [
        {"time": "Just now", "user": "Ahmad R.", "action": "Completed workpaper review", "type": "success", "icon": "✅"},
        {"time": "2m ago", "user": "System", "action": "High-risk transaction detected - Alert #4521", "type": "danger", "icon": "🚨"},
        {"time": "5m ago", "user": "Budi S.", "action": "Uploaded 3 documents to Credit Risk folder", "type": "info", "icon": "📁"},
        {"time": "8m ago", "user": "AI Assistant", "action": "Generated 5 audit procedures for KYC review", "type": "primary", "icon": "🤖"},
        {"time": "12m ago", "user": "Citra D.", "action": "Updated issue ISS-003 status to In Progress", "type": "warning", "icon": "📌"},
        {"time": "15m ago", "user": "System", "action": "Daily backup completed successfully", "type": "success", "icon": "💾"},
        {"time": "22m ago", "user": "Dewi P.", "action": "Created new finding: Credit limit breach", "type": "danger", "icon": "📋"},
        {"time": "30m ago", "user": "Ahmad R.", "action": "Logged 4 hours to Treasury Audit", "type": "info", "icon": "⏱️"},
    ]
    
    type_colors = {
        "success": t['success'],
        "danger": t['danger'],
        "warning": t['warning'],
        "info": t['primary'],
        "primary": t['accent']
    }
    
    for activity in activities:
        color = type_colors.get(activity['type'], t['text_muted'])
        
        html = (
            '<div style="display:flex;align-items:start;gap:1rem;padding:0.75rem;border-bottom:1px solid ' + t['border'] + ';">'
            '<div style="width:36px;height:36px;background:' + color + '20;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
            '<span style="font-size:1rem;">' + activity['icon'] + '</span>'
            '</div>'
            '<div style="flex:1;">'
            '<div style="color:' + t['text'] + ';font-size:0.85rem;">'
            '<strong>' + activity['user'] + '</strong> ' + activity['action'] +
            '</div>'
            '<div style="color:' + t['text_muted'] + ';font-size:0.7rem;margin-top:0.25rem;">' + activity['time'] + '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def _render_alerts_panel(t: dict):
    """Render alerts panel."""
    st.markdown("### 🚨 Active Alerts")
    
    alerts = [
        {"title": "AML Alert Backlog > 100", "severity": "critical", "time": "Active 2h"},
        {"title": "System response time degraded", "severity": "high", "time": "Active 45m"},
        {"title": "Credit limit breach - Case #4521", "severity": "critical", "time": "Active 30m"},
        {"title": "Failed login attempts spike", "severity": "medium", "time": "Active 1h"},
        {"title": "Backup job delayed", "severity": "low", "time": "Active 20m"},
    ]
    
    severity_colors = {
        "critical": t['danger'],
        "high": t['warning'],
        "medium": t['accent'],
        "low": t['success']
    }
    
    for alert in alerts:
        color = severity_colors.get(alert['severity'], t['text_muted'])
        
        html = (
            '<div style="background:' + color + '10;border-left:4px solid ' + color + ';border-radius:0 8px 8px 0;padding:0.75rem;margin-bottom:0.5rem;">'
            '<div style="font-weight:600;color:' + t['text'] + ';font-size:0.85rem;">' + alert['title'] + '</div>'
            '<div style="display:flex;justify-content:space-between;margin-top:0.25rem;">'
            '<span style="color:' + color + ';font-size:0.7rem;text-transform:uppercase;font-weight:600;">' + alert['severity'] + '</span>'
            '<span style="color:' + t['text_muted'] + ';font-size:0.7rem;">' + alert['time'] + '</span>'
            '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def _render_team_status(t: dict):
    """Render team status panel."""
    st.markdown("### 👥 Team Status")
    
    team = [
        {"name": "Ahmad R.", "status": "Online", "task": "Treasury Audit", "color": t['success']},
        {"name": "Budi S.", "status": "In Meeting", "task": "AML Review", "color": t['warning']},
        {"name": "Citra D.", "status": "Online", "task": "IT Assessment", "color": t['success']},
        {"name": "Dewi P.", "status": "Away", "task": "Credit Review", "color": t['text_muted']},
        {"name": "Eko P.", "status": "Offline", "task": "-", "color": t['danger']},
    ]
    
    for member in team:
        initial = member['name'][0]
        html = (
            '<div style="display:flex;align-items:center;gap:0.75rem;padding:0.5rem 0;border-bottom:1px solid ' + t['border'] + ';">'
            '<div style="position:relative;">'
            '<div style="width:36px;height:36px;background:' + t['primary'] + '20;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.9rem;">'
            + initial +
            '</div>'
            '</div>'
            '<div style="flex:1;">'
            '<div style="font-weight:600;color:' + t['text'] + ';font-size:0.85rem;">' + member['name'] + '</div>'
            '<div style="font-size:0.7rem;color:' + t['text_muted'] + ';">' + member['task'] + '</div>'
            '</div>'
            '<div style="font-size:0.7rem;color:' + member['color'] + ';">' + member['status'] + '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def _render_performance_gauges(t: dict):
    """Render performance gauge meters using simple progress bars."""
    st.markdown("### 📊 Performance Metrics")
    
    gauges = [
        {"label": "Audit Plan Progress", "value": 67, "target": 75, "color": t['primary']},
        {"label": "Finding Resolution", "value": 82, "target": 90, "color": t['success']},
        {"label": "Quality Score", "value": 94, "target": 95, "color": t['accent']},
        {"label": "AI Utilization", "value": 45, "target": 60, "color": t['warning']},
    ]
    
    cols = st.columns(4)
    
    for col, gauge in zip(cols, gauges):
        with col:
            pct = gauge['value']
            target = gauge['target']
            color = gauge['color']
            label = gauge['label']
            
            html = (
                '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:12px;padding:1.25rem;text-align:center;">'
                '<div style="font-size:2.5rem;font-weight:700;color:' + color + ';">' + str(pct) + '%</div>'
                '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';margin:0.5rem 0;">Target: ' + str(target) + '%</div>'
                '<div style="height:8px;background:' + t['border'] + ';border-radius:4px;overflow:hidden;margin:0.5rem 0;">'
                '<div style="width:' + str(pct) + '%;height:100%;background:' + color + ';border-radius:4px;"></div>'
                '</div>'
                '<div style="font-size:0.8rem;color:' + t['text'] + ';margin-top:0.75rem;">' + label + '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)


def _render_monitoring_grid(t: dict):
    """Render system monitoring grid."""
    st.markdown("### 🖥️ System Health")
    
    systems = [
        {"name": "Core Banking", "status": "Operational", "uptime": "99.9%", "icon": "🏦", "color": t['success']},
        {"name": "AURIX Platform", "status": "Operational", "uptime": "99.8%", "icon": "🔍", "color": t['success']},
        {"name": "Document Server", "status": "Operational", "uptime": "99.5%", "icon": "📁", "color": t['success']},
        {"name": "AI Services", "status": "Degraded", "uptime": "98.2%", "icon": "🤖", "color": t['warning']},
        {"name": "Email Gateway", "status": "Operational", "uptime": "99.9%", "icon": "📧", "color": t['success']},
        {"name": "Backup System", "status": "Maintenance", "uptime": "97.5%", "icon": "💾", "color": t['accent']},
    ]
    
    cols = st.columns(6)
    
    for col, sys in zip(cols, systems):
        with col:
            html = (
                '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-top:4px solid ' + sys['color'] + ';border-radius:12px;padding:1rem;text-align:center;">'
                '<div style="font-size:2rem;margin-bottom:0.5rem;">' + sys['icon'] + '</div>'
                '<div style="font-weight:600;color:' + t['text'] + ';font-size:0.85rem;margin-bottom:0.25rem;">' + sys['name'] + '</div>'
                '<div style="font-size:0.7rem;color:' + sys['color'] + ';font-weight:600;margin-bottom:0.25rem;">' + sys['status'] + '</div>'
                '<div style="font-size:0.65rem;color:' + t['text_muted'] + ';">⬆️ ' + sys['uptime'] + '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)
