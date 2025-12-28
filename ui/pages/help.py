"""
Help Page Module for AURIX.
Documentation, user guides, and support resources.
"""

import streamlit as st
from typing import Dict, List

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from app.constants import APP_NAME, APP_VERSION


class HelpPage:
    """Help and documentation page."""
    
    def render(self):
        """Render the Help page."""
        render_page_header("Help & Documentation", "User guides and support resources")
        
        t = get_current_theme()
        
        # Search
        search_query = st.text_input(
            "🔍 Search documentation",
            placeholder="Search for help topics...",
            key="help_search"
        )
        
        st.markdown("---")
        
        # Tabs for different help sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "📚 Getting Started",
            "🎓 User Guide",
            "❓ FAQ",
            "📞 Support"
        ])
        
        with tab1:
            self._render_getting_started()
        
        with tab2:
            self._render_user_guide()
        
        with tab3:
            self._render_faq()
        
        with tab4:
            self._render_support()
        
        render_footer()
    
    def _render_getting_started(self):
        """Render getting started section."""
        t = get_current_theme()
        
        st.markdown("### 🚀 Getting Started with AURIX")
        
        st.markdown(f'''
        <div class="pro-card" style="background:linear-gradient(135deg, {t['primary']}15, {t['accent']}15);padding:1.5rem;margin-bottom:1.5rem;">
            <h4 style="margin:0 0 0.5rem 0;color:{t['text']} !important;">Welcome to AURIX!</h4>
            <p style="color:{t['text_secondary']} !important;margin:0;">
                AURIX (AUdit Risk Intelligence eXcellence) is a comprehensive AI-powered platform 
                designed for Internal Auditors in the Indonesian financial industry. 
                Follow this guide to get started quickly.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Quick start steps
        steps = [
            ("1️⃣", "Configure AI Provider", "Go to Settings → AI Provider to set up your preferred LLM provider. You can use free providers like Groq, Together AI, or Google AI Studio."),
            ("2️⃣", "Upload Documents", "Navigate to Documents module to upload your audit-related documents (policies, regulations, working papers)."),
            ("3️⃣", "Explore Modules", "Use the sidebar to navigate between different modules: Risk Assessment, Findings, PTCF Builder, and more."),
            ("4️⃣", "Chat with AI", "Use the AI Chat to ask questions about audit procedures, regulations, or risk assessment."),
            ("5️⃣", "Generate Reports", "Use Analytics module to generate comprehensive audit reports and dashboards.")
        ]
        
        for icon, title, desc in steps:
            st.markdown(f'''
            <div class="pro-card" style="padding:1rem;margin-bottom:0.75rem;">
                <div style="display:flex;gap:1rem;align-items:start;">
                    <span style="font-size:1.5rem;">{icon}</span>
                    <div>
                        <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.25rem;">{title}</div>
                        <div style="font-size:0.9rem;color:{t['text_secondary']} !important;">{desc}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Video tutorial placeholder
        st.markdown("### 🎥 Video Tutorials")
        
        tutorials = [
            ("Introduction to AURIX", "5 min", "Overview of all features"),
            ("Setting Up AI Provider", "3 min", "Configure LLM integration"),
            ("Using PTCF Builder", "8 min", "Create professional audit prompts"),
            ("Risk Assessment Workflow", "10 min", "Complete risk assessment guide")
        ]
        
        cols = st.columns(2)
        for i, (title, duration, desc) in enumerate(tutorials):
            with cols[i % 2]:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;text-align:center;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">🎬</div>
                    <div style="font-weight:600;color:{t['text']} !important;">{title}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']} !important;">{duration} • {desc}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_user_guide(self):
        """Render user guide section."""
        t = get_current_theme()
        
        st.markdown("### 📖 User Guide")
        
        modules = {
            "Dashboard": {
                "icon": "🏠",
                "desc": "Overview of audit activities and key metrics",
                "features": ["Real-time visitor statistics", "Quick access to all modules", "Summary of open findings"]
            },
            "Documents": {
                "icon": "📄",
                "desc": "Upload and manage audit documents",
                "features": ["Multi-file upload", "Document categorization", "Full-text search", "RAG integration"]
            },
            "Risk Assessment": {
                "icon": "⚖️",
                "desc": "Perform risk assessments using standard methodology",
                "features": ["Risk scoring matrix", "Control evaluation", "Risk heatmap visualization"]
            },
            "PTCF Builder": {
                "icon": "🎭",
                "desc": "Build professional audit prompts",
                "features": ["Persona-Task-Context-Format framework", "Template library", "AI execution"]
            },
            "Findings Tracker": {
                "icon": "📋",
                "desc": "Manage audit findings lifecycle",
                "features": ["5Cs documentation", "Status tracking", "Due date monitoring", "Export capabilities"]
            },
            "Continuous Audit": {
                "icon": "🔄",
                "desc": "Real-time monitoring and alerting",
                "features": ["Custom rule creation", "Alert dashboard", "Trend analysis"]
            },
            "KRI Dashboard": {
                "icon": "📊",
                "desc": "Key Risk Indicators monitoring",
                "features": ["KRI gauges", "Threshold alerts", "Historical trends"]
            },
            "Fraud Detection": {
                "icon": "🔍",
                "desc": "Red flag analysis and fraud investigation",
                "features": ["Red flag scanner", "Case management", "Risk scoring"]
            },
            "AI Chat": {
                "icon": "🤖",
                "desc": "Conversational AI assistant",
                "features": ["Context-aware responses", "Quick prompts", "Chat history"]
            },
            "Analytics": {
                "icon": "📈",
                "desc": "Comprehensive audit analytics",
                "features": ["Performance metrics", "Coverage analysis", "Report generation"]
            }
        }
        
        for module, info in modules.items():
            with st.expander(f"{info['icon']} {module}", expanded=False):
                st.markdown(f'''
                <div style="color:{t['text_secondary']} !important;margin-bottom:1rem;">
                    {info['desc']}
                </div>
                <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.5rem;">Key Features:</div>
                ''', unsafe_allow_html=True)
                
                for feature in info['features']:
                    st.markdown(f"- ✓ {feature}")
    
    def _render_faq(self):
        """Render FAQ section."""
        t = get_current_theme()
        
        st.markdown("### ❓ Frequently Asked Questions")
        
        faqs = [
            {
                "q": "How do I set up an AI provider?",
                "a": "Go to Settings → AI Provider. Select your preferred provider (Groq, Together AI, Google AI Studio, etc.), enter your API key, and click 'Save Key'. Most providers offer free API access."
            },
            {
                "q": "Is my data secure?",
                "a": "AURIX runs entirely in your browser session. Document data is processed locally and sent to your chosen AI provider only when explicitly requested. No data is stored on our servers."
            },
            {
                "q": "Which AI providers are free?",
                "a": "Groq, Together AI, Google AI Studio (Gemini), and OpenRouter offer free tiers. Ollama allows you to run models locally for free. Mock mode requires no API key and is available for testing."
            },
            {
                "q": "How do I export my findings?",
                "a": "Go to Findings Tracker → Export tab. You can export findings in CSV format for Excel or generate a markdown summary report."
            },
            {
                "q": "What is the PTCF framework?",
                "a": "PTCF stands for Persona-Task-Context-Format. It's a structured approach to crafting effective AI prompts, following best practices from McKinsey and Big 4 consulting methodologies."
            },
            {
                "q": "Can I customize the risk assessment criteria?",
                "a": "Yes, the risk assessment module uses configurable likelihood and impact scales. You can also add custom control factors in the assessment form."
            },
            {
                "q": "How do I create continuous audit rules?",
                "a": "Go to Continuous Audit → Create Rule tab. Define the rule name, description, category, threshold values, and monitoring schedule."
            },
            {
                "q": "Does AURIX support Indonesian regulations?",
                "a": "Yes, AURIX includes a comprehensive database of OJK, BI, and ISO regulations relevant to Indonesian financial institutions. The AI is trained to provide context-aware regulatory guidance."
            },
            {
                "q": "How do I backup my data?",
                "a": "Go to Settings → Data & Export → Export All Data. This downloads a JSON backup file that can be restored later using the 'Import Backup' feature."
            },
            {
                "q": "Is there a mobile version?",
                "a": "AURIX is a responsive web application that works on mobile browsers. For the best experience, we recommend using a desktop or tablet."
            }
        ]
        
        for faq in faqs:
            with st.expander(f"💬 {faq['q']}", expanded=False):
                st.markdown(f'''
                <div style="color:{t['text_secondary']} !important;padding:0.5rem 0;">
                    {faq['a']}
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_support(self):
        """Render support section."""
        t = get_current_theme()
        
        st.markdown("### 📞 Support & Contact")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:2rem;">
                <div style="font-size:3rem;margin-bottom:1rem;">📧</div>
                <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.5rem;">Email Support</div>
                <div style="color:{t['text_secondary']} !important;margin-bottom:1rem;">
                    For technical issues and feature requests
                </div>
                <a href="mailto:sopian.hadianto@gmail.com" style="color:{t['primary']} !important;">
                    sopian.hadianto@gmail.com
                </a>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:2rem;">
                <div style="font-size:3rem;margin-bottom:1rem;">💬</div>
                <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.5rem;">Community</div>
                <div style="color:{t['text_secondary']} !important;margin-bottom:1rem;">
                    Join our community for discussions
                </div>
                <a href="https://github.com/mshadianto/aurix" target="_blank" style="color:{t['primary']} !important;">
                    GitHub Discussions
                </a>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feedback form
        st.markdown("### 💡 Submit Feedback")
        
        feedback_type = st.selectbox(
            "Feedback Type",
            ["Bug Report", "Feature Request", "General Feedback", "Documentation"],
            key="feedback_type"
        )
        
        feedback_message = st.text_area(
            "Your Feedback",
            height=150,
            placeholder="Describe your feedback in detail...",
            key="feedback_message"
        )
        
        if st.button("📤 Submit Feedback", type="primary"):
            if feedback_message:
                st.success("✓ Thank you for your feedback! We'll review it shortly.")
            else:
                st.error("Please enter your feedback message.")
        
        # Resources
        st.markdown("### 📚 Additional Resources")
        
        resources = [
            ("📖 Documentation", "https://docs.aurix.id", "Comprehensive documentation"),
            ("🎥 YouTube Channel", "https://youtube.com/@aurix", "Video tutorials"),
            ("📰 Blog", "https://blog.aurix.id", "Tips and best practices"),
            ("🐙 GitHub", "https://github.com/mshadianto/aurix", "Source code and issues")
        ]
        
        cols = st.columns(4)
        for i, (name, url, desc) in enumerate(resources):
            with cols[i]:
                st.markdown(f'''
                <div class="pro-card" style="text-align:center;padding:1rem;">
                    <div style="font-size:1.5rem;margin-bottom:0.5rem;">{name.split()[0]}</div>
                    <div style="font-size:0.85rem;font-weight:600;color:{t['text']} !important;">{name.split(maxsplit=1)[1]}</div>
                    <div style="font-size:0.75rem;color:{t['text_muted']} !important;">{desc}</div>
                </div>
                ''', unsafe_allow_html=True)


def render():
    """Entry point for the Help page."""
    page = HelpPage()
    page.render()
