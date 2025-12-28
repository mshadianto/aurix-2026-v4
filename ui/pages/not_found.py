"""
Not Found Page Module for AURIX.
404 error page for invalid routes.
"""

import streamlit as st

from ui.styles.css_builder import get_current_theme
from ui.components import render_footer


class NotFoundPage:
    """404 Not Found page."""
    
    def __init__(self, requested_page: str = ""):
        self.requested_page = requested_page
    
    def render(self):
        """Render the Not Found page."""
        t = get_current_theme()
        
        st.markdown(f'''
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:8rem;margin-bottom:1rem;opacity:0.3;">404</div>
            <h1 style="color:{t['text']} !important;margin:0 0 0.5rem 0;">Page Not Found</h1>
            <div style="font-size:1.1rem;color:{t['text_secondary']} !important;max-width:500px;margin:0 auto 2rem;">
                The page you're looking for doesn't exist or has been moved.
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if self.requested_page:
            st.markdown(f'''
            <div style="text-align:center;margin-bottom:2rem;">
                <div class="pro-card" style="display:inline-block;padding:1rem 2rem;background:{t['bg_secondary']};">
                    <span style="color:{t['text_muted']} !important;">Requested:</span>
                    <code style="margin-left:0.5rem;color:{t['warning']} !important;">{self.requested_page}</code>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Suggested pages
        st.markdown("### 🔗 Maybe you were looking for:")
        
        suggestions = [
            ("🏠", "Dashboard", "dashboard", "Main overview and statistics"),
            ("📄", "Documents", "documents", "Upload and manage documents"),
            ("⚖️", "Risk Assessment", "risk_assessment", "Perform risk evaluations"),
            ("📋", "Findings", "findings", "Track audit findings"),
            ("🤖", "AI Chat", "chat", "Get AI assistance"),
            ("⚙️", "Settings", "settings", "Configure the application")
        ]
        
        cols = st.columns(3)
        for i, (icon, name, page_key, desc) in enumerate(suggestions):
            with cols[i % 3]:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;text-align:center;margin-bottom:1rem;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-weight:600;color:{t['text']} !important;">{name}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']} !important;">{desc}</div>
                </div>
                ''', unsafe_allow_html=True)
                
                if st.button(f"Go to {name}", key=f"goto_{page_key}", use_container_width=True):
                    st.session_state.current_page = page_key
                    st.rerun()
        
        st.markdown("---")
        
        # Search suggestion
        st.markdown(f'''
        <div style="text-align:center;padding:2rem;">
            <div style="color:{t['text_muted']} !important;margin-bottom:1rem;">
                Still can't find what you need?
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 Return to Dashboard", type="primary", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
        with col2:
            if st.button("❓ Get Help", use_container_width=True):
                st.session_state.current_page = 'help'
                st.rerun()
        
        render_footer()


def render(requested_page: str = ""):
    """Entry point for the Not Found page."""
    page = NotFoundPage(requested_page)
    page.render()
