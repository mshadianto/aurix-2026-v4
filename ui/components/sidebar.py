"""
Enhanced Sidebar Component for AURIX 2026.
Features:
- Grouped navigation (Core Audit, Intelligence, Labs, Admin)
- Floating Copilot FAB integration
- Theme toggle and stats
"""

import streamlit as st
from typing import List, Dict, Optional
from ui.styles.css_builder import get_current_theme
from ui.components.badges import render_badge


def render_logo():
    """Render AURIX logo with native Streamlit."""
    st.markdown("### 🛡️ AURIX")
    st.caption("v4.2 Excellence 2026")


def render_theme_toggle():
    """Render theme toggle buttons."""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("☀️ Light", use_container_width=True, key="light_btn"):
            st.session_state.theme = 'light'
            st.rerun()
    
    with col2:
        if st.button("🌙 Dark", use_container_width=True, key="dark_btn"):
            st.session_state.theme = 'dark'
            st.rerun()


# ============================================
# COMPACT NAVIGATION - Premium 2026
# ============================================

# Simplified navigation structure
NAVIGATION_SECTIONS = {
    "MAIN": [
        "📊 Dashboard",
        "🎛️ Command Center",
        "📋 Findings Tracker",
    ],
    "AUDIT": [
        "📁 Documents",
        "📝 Workpapers",
        "⚖️ Risk Assessment",
        "🎭 PTCF Builder",
        "📅 Audit Planning",
    ],
    "ANALYTICS": [
        "📈 KRI Dashboard",
        "🔄 Continuous Audit",
        "🔍 Fraud Detection",
        "📊 Analytics",
        "🔄 Process Mining",
    ],
    "TOOLS": [
        "🌐 Risk Universe",
        "📌 Issue Tracker",
        "🔬 Root Cause Analyzer",
        "🧮 Sampling Calculator",
        "📆 Audit Timeline",
    ],
    "MORE": [
        "📜 Regulatory RAG",
        "🧪 AI Lab",
        "📑 Report Builder",
        "👥 Team Hub",
        "🎮 Gamification",
        "⚙️ Settings",
    ],
}


def render_compact_navigation(routes: List[str]) -> str:
    """Render compact navigation with tabs and selectbox."""
    t = get_current_theme()
    gold = t.get('gold', t['accent'])

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "📊 Dashboard"

    # Section selector
    section_labels = {
        "MAIN": "🎯 Main",
        "AUDIT": "📋 Audit",
        "ANALYTICS": "📊 Analytics",
        "TOOLS": "🔧 Tools",
        "MORE": "⚙️ More",
    }

    # Find current section
    current_section = "MAIN"
    for section, pages in NAVIGATION_SECTIONS.items():
        if st.session_state.current_page in pages:
            current_section = section
            break

    # Section tabs
    sections = list(section_labels.keys())
    cols = st.columns(len(sections))

    for i, (col, section) in enumerate(zip(cols, sections)):
        with col:
            is_active = section == current_section
            if st.button(
                section_labels[section].split()[0],  # Just emoji
                key=f"sec_{section}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                # Switch to first page of section
                available = [p for p in NAVIGATION_SECTIONS[section] if p in routes or p in ["🔄 Process Mining", "📜 Regulatory RAG"]]
                if available:
                    st.session_state.current_page = available[0]
                    st.rerun()

    # Page list for current section
    available_pages = [p for p in NAVIGATION_SECTIONS[current_section]
                       if p in routes or p in ["🔄 Process Mining", "📜 Regulatory RAG"]]

    if available_pages:
        selected = st.radio(
            "Navigate",
            available_pages,
            index=available_pages.index(st.session_state.current_page) if st.session_state.current_page in available_pages else 0,
            key="nav_radio",
            label_visibility="collapsed"
        )

        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.rerun()

    return st.session_state.current_page


def render_grouped_navigation(routes: List[str], categories: Dict[str, List[str]]) -> str:
    """Wrapper for backward compatibility."""
    return render_compact_navigation(routes)


def render_session_stats():
    """Render session statistics using native Streamlit."""
    doc_count = len(st.session_state.get('documents', []))
    finding_count = len(st.session_state.get('findings', []))

    st.caption("📊 QUICK STATS")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Docs", doc_count)
    with col2:
        st.metric("Findings", finding_count)
    with col3:
        st.metric("Alerts", 3)


def render_llm_config():
    """Render LLM configuration section."""
    from app.constants import LLM_PROVIDER_INFO

    st.caption("🤖 AI PROVIDER")

    providers = list(LLM_PROVIDER_INFO.keys())

    provider = st.selectbox(
        "Provider",
        providers,
        key="llm_provider",
        label_visibility="collapsed",
        format_func=lambda x: f"{LLM_PROVIDER_INFO[x]['name']} {'🆓' if LLM_PROVIDER_INFO[x]['free'] else '💎'}"
    )

    info = LLM_PROVIDER_INFO.get(provider, {})

    if provider not in ['mock', 'ollama']:
        st.text_input(
            "API Key",
            type="password",
            key="api_key_input",
            label_visibility="collapsed",
            placeholder="Enter API key..."
        )

    if info.get('url'):
        st.link_button("Get API Key →", info['url'], use_container_width=True)


def render_sidebar(routes: List[str], categories: Dict[str, List[str]]) -> str:
    """Render compact sidebar with navigation."""
    with st.sidebar:
        render_logo()
        render_theme_toggle()

        st.divider()

        selected_page = render_grouped_navigation(routes, categories)

        st.divider()

        render_session_stats()

        st.divider()

        render_llm_config()

        st.caption("💡 Press 🤖 for AI Copilot")

    return selected_page
