"""
About Page Module for AURIX.
Application information, credits, and version history.
"""

import streamlit as st
from datetime import datetime

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from app.constants import APP_NAME, APP_VERSION, APP_DESCRIPTION


class AboutPage:
    """About page with application information."""
    
    def render(self):
        """Render the About page."""
        render_page_header("About AURIX", "Application information and credits")
        
        t = get_current_theme()
        
        # Hero section
        st.markdown(f'''
        <div style="text-align:center;padding:3rem 1rem;background:linear-gradient(135deg, {t['primary']}15, {t['accent']}15);border-radius:16px;margin-bottom:2rem;">
            <div style="font-size:4rem;margin-bottom:1rem;">🔍</div>
            <h1 style="color:{t['text']} !important;margin:0 0 0.5rem 0;font-size:2.5rem;">{APP_NAME}</h1>
            <div style="font-size:1.1rem;color:{t['primary']} !important;font-weight:600;margin-bottom:1rem;">
                AUdit Risk Intelligence eXcellence
            </div>
            <div style="color:{t['text_secondary']} !important;max-width:600px;margin:0 auto;">
                {APP_DESCRIPTION}
            </div>
            <div style="margin-top:1.5rem;">
                <span class="badge" style="background:{t['primary']};color:white;padding:0.5rem 1rem;font-size:1rem;">
                    Version {APP_VERSION}
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Features section
        st.markdown("### ✨ Key Features")
        
        features = [
            ("🤖", "AI-Powered Intelligence", "Leverage advanced LLM capabilities for audit analysis, risk assessment, and procedure generation."),
            ("📊", "Comprehensive Analytics", "Real-time dashboards, KRI monitoring, and trend analysis for data-driven audit decisions."),
            ("🔍", "Fraud Detection", "Red flag analysis and case management tools for fraud investigation."),
            ("📋", "PTCF Framework", "Professional prompt engineering using Persona-Task-Context-Format methodology."),
            ("📚", "Regulatory Compliance", "Built-in Indonesian financial regulations (OJK, BI) for compliance tracking."),
            ("🔄", "Continuous Audit", "Real-time monitoring with customizable rules and automated alerting."),
            ("💰", "Free LLM Access", "Integration with free AI providers (Groq, Together AI, Google AI Studio)."),
            ("🎨", "Modern UI/UX", "Enterprise-grade interface with dark/light mode and responsive design.")
        ]
        
        cols = st.columns(2)
        for i, (icon, title, desc) in enumerate(features):
            with cols[i % 2]:
                st.markdown(f'''
                <div class="pro-card" style="padding:1.25rem;margin-bottom:1rem;">
                    <div style="display:flex;gap:1rem;align-items:start;">
                        <span style="font-size:2rem;">{icon}</span>
                        <div>
                            <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.25rem;">{title}</div>
                            <div style="font-size:0.9rem;color:{t['text_secondary']} !important;">{desc}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Technology stack
        st.markdown("### 🛠️ Technology Stack")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="pro-card" style="padding:1.5rem;text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🐍</div>
                <div style="font-weight:600;color:{t['text']} !important;">Backend</div>
                <div style="font-size:0.85rem;color:{t['text_muted']} !important;margin-top:0.5rem;">
                    Python 3.11+<br>
                    Streamlit<br>
                    LangChain<br>
                    PostgreSQL
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="pro-card" style="padding:1.5rem;text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🤖</div>
                <div style="font-weight:600;color:{t['text']} !important;">AI/LLM</div>
                <div style="font-size:0.85rem;color:{t['text_muted']} !important;margin-top:0.5rem;">
                    Groq<br>
                    Together AI<br>
                    Google Gemini<br>
                    OpenRouter
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="pro-card" style="padding:1.5rem;text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🎨</div>
                <div style="font-weight:600;color:{t['text']} !important;">Frontend</div>
                <div style="font-size:0.85rem;color:{t['text_muted']} !important;margin-top:0.5rem;">
                    Streamlit UI<br>
                    Custom CSS<br>
                    Responsive Design<br>
                    Dark/Light Theme
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Version history
        st.markdown("### 📜 Version History")
        
        versions = [
            ("4.0.0", "December 2024", "Major Release", [
                "Complete architecture redesign",
                "New modular page structure",
                "Enhanced PTCF Builder",
                "Fraud Detection module",
                "KRI Dashboard",
                "Continuous Audit monitoring"
            ]),
            ("3.0.0", "November 2024", "Feature Release", [
                "PostgreSQL integration",
                "Real-time visitor analytics",
                "Improved UI/UX",
                "Multi-provider LLM support"
            ]),
            ("2.0.0", "October 2024", "Feature Release", [
                "RAG implementation",
                "Document management",
                "Risk assessment module",
                "Findings tracker"
            ]),
            ("1.0.0", "September 2024", "Initial Release", [
                "Core platform launch",
                "Basic AI chat",
                "Simple document upload",
                "Initial UI design"
            ])
        ]
        
        for version, date, release_type, changes in versions:
            with st.expander(f"v{version} - {date} ({release_type})", expanded=version == "4.0.0"):
                for change in changes:
                    st.markdown(f"- ✓ {change}")
        
        st.markdown("---")
        
        # Credits
        st.markdown("### 👥 Credits & Acknowledgments")
        
        st.markdown(f'''
        <div class="pro-card" style="padding:1.5rem;">
            <div style="margin-bottom:1rem;">
                <div style="font-weight:600;color:{t['text']} !important;">Developed by</div>
                <div style="color:{t['text_secondary']} !important;">
                    MS Hadianto - GRC Expert | AI-Powered Builder<br>
                    <a href="https://github.com/mshadianto" target="_blank" style="color:{t['primary']} !important;">github.com/mshadianto</a>
                </div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="font-weight:600;color:{t['text']} !important;">Methodology</div>
                <div style="color:{t['text_secondary']} !important;">McKinsey Consulting & Big 4 Audit Frameworks</div>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="font-weight:600;color:{t['text']} !important;">Regulatory Framework</div>
                <div style="color:{t['text_secondary']} !important;">OJK, Bank Indonesia, ISO Standards</div>
            </div>
            <div>
                <div style="font-weight:600;color:{t['text']} !important;">Special Thanks</div>
                <div style="color:{t['text_secondary']} !important;">
                    Anthropic (Claude AI), Streamlit Team, Open Source Community
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # License
        st.markdown("### 📄 License")
        
        st.markdown(f'''
        <div class="pro-card" style="padding:1.5rem;background:{t['bg_secondary']};">
            <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.5rem;">MIT License</div>
            <div style="font-size:0.85rem;color:{t['text_secondary']} !important;">
                Copyright © 2024 AURIX Project
                <br><br>
                Permission is hereby granted, free of charge, to any person obtaining a copy
                of this software and associated documentation files (the "Software"), to deal
                in the Software without restriction, including without limitation the rights
                to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                copies of the Software, and to permit persons to whom the Software is
                furnished to do so, subject to the following conditions:
                <br><br>
                The above copyright notice and this permission notice shall be included in all
                copies or substantial portions of the Software.
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        render_footer()


def render():
    """Entry point for the About page."""
    page = AboutPage()
    page.render()
