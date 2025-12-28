"""
Workpaper Generator Module for AURIX.
AI-powered working paper creation with templates and export.
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, List, Any
import json
import uuid

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from data.seeds import AUDIT_UNIVERSE, get_all_audit_areas
from app.constants import WORKING_PAPER_TEMPLATES


def render():
    """Render the workpaper generator page."""
    t = get_current_theme()
    
    render_page_header(
        "📝 Workpaper Generator",
        "Create professional audit working papers with AI assistance"
    )
    
    # Initialize session state
    if 'workpapers' not in st.session_state:
        st.session_state.workpapers = []
    if 'current_workpaper' not in st.session_state:
        st.session_state.current_workpaper = None
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Create New",
        "📚 My Workpapers",
        "📋 Templates",
        "🤖 AI Assistant"
    ])
    
    with tab1:
        _render_create_workpaper(t)
    
    with tab2:
        _render_workpaper_list(t)
    
    with tab3:
        _render_templates(t)
    
    with tab4:
        _render_ai_assistant(t)
    
    render_footer()


def _render_create_workpaper(t: dict):
    """Render workpaper creation form."""
    st.markdown("### ✨ Create New Working Paper")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Header Information
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
            <h4 style="color:{t['text']};margin-bottom:1rem;">📋 Header Information</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        wp_ref = st.text_input("Reference Number", value=f"WP-{datetime.now().strftime('%Y%m%d')}-001")
        wp_title = st.text_input("Working Paper Title", placeholder="e.g., Credit Risk Assessment - Q4 2024")
        
        audit_area = st.selectbox("Audit Area", options=get_all_audit_areas())
        
        template_type = st.selectbox(
            "Template Type",
            options=list(WORKING_PAPER_TEMPLATES.keys())
        )
        
        col1a, col1b = st.columns(2)
        with col1a:
            prepared_by = st.text_input("Prepared By", placeholder="Your name")
        with col1b:
            prepared_date = st.date_input("Prepared Date", value=date.today())
        
        col1c, col1d = st.columns(2)
        with col1c:
            reviewed_by = st.text_input("Reviewed By", placeholder="Reviewer name")
        with col1d:
            review_date = st.date_input("Review Date", value=date.today())
    
    with col2:
        # Objective and Scope
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
            <h4 style="color:{t['text']};margin-bottom:1rem;">🎯 Objective & Scope</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        objective = st.text_area(
            "Audit Objective",
            placeholder="To assess the design and operating effectiveness of controls over...",
            height=100
        )
        
        scope = st.text_area(
            "Scope",
            placeholder="This review covers the period from... to... and includes...",
            height=100
        )
        
        methodology = st.multiselect(
            "Testing Methodology",
            options=["Inquiry", "Observation", "Inspection", "Reperformance", "Analytical Review", "Walkthrough"],
            default=["Inquiry", "Inspection"]
        )
        
        sample_size = st.number_input("Sample Size", min_value=1, max_value=1000, value=25)
    
    st.markdown("---")
    
    # Content Sections based on template
    st.markdown("### 📝 Working Paper Content")
    
    template_sections = WORKING_PAPER_TEMPLATES.get(template_type, {}).get("sections", [])
    
    sections_content = {}
    for i, section in enumerate(template_sections):
        with st.expander(f"📌 {section}", expanded=(i == 0)):
            content = st.text_area(
                f"Content for {section}",
                key=f"section_{i}",
                height=150,
                placeholder=f"Enter details for {section}..."
            )
            sections_content[section] = content
    
    # Action buttons
    st.markdown("---")
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("💾 Save Draft", use_container_width=True):
            workpaper = {
                'id': str(uuid.uuid4()),
                'reference': wp_ref,
                'title': wp_title,
                'audit_area': audit_area,
                'template_type': template_type,
                'prepared_by': prepared_by,
                'prepared_date': str(prepared_date),
                'reviewed_by': reviewed_by,
                'review_date': str(review_date),
                'objective': objective,
                'scope': scope,
                'methodology': methodology,
                'sample_size': sample_size,
                'sections': sections_content,
                'status': 'Draft',
                'created_at': datetime.now().isoformat()
            }
            st.session_state.workpapers.append(workpaper)
            st.success(f"✅ Working paper '{wp_title}' saved as draft!")
    
    with col_btn2:
        if st.button("🤖 AI Generate", use_container_width=True, type="primary"):
            st.info("🔄 AI will generate content based on your objective and scope...")
            # AI generation would go here
    
    with col_btn3:
        if st.button("📄 Preview", use_container_width=True):
            st.info("📋 Preview feature - coming soon!")
    
    with col_btn4:
        if st.button("📤 Export", use_container_width=True):
            st.info("📥 Export to Word/PDF - coming soon!")


def _render_workpaper_list(t: dict):
    """Render list of saved workpapers."""
    st.markdown("### 📚 My Working Papers")
    
    workpapers = st.session_state.get('workpapers', [])
    
    if not workpapers:
        st.info("📝 No working papers yet. Create your first one in the 'Create New' tab!")
        return
    
    # Summary metrics
    cols = st.columns(4)
    total = len(workpapers)
    drafts = len([w for w in workpapers if w.get('status') == 'Draft'])
    reviewed = len([w for w in workpapers if w.get('status') == 'Reviewed'])
    approved = len([w for w in workpapers if w.get('status') == 'Approved'])
    
    metrics = [
        ("Total", str(total), t['accent']),
        ("Draft", str(drafts), t['warning']),
        ("Reviewed", str(reviewed), t['primary']),
        ("Approved", str(approved), t['success']),
    ]
    
    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:{color};">{value}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">{label}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter
    col_filter1, col_filter2 = st.columns([2, 1])
    with col_filter1:
        search = st.text_input("🔍 Search", placeholder="Search by title or reference...")
    with col_filter2:
        status_filter = st.selectbox("Status", options=["All", "Draft", "Reviewed", "Approved"])
    
    # Workpaper cards
    for wp in workpapers:
        if search and search.lower() not in wp['title'].lower() and search.lower() not in wp['reference'].lower():
            continue
        if status_filter != "All" and wp.get('status') != status_filter:
            continue
        
        status_color = {
            'Draft': t['warning'],
            'Reviewed': t['primary'],
            'Approved': t['success']
        }.get(wp.get('status', 'Draft'), t['text_muted'])
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:start;">
                <div>
                    <div style="font-weight:600;color:{t['text']};font-size:1rem;">{wp['title']}</div>
                    <div style="font-size:0.85rem;color:{t['text_muted']};margin-top:0.25rem;">
                        {wp['reference']} • {wp['audit_area']} • {wp['template_type']}
                    </div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};margin-top:0.5rem;">
                        Prepared by {wp['prepared_by']} on {wp['prepared_date']}
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="background:{status_color}20;color:{status_color};padding:0.25rem 0.75rem;border-radius:20px;font-size:0.75rem;font-weight:600;">
                        {wp.get('status', 'Draft')}
                    </span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_templates(t: dict):
    """Render workpaper templates."""
    st.markdown("### 📋 Working Paper Templates")
    
    st.markdown(f'''
    <p style="color:{t['text_secondary']};">
    Choose from pre-built templates designed for various audit scenarios.
    Each template includes structured sections following IIA standards.
    </p>
    ''', unsafe_allow_html=True)
    
    for template_name, template_data in WORKING_PAPER_TEMPLATES.items():
        with st.expander(f"📄 {template_name}", expanded=False):
            st.markdown(f"**Format:** {template_data.get('format', 'Standard')}")
            st.markdown("**Sections:**")
            for i, section in enumerate(template_data.get('sections', []), 1):
                st.markdown(f"  {i}. {section}")
            
            if st.button(f"Use Template", key=f"use_{template_name}"):
                st.success(f"✅ Template '{template_name}' selected! Go to 'Create New' tab.")


def _render_ai_assistant(t: dict):
    """Render AI assistant for workpaper generation."""
    st.markdown("### 🤖 AI Workpaper Assistant")
    
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, {t['primary']}20, {t['accent']}20);border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <h4 style="color:{t['text']};margin-bottom:0.5rem;">💡 How AI Can Help</h4>
        <ul style="color:{t['text_secondary']};margin:0;padding-left:1.25rem;">
            <li>Generate procedure steps from audit objectives</li>
            <li>Create sample selection criteria</li>
            <li>Draft conclusions based on test results</li>
            <li>Suggest additional tests based on findings</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Quick Generate")
        
        gen_type = st.selectbox(
            "What to generate?",
            options=[
                "Audit Procedures",
                "Sample Selection Criteria",
                "Test Conclusion",
                "Exception Documentation",
                "Follow-up Actions"
            ]
        )
        
        context = st.text_area(
            "Provide context",
            placeholder="Describe the audit area, objective, or findings...",
            height=150
        )
        
        if st.button("🚀 Generate", type="primary", use_container_width=True):
            if context:
                with st.spinner("AI is generating..."):
                    # AI generation placeholder
                    st.markdown(f'''
                    <div style="background:{t['card']};border:1px solid {t['success']};border-radius:12px;padding:1.5rem;margin-top:1rem;">
                        <h5 style="color:{t['success']};margin-bottom:1rem;">✅ Generated {gen_type}</h5>
                        <p style="color:{t['text_secondary']};">
                        Based on your input about "{context[:50]}...", here are the suggested {gen_type.lower()}:
                        </p>
                        <ol style="color:{t['text']};">
                            <li>Review documentation and policies related to the process</li>
                            <li>Interview process owners to understand control design</li>
                            <li>Select sample of transactions for testing</li>
                            <li>Perform substantive testing on selected samples</li>
                            <li>Document results and exceptions</li>
                        </ol>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.warning("Please provide context for AI generation.")
    
    with col2:
        st.markdown("#### 💬 Ask AI")
        
        question = st.text_input(
            "Ask a question about your workpaper",
            placeholder="e.g., What procedures should I include for cash audit?"
        )
        
        if st.button("Ask", use_container_width=True):
            if question:
                st.markdown(f'''
                <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-top:1rem;">
                    <p style="color:{t['text_muted']};font-size:0.85rem;margin-bottom:0.5rem;">AI Response:</p>
                    <p style="color:{t['text']};">
                    For cash audit procedures, you should typically include:
                    cash count verification, dual custody testing, reconciliation review,
                    insurance coverage verification, and surprise cash counts.
                    Refer to ISA 500 for guidance on sufficient appropriate audit evidence.
                    </p>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("#### 📖 Quick References")
        
        refs = [
            ("IIA Standards", "Standards for Professional Practice"),
            ("ISA 500", "Audit Evidence"),
            ("ISA 530", "Audit Sampling"),
            ("COSO Framework", "Internal Control"),
        ]
        
        for ref_title, ref_desc in refs:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:0.75rem;margin-bottom:0.5rem;">
                <div style="font-weight:600;color:{t['text']};font-size:0.9rem;">{ref_title}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{ref_desc}</div>
            </div>
            ''', unsafe_allow_html=True)
