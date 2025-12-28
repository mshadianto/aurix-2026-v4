"""
Report Builder Module for AURIX.
Generate comprehensive audit reports with customizable templates.
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, List, Any
import json

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from data.seeds import AUDIT_UNIVERSE


def render():
    """Render the report builder page."""
    t = get_current_theme()
    
    render_page_header(
        "📑 Report Builder",
        "Generate professional audit reports with AI assistance"
    )
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Build Report",
        "📋 Templates",
        "📚 My Reports",
        "📤 Export Center"
    ])
    
    with tab1:
        _render_build_report(t)
    
    with tab2:
        _render_templates(t)
    
    with tab3:
        _render_my_reports(t)
    
    with tab4:
        _render_export_center(t)
    
    render_footer()


def _render_build_report(t: dict):
    """Render report builder interface."""
    st.markdown("### 📝 Build Audit Report")
    
    # Report type selection
    report_type = st.selectbox(
        "Report Type",
        options=[
            "Internal Audit Report",
            "Executive Summary",
            "Quarterly Audit Report",
            "Annual Audit Report",
            "Special Investigation Report",
            "Follow-up Audit Report",
            "Control Assessment Report"
        ]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Report Header")
        
        report_title = st.text_input(
            "Report Title",
            value=f"{report_type} - {datetime.now().strftime('%B %Y')}"
        )
        
        report_ref = st.text_input(
            "Reference Number",
            value=f"IA/{datetime.now().strftime('%Y')}/{datetime.now().strftime('%m')}/001"
        )
        
        audit_area = st.selectbox("Audit Area", options=list(AUDIT_UNIVERSE.keys()))
        
        col1a, col1b = st.columns(2)
        with col1a:
            period_start = st.date_input("Period Start", value=date(2024, 10, 1))
        with col1b:
            period_end = st.date_input("Period End", value=date(2024, 12, 31))
    
    with col2:
        st.markdown("#### 👥 Report Details")
        
        prepared_by = st.text_input("Prepared By", placeholder="Lead Auditor name")
        reviewed_by = st.text_input("Reviewed By", placeholder="Audit Manager name")
        approved_by = st.text_input("Approved By", placeholder="CAE name")
        
        report_date = st.date_input("Report Date", value=date.today())
        
        distribution = st.multiselect(
            "Distribution",
            options=["Audit Committee", "Board of Directors", "CEO", "CFO", "CRO", "Auditee Management"],
            default=["Audit Committee", "Auditee Management"]
        )
    
    st.markdown("---")
    
    # Report sections
    st.markdown("### 📄 Report Content")
    
    # Executive Summary
    with st.expander("📌 Executive Summary", expanded=True):
        exec_summary = st.text_area(
            "Executive Summary",
            height=150,
            placeholder="Provide a high-level overview of audit objectives, scope, key findings, and overall conclusion...",
            key="exec_summary"
        )
        
        overall_rating = st.select_slider(
            "Overall Rating",
            options=["Satisfactory", "Needs Improvement", "Unsatisfactory"],
            value="Needs Improvement"
        )
    
    # Background
    with st.expander("📋 Background & Objectives"):
        background = st.text_area(
            "Background",
            height=100,
            placeholder="Describe the background context for this audit...",
            key="background"
        )
        
        objectives = st.text_area(
            "Audit Objectives",
            height=100,
            placeholder="List the key objectives of this audit engagement...",
            key="objectives"
        )
    
    # Scope & Methodology
    with st.expander("🎯 Scope & Methodology"):
        scope = st.text_area(
            "Scope",
            height=100,
            placeholder="Define the audit scope including period, processes, and systems covered...",
            key="scope"
        )
        
        methodology = st.multiselect(
            "Testing Methodology Used",
            options=["Inquiry", "Observation", "Inspection", "Reperformance", "Analytical Review", "Walkthrough", "Data Analytics"],
            default=["Inquiry", "Inspection", "Walkthrough"]
        )
        
        limitations = st.text_area(
            "Scope Limitations (if any)",
            height=80,
            placeholder="Document any limitations encountered during the audit...",
            key="limitations"
        )
    
    # Findings Summary
    with st.expander("🔍 Findings Summary"):
        st.markdown("#### Finding Distribution")
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            critical_count = st.number_input("Critical", min_value=0, max_value=50, value=0)
        with col_f2:
            high_count = st.number_input("High", min_value=0, max_value=50, value=2)
        with col_f3:
            medium_count = st.number_input("Medium", min_value=0, max_value=50, value=3)
        with col_f4:
            low_count = st.number_input("Low", min_value=0, max_value=50, value=1)
        
        # Get findings from session state
        findings = st.session_state.get('findings', [])
        if findings:
            st.markdown("**Available findings to include:**")
            selected_findings = []
            for i, f in enumerate(findings[:10]):
                if st.checkbox(f"{f.get('title', 'Finding')} - {f.get('rating', 'N/A')}", key=f"finding_{i}"):
                    selected_findings.append(f)
    
    # Recommendations
    with st.expander("💡 Key Recommendations"):
        recommendations = st.text_area(
            "Summary of Key Recommendations",
            height=150,
            placeholder="Summarize the key recommendations from this audit...",
            key="recommendations"
        )
    
    # Management Response
    with st.expander("📣 Management Response"):
        mgmt_response = st.text_area(
            "Management Response",
            height=150,
            placeholder="Include management's response and action plans...",
            key="mgmt_response"
        )
        
        agreed_actions = st.number_input("Agreed Actions", min_value=0, max_value=100, value=5)
        target_date = st.date_input("Target Completion Date", value=date(2025, 3, 31))
    
    # Conclusion
    with st.expander("✅ Conclusion"):
        conclusion = st.text_area(
            "Audit Conclusion",
            height=100,
            placeholder="Provide the overall audit conclusion and opinion...",
            key="conclusion"
        )
    
    st.markdown("---")
    
    # Actions
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("✅ Report draft saved!")
    
    with col_btn2:
        if st.button("👁️ Preview", use_container_width=True):
            st.info("📄 Preview mode - coming soon!")
    
    with col_btn3:
        if st.button("🤖 AI Enhance", use_container_width=True, type="primary"):
            st.info("🔄 AI will enhance your report content...")
    
    with col_btn4:
        if st.button("📤 Export", use_container_width=True):
            st.info("📥 Export to Word/PDF - coming soon!")


def _render_templates(t: dict):
    """Render report templates."""
    st.markdown("### 📋 Report Templates")
    
    templates = [
        {
            "name": "Internal Audit Report - Standard",
            "desc": "Comprehensive template following IIA standards",
            "sections": ["Executive Summary", "Background", "Scope", "Findings", "Recommendations", "Conclusion"],
            "pages": "8-12"
        },
        {
            "name": "Executive Summary Report",
            "desc": "One-page summary for senior management",
            "sections": ["Key Highlights", "Risk Rating", "Critical Findings", "Action Required"],
            "pages": "1-2"
        },
        {
            "name": "Quarterly Audit Report",
            "desc": "Periodic report for Audit Committee",
            "sections": ["Audit Activity", "Resource Utilization", "Finding Summary", "Follow-ups", "Upcoming Audits"],
            "pages": "5-8"
        },
        {
            "name": "Control Assessment Report",
            "desc": "Detailed control evaluation report",
            "sections": ["Control Objectives", "Control Matrix", "Test Results", "Gap Analysis", "Remediation Plan"],
            "pages": "10-15"
        },
        {
            "name": "Investigation Report",
            "desc": "Special investigation findings",
            "sections": ["Case Background", "Investigation Scope", "Evidence Analysis", "Findings", "Recommendations"],
            "pages": "Variable"
        },
    ]
    
    for template in templates:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:start;">
                <div style="flex:1;">
                    <div style="font-weight:600;color:{t['text']};font-size:1.1rem;">{template['name']}</div>
                    <div style="font-size:0.85rem;color:{t['text_secondary']};margin-top:0.25rem;">{template['desc']}</div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};margin-top:0.75rem;">
                        <strong>Sections:</strong> {', '.join(template['sections'])}
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="background:{t['primary']}20;color:{t['primary']};padding:0.25rem 0.75rem;border-radius:12px;font-size:0.75rem;">
                        {template['pages']} pages
                    </span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button(f"Use Template", key=f"use_{template['name']}", use_container_width=False):
            st.success(f"✅ Template '{template['name']}' loaded!")


def _render_my_reports(t: dict):
    """Render saved reports."""
    st.markdown("### 📚 My Reports")
    
    # Sample reports
    sample_reports = [
        {"title": "Credit Risk Review Q4 2024", "status": "Draft", "date": "2024-12-01", "type": "Internal Audit Report"},
        {"title": "IT Security Assessment", "status": "Under Review", "date": "2024-11-15", "type": "Control Assessment"},
        {"title": "AML Process Audit", "status": "Final", "date": "2024-10-20", "type": "Internal Audit Report"},
        {"title": "Q3 2024 Audit Report", "status": "Issued", "date": "2024-10-01", "type": "Quarterly Report"},
    ]
    
    # Filters
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search = st.text_input("🔍 Search reports", placeholder="Search by title...")
    with col_f2:
        status_filter = st.selectbox("Status", ["All", "Draft", "Under Review", "Final", "Issued"])
    
    # Report list
    for report in sample_reports:
        if search and search.lower() not in report['title'].lower():
            continue
        if status_filter != "All" and report['status'] != status_filter:
            continue
        
        status_colors = {
            'Draft': t['warning'],
            'Under Review': t['primary'],
            'Final': t['accent'],
            'Issued': t['success']
        }
        color = status_colors.get(report['status'], t['text_muted'])
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-weight:600;color:{t['text']};">{report['title']}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']};margin-top:0.25rem;">
                        {report['type']} • Created {report['date']}
                    </div>
                </div>
                <span style="background:{color}20;color:{color};padding:0.25rem 0.75rem;border-radius:20px;font-size:0.75rem;font-weight:600;">
                    {report['status']}
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_export_center(t: dict):
    """Render export options."""
    st.markdown("### 📤 Export Center")
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <p style="color:{t['text_secondary']};margin:0;">
        Export your reports in various formats for distribution and archiving.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Document Formats")
        
        formats = [
            ("📝 Microsoft Word (.docx)", "Editable document format", "docx"),
            ("📕 PDF Document (.pdf)", "Print-ready format", "pdf"),
            ("📊 PowerPoint (.pptx)", "Presentation format", "pptx"),
        ]
        
        for name, desc, fmt in formats:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.75rem;">
                <div style="font-weight:600;color:{t['text']};">{name}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">{desc}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button(f"Export as {fmt.upper()}", key=f"export_{fmt}", use_container_width=True):
                st.info(f"📥 Exporting to {fmt.upper()}...")
    
    with col2:
        st.markdown("#### 📊 Data Formats")
        
        data_formats = [
            ("📋 Excel (.xlsx)", "Findings and data tables", "xlsx"),
            ("📄 CSV (.csv)", "Raw data export", "csv"),
            ("🔗 JSON (.json)", "Structured data", "json"),
        ]
        
        for name, desc, fmt in data_formats:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.75rem;">
                <div style="font-weight:600;color:{t['text']};">{name}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">{desc}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button(f"Export as {fmt.upper()}", key=f"export_data_{fmt}", use_container_width=True):
                st.info(f"📥 Exporting to {fmt.upper()}...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Bulk export
        st.markdown("#### 📦 Bulk Export")
        
        if st.button("📦 Export All Reports", use_container_width=True, type="primary"):
            st.info("📥 Preparing bulk export...")
