"""
Audit Planning Module for AURIX.
Annual audit plan, timeline visualization, and resource management.
"""

import streamlit as st
from datetime import datetime, date, timedelta
from typing import Dict, List, Any
import json
import uuid
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer, render_progress_bar
from data.seeds import AUDIT_UNIVERSE, get_all_audit_areas


def render():
    """Render the audit planning page."""
    t = get_current_theme()
    
    render_page_header(
        "📅 Audit Planning",
        "Annual audit plan, scheduling, and resource management"
    )
    
    # Initialize session state
    if 'audit_plan' not in st.session_state:
        st.session_state.audit_plan = _generate_sample_plan()
    if 'audit_resources' not in st.session_state:
        st.session_state.audit_resources = _generate_sample_resources()
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Plan Overview",
        "📅 Timeline",
        "👥 Resources",
        "➕ Add Engagement",
        "📈 Coverage Analysis"
    ])
    
    with tab1:
        _render_plan_overview(t)
    
    with tab2:
        _render_timeline(t)
    
    with tab3:
        _render_resources(t)
    
    with tab4:
        _render_add_engagement(t)
    
    with tab5:
        _render_coverage_analysis(t)
    
    render_footer()


def _generate_sample_plan():
    """Generate sample audit plan data."""
    statuses = ['Planned', 'In Progress', 'Completed', 'Deferred']
    priorities = ['High', 'Medium', 'Low']
    risk_ratings = ['High', 'Medium', 'Low']
    
    sample_engagements = []
    all_areas = get_all_audit_areas()
    
    for i, area in enumerate(all_areas[:15]):  # Generate 15 sample engagements
        start_month = random.randint(1, 10)
        duration = random.randint(2, 6)
        
        engagement = {
            'id': str(uuid.uuid4()),
            'name': f"{area} Review",
            'audit_area': area,
            'category': [cat for cat, areas in AUDIT_UNIVERSE.items() if area in areas][0],
            'status': statuses[min(i // 4, 3)],
            'priority': random.choice(priorities),
            'risk_rating': random.choice(risk_ratings),
            'start_date': date(2025, start_month, 1).isoformat(),
            'end_date': date(2025, min(start_month + duration, 12), 28).isoformat(),
            'budgeted_hours': random.randint(80, 320),
            'actual_hours': random.randint(0, 200) if i < 8 else 0,
            'lead_auditor': random.choice(['Ahmad R.', 'Budi S.', 'Citra D.', 'Dewi P.']),
            'team_size': random.randint(2, 5),
            'completion': random.randint(0, 100) if i < 8 else 0,
        }
        sample_engagements.append(engagement)
    
    return sample_engagements


def _generate_sample_resources():
    """Generate sample resource data."""
    return [
        {'name': 'Ahmad Rizki', 'role': 'Audit Manager', 'capacity': 160, 'allocated': 120, 'skills': ['Credit Risk', 'Operational Risk']},
        {'name': 'Budi Santoso', 'role': 'Senior Auditor', 'capacity': 160, 'allocated': 145, 'skills': ['IT Audit', 'Cybersecurity']},
        {'name': 'Citra Dewi', 'role': 'Senior Auditor', 'capacity': 160, 'allocated': 100, 'skills': ['Compliance', 'AML']},
        {'name': 'Dewi Permata', 'role': 'Staff Auditor', 'capacity': 160, 'allocated': 155, 'skills': ['Financial Audit', 'Treasury']},
        {'name': 'Eko Prasetyo', 'role': 'Staff Auditor', 'capacity': 160, 'allocated': 80, 'skills': ['Operations', 'HR']},
        {'name': 'Fitri Handayani', 'role': 'IT Auditor', 'capacity': 160, 'allocated': 140, 'skills': ['IT General Controls', 'Application Security']},
    ]


def _render_plan_overview(t: dict):
    """Render plan overview with KPIs."""
    st.markdown("### 📊 Annual Audit Plan 2025")
    
    plan = st.session_state.audit_plan
    
    # Calculate metrics
    total = len(plan)
    completed = len([e for e in plan if e['status'] == 'Completed'])
    in_progress = len([e for e in plan if e['status'] == 'In Progress'])
    planned = len([e for e in plan if e['status'] == 'Planned'])
    deferred = len([e for e in plan if e['status'] == 'Deferred'])
    
    total_hours = sum(e['budgeted_hours'] for e in plan)
    actual_hours = sum(e['actual_hours'] for e in plan)
    
    # Summary cards
    cols = st.columns(6)
    
    metrics = [
        ("Total Audits", str(total), t['text']),
        ("Completed", str(completed), t['success']),
        ("In Progress", str(in_progress), t['primary']),
        ("Planned", str(planned), t['accent']),
        ("Deferred", str(deferred), t['warning']),
        ("Hours Used", f"{actual_hours:,}/{total_hours:,}", t['text_muted']),
    ]
    
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:{color};">{value}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{label}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress bar
    completion_pct = (completed / total * 100) if total > 0 else 0
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
            <span style="font-weight:600;color:{t['text']};">Annual Plan Progress</span>
            <span style="font-weight:600;color:{t['success']};">{completion_pct:.1f}%</span>
        </div>
        <div style="height:12px;background:{t['border']};border-radius:6px;overflow:hidden;">
            <div style="width:{completion_pct}%;height:100%;background:linear-gradient(90deg, {t['success']}, {t['accent']});border-radius:6px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:0.5rem;font-size:0.75rem;color:{t['text_muted']};">
            <span>{completed} completed</span>
            <span>{in_progress} in progress</span>
            <span>{planned} planned</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Filter and engagement list
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        search = st.text_input("🔍 Search engagements", placeholder="Search by name or area...")
    with col_f2:
        status_filter = st.selectbox("Status", ["All", "Completed", "In Progress", "Planned", "Deferred"])
    with col_f3:
        priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    
    # Engagement cards
    for eng in plan:
        if search and search.lower() not in eng['name'].lower() and search.lower() not in eng['audit_area'].lower():
            continue
        if status_filter != "All" and eng['status'] != status_filter:
            continue
        if priority_filter != "All" and eng['priority'] != priority_filter:
            continue
        
        status_colors = {
            'Completed': t['success'],
            'In Progress': t['primary'],
            'Planned': t['accent'],
            'Deferred': t['warning']
        }
        status_color = status_colors.get(eng['status'], t['text_muted'])
        
        priority_colors = {
            'High': t['danger'],
            'Medium': t['warning'],
            'Low': t['success']
        }
        priority_color = priority_colors.get(eng['priority'], t['text_muted'])
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;justify-content:space-between;align-items:start;">
                <div style="flex:1;">
                    <div style="font-weight:600;color:{t['text']};font-size:1rem;">{eng['name']}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']};margin-top:0.25rem;">
                        📁 {eng['category']} • 👤 {eng['lead_auditor']} • 👥 {eng['team_size']} members
                    </div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};margin-top:0.5rem;">
                        📅 {eng['start_date']} to {eng['end_date']} • ⏱️ {eng['actual_hours']}/{eng['budgeted_hours']} hours
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="background:{status_color}20;color:{status_color};padding:0.25rem 0.75rem;border-radius:20px;font-size:0.75rem;font-weight:600;display:inline-block;margin-bottom:0.5rem;">
                        {eng['status']}
                    </span>
                    <br>
                    <span style="background:{priority_color}20;color:{priority_color};padding:0.2rem 0.5rem;border-radius:12px;font-size:0.7rem;">
                        {eng['priority']} Priority
                    </span>
                </div>
            </div>
            <div style="margin-top:0.75rem;">
                <div style="height:6px;background:{t['border']};border-radius:3px;overflow:hidden;">
                    <div style="width:{eng['completion']}%;height:100%;background:{status_color};"></div>
                </div>
                <div style="text-align:right;font-size:0.7rem;color:{t['text_muted']};margin-top:0.25rem;">{eng['completion']}% complete</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_timeline(t: dict):
    """Render Gantt-style timeline."""
    st.markdown("### 📅 Audit Timeline - 2025")
    
    plan = st.session_state.audit_plan
    
    # Month headers
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Create timeline header
    header_cols = "".join([f'<div style="flex:1;text-align:center;font-size:0.7rem;color:{t["text_muted"]};">{m}</div>' for m in months])
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:1rem;">
        <div style="display:flex;border-bottom:1px solid {t['border']};padding-bottom:0.5rem;margin-bottom:1rem;">
            <div style="width:200px;font-weight:600;color:{t['text']};font-size:0.85rem;">Engagement</div>
            <div style="flex:1;display:flex;">{header_cols}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Timeline bars
    status_colors = {
        'Completed': t['success'],
        'In Progress': t['primary'],
        'Planned': t['accent'],
        'Deferred': t['warning']
    }
    
    for eng in plan[:10]:  # Show first 10
        start_month = int(eng['start_date'].split('-')[1])
        end_month = int(eng['end_date'].split('-')[1])
        
        bar_start = (start_month - 1) / 12 * 100
        bar_width = (end_month - start_month + 1) / 12 * 100
        
        color = status_colors.get(eng['status'], t['text_muted'])
        
        st.markdown(f'''
        <div style="display:flex;align-items:center;margin-bottom:0.5rem;">
            <div style="width:200px;font-size:0.75rem;color:{t['text']};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="{eng['name']}">{eng['name'][:25]}...</div>
            <div style="flex:1;height:20px;position:relative;background:{t['bg_secondary']};border-radius:4px;">
                <div style="position:absolute;left:{bar_start}%;width:{bar_width}%;height:100%;background:{color};border-radius:4px;opacity:0.8;"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Legend
    st.markdown(f'''
    <div style="display:flex;gap:1.5rem;margin-top:1rem;justify-content:center;">
        <span style="font-size:0.75rem;color:{t['text_muted']};"><span style="display:inline-block;width:12px;height:12px;background:{t['success']};border-radius:2px;margin-right:4px;"></span> Completed</span>
        <span style="font-size:0.75rem;color:{t['text_muted']};"><span style="display:inline-block;width:12px;height:12px;background:{t['primary']};border-radius:2px;margin-right:4px;"></span> In Progress</span>
        <span style="font-size:0.75rem;color:{t['text_muted']};"><span style="display:inline-block;width:12px;height:12px;background:{t['accent']};border-radius:2px;margin-right:4px;"></span> Planned</span>
        <span style="font-size:0.75rem;color:{t['text_muted']};"><span style="display:inline-block;width:12px;height:12px;background:{t['warning']};border-radius:2px;margin-right:4px;"></span> Deferred</span>
    </div>
    ''', unsafe_allow_html=True)


def _render_resources(t: dict):
    """Render resource management."""
    st.markdown("### 👥 Resource Allocation")
    
    resources = st.session_state.audit_resources
    
    # Team capacity overview
    total_capacity = sum(r['capacity'] for r in resources)
    total_allocated = sum(r['allocated'] for r in resources)
    utilization = (total_allocated / total_capacity * 100) if total_capacity > 0 else 0
    
    cols = st.columns(4)
    
    metrics = [
        ("Team Size", str(len(resources)), t['primary']),
        ("Total Capacity", f"{total_capacity}h/month", t['accent']),
        ("Allocated", f"{total_allocated}h", t['success']),
        ("Utilization", f"{utilization:.0f}%", t['warning'] if utilization > 90 else t['success']),
    ]
    
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:{color};">{value}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{label}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Resource cards
    for res in resources:
        util_pct = (res['allocated'] / res['capacity'] * 100) if res['capacity'] > 0 else 0
        util_color = t['danger'] if util_pct > 95 else (t['warning'] if util_pct > 80 else t['success'])
        
        skills_html = " ".join([f'<span style="background:{t["primary"]}20;color:{t["primary"]};padding:0.15rem 0.5rem;border-radius:12px;font-size:0.65rem;margin-right:0.25rem;">{s}</span>' for s in res['skills']])
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-weight:600;color:{t['text']};">{res['name']}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']};">{res['role']}</div>
                    <div style="margin-top:0.5rem;">{skills_html}</div>
                </div>
                <div style="text-align:right;min-width:150px;">
                    <div style="font-size:0.8rem;color:{t['text_muted']};margin-bottom:0.25rem;">
                        {res['allocated']}h / {res['capacity']}h
                    </div>
                    <div style="height:8px;background:{t['border']};border-radius:4px;overflow:hidden;">
                        <div style="width:{util_pct}%;height:100%;background:{util_color};"></div>
                    </div>
                    <div style="font-size:0.7rem;color:{util_color};margin-top:0.25rem;">{util_pct:.0f}% utilized</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_add_engagement(t: dict):
    """Render form to add new engagement."""
    st.markdown("### ➕ Add New Audit Engagement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        eng_name = st.text_input("Engagement Name", placeholder="e.g., Credit Risk Review Q1 2025")
        
        category = st.selectbox("Category", options=list(AUDIT_UNIVERSE.keys()))
        audit_area = st.selectbox("Audit Area", options=AUDIT_UNIVERSE.get(category, []))
        
        col1a, col1b = st.columns(2)
        with col1a:
            start_date = st.date_input("Start Date", value=date.today())
        with col1b:
            end_date = st.date_input("End Date", value=date.today() + timedelta(days=30))
    
    with col2:
        priority = st.selectbox("Priority", options=["High", "Medium", "Low"])
        risk_rating = st.selectbox("Risk Rating", options=["High", "Medium", "Low"])
        
        budgeted_hours = st.number_input("Budgeted Hours", min_value=20, max_value=1000, value=160)
        
        resources = st.session_state.audit_resources
        lead_auditor = st.selectbox("Lead Auditor", options=[r['name'] for r in resources])
        
        team_size = st.number_input("Team Size", min_value=1, max_value=10, value=3)
    
    objectives = st.text_area("Objectives", placeholder="Define the objectives of this audit engagement...")
    
    if st.button("➕ Add to Plan", type="primary", use_container_width=True):
        if eng_name and audit_area:
            new_engagement = {
                'id': str(uuid.uuid4()),
                'name': eng_name,
                'audit_area': audit_area,
                'category': category,
                'status': 'Planned',
                'priority': priority,
                'risk_rating': risk_rating,
                'start_date': str(start_date),
                'end_date': str(end_date),
                'budgeted_hours': budgeted_hours,
                'actual_hours': 0,
                'lead_auditor': lead_auditor,
                'team_size': team_size,
                'completion': 0,
                'objectives': objectives
            }
            st.session_state.audit_plan.append(new_engagement)
            st.success(f"✅ '{eng_name}' added to audit plan!")
        else:
            st.error("Please fill in all required fields.")


def _render_coverage_analysis(t: dict):
    """Render audit coverage analysis."""
    st.markdown("### 📈 Audit Universe Coverage Analysis")
    
    plan = st.session_state.audit_plan
    
    # Calculate coverage by category
    coverage_data = {}
    for category, areas in AUDIT_UNIVERSE.items():
        total_areas = len(areas)
        covered_areas = len([e for e in plan if e['category'] == category])
        coverage_pct = (covered_areas / total_areas * 100) if total_areas > 0 else 0
        coverage_data[category] = {
            'total': total_areas,
            'covered': covered_areas,
            'pct': coverage_pct
        }
    
    # Coverage cards
    for category, data in coverage_data.items():
        color = t['success'] if data['pct'] >= 50 else (t['warning'] if data['pct'] >= 25 else t['danger'])
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                <span style="font-weight:600;color:{t['text']};">{category}</span>
                <span style="color:{color};font-weight:600;">{data['pct']:.0f}% covered</span>
            </div>
            <div style="height:10px;background:{t['border']};border-radius:5px;overflow:hidden;margin-bottom:0.5rem;">
                <div style="width:{data['pct']}%;height:100%;background:{color};"></div>
            </div>
            <div style="font-size:0.75rem;color:{t['text_muted']};">
                {data['covered']} of {data['total']} audit areas covered in current plan
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Gap analysis
    st.markdown("#### 🔍 Coverage Gaps")
    
    gaps_found = False
    for category, areas in AUDIT_UNIVERSE.items():
        covered = [e['audit_area'] for e in plan if e['category'] == category]
        uncovered = [a for a in areas if a not in covered]
        
        if uncovered:
            gaps_found = True
            st.markdown(f"**{category}** - {len(uncovered)} uncovered areas:")
            for area in uncovered:
                st.markdown(f"- ⚠️ {area}")
    
    if not gaps_found:
        st.success("✅ All audit universe areas are covered in the current plan!")
