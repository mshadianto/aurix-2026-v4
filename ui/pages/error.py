"""
Error Page Module for AURIX.
Display error messages and recovery options.
"""

import streamlit as st
from typing import Optional

from ui.styles.css_builder import get_current_theme
from ui.components import render_footer


class ErrorPage:
    """Error page for displaying errors and recovery options."""
    
    def __init__(self, error_message: Optional[str] = None, error_code: Optional[str] = None):
        self.error_message = error_message or "An unexpected error occurred"
        self.error_code = error_code or "ERR_UNKNOWN"
    
    def render(self):
        """Render the Error page."""
        t = get_current_theme()
        
        st.markdown(f'''
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:6rem;margin-bottom:1rem;">⚠️</div>
            <h1 style="color:{t['danger']} !important;margin:0 0 0.5rem 0;">Oops! Something went wrong</h1>
            <div style="font-size:1.1rem;color:{t['text_secondary']} !important;max-width:500px;margin:0 auto 2rem;">
                {self.error_message}
            </div>
            <div class="pro-card" style="display:inline-block;padding:1rem 2rem;background:{t['bg_secondary']};">
                <span style="color:{t['text_muted']} !important;">Error Code:</span>
                <code style="margin-left:0.5rem;color:{t['danger']} !important;">{self.error_code}</code>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Recovery options
        st.markdown("### What can you do?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:1.5rem;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🔄</div>
                <div style="font-weight:600;color:{t['text']} !important;">Refresh Page</div>
                <div style="font-size:0.85rem;color:{t['text_muted']} !important;">Try reloading the page</div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("🔄 Refresh", key="refresh_btn", use_container_width=True):
                st.rerun()
        
        with col2:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:1.5rem;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🏠</div>
                <div style="font-weight:600;color:{t['text']} !important;">Go to Dashboard</div>
                <div style="font-size:0.85rem;color:{t['text_muted']} !important;">Return to main page</div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("🏠 Dashboard", key="dashboard_btn", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
        with col3:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:1.5rem;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">📞</div>
                <div style="font-weight:600;color:{t['text']} !important;">Get Help</div>
                <div style="font-size:0.85rem;color:{t['text_muted']} !important;">Contact support</div>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("📞 Help", key="help_btn", use_container_width=True):
                st.session_state.current_page = 'help'
                st.rerun()
        
        # Error details (collapsible)
        with st.expander("🔍 Technical Details", expanded=False):
            st.markdown(f'''
            <div style="font-family:monospace;font-size:0.85rem;background:{t['bg_secondary']};padding:1rem;border-radius:8px;">
                <div><strong>Error Code:</strong> {self.error_code}</div>
                <div><strong>Message:</strong> {self.error_message}</div>
                <div><strong>Timestamp:</strong> {st.session_state.get('error_timestamp', 'N/A')}</div>
                <div><strong>Page:</strong> {st.session_state.get('current_page', 'unknown')}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('''
            If this error persists, please:
            1. Clear your browser cache
            2. Try using a different browser
            3. Contact support with the error details above
            ''')
        
        render_footer()


def render(error_message: Optional[str] = None, error_code: Optional[str] = None):
    """Entry point for the Error page."""
    page = ErrorPage(error_message, error_code)
    page.render()
