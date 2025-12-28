"""
Regulatory RAG Page for AURIX 2026.
AI-powered compliance validation against Indonesian regulations.
"""

import streamlit as st
from datetime import datetime

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer

# Import regulatory module
import sys
sys.path.insert(0, '/home/claude/aurix_integrated')
from modules.regulatory_rag import (
    RegulatoryValidator,
    ComplianceStatus,
    ESGCategory,
    SAMPLE_QUERIES
)


class RegulatoryRAGPage:
    """Regulatory compliance validation using RAG."""
    
    def __init__(self):
        self.validator = RegulatoryValidator()
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state."""
        if 'rag_history' not in st.session_state:
            st.session_state.rag_history = []
        if 'last_compliance_result' not in st.session_state:
            st.session_state.last_compliance_result = None
    
    def render(self):
        """Render the Regulatory RAG page."""
        render_page_header(
            "Regulatory RAG",
            "AI-Powered Compliance Validation for Indonesian Regulations"
        )
        
        t = get_current_theme()
        
        # Header banner
        st.markdown(f'''
        <div style="background:linear-gradient(135deg, #1E3A5F 0%, #2E7D32 100%);
                    color:white;padding:2rem;border-radius:12px;margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:1.5rem;">
                <span style="font-size:3rem;">📜</span>
                <div>
                    <h2 style="margin:0;color:white;">Indonesian Regulatory Compliance</h2>
                    <p style="margin:0.5rem 0 0 0;opacity:0.9;">
                        Validate business activities against OJK, BI, and BPKH regulations 
                        including ESG Taxonomy (POJK 6/2022) and Sharia compliance.
                    </p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Main layout
        col_input, col_result = st.columns([1, 1])
        
        with col_input:
            self._render_input_section()
        
        with col_result:
            self._render_result_section()
        
        # Regulations reference
        st.markdown("---")
        self._render_regulations_reference()
        
        render_footer()
    
    def _render_input_section(self):
        """Render input section."""
        t = get_current_theme()
        
        st.markdown("### 📝 Compliance Query")
        
        # Quick examples
        st.markdown("**Quick Examples:**")
        
        example_cols = st.columns(3)
        examples = [
            ("🌿 Green", "We plan to invest in solar panel manufacturing"),
            ("🏭 Brown", "We invest in coal mining operations"),
            ("🕌 Sharia", "Portfolio includes alcohol distributors")
        ]
        
        for col, (label, query) in zip(example_cols, examples):
            with col:
                if st.button(label, key=f"ex_{label}", use_container_width=True):
                    st.session_state.rag_query = query
                    st.rerun()
        
        # Text input
        query = st.text_area(
            "Describe your business activity or investment:",
            value=st.session_state.get('rag_query', ''),
            height=120,
            placeholder="Example: Our company plans to finance a new coal-fired power plant...",
            key="compliance_query"
        )
        
        # Validate button
        if st.button("🔍 Validate Compliance", type="primary", use_container_width=True):
            if query.strip():
                with st.spinner("🔄 Analyzing compliance..."):
                    import time
                    time.sleep(1)
                    result = self.validator.validate(query)
                    st.session_state.last_compliance_result = result
                    
                    # Add to history
                    st.session_state.rag_history.append({
                        "query": query,
                        "status": result.overall_status.value,
                        "score": result.compliance_score,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                st.rerun()
            else:
                st.warning("Please enter a query to validate")
        
        # History
        if st.session_state.rag_history:
            st.markdown("---")
            st.markdown("#### 📋 Recent Queries")
            
            for i, item in enumerate(reversed(st.session_state.rag_history[-5:])):
                status_colors = {
                    "compliant": t['success'],
                    "non_compliant": t['danger'],
                    "requires_review": t['warning']
                }
                color = status_colors.get(item['status'], t['text_muted'])
                
                st.markdown(f'''
                <div style="background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;
                            margin-bottom:0.5rem;border-left:3px solid {color};">
                    <div style="font-size:0.85rem;color:{t['text']};">
                        {item['query'][:50]}{'...' if len(item['query']) > 50 else ''}
                    </div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};margin-top:0.25rem;">
                        Score: {item['score']:.0f} | {item['timestamp']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_result_section(self):
        """Render compliance result section."""
        t = get_current_theme()
        
        st.markdown("### 📊 Compliance Result")
        
        result = st.session_state.last_compliance_result
        
        if result is None:
            st.info("👈 Enter a query and click 'Validate Compliance' to see results")
            return
        
        # Status indicator
        status_config = {
            ComplianceStatus.COMPLIANT: {
                "color": t['success'],
                "icon": "✅",
                "label": "COMPLIANT",
                "bg": f"{t['success']}15"
            },
            ComplianceStatus.NON_COMPLIANT: {
                "color": t['danger'],
                "icon": "❌",
                "label": "NON-COMPLIANT",
                "bg": f"{t['danger']}15"
            },
            ComplianceStatus.REQUIRES_REVIEW: {
                "color": t['warning'],
                "icon": "⚠️",
                "label": "REQUIRES REVIEW",
                "bg": f"{t['warning']}15"
            }
        }
        
        config = status_config.get(result.overall_status, status_config[ComplianceStatus.REQUIRES_REVIEW])
        
        # Main result card
        st.markdown(f'''
        <div style="background:{config['bg']};border:2px solid {config['color']};
                    padding:1.5rem;border-radius:12px;text-align:center;margin-bottom:1rem;">
            <div style="font-size:3rem;margin-bottom:0.5rem;">{config['icon']}</div>
            <div style="font-size:1.5rem;font-weight:700;color:{config['color']};">
                {config['label']}
            </div>
            <div style="font-size:2.5rem;font-weight:700;color:{t['text']};margin-top:0.5rem;">
                {result.compliance_score:.0f}<span style="font-size:1rem;color:{t['text_muted']};">/100</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # ESG Category
        if result.esg_category:
            esg_config = {
                ESGCategory.GREEN: ("🌿", "GREEN", t['success']),
                ESGCategory.BROWN: ("🏭", "BROWN", t['danger']),
                ESGCategory.TRANSITION: ("🔄", "TRANSITION", t['warning']),
                ESGCategory.NEUTRAL: ("⚪", "NEUTRAL", t['text_muted'])
            }
            icon, label, color = esg_config.get(result.esg_category, ("⚪", "NEUTRAL", t['text_muted']))
            
            st.markdown(f'''
            <div style="background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;gap:0.75rem;
                        margin-bottom:1rem;">
                <span style="font-size:1.5rem;">{icon}</span>
                <span style="font-weight:600;color:{color};">ESG Category: {label}</span>
            </div>
            ''', unsafe_allow_html=True)
        
        # Risk Factors
        if result.risk_factors:
            st.markdown("#### ⚠️ Risk Factors")
            for risk in result.risk_factors:
                st.markdown(f'''
                <div style="background:{t['danger']}10;padding:0.5rem 0.75rem;border-radius:6px;
                            margin-bottom:0.5rem;display:flex;align-items:center;gap:0.5rem;">
                    <span style="color:{t['danger']};">⚡</span>
                    <span style="color:{t['text_secondary']};font-size:0.9rem;">{risk}</span>
                </div>
                ''', unsafe_allow_html=True)
        
        # Matched Regulations
        if result.matched_regulations:
            st.markdown("#### 📚 Relevant Regulations")
            for reg in result.matched_regulations[:3]:
                st.markdown(f'''
                <div style="background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;
                            margin-bottom:0.5rem;border-left:3px solid {t['primary']};">
                    <div style="font-weight:600;color:{t['text']};">
                        {reg.regulation_id} - {reg.article}
                    </div>
                    <div style="font-size:0.85rem;color:{t['text_secondary']};margin-top:0.25rem;">
                        {reg.excerpt[:100]}...
                    </div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};margin-top:0.25rem;">
                        Issuer: {reg.issuer} | Year: {reg.year} | Relevance: {reg.relevance_score*100:.0f}%
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Recommendations
        if result.recommendations:
            st.markdown("#### 💡 Recommendations")
            for rec in result.recommendations:
                st.markdown(f'''
                <div style="display:flex;align-items:flex-start;gap:0.5rem;padding:0.5rem 0;">
                    <span style="color:{t['success']};">✓</span>
                    <span style="color:{t['text_secondary']};font-size:0.9rem;">{rec}</span>
                </div>
                ''', unsafe_allow_html=True)
        
        # Export button
        st.markdown("---")
        if st.button("📤 Export Compliance Report", use_container_width=True):
            st.toast("📄 Generating PDF report...")
    
    def _render_regulations_reference(self):
        """Render regulations reference section."""
        t = get_current_theme()
        
        st.markdown("### 📖 Regulatory Knowledge Base")
        
        regulations = self.validator.list_all_regulations()
        
        # Group by issuer
        issuers = {}
        for reg in regulations:
            issuer = reg['issuer']
            if issuer not in issuers:
                issuers[issuer] = []
            issuers[issuer].append(reg)
        
        cols = st.columns(len(issuers))
        
        issuer_icons = {"OJK": "🏛️", "BI": "🏦", "BPKH": "🕌"}
        
        for col, (issuer, regs) in zip(cols, issuers.items()):
            with col:
                st.markdown(f'''
                <div style="background:{t['bg_secondary']};padding:1rem;border-radius:12px;height:100%;">
                    <div style="text-align:center;margin-bottom:1rem;">
                        <span style="font-size:2rem;">{issuer_icons.get(issuer, '📋')}</span>
                        <div style="font-weight:700;color:{t['text']};margin-top:0.5rem;">{issuer}</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                for reg in regs:
                    st.markdown(f'''
                    <div style="background:{t['card']};padding:0.75rem;border-radius:6px;
                                margin-bottom:0.5rem;border:1px solid {t['border']};">
                        <div style="font-weight:600;font-size:0.85rem;color:{t['primary']};">
                            {reg['id']}
                        </div>
                        <div style="font-size:0.75rem;color:{t['text_secondary']};margin-top:0.25rem;">
                            {reg['title'][:40]}...
                        </div>
                        <div style="font-size:0.7rem;color:{t['text_muted']};margin-top:0.25rem;">
                            Year: {reg['year']} | Articles: {reg['article_count']}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)


def render():
    """Entry point for the Regulatory RAG page."""
    page = RegulatoryRAGPage()
    page.render()
