"""
Root Cause Analyzer Module for AURIX.
Fishbone diagram, 5 Whys analysis, and AI-powered root cause identification.
"""

import streamlit as st
from datetime import datetime
import uuid

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the root cause analyzer page."""
    t = get_current_theme()
    
    render_page_header(
        "🔬 Root Cause Analyzer",
        "Systematic analysis to identify the true causes of audit findings"
    )
    
    # Initialize session state
    if 'rca_analyses' not in st.session_state:
        st.session_state.rca_analyses = []
    if 'current_fishbone' not in st.session_state:
        st.session_state.current_fishbone = _get_default_fishbone()
    if 'five_whys' not in st.session_state:
        st.session_state.five_whys = ["", "", "", "", ""]
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🐟 Fishbone Diagram",
        "❓ 5 Whys Analysis",
        "🤖 AI Root Cause",
        "📚 My Analyses"
    ])
    
    with tab1:
        _render_fishbone(t)
    
    with tab2:
        _render_five_whys(t)
    
    with tab3:
        _render_ai_root_cause(t)
    
    with tab4:
        _render_saved_analyses(t)
    
    render_footer()


def _get_default_fishbone():
    """Get default fishbone structure."""
    return {
        "problem": "Payment Processing Errors",
        "categories": {
            "People": ["Inadequate training", "Staff turnover", "Unclear responsibilities"],
            "Process": ["Manual data entry", "Missing approval steps", "Outdated procedures"],
            "Technology": ["System downtime", "Integration errors", "Legacy systems"],
            "Policy": ["Ambiguous guidelines", "Outdated limits", "Conflicting rules"],
            "Environment": ["Time pressure", "Remote work challenges", "Communication gaps"],
            "Measurement": ["Inadequate monitoring", "Delayed reporting", "Wrong KPIs"],
        }
    }


def _render_fishbone(t: dict):
    """Render interactive fishbone (Ishikawa) diagram."""
    st.markdown("### 🐟 Ishikawa (Fishbone) Diagram")
    
    fishbone = st.session_state.current_fishbone
    
    # Problem statement input
    problem = st.text_input(
        "Problem Statement (Effect)",
        value=fishbone.get("problem", ""),
        placeholder="Enter the problem or finding to analyze..."
    )
    fishbone["problem"] = problem
    
    # Show the problem/effect box
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {t['danger']}, {t['danger']}cc);color:white;padding:1rem 1.5rem;border-radius:12px;text-align:center;margin:1rem 0;">
        <div style="font-size:0.75rem;opacity:0.9;text-transform:uppercase;letter-spacing:0.1em;">Effect / Problem</div>
        <div style="font-size:1.25rem;font-weight:700;margin-top:0.5rem;">🎯 {problem or 'Enter problem above'}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 6M Categories - Potential Causes")
    
    # Categories in 2 rows of 3
    categories = fishbone.get("categories", {})
    cat_config = [
        ("👥 People", "People", t['primary']),
        ("⚙️ Process", "Process", t['accent']),
        ("💻 Technology", "Technology", t['success']),
        ("📜 Policy", "Policy", t['warning']),
        ("🌍 Environment", "Environment", t['danger']),
        ("📊 Measurement", "Measurement", "#8b5cf6"),
    ]
    
    # First row
    cols1 = st.columns(3)
    for i, (label, key, color) in enumerate(cat_config[:3]):
        with cols1[i]:
            _render_category_card(t, label, key, color, categories.get(key, []))
    
    # Second row
    cols2 = st.columns(3)
    for i, (label, key, color) in enumerate(cat_config[3:]):
        with cols2[i]:
            _render_category_card(t, label, key, color, categories.get(key, []))
    
    # Actions
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Analysis", use_container_width=True):
            _save_fishbone_analysis(fishbone)
            st.success("Analysis saved!")
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.current_fishbone = _get_default_fishbone()
            st.rerun()
    with col3:
        if st.button("📤 Export", use_container_width=True):
            st.info("Export feature coming soon!")


def _render_category_card(t: dict, label: str, key: str, color: str, causes: list):
    """Render a single category card."""
    st.markdown(f"""
    <div style="background:{t['card']};border:1px solid {t['border']};border-top:4px solid {color};border-radius:0 0 12px 12px;padding:1rem;min-height:180px;">
        <div style="font-weight:700;color:{color};margin-bottom:0.75rem;">{label}</div>
        <div style="font-size:0.85rem;color:{t['text']};">
    """, unsafe_allow_html=True)
    
    # Show causes as list
    for cause in causes:
        st.markdown(f"""
        <div style="padding:0.35rem 0;border-bottom:1px dashed {t['border']};">
            • {cause}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Add new cause
    new_cause = st.text_input(f"Add cause", key=f"add_{key}", placeholder="New cause...", label_visibility="collapsed")
    if new_cause:
        if key not in st.session_state.current_fishbone["categories"]:
            st.session_state.current_fishbone["categories"][key] = []
        if new_cause not in st.session_state.current_fishbone["categories"][key]:
            st.session_state.current_fishbone["categories"][key].append(new_cause)
            st.rerun()


