"""
Application Router - Handles page navigation and rendering.
AURIX Excellence 2026 Edition
"""

import streamlit as st
from typing import Dict, Callable, Any

from ui.components.sidebar import render_sidebar
from ui.components.floating_copilot import render_floating_copilot
from ui.styles.css_builder import inject_css
from ui.pages import (
    dashboard,
    documents,
    ptcf_builder,
    risk_assessment,
    findings,
    continuous_audit,
    kri_dashboard,
    fraud_detection,
    regulatory_compliance,
    chat,
    analytics,
    settings,
    help,
    about,
    error,
    not_found
)
# Enhanced modules v4.1
from ui.pages import workpaper, audit_planning, sampling, report_builder
# WOW modules v4.2
from ui.pages import (
    gamification,
    risk_universe,
    root_cause,
    issue_tracker,
    command_center,
    ai_lab,
    timeline,
    team_hub
)
# 2026 Excellence modules
from ui.pages import process_mining, regulatory_rag


class Router:
    """
    Application router that handles page navigation.
    Implements a simple routing pattern for Streamlit.
    """
    
    def __init__(self):
        """Initialize router with page mappings."""
        self.routes: Dict[str, Callable] = {
            # Main
            "📊 Dashboard": dashboard.render,
            "🎛️ Command Center": command_center.render,
            "📁 Documents": documents.render,
            "🎭 PTCF Builder": ptcf_builder.render,
            # Audit Tools
            "⚖️ Risk Assessment": risk_assessment.render,
            "🌐 Risk Universe": risk_universe.render,
            "📋 Findings Tracker": findings.render,
            "📌 Issue Tracker": issue_tracker.render,
            "📝 Workpapers": workpaper.render,
            "📅 Audit Planning": audit_planning.render,
            "📆 Audit Timeline": timeline.render,
            "🔬 Root Cause Analyzer": root_cause.render,
            "🧮 Sampling Calculator": sampling.render,
            # Monitoring
            "🔄 Continuous Audit": continuous_audit.render,
            "📈 KRI Dashboard": kri_dashboard.render,
            "🔍 Fraud Detection": fraud_detection.render,
            # 2026 Intelligence
            "🔄 Process Mining": process_mining.render,
            "📜 Regulatory RAG": regulatory_rag.render,
            # Intelligence
            "🤖 AI Chat": chat.render,
            "🧪 AI Lab": ai_lab.render,
            "📊 Analytics": analytics.render,
            "📑 Report Builder": report_builder.render,
            # Collaboration
            "👥 Team Hub": team_hub.render,
            "🎮 Gamification": gamification.render,
            # Reference
            "📚 Regulations": regulatory_compliance.render,
            "⚙️ Settings": settings.render,
            "❓ Help": help.render,
            "ℹ️ About": about.render,
        }
        
        self.page_categories = {
            "Main": [
                "📊 Dashboard",
                "🎛️ Command Center",
                "📁 Documents",
                "🎭 PTCF Builder",
            ],
            "Audit Tools": [
                "⚖️ Risk Assessment",
                "🌐 Risk Universe",
                "📋 Findings Tracker",
                "📌 Issue Tracker",
                "📝 Workpapers",
                "📅 Audit Planning",
                "📆 Audit Timeline",
                "🔬 Root Cause Analyzer",
                "🧮 Sampling Calculator",
            ],
            "Monitoring": [
                "🔄 Continuous Audit",
                "📈 KRI Dashboard",
                "🔍 Fraud Detection",
                "🔄 Process Mining",
                "📜 Regulatory RAG",
            ],
            "Intelligence": [
                "🤖 AI Chat",
                "🧪 AI Lab",
                "📊 Analytics",
                "📑 Report Builder",
            ],
            "Collaboration": [
                "👥 Team Hub",
                "🎮 Gamification",
            ],
            "Reference": [
                "📚 Regulations",
                "⚙️ Settings",
                "❓ Help",
                "ℹ️ About",
            ]
        }
    
    def render(self):
        """Main render method - renders sidebar, page, and floating copilot."""
        # Inject CSS styles
        inject_css()
        
        # Render sidebar and get selected page
        selected_page = render_sidebar(
            routes=list(self.routes.keys()),
            categories=self.page_categories
        )
        
        # Store current page in session
        st.session_state.current_page = selected_page
        
        # Render selected page
        self._render_page(selected_page)
        
        # Render floating AI Copilot (2026 feature)
        st.markdown("---")
        render_floating_copilot()
    
    def _render_page(self, page_name: str):
        """Render specific page by name."""
        if page_name in self.routes:
            try:
                self.routes[page_name]()
            except Exception as e:
                self._render_error_page(page_name, e)
        else:
            self._render_404(page_name)
    
    def _render_error_page(self, page_name: str, err: Exception):
        """Render error page when page fails to load."""
        st.session_state.error_timestamp = st.session_state.get('error_timestamp', '')
        from datetime import datetime
        st.session_state.error_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        error.render(
            error_message=f"Failed to load {page_name}: {str(err)}",
            error_code="ERR_PAGE_LOAD"
        )
    
    def _render_404(self, requested_page: str = ""):
        """Render 404 not found page."""
        not_found.render(requested_page)
    
    def get_page_icon(self, page_name: str) -> str:
        """Extract icon from page name."""
        if " " in page_name:
            return page_name.split(" ")[0]
        return "📄"
    
    def get_page_title(self, page_name: str) -> str:
        """Extract title from page name (without icon)."""
        if " " in page_name:
            return " ".join(page_name.split(" ")[1:])
        return page_name
