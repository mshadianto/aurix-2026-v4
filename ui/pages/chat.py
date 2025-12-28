"""
Chat Page Module for AURIX.
LLM-powered conversational interface for audit assistance.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
import uuid

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from data.seeds import SYSTEM_PROMPTS, AUDIT_UNIVERSE, REGULATIONS
from app.constants import LLM_PROVIDER_INFO, AUDIT_PERSONAS


class ChatPage:
    """Chat interface for LLM-powered audit assistance."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for chat."""
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        
        if 'chat_persona' not in st.session_state:
            st.session_state.chat_persona = 'default'
        
        if 'chat_context' not in st.session_state:
            st.session_state.chat_context = []
    
    def render(self):
        """Render the Chat page."""
        render_page_header("AI Chat Assistant", "Intelligent audit guidance powered by AI")
        
        t = get_current_theme()
        
        # Sidebar configuration
        with st.sidebar:
            self._render_chat_config()
        
        # Main chat interface
        self._render_chat_interface()
        
        render_footer()
    
    def _render_chat_config(self):
        """Render chat configuration in sidebar."""
        t = get_current_theme()
        
        st.markdown("### 🤖 AI Configuration")
        
        # Provider selection
        provider = st.session_state.get('llm_provider', 'mock')
        
        st.markdown(f'''
        <div style="padding:0.5rem;background:{t['bg_secondary']};border-radius:8px;margin-bottom:1rem;">
            <div style="font-size:0.8rem;color:{t['text_muted']} !important;">Current Provider</div>
            <div style="font-weight:600;color:{t['text']} !important;">{LLM_PROVIDER_INFO.get(provider, {}).get('name', 'Mock')}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Persona selection
        st.markdown("#### Persona")
        persona = st.selectbox(
            "Select AI Persona",
            options=list(SYSTEM_PROMPTS.keys()),
            format_func=lambda x: x.replace('_', ' ').title(),
            key="persona_select",
            label_visibility="collapsed"
        )
        st.session_state.chat_persona = persona
        
        # Show persona description
        st.markdown(f'''
        <div style="font-size:0.75rem;color:{t['text_secondary']} !important;padding:0.5rem;background:{t['bg_secondary']};border-radius:4px;max-height:100px;overflow-y:auto;">
            {SYSTEM_PROMPTS.get(persona, '')[:200]}...
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick context
        st.markdown("#### Quick Context")
        
        audit_area = st.selectbox(
            "Focus Area",
            options=["None"] + [area for areas in AUDIT_UNIVERSE.values() for area in areas],
            key="chat_audit_area"
        )
        
        if audit_area != "None":
            if audit_area not in st.session_state.chat_context:
                st.session_state.chat_context.append(f"Focus: {audit_area}")
        
        # Regulation context
        reg_category = st.selectbox(
            "Regulation Category",
            options=["None"] + list(REGULATIONS.keys()),
            key="chat_reg_category"
        )
        
        st.markdown("---")
        
        # Chat controls
        st.markdown("#### Chat Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_messages = []
                st.rerun()
        
        with col2:
            if st.button("💾 Export", use_container_width=True):
                self._export_chat()
        
        # Quick prompts
        st.markdown("#### Quick Prompts")
        
        quick_prompts = [
            "Identify top 5 risks for credit portfolio",
            "Generate audit procedures for KYC",
            "Explain POJK requirements for risk management",
            "Best practices for IT General Controls",
            "AML red flags checklist"
        ]
        
        for prompt in quick_prompts:
            if st.button(f"💡 {prompt[:30]}...", key=f"quick_{prompt[:10]}", use_container_width=True):
                self._send_message(prompt)
                st.rerun()
    
    def _render_chat_interface(self):
        """Render the main chat interface."""
        t = get_current_theme()
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Welcome message if no messages
            if not st.session_state.chat_messages:
                st.markdown(f'''
                <div style="text-align:center;padding:3rem 1rem;">
                    <div style="font-size:4rem;margin-bottom:1rem;">🤖</div>
                    <h2 style="color:{t['text']} !important;margin-bottom:0.5rem;">AURIX AI Assistant</h2>
                    <p style="color:{t['text_secondary']} !important;max-width:500px;margin:0 auto;">
                        Your intelligent audit companion. Ask questions about risk assessment, 
                        audit procedures, regulations, or any audit-related topics.
                    </p>
                </div>
                ''', unsafe_allow_html=True)
                
                # Suggestion cards
                st.markdown("### 💡 Suggested Questions")
                
                suggestions = [
                    ("🎯", "Risk Assessment", "Help me identify key risks in credit operations"),
                    ("📋", "Audit Procedures", "Generate testing procedures for treasury management"),
                    ("📚", "Regulations", "Explain POJK 55/2016 governance requirements"),
                    ("🔍", "Fraud Detection", "What are common fraud red flags in banking?")
                ]
                
                cols = st.columns(2)
                for i, (icon, title, prompt) in enumerate(suggestions):
                    with cols[i % 2]:
                        if st.button(
                            f"{icon} **{title}**\n\n{prompt[:40]}...",
                            key=f"suggest_{i}",
                            use_container_width=True
                        ):
                            self._send_message(prompt)
                            st.rerun()
            
            else:
                # Display messages
                for msg in st.session_state.chat_messages:
                    self._render_message(msg)
        
        # Input area at bottom
        st.markdown("---")
        
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "Message",
                placeholder="Ask anything about audit, risk, compliance...",
                key="chat_input",
                label_visibility="collapsed"
            )
        
        with col2:
            send_clicked = st.button("📤 Send", type="primary", use_container_width=True)
        
        if send_clicked and user_input:
            self._send_message(user_input)
            st.rerun()
    
    def _render_message(self, msg: Dict):
        """Render a single chat message."""
        t = get_current_theme()
        
        is_user = msg['role'] == 'user'
        
        if is_user:
            st.markdown(f'''
            <div style="display:flex;justify-content:flex-end;margin-bottom:1rem;">
                <div style="max-width:80%;background:{t['primary']};color:white;padding:1rem;border-radius:12px 12px 4px 12px;">
                    <div style="white-space:pre-wrap;">{msg['content']}</div>
                    <div style="font-size:0.7rem;opacity:0.7;text-align:right;margin-top:0.5rem;">
                        {msg['timestamp']}
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div style="display:flex;justify-content:flex-start;margin-bottom:1rem;">
                <div style="max-width:80%;background:{t['card']};border:1px solid {t['border']};padding:1rem;border-radius:12px 12px 12px 4px;">
                    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                        <span style="font-size:1.25rem;">🤖</span>
                        <span style="font-size:0.8rem;color:{t['primary']} !important;">AURIX AI</span>
                    </div>
                    <div style="color:{t['text']} !important;white-space:pre-wrap;">{msg['content']}</div>
                    <div style="font-size:0.7rem;color:{t['text_muted']} !important;margin-top:0.5rem;">
                        {msg['timestamp']} • {msg.get('provider', 'mock')}
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    def _send_message(self, content: str):
        """Send a message and get AI response."""
        # Add user message
        user_msg = {
            'role': 'user',
            'content': content,
            'timestamp': datetime.now().strftime('%H:%M')
        }
        st.session_state.chat_messages.append(user_msg)
        
        # Generate AI response
        response = self._generate_response(content)
        
        ai_msg = {
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().strftime('%H:%M'),
            'provider': st.session_state.get('llm_provider', 'mock')
        }
        st.session_state.chat_messages.append(ai_msg)
    
    def _generate_response(self, query: str) -> str:
        """Generate AI response (mock for demo)."""
        query_lower = query.lower()
        
        # Context-aware responses
        if 'risk' in query_lower:
            return """## Risk Assessment Analysis

Based on your query, here are the key considerations:

### Top Risk Areas to Consider

1. **Credit Risk**
   - NPL ratio trends and management
   - Collateral valuation accuracy
   - Credit concentration limits

2. **Operational Risk**
   - Process control gaps
   - System reliability
   - Staff competency

3. **Compliance Risk**
   - Regulatory reporting timeliness
   - Policy adherence
   - Documentation completeness

### Recommended Actions

| Priority | Action | Timeline |
|----------|--------|----------|
| HIGH | Review credit monitoring process | Immediate |
| MEDIUM | Update risk assessment matrix | 2 weeks |
| LOW | Enhance staff training | 1 month |

💡 *Tip: Use the Risk Assessment module for detailed analysis.*"""

        elif 'procedure' in query_lower or 'audit' in query_lower:
            return """## Audit Procedures

Here are recommended audit procedures for your focus area:

### Test Plan

| Step | Procedure | Nature | Sample |
|------|-----------|--------|--------|
| 1 | Review policy documentation | Document Review | All |
| 2 | Walkthrough key processes | Inquiry/Observation | N/A |
| 3 | Test sample transactions | Testing | 25 items |
| 4 | Verify control effectiveness | Reperformance | 10 items |
| 5 | Review exception reports | Analytical | 3 months |

### Key Control Points

- ✅ Authorization limits
- ✅ Segregation of duties
- ✅ System access controls
- ✅ Reconciliation procedures
- ✅ Management oversight

💡 *Use PTCF Builder to customize these procedures.*"""

        elif 'pojk' in query_lower or 'regulation' in query_lower or 'compliance' in query_lower:
            return """## Regulatory Compliance Overview

### Key Regulations (OJK)

**POJK 55/2016 - Corporate Governance**
- Board structure requirements
- Committee composition
- Risk management framework
- Internal audit function

**POJK 18/2016 - Risk Management**
- Risk appetite framework
- Three lines of defense
- Risk reporting requirements
- Stress testing provisions

**POJK 40/2019 - Asset Quality**
- Credit classification criteria
- Provisioning requirements
- Restructuring guidelines
- Write-off procedures

### Compliance Checklist

| Regulation | Status | Gap | Priority |
|------------|--------|-----|----------|
| POJK 55/2016 | Partial | Governance docs | HIGH |
| POJK 18/2016 | Compliant | - | - |
| POJK 40/2019 | Partial | NPL reporting | MEDIUM |

💡 *Visit Regulatory Compliance module for detailed tracking.*"""

        elif 'fraud' in query_lower:
            return """## Fraud Detection Guidance

### Common Fraud Red Flags

**Financial Statement Fraud**
- 🚩 Unusual year-end transactions
- 🚩 Aggressive revenue recognition
- 🚩 Management override of controls
- 🚩 Significant related party transactions

**Asset Misappropriation**
- 🚩 Missing inventory or assets
- 🚩 Duplicate vendor payments
- 🚩 Fictitious vendors
- 🚩 Unauthorized cash withdrawals

**AML Red Flags**
- 🚩 Structuring transactions
- 🚩 Unusual wire patterns
- 🚩 Cash-intensive businesses
- 🚩 Complex ownership structures

### Investigation Steps

1. Document the initial indicator
2. Preserve relevant evidence
3. Expand scope of review
4. Interview relevant parties
5. Assess financial impact
6. Report findings appropriately

💡 *Use Fraud Detection module for systematic analysis.*"""

        else:
            return f"""## AURIX AI Response

Thank you for your question about: *{query[:100]}*

I'm here to help with:

- **Risk Assessment** - Identify and evaluate audit risks
- **Audit Procedures** - Generate testing methodologies
- **Regulatory Compliance** - Indonesian banking regulations
- **Fraud Detection** - Red flag identification
- **Best Practices** - Big 4 & McKinsey methodologies

### How Can I Help?

Please provide more context about:
1. The specific audit area you're focusing on
2. The type of institution (bank, insurance, etc.)
3. Any particular regulations or standards to consider

I'll provide tailored guidance based on professional audit methodologies and Indonesian regulatory requirements.

💡 *Try asking about specific topics like "credit risk audit procedures" or "POJK compliance requirements".*"""
    
    def _export_chat(self):
        """Export chat history."""
        if not st.session_state.chat_messages:
            st.warning("No messages to export.")
            return
        
        export_text = f"AURIX Chat Export\n"
        export_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        export_text += "=" * 50 + "\n\n"
        
        for msg in st.session_state.chat_messages:
            role = "User" if msg['role'] == 'user' else "AURIX AI"
            export_text += f"[{msg['timestamp']}] {role}:\n"
            export_text += msg['content'] + "\n\n"
        
        st.download_button(
            "📥 Download Chat",
            export_text,
            file_name=f"aurix_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )


def render():
    """Entry point for the Chat page."""
    page = ChatPage()
    page.render()
