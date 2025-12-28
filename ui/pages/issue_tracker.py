"""
Issue Tracker Module for AURIX.
Kanban-style issue tracking for audit findings and remediation.
"""

import streamlit as st
from datetime import datetime, date, timedelta
import uuid
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the issue tracker page."""
    t = get_current_theme()
    
    render_page_header(
        "📌 Issue Tracker",
        "Track and manage audit issues with Kanban-style workflow"
    )
    
    # Initialize issues
    if 'issues' not in st.session_state:
        st.session_state.issues = _generate_sample_issues()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Kanban Board",
        "📊 List View",
        "➕ New Issue",
        "📈 Analytics"
    ])
    
    with tab1:
        _render_kanban_board(t)
    
    with tab2:
        _render_list_view(t)
    
    with tab3:
        _render_new_issue(t)
    
    with tab4:
        _render_analytics(t)
    
    render_footer()


def _generate_sample_issues():
    """Generate sample issues."""
    return [
        {"id": "ISS-001", "title": "Segregation of Duties Violation", "status": "Open", "priority": "Critical", "assignee": "Ahmad R.", "due": "2025-01-15", "category": "Controls", "progress": 0},
        {"id": "ISS-002", "title": "Incomplete KYC Documentation", "status": "In Progress", "priority": "High", "assignee": "Budi S.", "due": "2025-01-20", "category": "Compliance", "progress": 40},
        {"id": "ISS-003", "title": "System Access Rights Review", "status": "In Progress", "priority": "Medium", "assignee": "Citra D.", "due": "2025-01-25", "category": "IT", "progress": 65},
        {"id": "ISS-004", "title": "Credit Limit Breach - 3 Cases", "status": "Open", "priority": "High", "assignee": "Dewi P.", "due": "2025-01-18", "category": "Credit", "progress": 0},
        {"id": "ISS-005", "title": "Vendor Master Data Cleanup", "status": "Review", "priority": "Medium", "assignee": "Ahmad R.", "due": "2025-01-10", "category": "Operations", "progress": 90},
        {"id": "ISS-006", "title": "AML Alert Backlog", "status": "In Progress", "priority": "Critical", "assignee": "Budi S.", "due": "2025-01-12", "category": "AML", "progress": 55},
        {"id": "ISS-007", "title": "Patch Management Gaps", "status": "Review", "priority": "High", "assignee": "Citra D.", "due": "2025-01-08", "category": "IT", "progress": 95},
        {"id": "ISS-008", "title": "Reconciliation Delays", "status": "Closed", "priority": "Medium", "assignee": "Dewi P.", "due": "2025-01-05", "category": "Operations", "progress": 100},
        {"id": "ISS-009", "title": "Policy Documentation Update", "status": "Closed", "priority": "Low", "assignee": "Ahmad R.", "due": "2025-01-03", "category": "Compliance", "progress": 100},
        {"id": "ISS-010", "title": "BCP Testing Overdue", "status": "Open", "priority": "High", "assignee": "Citra D.", "due": "2025-01-30", "category": "IT", "progress": 0},
    ]


def _render_kanban_board(t: dict):
    """Render Kanban board view."""
    st.markdown("### 📋 Issue Kanban Board")
    
    issues = st.session_state.issues
    
    # Status columns
    statuses = ["Open", "In Progress", "Review", "Closed"]
    status_icons = ["📥", "🔄", "👁️", "✅"]
    status_colors = [t['danger'], t['primary'], t['warning'], t['success']]
    
    # Summary stats
    cols = st.columns(4)
    for col, status, icon, color in zip(cols, statuses, status_icons, status_colors):
        count = len([i for i in issues if i['status'] == status])
        with col:
            card_html = (
                '<div style="background:' + color + '15;border:2px solid ' + color + ';border-radius:12px;padding:1rem;text-align:center;">'
                '<div style="font-size:1.5rem;">' + icon + '</div>'
                '<div style="font-size:1.75rem;font-weight:700;color:' + color + ';">' + str(count) + '</div>'
                '<div style="font-size:0.8rem;color:' + t['text_muted'] + ';">' + status + '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kanban columns
    cols = st.columns(4)
    
    priority_colors = {"Critical": t['danger'], "High": t['warning'], "Medium": t['accent'], "Low": t['success']}
    
    for col, status, icon, status_color in zip(cols, statuses, status_icons, status_colors):
        with col:
            # Column header
            count = len([i for i in issues if i['status'] == status])
            header_html = (
                '<div style="background:' + status_color + '10;border-top:4px solid ' + status_color + ';border-radius:12px;padding:1rem;margin-bottom:0.5rem;">'
                '<div style="font-weight:700;color:' + t['text'] + ';display:flex;align-items:center;gap:0.5rem;">'
                '<span>' + icon + '</span>'
                '<span>' + status + '</span>'
                '<span style="background:' + status_color + ';color:white;padding:0.1rem 0.5rem;border-radius:10px;font-size:0.7rem;margin-left:auto;">' + str(count) + '</span>'
                '</div>'
                '</div>'
            )
            st.markdown(header_html, unsafe_allow_html=True)
            
            # Issue cards
            for issue in [i for i in issues if i['status'] == status]:
                priority_color = priority_colors.get(issue['priority'], t['text_muted'])
                title_short = issue['title'][:25] + '...' if len(issue['title']) > 25 else issue['title']
                assignee_short = issue['assignee'].split()[0]
                progress = str(issue['progress'])
                
                card_html = (
                    '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-left:4px solid ' + priority_color + ';border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">'
                    '<div style="font-size:0.65rem;color:' + t['text_muted'] + ';margin-bottom:0.25rem;">' + issue['id'] + '</div>'
                    '<div style="font-weight:600;color:' + t['text'] + ';font-size:0.8rem;margin-bottom:0.5rem;">' + title_short + '</div>'
                    '<div style="display:flex;justify-content:space-between;align-items:center;">'
                    '<span style="background:' + priority_color + '20;color:' + priority_color + ';padding:0.1rem 0.4rem;border-radius:6px;font-size:0.6rem;font-weight:600;">' + issue['priority'] + '</span>'
                    '<span style="font-size:0.65rem;color:' + t['text_muted'] + ';">👤 ' + assignee_short + '</span>'
                    '</div>'
                    '<div style="height:4px;background:' + t['border'] + ';border-radius:2px;margin-top:0.5rem;overflow:hidden;">'
                    '<div style="width:' + progress + '%;height:100%;background:' + priority_color + ';"></div>'
                    '</div>'
                    '</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
    
    # Drag hint
    hint_html = (
        '<div style="text-align:center;margin-top:1rem;font-size:0.75rem;color:' + t['text_muted'] + ';">'
        '💡 Click on any issue to view details and update status'
        '</div>'
    )
    st.markdown(hint_html, unsafe_allow_html=True)


def _render_list_view(t: dict):
    """Render list view of issues."""
    st.markdown("### 📊 Issue List")
    
    issues = st.session_state.issues
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_status = st.selectbox("Status", ["All", "Open", "In Progress", "Review", "Closed"])
    with col2:
        filter_priority = st.selectbox("Priority", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        filter_assignee = st.selectbox("Assignee", ["All"] + list(set(i['assignee'] for i in issues)))
    with col4:
        search = st.text_input("🔍 Search", placeholder="Search issues...")
    
    # Filter issues
    filtered = issues
    if filter_status != "All":
        filtered = [i for i in filtered if i['status'] == filter_status]
    if filter_priority != "All":
        filtered = [i for i in filtered if i['priority'] == filter_priority]
    if filter_assignee != "All":
        filtered = [i for i in filtered if i['assignee'] == filter_assignee]
    if search:
        filtered = [i for i in filtered if search.lower() in i['title'].lower() or search.lower() in i['id'].lower()]
    
    priority_colors = {"Critical": t['danger'], "High": t['warning'], "Medium": t['accent'], "Low": t['success']}
    status_colors = {"Open": t['danger'], "In Progress": t['primary'], "Review": t['warning'], "Closed": t['success']}
    
    # Table header
    header_html = (
        '<div style="display:grid;grid-template-columns:80px 1fr 100px 100px 120px 100px 80px;gap:0.5rem;padding:0.75rem;background:' + t['bg_secondary'] + ';border-radius:8px 8px 0 0;font-weight:600;font-size:0.8rem;color:' + t['text'] + ';">'
        '<div>ID</div>'
        '<div>Title</div>'
        '<div>Status</div>'
        '<div>Priority</div>'
        '<div>Assignee</div>'
        '<div>Due Date</div>'
        '<div>Progress</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Table rows
    for issue in filtered:
        priority_color = priority_colors.get(issue['priority'], t['text_muted'])
        status_color = status_colors.get(issue['status'], t['text_muted'])
        
        # Check if overdue
        is_overdue = issue['due'] < datetime.now().strftime('%Y-%m-%d') and issue['status'] != 'Closed'
        due_color = '#dc2626' if is_overdue else t['text_muted']
        overdue_icon = '⚠️ ' if is_overdue else ''
        progress = str(issue['progress'])
        
        row_html = (
            '<div style="display:grid;grid-template-columns:80px 1fr 100px 100px 120px 100px 80px;gap:0.5rem;padding:0.75rem;background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-top:none;font-size:0.85rem;align-items:center;">'
            '<div style="color:' + t['primary'] + ';font-weight:600;">' + issue['id'] + '</div>'
            '<div style="color:' + t['text'] + ';">' + issue['title'] + '</div>'
            '<div><span style="background:' + status_color + '20;color:' + status_color + ';padding:0.2rem 0.5rem;border-radius:12px;font-size:0.7rem;font-weight:600;">' + issue['status'] + '</span></div>'
            '<div><span style="background:' + priority_color + '20;color:' + priority_color + ';padding:0.2rem 0.5rem;border-radius:12px;font-size:0.7rem;font-weight:600;">' + issue['priority'] + '</span></div>'
            '<div style="color:' + t['text_muted'] + ';">👤 ' + issue['assignee'] + '</div>'
            '<div style="color:' + due_color + ';">' + overdue_icon + issue['due'] + '</div>'
            '<div>'
            '<div style="height:6px;background:' + t['border'] + ';border-radius:3px;overflow:hidden;">'
            '<div style="width:' + progress + '%;height:100%;background:' + status_color + ';"></div>'
            '</div>'
            '<div style="font-size:0.65rem;color:' + t['text_muted'] + ';text-align:center;">' + progress + '%</div>'
            '</div>'
            '</div>'
        )
        st.markdown(row_html, unsafe_allow_html=True)


def _render_new_issue(t: dict):
    """Render new issue form."""
    st.markdown("### ➕ Create New Issue")
    
    col1, col2 = st.columns(2)
    
    with col1:
        issue_title = st.text_input("Issue Title", placeholder="Brief description of the issue")
        
        category = st.selectbox("Category", ["Controls", "Compliance", "IT", "Credit", "Operations", "AML", "Treasury", "HR"])
        
        priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
        
        assignee = st.selectbox("Assignee", ["Ahmad R.", "Budi S.", "Citra D.", "Dewi P.", "Unassigned"])
    
    with col2:
        due_date = st.date_input("Due Date", value=date.today() + timedelta(days=30))
        
        related_finding = st.text_input("Related Finding ID", placeholder="e.g., FND-2024-001")
        
        source = st.selectbox("Source", ["Internal Audit", "External Audit", "Regulatory", "Self-Identified", "Management"])
        
        auditee = st.text_input("Auditee / Process Owner", placeholder="Name of responsible person")
    
    description = st.text_area(
        "Issue Description",
        height=150,
        placeholder="Detailed description of the issue, including:\n- What was found\n- Where it occurred\n- Impact assessment\n- Root cause (if known)"
    )
    
    recommended_action = st.text_area(
        "Recommended Action",
        height=100,
        placeholder="What actions should be taken to resolve this issue?"
    )
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("💾 Save as Draft", use_container_width=True):
            st.info("Draft saved!")
    
    with col_btn2:
        if st.button("📤 Create Issue", type="primary", use_container_width=True):
            if issue_title:
                new_id = "ISS-" + str(len(st.session_state.issues)+1).zfill(3)
                new_issue = {
                    "id": new_id,
                    "title": issue_title,
                    "status": "Open",
                    "priority": priority,
                    "assignee": assignee,
                    "due": str(due_date),
                    "category": category,
                    "progress": 0
                }
                st.session_state.issues.append(new_issue)
                st.success("✅ Issue " + new_id + " created successfully!")
            else:
                st.error("Please enter an issue title.")
    
    with col_btn3:
        if st.button("🔄 Clear Form", use_container_width=True):
            st.rerun()


def _render_analytics(t: dict):
    """Render issue analytics."""
    st.markdown("### 📈 Issue Analytics")
    
    issues = st.session_state.issues
    
    # Summary metrics
    total = len(issues)
    open_issues = len([i for i in issues if i['status'] == 'Open'])
    in_progress = len([i for i in issues if i['status'] == 'In Progress'])
    overdue = len([i for i in issues if i['due'] < datetime.now().strftime('%Y-%m-%d') and i['status'] != 'Closed'])
    critical = len([i for i in issues if i['priority'] == 'Critical' and i['status'] != 'Closed'])
    
    cols = st.columns(5)
    
    metrics = [
        ("Total Issues", total, t['text'], "📋"),
        ("Open", open_issues, t['danger'], "📥"),
        ("In Progress", in_progress, t['primary'], "🔄"),
        ("Overdue", overdue, t['danger'], "⚠️"),
        ("Critical Open", critical, t['danger'], "🔴"),
    ]
    
    for col, (label, value, color, icon) in zip(cols, metrics):
        with col:
            card_html = (
                '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:12px;padding:1rem;text-align:center;">'
                '<div style="font-size:1.5rem;margin-bottom:0.25rem;">' + icon + '</div>'
                '<div style="font-size:1.75rem;font-weight:700;color:' + color + ';">' + str(value) + '</div>'
                '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">' + label + '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts simulation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### By Status")
        
        status_data = {"Open": 3, "In Progress": 3, "Review": 2, "Closed": 2}
        status_colors_map = {"Open": t['danger'], "In Progress": t['primary'], "Review": t['warning'], "Closed": t['success']}
        
        for status, count in status_data.items():
            pct = count / total * 100
            color = status_colors_map[status]
            pct_str = str(int(pct))
            
            bar_html = (
                '<div style="margin-bottom:0.75rem;">'
                '<div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">'
                '<span style="color:' + t['text'] + ';font-size:0.85rem;">' + status + '</span>'
                '<span style="color:' + t['text_muted'] + ';font-size:0.85rem;">' + str(count) + ' (' + pct_str + '%)</span>'
                '</div>'
                '<div style="height:20px;background:' + t['border'] + ';border-radius:10px;overflow:hidden;">'
                '<div style="width:' + pct_str + '%;height:100%;background:' + color + ';border-radius:10px;"></div>'
                '</div>'
                '</div>'
            )
            st.markdown(bar_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### By Priority")
        
        priority_data = {"Critical": 2, "High": 4, "Medium": 3, "Low": 1}
        priority_colors_map = {"Critical": t['danger'], "High": t['warning'], "Medium": t['accent'], "Low": t['success']}
        
        for priority, count in priority_data.items():
            pct = count / total * 100
            color = priority_colors_map[priority]
            pct_str = str(int(pct))
            
            bar_html = (
                '<div style="margin-bottom:0.75rem;">'
                '<div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">'
                '<span style="color:' + t['text'] + ';font-size:0.85rem;">' + priority + '</span>'
                '<span style="color:' + t['text_muted'] + ';font-size:0.85rem;">' + str(count) + ' (' + pct_str + '%)</span>'
                '</div>'
                '<div style="height:20px;background:' + t['border'] + ';border-radius:10px;overflow:hidden;">'
                '<div style="width:' + pct_str + '%;height:100%;background:' + color + ';border-radius:10px;"></div>'
                '</div>'
                '</div>'
            )
            st.markdown(bar_html, unsafe_allow_html=True)
    
    # Aging analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Issue Aging Analysis")
    
    aging_brackets = [
        ("0-7 days", 2, t['success']),
        ("8-14 days", 3, t['accent']),
        ("15-30 days", 2, t['warning']),
        ("31-60 days", 2, t['danger']),
        (">60 days", 1, "#7f1d1d"),
    ]
    
    cols = st.columns(5)
    for col, (bracket, count, color) in zip(cols, aging_brackets):
        with col:
            card_html = (
                '<div style="background:' + color + '20;border:1px solid ' + color + ';border-radius:12px;padding:1rem;text-align:center;">'
                '<div style="font-size:1.5rem;font-weight:700;color:' + color + ';">' + str(count) + '</div>'
                '<div style="font-size:0.7rem;color:' + t['text_muted'] + ';">' + bracket + '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
