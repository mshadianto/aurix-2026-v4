"""
Audit Copilot Module for AURIX.
Proactive AI assistant with real-time suggestions and smart automation.
"""

import streamlit as st
from datetime import datetime, timedelta
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the Audit Copilot page."""
    t = get_current_theme()
    
    render_page_header(
        "Audit Copilot",
        "🤖",
        "Your intelligent AI partner for smarter auditing"
    )
    
    # Initialize copilot state
    if 'copilot_mode' not in st.session_state:
        st.session_state.copilot_mode = 'assistant'
    if 'copilot_messages' not in st.session_state:
        st.session_state.copilot_messages = []
    
    # Stunning hero section
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);border-radius:24px;padding:2.5rem;margin-bottom:2rem;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-100px;right:-100px;width:300px;height:300px;background:rgba(255,255,255,0.1);border-radius:50%;"></div>
        <div style="position:absolute;bottom:-50px;left:-50px;width:200px;height:200px;background:rgba(255,255,255,0.05);border-radius:50%;"></div>
        <div style="position:absolute;top:50%;right:10%;transform:translateY(-50%);font-size:8rem;opacity:0.2;">🤖</div>
        
        <div style="position:relative;z-index:1;">
            <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;">
                <div style="width:60px;height:60px;background:rgba(255,255,255,0.2);border-radius:16px;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(10px);">
                    <span style="font-size:2rem;">🧠</span>
                </div>
                <div>
                    <div style="color:white;font-size:1.75rem;font-weight:800;">AURIX Copilot</div>
                    <div style="color:rgba(255,255,255,0.8);font-size:0.9rem;">Powered by Advanced AI • Always Learning</div>
                </div>
            </div>
            
            <div style="display:flex;gap:1rem;margin-top:1.5rem;">
                <div style="background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);padding:1rem 1.5rem;border-radius:12px;flex:1;text-align:center;">
                    <div style="color:white;font-size:1.5rem;font-weight:700;">1,247</div>
                    <div style="color:rgba(255,255,255,0.7);font-size:0.75rem;">Suggestions Given</div>
                </div>
                <div style="background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);padding:1rem 1.5rem;border-radius:12px;flex:1;text-align:center;">
                    <div style="color:white;font-size:1.5rem;font-weight:700;">89%</div>
                    <div style="color:rgba(255,255,255,0.7);font-size:0.75rem;">Accuracy Rate</div>
                </div>
                <div style="background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);padding:1rem 1.5rem;border-radius:12px;flex:1;text-align:center;">
                    <div style="color:white;font-size:1.5rem;font-weight:700;">42h</div>
                    <div style="color:rgba(255,255,255,0.7);font-size:0.75rem;">Time Saved</div>
                </div>
                <div style="background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);padding:1rem 1.5rem;border-radius:12px;flex:1;text-align:center;">
                    <div style="color:white;font-size:1.5rem;font-weight:700;">24/7</div>
                    <div style="color:rgba(255,255,255,0.7);font-size:0.75rem;">Always Available</div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Mode selector
    col1, col2, col3, col4 = st.columns(4)
    
    modes = [
        ("assistant", "💬", "Chat Assistant", "Ask anything"),
        ("proactive", "🔮", "Proactive Mode", "AI suggestions"),
        ("automation", "⚡", "Smart Automation", "Auto-complete tasks"),
        ("learning", "📚", "Learning Mode", "Teach Copilot"),
    ]
    
    for col, (mode_id, icon, name, desc) in zip([col1, col2, col3, col4], modes):
        with col:
            is_active = st.session_state.copilot_mode == mode_id
            if st.button(
                f"{icon} {name}",
                key=f"mode_{mode_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.copilot_mode = mode_id
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render based on mode
    if st.session_state.copilot_mode == 'assistant':
        _render_chat_assistant(t)
    elif st.session_state.copilot_mode == 'proactive':
        _render_proactive_mode(t)
    elif st.session_state.copilot_mode == 'automation':
        _render_automation_mode(t)
    else:
        _render_learning_mode(t)
    
    render_footer()


def _render_chat_assistant(t: dict):
    """Render chat assistant mode."""
    
    # Quick action buttons
    st.markdown("#### ⚡ Quick Actions")
    
    quick_actions = [
        ("📋 Generate Audit Program", "audit_program"),
        ("🔍 Analyze Risk", "risk_analysis"),
        ("📝 Draft Finding", "draft_finding"),
        ("📊 Create Report", "create_report"),
        ("🔗 Check Regulation", "check_regulation"),
        ("💡 Get Recommendation", "recommendation"),
    ]
    
    cols = st.columns(6)
    for col, (label, action) in zip(cols, quick_actions):
        with col:
            if st.button(label, key=f"qa_{action}", use_container_width=True):
                st.session_state.copilot_messages.append({
                    "role": "user",
                    "content": f"Help me {label.split(' ', 1)[1].lower()}"
                })
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:20px;padding:1.5rem;min-height:400px;max-height:500px;overflow-y:auto;">
        ''', unsafe_allow_html=True)
        
        # Welcome message if empty
        if not st.session_state.copilot_messages:
            st.markdown(f'''
            <div style="text-align:center;padding:3rem;">
                <div style="font-size:4rem;margin-bottom:1rem;">🤖</div>
                <div style="font-size:1.25rem;font-weight:600;color:{t['text']};margin-bottom:0.5rem;">
                    Hi! I'm your Audit Copilot
                </div>
                <div style="color:{t['text_secondary']};max-width:400px;margin:0 auto;">
                    I can help you with audit procedures, risk assessment, finding documentation, 
                    regulatory compliance, and much more. Just ask!
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            # Display messages
            for msg in st.session_state.copilot_messages[-10:]:
                if msg['role'] == 'user':
                    st.markdown(f'''
                    <div style="display:flex;justify-content:flex-end;margin-bottom:1rem;">
                        <div style="background:linear-gradient(135deg, {t['primary']}, {t['accent']});color:white;padding:1rem 1.25rem;border-radius:20px 20px 4px 20px;max-width:70%;">
                            {msg['content']}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div style="display:flex;gap:0.75rem;margin-bottom:1rem;">
                        <div style="width:36px;height:36px;background:linear-gradient(135deg, #667eea, #764ba2);border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                            <span style="font-size:1.25rem;">🤖</span>
                        </div>
                        <div style="background:{t['bg_secondary']};padding:1rem 1.25rem;border-radius:4px 20px 20px 20px;max-width:70%;">
                            <div style="color:{t['text']};">{msg['content']}</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Message Copilot",
            placeholder="Ask me anything about auditing...",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("🚀 Send", type="primary", use_container_width=True):
            if user_input:
                st.session_state.copilot_messages.append({"role": "user", "content": user_input})
                
                # Simulated AI response
                responses = [
                    "I'll help you with that! Based on my analysis, here are my recommendations:\n\n1. Start with a risk-based approach\n2. Focus on key controls\n3. Document all exceptions\n\nWould you like me to elaborate on any of these?",
                    "Great question! Let me analyze this for you...\n\nBased on regulatory requirements and best practices, I recommend:\n\n• Review the control design first\n• Test operating effectiveness\n• Consider automated monitoring\n\nShall I generate detailed procedures?",
                    "I've reviewed the relevant standards and here's my analysis:\n\n**Key Points:**\n- POJK requirements are met\n- IIA Standards 2300 applicable\n- Sample size of 25 recommended\n\nDo you want me to create an audit program?",
                ]
                
                st.session_state.copilot_messages.append({
                    "role": "assistant",
                    "content": random.choice(responses)
                })
                st.rerun()


def _render_proactive_mode(t: dict):
    """Render proactive suggestions mode."""
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:2rem;">
        <div style="display:flex;align-items:center;gap:1rem;">
            <div style="width:50px;height:50px;background:linear-gradient(135deg, #f093fb, #f5576c);border-radius:12px;display:flex;align-items:center;justify-content:center;">
                <span style="font-size:1.5rem;">🔮</span>
            </div>
            <div>
                <div style="font-weight:700;color:{t['text']};">Proactive Intelligence Active</div>
                <div style="color:{t['text_secondary']};font-size:0.9rem;">Copilot is analyzing your work and generating real-time suggestions</div>
            </div>
            <div style="margin-left:auto;display:flex;align-items:center;gap:0.5rem;">
                <div style="width:10px;height:10px;background:#22c55e;border-radius:50%;animation:pulse 2s infinite;"></div>
                <span style="color:{t['success']};font-size:0.85rem;font-weight:600;">Monitoring</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Proactive suggestions
    suggestions = [
        {
            "type": "warning",
            "icon": "⚠️",
            "title": "Potential Issue Detected",
            "message": "I noticed the Credit Risk audit hasn't tested segregation of duties. This is a critical control area per POJK 40/2019.",
            "action": "Add SoD Test",
            "confidence": 94,
            "color": t['warning']
        },
        {
            "type": "recommendation",
            "icon": "💡",
            "title": "Efficiency Opportunity",
            "message": "Based on similar audits, you can reduce testing time by 30% using data analytics for transaction sampling.",
            "action": "Apply Analytics",
            "confidence": 87,
            "color": t['primary']
        },
        {
            "type": "insight",
            "icon": "🔍",
            "title": "Pattern Recognized",
            "message": "I found 3 similar findings from past audits. Consider reviewing historical remediation approaches.",
            "action": "View History",
            "confidence": 91,
            "color": t['accent']
        },
        {
            "type": "regulatory",
            "icon": "📜",
            "title": "Regulatory Update",
            "message": "New OJK circular SE-15/2024 affects your current audit scope. Review recommended.",
            "action": "Review Update",
            "confidence": 98,
            "color": t['danger']
        },
        {
            "type": "quality",
            "icon": "✨",
            "title": "Quality Enhancement",
            "message": "Your finding documentation can be improved. Missing: Root cause analysis and risk quantification.",
            "action": "Enhance Finding",
            "confidence": 85,
            "color": t['success']
        },
    ]
    
    for s in suggestions:
        st.markdown(f'''
        <div style="background:{t['card']};border-left:4px solid {s['color']};border-radius:0 16px 16px 0;padding:1.25rem;margin-bottom:1rem;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;right:0;background:{s['color']}15;padding:0.5rem 1rem;border-radius:0 16px 0 16px;font-size:0.7rem;color:{s['color']};font-weight:600;">
                {s['confidence']}% confidence
            </div>
            
            <div style="display:flex;gap:1rem;align-items:start;">
                <div style="font-size:2rem;">{s['icon']}</div>
                <div style="flex:1;">
                    <div style="font-weight:700;color:{t['text']};margin-bottom:0.25rem;">{s['title']}</div>
                    <div style="color:{t['text_secondary']};font-size:0.9rem;margin-bottom:1rem;">{s['message']}</div>
                    <div style="display:flex;gap:0.5rem;">
                        <button style="background:{s['color']};color:white;border:none;padding:0.5rem 1rem;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem;">
                            {s['action']}
                        </button>
                        <button style="background:transparent;color:{t['text_muted']};border:1px solid {t['border']};padding:0.5rem 1rem;border-radius:8px;cursor:pointer;font-size:0.85rem;">
                            Dismiss
                        </button>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_automation_mode(t: dict):
    """Render smart automation mode."""
    
    st.markdown("#### ⚡ Smart Automation Center")
    
    # Automation cards
    automations = [
        {
            "name": "Auto-Generate Workpapers",
            "desc": "Automatically create workpapers from audit program",
            "status": "active",
            "runs": 45,
            "icon": "📝"
        },
        {
            "name": "Smart Document Filing",
            "desc": "AI categorizes and files documents automatically",
            "status": "active",
            "runs": 234,
            "icon": "📁"
        },
        {
            "name": "Finding Draft Generator",
            "desc": "Generate finding drafts from test results",
            "status": "paused",
            "runs": 28,
            "icon": "📋"
        },
        {
            "name": "Risk Score Calculator",
            "desc": "Auto-calculate risk scores based on criteria",
            "status": "active",
            "runs": 156,
            "icon": "🎯"
        },
        {
            "name": "Compliance Checker",
            "desc": "Check documents against regulatory requirements",
            "status": "active",
            "runs": 89,
            "icon": "✅"
        },
        {
            "name": "Report Compiler",
            "desc": "Compile findings into formatted reports",
            "status": "paused",
            "runs": 12,
            "icon": "📊"
        },
    ]
    
    cols = st.columns(3)
    
    for i, auto in enumerate(automations):
        with cols[i % 3]:
            status_color = t['success'] if auto['status'] == 'active' else t['text_muted']
            
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:1rem;position:relative;">
                <div style="position:absolute;top:1rem;right:1rem;">
                    <div style="width:10px;height:10px;background:{status_color};border-radius:50%;"></div>
                </div>
                
                <div style="font-size:2.5rem;margin-bottom:1rem;">{auto['icon']}</div>
                <div style="font-weight:700;color:{t['text']};margin-bottom:0.25rem;">{auto['name']}</div>
                <div style="color:{t['text_secondary']};font-size:0.85rem;margin-bottom:1rem;min-height:40px;">{auto['desc']}</div>
                
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:0.75rem;color:{t['text_muted']};">🔄 {auto['runs']} runs</span>
                    <span style="color:{status_color};font-size:0.75rem;font-weight:600;text-transform:uppercase;">{auto['status']}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.button(
                "Configure" if auto['status'] == 'active' else "Activate",
                key=f"auto_{i}",
                use_container_width=True
            )
    
    # Create new automation
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ➕ Create Custom Automation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Automation Name", placeholder="My custom automation...")
        st.selectbox("Trigger", ["On document upload", "Daily schedule", "Manual trigger", "On finding creation"])
    
    with col2:
        st.selectbox("Action", ["Generate workpaper", "Send notification", "Run analysis", "Create report"])
        st.selectbox("Output", ["Save to Documents", "Email notification", "Dashboard alert"])
    
    st.button("🚀 Create Automation", type="primary")


def _render_learning_mode(t: dict):
    """Render learning mode."""
    
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, #11998e, #38ef7d);border-radius:16px;padding:2rem;margin-bottom:2rem;color:white;">
        <div style="display:flex;align-items:center;gap:1rem;">
            <div style="font-size:3rem;">📚</div>
            <div>
                <div style="font-weight:700;font-size:1.25rem;">Teach Your Copilot</div>
                <div style="opacity:0.9;">Help Copilot learn your preferences and audit methodology</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Learning categories
    st.markdown("#### 🎓 Training Categories")
    
    categories = [
        {"name": "Audit Methodology", "progress": 75, "lessons": 12, "icon": "📋"},
        {"name": "Risk Assessment", "progress": 60, "lessons": 8, "icon": "🎯"},
        {"name": "Finding Writing", "progress": 90, "lessons": 15, "icon": "📝"},
        {"name": "Regulatory Knowledge", "progress": 45, "lessons": 20, "icon": "📜"},
    ]
    
    cols = st.columns(4)
    
    for col, cat in zip(cols, categories):
        with col:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.25rem;text-align:center;">
                <div style="font-size:2.5rem;margin-bottom:0.75rem;">{cat['icon']}</div>
                <div style="font-weight:600;color:{t['text']};margin-bottom:0.5rem;">{cat['name']}</div>
                <div style="height:8px;background:{t['border']};border-radius:4px;margin-bottom:0.5rem;overflow:hidden;">
                    <div style="width:{cat['progress']}%;height:100%;background:linear-gradient(90deg, #11998e, #38ef7d);"></div>
                </div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{cat['progress']}% • {cat['lessons']} lessons</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Teach copilot
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💡 Teach Something New")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        teach_topic = st.selectbox(
            "What would you like to teach?",
            ["Custom audit procedure", "Finding template", "Risk criteria", "Sampling approach", "Report format"]
        )
        
        teach_content = st.text_area(
            "Share your knowledge",
            height=150,
            placeholder="Describe your methodology, template, or approach in detail..."
        )
        
        if st.button("🎓 Teach Copilot", type="primary"):
            st.success("✅ Thank you! Copilot has learned something new!")
    
    with col2:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.25rem;">
            <div style="font-weight:600;color:{t['text']};margin-bottom:1rem;">📊 Learning Stats</div>
            
            <div style="margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:0.25rem;">
                    <span style="color:{t['text_muted']};">Lessons Completed</span>
                    <span style="color:{t['text']};font-weight:600;">55</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:0.25rem;">
                    <span style="color:{t['text_muted']};">Custom Rules</span>
                    <span style="color:{t['text']};font-weight:600;">23</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:0.25rem;">
                    <span style="color:{t['text_muted']};">Templates Learned</span>
                    <span style="color:{t['text']};font-weight:600;">18</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                    <span style="color:{t['text_muted']};">Accuracy Boost</span>
                    <span style="color:{t['success']};font-weight:600;">+12%</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
