"""
Audit Timeline Module for AURIX.
Simplified timeline visualization for audit engagements.
"""

import streamlit as st
from datetime import datetime, date, timedelta

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the audit timeline page."""
    t = get_current_theme()
    
    render_page_header(
        "📅 Audit Timeline",
        "Visual timeline of all audit engagements and milestones"
    )
    
    # Timeline controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        view_mode = st.selectbox("View", ["Quarter", "Month", "Year"], label_visibility="collapsed")
    with col2:
        st.button("◀ Previous", use_container_width=True)
    with col3:
        st.button("Today", use_container_width=True)
    with col4:
        st.button("Next ▶", use_container_width=True)
    
    # Current period display
    st.markdown(f"""
    <div style="text-align:center;margin:1.5rem 0;">
        <div style="font-size:1.5rem;font-weight:700;color:{t['text']};">Q1 2025</div>
        <div style="color:{t['text_muted']};">January - March 2025</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📊 Gantt View", "📍 Milestones"])
    
    with tab1:
        _render_gantt_simple(t)
    
    with tab2:
        _render_milestones(t)
    
    render_footer()


def _render_gantt_simple(t: dict):
    """Render simplified Gantt timeline using progress bars."""
    
    # Engagements data
    engagements = [
        {"name": "Credit Risk Assessment", "start": "W1", "end": "W8", "progress": 75, "status": "active", "lead": "Ahmad R.", "weeks": 8},
        {"name": "IT General Controls", "start": "W3", "end": "W8", "progress": 40, "status": "active", "lead": "Citra D.", "weeks": 6},
        {"name": "AML/CFT Review", "start": "W2", "end": "W11", "progress": 60, "status": "active", "lead": "Budi S.", "weeks": 10},
        {"name": "Treasury Operations", "start": "W6", "end": "W10", "progress": 0, "status": "planned", "lead": "Dewi P.", "weeks": 5},
        {"name": "Branch Audit - Jakarta", "start": "W8", "end": "W11", "progress": 0, "status": "planned", "lead": "Ahmad R.", "weeks": 4},
        {"name": "Vendor Management", "start": "W10", "end": "W12", "progress": 0, "status": "planned", "lead": "Citra D.", "weeks": 3},
    ]
    
    status_colors = {
        "active": t['primary'],
        "planned": t['accent'],
        "completed": t['success'],
        "delayed": t['danger']
    }
    
    status_icons = {
        "active": "🔵",
        "planned": "⚪",
        "completed": "✅",
        "delayed": "🔴"
    }
    
    # Engagement cards
    for eng in engagements:
        color = status_colors.get(eng['status'], t['text_muted'])
        icon = status_icons.get(eng['status'], "⚪")
        progress = eng['progress']
        
        col1, col2, col3 = st.columns([3, 4, 1])
        
        with col1:
            st.markdown(f"""
            <div style="padding:0.5rem;">
                <div style="font-weight:600;color:{t['text']};">{icon} {eng['name']}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">👤 {eng['lead']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="padding:0.5rem;">
                <div style="font-size:0.7rem;color:{t['text_muted']};margin-bottom:0.25rem;">{eng['start']} → {eng['end']} ({eng['weeks']}w)</div>
                <div style="height:20px;background:{t['bg_secondary']};border-radius:10px;overflow:hidden;">
                    <div style="height:100%;width:{progress}%;background:{color};border-radius:10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="padding:0.5rem;text-align:center;">
                <div style="font-size:1.25rem;font-weight:700;color:{color};">{progress}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<hr style='margin:0.25rem 0;border-color:{t['border']};opacity:0.3;'>", unsafe_allow_html=True)
    
    # Legend
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(4)
    legends = [
        ("Active", t['primary'], "🔵"),
        ("Planned", t['accent'], "⚪"),
        ("Completed", t['success'], "✅"),
        ("Delayed", t['danger'], "🔴")
    ]
    for col, (label, color, icon) in zip(cols, legends):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:0.5rem;background:{t['card']};border-radius:8px;border:1px solid {t['border']};">
                <span style="color:{color};">{icon}</span>
                <span style="font-size:0.8rem;color:{t['text']};margin-left:0.5rem;">{label}</span>
            </div>
            """, unsafe_allow_html=True)


def _render_milestones(t: dict):
    """Render milestones list."""
    
    milestones = [
        {"date": "Jan 15", "title": "Q4 2024 Report Submission", "type": "deadline", "status": "completed"},
        {"date": "Jan 31", "title": "Annual Audit Plan Approval", "type": "approval", "status": "completed"},
        {"date": "Feb 15", "title": "Credit Risk Draft Report", "type": "deliverable", "status": "upcoming"},
        {"date": "Feb 28", "title": "OJK Exam Preparation", "type": "regulatory", "status": "upcoming"},
        {"date": "Mar 15", "title": "IT Audit Fieldwork Complete", "type": "milestone", "status": "upcoming"},
        {"date": "Mar 31", "title": "AC Presentation Q1", "type": "presentation", "status": "upcoming"},
    ]
    
    type_icons = {
        "deadline": "⏰",
        "approval": "✅",
        "deliverable": "📄",
        "regulatory": "📋",
        "milestone": "🎯",
        "presentation": "📊"
    }
    
    st.markdown("### 📍 Key Milestones")
    
    for ms in milestones:
        icon = type_icons.get(ms['type'], "📌")
        is_completed = ms['status'] == 'completed'
        
        if is_completed:
            color = t['success']
            badge_text = "COMPLETED"
        else:
            color = t['primary']
            badge_text = "UPCOMING"
        
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-left:4px solid {color};border-radius:0 12px 12px 0;padding:1rem;margin-bottom:0.75rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-weight:600;color:{t['text']};">{icon} {ms['title']}</span>
                    <div style="font-size:0.75rem;color:{t['text_muted']};margin-top:0.25rem;">📅 {ms['date']} 2025</div>
                </div>
                <span style="padding:0.25rem 0.75rem;background:{color}20;color:{color};border-radius:20px;font-size:0.7rem;font-weight:600;">
                    {badge_text}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
