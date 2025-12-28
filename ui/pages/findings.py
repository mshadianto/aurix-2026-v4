"""
Findings Management Page Module for AURIX.
Full lifecycle management of audit findings with tracking and analytics.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

from ui.styles.css_builder import get_current_theme
from ui.components import (
    render_page_header,
    render_footer,
    render_badge,
    risk_badge,
    status_badge,
    render_metric_card,
    render_alert
)
from data.seeds import AUDIT_UNIVERSE, get_all_audit_areas
from app.constants import FindingStatus, FINDING_SEVERITY


class FindingsPage:
    """Audit Findings management page with full lifecycle tracking."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for findings."""
        if 'findings' not in st.session_state:
            st.session_state.findings = []
    
    def render(self):
        """Render the Findings Management page."""
        render_page_header("Findings Tracker", "Full lifecycle management of audit findings")
        
        t = get_current_theme()
        
        # Summary Metrics
        self._render_summary_metrics()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 All Findings", 
            "➕ New Finding", 
            "📊 Analytics",
            "📤 Export"
        ])
        
        with tab1:
            self._render_findings_list()
        
        with tab2:
            self._render_new_finding_form()
        
        with tab3:
            self._render_analytics()
        
        with tab4:
            self._render_export()
        
        render_footer()
    
    def _render_summary_metrics(self):
        """Render summary metrics at the top."""
        t = get_current_theme()
        
        findings = st.session_state.findings
        total = len(findings)
        open_count = len([f for f in findings if f.get('status') == FindingStatus.OPEN])
        in_progress = len([f for f in findings if f.get('status') == FindingStatus.IN_PROGRESS])
        closed = len([f for f in findings if f.get('status') == FindingStatus.CLOSED])
        
        # Count overdue
        today = datetime.now().date()
        overdue = len([
            f for f in findings 
            if f.get('status') != FindingStatus.CLOSED 
            and datetime.strptime(f.get('due_date', '2099-12-31'), '%Y-%m-%d').date() < today
        ])
        
        # Count by severity
        high_count = len([f for f in findings if f.get('severity') in ['HIGH', 'CRITICAL']])
        this_month = len([f for f in findings if f.get('created_at', '').startswith(datetime.now().strftime('%Y-%m'))])
        
        # Use Streamlit columns for metrics
        cols = st.columns(4)
        
        metrics_data = [
            ("TOTAL FINDINGS", str(total), f"+{this_month} this month", t['accent']),
            ("OPEN", str(open_count), f"{in_progress} in progress", t['danger'] if open_count > 0 else t['success']),
            ("HIGH PRIORITY", str(high_count), "Requires attention" if high_count > 0 else "All clear", t['danger'] if high_count > 0 else t['success']),
            ("OVERDUE", str(overdue), "Action needed" if overdue > 0 else "On track", t['danger'] if overdue > 0 else t['success']),
        ]
        
        for col, (label, value, change, color) in zip(cols, metrics_data):
            with col:
                st.markdown(f'''
                <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;">
                    <div style="font-size:0.75rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:{t['text_muted']} !important;margin-bottom:0.5rem;">{label}</div>
                    <div style="font-size:1.75rem;font-weight:700;color:{t['text']} !important;">{value}</div>
                    <div style="font-size:0.75rem;margin-top:0.25rem;color:{color} !important;">{change}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_findings_list(self):
        """Render the list of all findings with filters."""
        t = get_current_theme()
        
        st.markdown("### 📋 Findings List")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", FindingStatus.OPEN, FindingStatus.IN_PROGRESS, FindingStatus.CLOSED],
                key="findings_status_filter"
            )
        
        with col2:
            severity_filter = st.selectbox(
                "Severity",
                ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
                key="findings_severity_filter"
            )
        
        with col3:
            area_filter = st.selectbox(
                "Audit Area",
                ["All"] + get_all_audit_areas(),
                key="findings_area_filter"
            )
        
        with col4:
            overdue_only = st.checkbox("Overdue Only", key="findings_overdue_only")
        
        st.markdown("---")
        
        # Apply filters
        filtered_findings = st.session_state.findings.copy()
        
        if status_filter != "All":
            filtered_findings = [f for f in filtered_findings if f.get('status') == status_filter]
        
        if severity_filter != "All":
            filtered_findings = [f for f in filtered_findings if f.get('severity') == severity_filter]
        
        if area_filter != "All":
            filtered_findings = [f for f in filtered_findings if f.get('audit_area') == area_filter]
        
        if overdue_only:
            today = datetime.now().date()
            filtered_findings = [
                f for f in filtered_findings 
                if f.get('status') != FindingStatus.CLOSED 
                and datetime.strptime(f.get('due_date', '2099-12-31'), '%Y-%m-%d').date() < today
            ]
        
        # Display findings
        if not filtered_findings:
            st.info("📭 No findings match the current filters.")
            
            if not st.session_state.findings:
                st.markdown(f'''
                <div class="pro-card" style="text-align:center;padding:2rem;">
                    <div style="font-size:3rem;margin-bottom:1rem;">📝</div>
                    <div style="font-size:1.1rem;font-weight:600;color:{t['text']} !important;margin-bottom:0.5rem;">
                        No Findings Yet
                    </div>
                    <div style="color:{t['text_secondary']} !important;">
                        Go to "New Finding" tab to create your first audit finding.
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            return
        
        st.markdown(f"**Showing {len(filtered_findings)} finding(s)**")
        
        # Sort by created date (newest first)
        filtered_findings.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        for finding in filtered_findings:
            self._render_finding_card(finding)
    
    def _render_finding_card(self, finding: Dict):
        """Render a single finding card."""
        t = get_current_theme()
        
        # Calculate days remaining/overdue
        due_date = datetime.strptime(finding.get('due_date', '2099-12-31'), '%Y-%m-%d').date()
        today = datetime.now().date()
        days_diff = (due_date - today).days
        
        is_overdue = days_diff < 0 and finding.get('status') != FindingStatus.CLOSED
        
        if is_overdue:
            days_text = f"🔴 {abs(days_diff)} days overdue"
            days_color = t['danger']
        elif days_diff <= 7:
            days_text = f"⚠️ {days_diff} days remaining"
            days_color = t['warning']
        else:
            days_text = f"{days_diff} days remaining"
            days_color = t['text_muted']
        
        # Severity styling
        severity = finding.get('severity', 'MEDIUM')
        severity_info = FINDING_SEVERITY.get(severity, FINDING_SEVERITY['MEDIUM'])
        
        with st.expander(f"{severity_info['icon']} {finding.get('id', 'F000')}: {finding.get('title', 'Untitled')}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;">
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Audit Area</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{finding.get('audit_area', 'N/A')}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Category</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{finding.get('category', 'N/A')}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Owner</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{finding.get('owner', 'Unassigned')}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Created</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{finding.get('created_at', 'N/A')}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Due Date</span>
                        <span style="font-weight:600;color:{days_color} !important;">
                            {finding.get('due_date', 'N/A')} ({days_text})
                        </span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Description section
                if finding.get('description'):
                    st.markdown(f'''
                    <div style="margin-top:1rem;padding:1rem;background:{t['bg_secondary']};border-radius:8px;">
                        <strong style="color:{t['text']} !important;">Description:</strong>
                        <p style="color:{t['text_secondary']} !important;margin-top:0.5rem;white-space:pre-wrap;">
                            {finding.get('description')}
                        </p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # 5Cs sections if available
                five_cs = ['condition', 'criteria', 'cause', 'consequence', 'recommendation']
                has_five_cs = any(finding.get(c) for c in five_cs)
                
                if has_five_cs:
                    st.markdown("#### 📋 5Cs Documentation")
                    for c in five_cs:
                        if finding.get(c):
                            st.markdown(f'''
                            <div style="margin-bottom:0.75rem;">
                                <strong style="color:{t['primary']} !important;">{c.title()}:</strong>
                                <span style="color:{t['text_secondary']} !important;"> {finding.get(c)}</span>
                            </div>
                            ''', unsafe_allow_html=True)
            
            with col2:
                # Status and severity badges
                st.markdown(risk_badge(severity), unsafe_allow_html=True)
                st.markdown(status_badge(finding.get('status', 'OPEN')), unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Update status
                if finding.get('status') != FindingStatus.CLOSED:
                    new_status = st.selectbox(
                        "Update Status",
                        [FindingStatus.OPEN, FindingStatus.IN_PROGRESS, FindingStatus.CLOSED],
                        index=[FindingStatus.OPEN, FindingStatus.IN_PROGRESS, FindingStatus.CLOSED].index(finding.get('status', FindingStatus.OPEN)),
                        key=f"status_{finding['id']}"
                    )
                    
                    if st.button("Update", key=f"update_{finding['id']}"):
                        finding['status'] = new_status
                        if new_status == FindingStatus.CLOSED:
                            finding['closed_at'] = datetime.now().strftime('%Y-%m-%d')
                        st.success("✓ Status updated")
                        st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("🗑️ Delete", key=f"delete_{finding['id']}"):
                    st.session_state.findings = [f for f in st.session_state.findings if f['id'] != finding['id']]
                    st.rerun()
    
    def _render_new_finding_form(self):
        """Render the form to create a new finding."""
        t = get_current_theme()
        
        st.markdown("### ➕ Create New Finding")
        
        st.markdown(f'''
        <div class="pro-card" style="background:{t['bg_secondary']};margin-bottom:1rem;">
            <p style="color:{t['text_secondary']} !important;margin:0;">
                Document audit findings using the 5Cs framework: Condition, Criteria, Cause, Consequence, and Corrective Action (Recommendation).
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Basic Information")
            
            finding_title = st.text_input(
                "Finding Title *",
                placeholder="e.g., Inadequate Credit Review Process",
                key="new_finding_title"
            )
            
            audit_category = st.selectbox(
                "Audit Category *",
                options=list(AUDIT_UNIVERSE.keys()),
                key="new_finding_category"
            )
            
            audit_area = st.selectbox(
                "Audit Area *",
                options=AUDIT_UNIVERSE[audit_category],
                key="new_finding_area"
            )
            
            severity = st.selectbox(
                "Severity *",
                options=["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"],
                index=2,
                key="new_finding_severity"
            )
            
            finding_category = st.selectbox(
                "Finding Category",
                options=[
                    "Control Deficiency",
                    "Compliance Issue",
                    "Process Inefficiency",
                    "System Weakness",
                    "Documentation Gap",
                    "Policy Violation",
                    "Fraud Indicator",
                    "Other"
                ],
                key="new_finding_type"
            )
        
        with col2:
            st.markdown("#### Assignment & Timeline")
            
            owner = st.text_input(
                "Owner/Responsible Party *",
                placeholder="e.g., Credit Division Head",
                key="new_finding_owner"
            )
            
            auditor = st.text_input(
                "Auditor",
                placeholder="e.g., Ahmad Fauzi",
                key="new_finding_auditor"
            )
            
            audit_report = st.text_input(
                "Audit Report Reference",
                placeholder="e.g., IA/2024/015",
                key="new_finding_report"
            )
            
            due_date = st.date_input(
                "Remediation Due Date *",
                value=datetime.now() + timedelta(days=30),
                key="new_finding_due_date"
            )
            
            status = st.selectbox(
                "Initial Status",
                options=[FindingStatus.OPEN, FindingStatus.IN_PROGRESS],
                key="new_finding_status"
            )
        
        st.markdown("---")
        st.markdown("#### 📋 5Cs Documentation")
        
        condition = st.text_area(
            "Condition (What was found) *",
            height=100,
            placeholder="Describe the factual observation or deficiency identified during the audit...",
            key="new_finding_condition"
        )
        
        criteria = st.text_area(
            "Criteria (What should be)",
            height=100,
            placeholder="Reference the policy, regulation, or standard that defines the expected state...",
            key="new_finding_criteria"
        )
        
        cause = st.text_area(
            "Cause (Root cause analysis)",
            height=100,
            placeholder="Explain why the condition occurred (root cause)...",
            key="new_finding_cause"
        )
        
        consequence = st.text_area(
            "Consequence/Effect (Impact)",
            height=100,
            placeholder="Describe the risk or impact of the finding...",
            key="new_finding_consequence"
        )
        
        recommendation = st.text_area(
            "Recommendation (Corrective action)",
            height=100,
            placeholder="Provide actionable recommendations to address the finding...",
            key="new_finding_recommendation"
        )
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("💾 Save Finding", type="primary", use_container_width=True):
                if not finding_title or not owner or not condition:
                    st.error("Please fill in all required fields (marked with *).")
                else:
                    new_finding = {
                        'id': f"F{len(st.session_state.findings) + 1:03d}",
                        'title': finding_title,
                        'audit_category': audit_category,
                        'audit_area': audit_area,
                        'severity': severity,
                        'category': finding_category,
                        'owner': owner,
                        'auditor': auditor,
                        'audit_report': audit_report,
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'status': status,
                        'condition': condition,
                        'criteria': criteria,
                        'cause': cause,
                        'consequence': consequence,
                        'recommendation': recommendation,
                        'description': condition,  # Use condition as description
                        'created_at': datetime.now().strftime('%Y-%m-%d'),
                        'closed_at': None
                    }
                    
                    st.session_state.findings.append(new_finding)
                    st.success(f"✓ Finding {new_finding['id']} created successfully!")
                    st.balloons()
        
        with col2:
            if st.button("🔄 Clear Form", use_container_width=True):
                st.rerun()
    
    def _render_analytics(self):
        """Render findings analytics dashboard."""
        t = get_current_theme()
        
        st.markdown("### 📊 Findings Analytics")
        
        findings = st.session_state.findings
        
        if not findings:
            st.info("📊 No findings data available for analytics. Create some findings first.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Status Distribution
            st.markdown("#### Status Distribution")
            
            status_counts = {
                FindingStatus.OPEN: 0,
                FindingStatus.IN_PROGRESS: 0,
                FindingStatus.CLOSED: 0
            }
            
            for f in findings:
                status = f.get('status', FindingStatus.OPEN)
                if status in status_counts:
                    status_counts[status] += 1
            
            total = len(findings)
            
            for status, count in status_counts.items():
                pct = (count / total * 100) if total > 0 else 0
                color = t['warning'] if status != FindingStatus.CLOSED else t['success']
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;">{status}</span>
                        <span style="font-weight:600;color:{color} !important;">{count} ({pct:.0f}%)</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width:{pct}%;background:{color};"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Severity Distribution
            st.markdown("#### Severity Distribution")
            
            severity_counts = {}
            for f in findings:
                sev = f.get('severity', 'MEDIUM')
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL']:
                count = severity_counts.get(sev, 0)
                pct = (count / total * 100) if total > 0 else 0
                info = FINDING_SEVERITY.get(sev, FINDING_SEVERITY['MEDIUM'])
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text']} !important;">{info['icon']} {sev}</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{count}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            # By Audit Area
            st.markdown("#### By Audit Area")
            
            area_counts = {}
            for f in findings:
                area = f.get('audit_area', 'Other')
                area_counts[area] = area_counts.get(area, 0) + 1
            
            # Sort by count
            sorted_areas = sorted(area_counts.items(), key=lambda x: x[1], reverse=True)
            
            for area, count in sorted_areas[:8]:
                pct = (count / total * 100) if total > 0 else 0
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;font-size:0.85rem;">{area}</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{count}</span>
                    </div>
                    <div class="progress-bar" style="height:4px;">
                        <div class="progress-fill" style="width:{pct}%;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Aging Analysis
            st.markdown("#### Aging Analysis")
            
            today = datetime.now().date()
            aging = {'0-30 days': 0, '31-60 days': 0, '61-90 days': 0, '90+ days': 0}
            
            for f in findings:
                if f.get('status') == FindingStatus.CLOSED:
                    continue
                created = datetime.strptime(f.get('created_at', today.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
                age = (today - created).days
                
                if age <= 30:
                    aging['0-30 days'] += 1
                elif age <= 60:
                    aging['31-60 days'] += 1
                elif age <= 90:
                    aging['61-90 days'] += 1
                else:
                    aging['90+ days'] += 1
            
            for period, count in aging.items():
                color = t['success'] if period == '0-30 days' else (t['warning'] if '60' in period else t['danger'])
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text']} !important;">{period}</span>
                        <span style="font-weight:600;color:{color} !important;">{count}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_export(self):
        """Render export options."""
        t = get_current_theme()
        
        st.markdown("### 📤 Export Findings")
        
        if not st.session_state.findings:
            st.info("No findings available to export.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:2rem;">
                <div style="font-size:3rem;margin-bottom:1rem;">📊</div>
                <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.5rem;">Export to CSV</div>
                <div style="color:{t['text_secondary']} !important;font-size:0.85rem;margin-bottom:1rem;">
                    Download findings data in CSV format for Excel analysis
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("📥 Download CSV", use_container_width=True):
                # Generate CSV content
                import csv
                import io
                
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=[
                    'id', 'title', 'audit_area', 'severity', 'status', 
                    'owner', 'due_date', 'created_at', 'condition', 'recommendation'
                ])
                writer.writeheader()
                
                for f in st.session_state.findings:
                    writer.writerow({
                        'id': f.get('id', ''),
                        'title': f.get('title', ''),
                        'audit_area': f.get('audit_area', ''),
                        'severity': f.get('severity', ''),
                        'status': f.get('status', ''),
                        'owner': f.get('owner', ''),
                        'due_date': f.get('due_date', ''),
                        'created_at': f.get('created_at', ''),
                        'condition': f.get('condition', ''),
                        'recommendation': f.get('recommendation', '')
                    })
                
                st.download_button(
                    "💾 Save CSV File",
                    output.getvalue(),
                    file_name=f"aurix_findings_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:2rem;">
                <div style="font-size:3rem;margin-bottom:1rem;">📄</div>
                <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.5rem;">Summary Report</div>
                <div style="color:{t['text_secondary']} !important;font-size:0.85rem;margin-bottom:1rem;">
                    Generate a summary report of all findings
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("📋 Generate Summary", use_container_width=True):
                findings = st.session_state.findings
                total = len(findings)
                open_count = len([f for f in findings if f.get('status') == FindingStatus.OPEN])
                high_count = len([f for f in findings if f.get('severity') in ['HIGH', 'CRITICAL']])
                
                summary = f"""# AURIX Findings Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Overview
- Total Findings: {total}
- Open Findings: {open_count}
- High/Critical Severity: {high_count}

## Findings by Status
- Open: {len([f for f in findings if f.get('status') == FindingStatus.OPEN])}
- In Progress: {len([f for f in findings if f.get('status') == FindingStatus.IN_PROGRESS])}
- Closed: {len([f for f in findings if f.get('status') == FindingStatus.CLOSED])}

## Findings List
"""
                for f in findings:
                    summary += f"\n### {f.get('id', 'F000')}: {f.get('title', 'Untitled')}\n"
                    summary += f"- Severity: {f.get('severity', 'N/A')}\n"
                    summary += f"- Status: {f.get('status', 'N/A')}\n"
                    summary += f"- Owner: {f.get('owner', 'N/A')}\n"
                    summary += f"- Due Date: {f.get('due_date', 'N/A')}\n"
                
                st.download_button(
                    "💾 Save Report",
                    summary,
                    file_name=f"aurix_findings_report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )


def render():
    """Entry point for the Findings page."""
    page = FindingsPage()
    page.render()
