"""
Settings Page Module for AURIX.
Application configuration and preferences.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer, render_alert
from app.constants import LLM_PROVIDER_INFO, APP_NAME, APP_VERSION


class SettingsPage:
    """Settings and configuration page."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize settings in session state."""
        defaults = {
            'llm_provider': 'mock',
            'api_key_input': '',
            'theme_mode': 'dark',
            'language': 'id',
            'auto_save': True,
            'show_tooltips': True,
            'compact_mode': False,
            'notifications_enabled': True,
            'export_format': 'xlsx'
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def render(self):
        """Render the Settings page."""
        render_page_header("Settings", "Configure your AURIX experience")
        
        t = get_current_theme()
        
        # Settings tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🤖 AI Provider",
            "🎨 Appearance",
            "⚙️ General",
            "📊 Data & Export"
        ])
        
        with tab1:
            self._render_ai_settings()
        
        with tab2:
            self._render_appearance_settings()
        
        with tab3:
            self._render_general_settings()
        
        with tab4:
            self._render_data_settings()
        
        render_footer()
    
    def _render_ai_settings(self):
        """Render AI provider settings."""
        t = get_current_theme()
        
        st.markdown("### 🤖 AI Provider Configuration")
        
        st.markdown(f'''
        <div class="pro-card" style="background:linear-gradient(135deg, {t['primary']}15, {t['accent']}15);margin-bottom:1.5rem;">
            <p style="color:{t['text_secondary']} !important;margin:0;">
                AURIX supports multiple LLM providers. Configure your preferred provider below.
                All providers marked with 🆓 offer free API access.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Provider selection
        st.markdown("#### Select Provider")
        
        current_provider = st.session_state.get('llm_provider', 'mock')
        
        cols = st.columns(3)
        
        for i, (key, info) in enumerate(LLM_PROVIDER_INFO.items()):
            with cols[i % 3]:
                is_selected = current_provider == key
                border_color = t['primary'] if is_selected else t['border']
                bg_color = f"{t['primary']}10" if is_selected else t['card']
                
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;border:2px solid {border_color};background:{bg_color};cursor:pointer;">
                    <div style="font-weight:600;color:{t['text']} !important;margin-bottom:0.25rem;">
                        {info['name']} {'✓' if is_selected else ''}
                    </div>
                    <div style="font-size:0.8rem;color:{t['text_secondary']} !important;">
                        {info['description']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                if st.button(f"Select {info['name']}", key=f"select_{key}", use_container_width=True):
                    st.session_state.llm_provider = key
                    st.success(f"✓ Provider changed to {info['name']}")
                    st.rerun()
        
        st.markdown("---")
        
        # API Key configuration
        st.markdown("#### API Key Configuration")
        
        selected_info = LLM_PROVIDER_INFO.get(current_provider, {})
        
        if current_provider != 'mock':
            col1, col2 = st.columns([3, 1])
            
            with col1:
                api_key = st.text_input(
                    f"{selected_info.get('name', '')} API Key",
                    type="password",
                    value=st.session_state.get('api_key_input', ''),
                    placeholder="Enter your API key...",
                    key="api_key_field"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Save Key", use_container_width=True):
                    st.session_state.api_key_input = api_key
                    st.success("✓ API key saved")
            
            # Get API key link
            if selected_info.get('url'):
                st.markdown(f'''
                <div style="margin-top:0.5rem;">
                    <a href="{selected_info['url']}" target="_blank" style="color:{t['primary']} !important;font-size:0.85rem;">
                        🔗 Get your {selected_info['name']} API key
                    </a>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("🧪 Mock mode is active. No API key required. Responses are simulated for demo purposes.")
        
        st.markdown("---")
        
        # Model selection
        st.markdown("#### Model Selection")
        
        default_model = selected_info.get('default_model', 'N/A')
        
        if current_provider == 'groq':
            models = ['llama-3.3-70b-versatile', 'llama-3.1-70b-versatile', 'mixtral-8x7b-32768', 'gemma2-9b-it']
        elif current_provider == 'together':
            models = ['meta-llama/Llama-3.3-70B-Instruct-Turbo', 'Qwen/Qwen2.5-72B-Instruct-Turbo', 'deepseek-ai/deepseek-llm-67b-chat']
        elif current_provider == 'google':
            models = ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-1.5-flash']
        elif current_provider == 'openrouter':
            models = ['google/gemma-2-9b-it:free', 'mistralai/mistral-7b-instruct:free', 'meta-llama/llama-3.2-3b-instruct:free']
        else:
            models = [default_model]
        
        selected_model = st.selectbox(
            "Select Model",
            options=models,
            index=0,
            key="model_select"
        )
        
        st.session_state['selected_model'] = selected_model
        
        # Test connection
        st.markdown("---")
        st.markdown("#### Test Connection")
        
        if st.button("🔌 Test API Connection", type="primary"):
            with st.spinner("Testing connection..."):
                if current_provider == 'mock':
                    st.success("✓ Mock provider is working correctly!")
                elif not st.session_state.get('api_key_input'):
                    st.error("Please enter an API key first.")
                else:
                    # Simulate test
                    import time
                    time.sleep(1)
                    st.success(f"✓ Successfully connected to {selected_info.get('name', 'provider')}!")
    
    def _render_appearance_settings(self):
        """Render appearance settings."""
        t = get_current_theme()
        
        st.markdown("### 🎨 Appearance Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Theme")
            
            theme_mode = st.radio(
                "Color Mode",
                options=['dark', 'light'],
                format_func=lambda x: '🌙 Dark Mode' if x == 'dark' else '☀️ Light Mode',
                index=0 if st.session_state.get('theme_mode', 'dark') == 'dark' else 1,
                key="theme_radio"
            )
            
            if theme_mode != st.session_state.get('theme_mode'):
                st.session_state.theme_mode = theme_mode
                st.info("Theme change will take effect on page reload.")
            
            st.markdown("#### Display Options")
            
            compact_mode = st.checkbox(
                "Compact Mode",
                value=st.session_state.get('compact_mode', False),
                help="Reduce spacing for more content on screen"
            )
            st.session_state.compact_mode = compact_mode
            
            show_tooltips = st.checkbox(
                "Show Tooltips",
                value=st.session_state.get('show_tooltips', True),
                help="Display helpful tooltips throughout the app"
            )
            st.session_state.show_tooltips = show_tooltips
        
        with col2:
            st.markdown("#### Language")
            
            language = st.selectbox(
                "Interface Language",
                options=['id', 'en'],
                format_func=lambda x: '🇮🇩 Bahasa Indonesia' if x == 'id' else '🇬🇧 English',
                index=0 if st.session_state.get('language', 'id') == 'id' else 1,
                key="language_select"
            )
            st.session_state.language = language
            
            st.markdown("#### Sidebar")
            
            sidebar_collapsed = st.checkbox(
                "Collapse Sidebar by Default",
                value=st.session_state.get('sidebar_collapsed', False)
            )
            st.session_state.sidebar_collapsed = sidebar_collapsed
        
        st.markdown("---")
        
        # Preview
        st.markdown("#### Theme Preview")
        
        preview_theme = t
        st.markdown(f'''
        <div class="pro-card" style="padding:1.5rem;">
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;">
                <div style="text-align:center;">
                    <div style="width:50px;height:50px;background:{preview_theme['primary']};border-radius:8px;margin:0 auto 0.5rem;"></div>
                    <div style="font-size:0.75rem;color:{preview_theme['text_muted']} !important;">Primary</div>
                </div>
                <div style="text-align:center;">
                    <div style="width:50px;height:50px;background:{preview_theme['success']};border-radius:8px;margin:0 auto 0.5rem;"></div>
                    <div style="font-size:0.75rem;color:{preview_theme['text_muted']} !important;">Success</div>
                </div>
                <div style="text-align:center;">
                    <div style="width:50px;height:50px;background:{preview_theme['warning']};border-radius:8px;margin:0 auto 0.5rem;"></div>
                    <div style="font-size:0.75rem;color:{preview_theme['text_muted']} !important;">Warning</div>
                </div>
                <div style="text-align:center;">
                    <div style="width:50px;height:50px;background:{preview_theme['danger']};border-radius:8px;margin:0 auto 0.5rem;"></div>
                    <div style="font-size:0.75rem;color:{preview_theme['text_muted']} !important;">Danger</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    def _render_general_settings(self):
        """Render general settings."""
        t = get_current_theme()
        
        st.markdown("### ⚙️ General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Auto-Save")
            
            auto_save = st.checkbox(
                "Enable Auto-Save",
                value=st.session_state.get('auto_save', True),
                help="Automatically save work in progress"
            )
            st.session_state.auto_save = auto_save
            
            if auto_save:
                auto_save_interval = st.slider(
                    "Auto-save interval (minutes)",
                    min_value=1,
                    max_value=30,
                    value=5,
                    key="auto_save_interval"
                )
            
            st.markdown("#### Notifications")
            
            notifications = st.checkbox(
                "Enable Notifications",
                value=st.session_state.get('notifications_enabled', True),
                help="Show system notifications and alerts"
            )
            st.session_state.notifications_enabled = notifications
        
        with col2:
            st.markdown("#### Session")
            
            st.markdown(f'''
            <div class="pro-card" style="padding:1rem;">
                <div class="list-item">
                    <span style="color:{t['text_muted']} !important;">Session Started</span>
                    <span style="color:{t['text']} !important;">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
                </div>
                <div class="list-item">
                    <span style="color:{t['text_muted']} !important;">Provider</span>
                    <span style="color:{t['text']} !important;">{st.session_state.get('llm_provider', 'mock').title()}</span>
                </div>
                <div class="list-item">
                    <span style="color:{t['text_muted']} !important;">Version</span>
                    <span style="color:{t['text']} !important;">{APP_VERSION}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🔄 Reset All Settings", use_container_width=True):
                for key in ['llm_provider', 'api_key_input', 'theme_mode', 'language', 
                           'auto_save', 'show_tooltips', 'compact_mode']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✓ Settings reset to defaults")
                st.rerun()
        
        st.markdown("---")
        
        # Keyboard shortcuts
        st.markdown("#### Keyboard Shortcuts")
        
        shortcuts = [
            ("Ctrl + S", "Save current work"),
            ("Ctrl + /", "Toggle sidebar"),
            ("Ctrl + K", "Quick search"),
            ("Ctrl + N", "New item"),
            ("Esc", "Close dialog")
        ]
        
        cols = st.columns(2)
        for i, (key, desc) in enumerate(shortcuts):
            with cols[i % 2]:
                st.markdown(f'''
                <div style="display:flex;align-items:center;gap:1rem;padding:0.5rem 0;">
                    <code style="background:{t['bg_secondary']};padding:0.25rem 0.5rem;border-radius:4px;color:{t['text']} !important;">{key}</code>
                    <span style="color:{t['text_secondary']} !important;">{desc}</span>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_data_settings(self):
        """Render data and export settings."""
        t = get_current_theme()
        
        st.markdown("### 📊 Data & Export Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Format")
            
            export_format = st.selectbox(
                "Default Export Format",
                options=['xlsx', 'csv', 'pdf', 'json'],
                format_func=lambda x: {'xlsx': '📊 Excel (.xlsx)', 'csv': '📋 CSV', 'pdf': '📄 PDF', 'json': '🔧 JSON'}[x],
                key="export_format_select"
            )
            st.session_state.export_format = export_format
            
            st.markdown("#### Data Retention")
            
            retention_days = st.slider(
                "Keep session data for (days)",
                min_value=1,
                max_value=90,
                value=30,
                key="retention_days"
            )
        
        with col2:
            st.markdown("#### Current Session Data")
            
            # Count session data
            data_counts = {
                'Documents': len(st.session_state.get('documents', [])),
                'Findings': len(st.session_state.get('findings', [])),
                'Risk Assessments': len(st.session_state.get('risk_assessments', [])),
                'Chat Messages': len(st.session_state.get('chat_messages', [])),
                'Fraud Cases': len(st.session_state.get('fraud_cases', []))
            }
            
            for name, count in data_counts.items():
                st.markdown(f'''
                <div class="pro-card" style="padding:0.5rem 1rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text_secondary']} !important;">{name}</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{count}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export/Import section
        st.markdown("#### Backup & Restore")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Export All Data", use_container_width=True):
                import json
                
                export_data = {
                    'version': APP_VERSION,
                    'exported_at': datetime.now().isoformat(),
                    'documents': st.session_state.get('documents', []),
                    'findings': st.session_state.get('findings', []),
                    'risk_assessments': st.session_state.get('risk_assessments', []),
                    'fraud_cases': st.session_state.get('fraud_cases', []),
                    'settings': {
                        'llm_provider': st.session_state.get('llm_provider', 'mock'),
                        'theme_mode': st.session_state.get('theme_mode', 'dark'),
                        'language': st.session_state.get('language', 'id')
                    }
                }
                
                st.download_button(
                    "💾 Download Backup",
                    json.dumps(export_data, indent=2, default=str),
                    file_name=f"aurix_backup_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col2:
            uploaded_backup = st.file_uploader(
                "Import Backup",
                type=['json'],
                key="backup_upload",
                label_visibility="collapsed"
            )
            
            if uploaded_backup:
                if st.button("📥 Restore Data", use_container_width=True):
                    import json
                    try:
                        backup_data = json.load(uploaded_backup)
                        # Restore data
                        for key in ['documents', 'findings', 'risk_assessments', 'fraud_cases']:
                            if key in backup_data:
                                st.session_state[key] = backup_data[key]
                        st.success("✓ Data restored successfully!")
                    except Exception as e:
                        st.error(f"Error restoring backup: {str(e)}")
        
        with col3:
            if st.button("🗑️ Clear All Data", use_container_width=True):
                if st.session_state.get('confirm_clear'):
                    for key in ['documents', 'findings', 'risk_assessments', 'chat_messages', 
                               'fraud_cases', 'ca_alerts', 'ptcf_prompts']:
                        if key in st.session_state:
                            st.session_state[key] = []
                    st.session_state.confirm_clear = False
                    st.success("✓ All data cleared")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm clearing all data")


def render():
    """Entry point for the Settings page."""
    page = SettingsPage()
    page.render()