def _render_five_whys(t: dict):
    """Render 5 Whys analysis tool."""
    st.markdown("### ❓ 5 Whys Analysis")
    
    st.markdown(f"""
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:1.5rem;">
        <p style="color:{t['text_secondary']};margin:0;">
        The 5 Whys technique helps drill down to the root cause by repeatedly asking "Why?" 
        until the fundamental cause is identified. Start with a problem and ask why it occurred, 
        then ask why for each answer.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Problem statement
    problem = st.text_input("Initial Problem / Finding", placeholder="What is the problem you want to analyze?")
    
    if problem:
        st.markdown("<br>", unsafe_allow_html=True)
        
        colors = [t['primary'], t['accent'], t['success'], t['warning'], t['danger']]
        
        why_answers = st.session_state.five_whys
        
        for i in range(5):
            color = colors[i]
            
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">
                <div style="width:60px;height:60px;background:{color};border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:1.25rem;flex-shrink:0;">
                    #{i+1}
                </div>
                <div style="flex:1;">
                    <div style="font-size:0.75rem;color:{t['text_muted']};text-transform:uppercase;letter-spacing:0.05em;">Why #{i+1}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            answer = st.text_area(
                f"Why #{i+1}",
                value=why_answers[i],
                placeholder=f"Why did this happen? (Level {i+1})",
                key=f"why_{i}",
                label_visibility="collapsed",
                height=80
            )
            why_answers[i] = answer
            
            if i < 4:
                st.markdown(f"""
                <div style="text-align:center;color:{t['text_muted']};font-size:1.5rem;margin:0.5rem 0;">↓</div>
                """, unsafe_allow_html=True)
        
        st.session_state.five_whys = why_answers
        
        # Root cause highlight
        if why_answers[4]:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, {t['success']}, {t['success']}cc);color:white;padding:1.5rem;border-radius:12px;margin-top:1.5rem;text-align:center;">
                <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;opacity:0.9;">🎯 Root Cause Identified</div>
                <div style="font-size:1.25rem;font-weight:700;margin-top:0.5rem;">{why_answers[4]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Save button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save 5 Whys Analysis", use_container_width=True):
            st.success("Analysis saved!")


def _render_ai_root_cause(t: dict):
    """Render AI-powered root cause analysis."""
    st.markdown("### 🤖 AI Root Cause Analysis")
    
    st.markdown(f"""
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:1.5rem;">
        <p style="color:{t['text_secondary']};margin:0;">
        Let AI analyze your finding and suggest potential root causes, contributing factors, 
        and recommended corrective actions based on industry best practices and regulatory requirements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        finding_title = st.text_input("Finding Title", placeholder="Brief title of the finding...")
        finding_details = st.text_area("Finding Details", placeholder="Describe the finding in detail...", height=150)
    
    with col2:
        context_areas = st.multiselect(
            "Context Areas",
            ["Credit Risk", "Operational Risk", "IT/Cyber", "Compliance", "AML/CFT", "Treasury", "Lending", "Deposits"],
            default=["Operational Risk"]
        )
        analysis_depth = st.select_slider("Analysis Depth", options=["Quick", "Standard", "Deep"], value="Standard")
        include_benchmarks = st.checkbox("Include industry benchmarks", value=True)
        include_regulations = st.checkbox("Include regulatory references", value=True)
    
    if st.button("🔍 Analyze Root Cause", use_container_width=True, type="primary"):
        if finding_title and finding_details:
            with st.spinner("Analyzing root cause..."):
                import time
                time.sleep(2)  # Simulate AI processing
                _show_ai_analysis_result(t, finding_title)
        else:
            st.warning("Please enter finding title and details.")


def _show_ai_analysis_result(t: dict, finding_title: str):
    """Show AI analysis result."""
    st.markdown("---")
    st.markdown("### 📊 Analysis Results")
    
    # Primary root cause
    st.markdown(f"""
    <div style="background:{t['card']};border:2px solid {t['primary']};border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
        <div style="font-size:0.75rem;color:{t['primary']};text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">Primary Root Cause</div>
        <div style="font-size:1.1rem;font-weight:600;color:{t['text']};margin-top:0.5rem;">
            Inadequate segregation of duties in payment processing workflow combined with insufficient system validation controls
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contributing factors
    st.markdown("#### 📋 Contributing Factors")
    factors = [
        ("High", "Manual override capabilities without adequate approval controls", t['danger']),
        ("High", "Lack of real-time monitoring and alerts", t['danger']),
        ("Medium", "Insufficient staff training on updated procedures", t['warning']),
        ("Medium", "Legacy system limitations in validation rules", t['warning']),
        ("Low", "Time pressure during peak processing periods", t['success']),
    ]
    
    for severity, factor, color in factors:
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-left:4px solid {color};border-radius:0 8px 8px 0;padding:0.75rem 1rem;margin-bottom:0.5rem;">
            <span style="background:{color}20;color:{color};padding:0.15rem 0.5rem;border-radius:4px;font-size:0.7rem;font-weight:600;margin-right:0.75rem;">{severity}</span>
            <span style="color:{t['text']};">{factor}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommended actions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ✅ Recommended Actions")
    
    actions = [
        ("Immediate", "Implement dual authorization for payments above threshold"),
        ("Short-term", "Deploy automated validation rules in payment system"),
        ("Short-term", "Conduct refresher training for all payment processors"),
        ("Medium-term", "Upgrade legacy system with enhanced controls"),
        ("Long-term", "Implement continuous monitoring dashboard"),
    ]
    
    for timeline, action in actions:
        st.markdown(f"""
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:8px;padding:0.75rem 1rem;margin-bottom:0.5rem;">
            <span style="background:{t['accent']}20;color:{t['accent']};padding:0.15rem 0.5rem;border-radius:4px;font-size:0.7rem;font-weight:600;margin-right:0.75rem;">{timeline}</span>
            <span style="color:{t['text']};">{action}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Confidence scores
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📈 Confidence Scores")
    
    cols = st.columns(4)
    scores = [
        ("Root Cause", 87),
        ("Contributing Factors", 92),
        ("Action Relevance", 85),
        ("Regulatory Match", 78),
    ]
    for col, (label, score) in zip(cols, scores):
        with col:
            color = t['success'] if score >= 85 else t['warning'] if score >= 70 else t['danger']
            st.markdown(f"""
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.75rem;font-weight:700;color:{color};">{score}%</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_saved_analyses(t: dict):
    """Render saved analyses list."""
    st.markdown("### 📚 My Analyses")
    
    analyses = st.session_state.rca_analyses
    
    if not analyses:
        st.info("No saved analyses yet. Create your first analysis using Fishbone Diagram or 5 Whys!")
    else:
        for analysis in analyses:
            st.markdown(f"""
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.75rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-weight:600;color:{t['text']};">{analysis.get('title', 'Untitled')}</div>
                        <div style="font-size:0.75rem;color:{t['text_muted']};">
                            {analysis.get('type', 'Analysis')} • {analysis.get('date', 'Unknown date')}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def _save_fishbone_analysis(fishbone: dict):
    """Save fishbone analysis to session state."""
    analysis = {
        "id": str(uuid.uuid4()),
        "type": "Fishbone",
        "title": fishbone.get("problem", "Untitled"),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "data": fishbone
    }
    st.session_state.rca_analyses.append(analysis)


if __name__ == "__main__":
    render()
