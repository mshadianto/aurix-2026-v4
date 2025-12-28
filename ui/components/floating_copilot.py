"""
Floating Audit Copilot Component for AURIX 2026.
Persistent AI assistant accessible from any page via FAB.

Features:
- Floating Action Button (FAB) toggle
- Contextual suggestions based on current page
- Chat history management
- Quick action shortcuts
"""

import streamlit as st
from typing import List, Dict, Optional, Any
from datetime import datetime

from ui.styles.css_builder import get_current_theme


def init_copilot_state():
    """Initialize copilot session state."""
    if 'copilot_open' not in st.session_state:
        st.session_state.copilot_open = False
    
    if 'copilot_messages' not in st.session_state:
        st.session_state.copilot_messages = []
    
    if 'copilot_context' not in st.session_state:
        st.session_state.copilot_context = {}


def get_contextual_suggestions() -> List[Dict[str, str]]:
    """Generate context-aware suggestions based on current page."""
    current_page = st.session_state.get('current_page', 'Dashboard')
    
    base_suggestions = [
        {"label": "📊 Summarize risks", "query": "Summarize key risks"},
        {"label": "✍️ Draft finding", "query": "Help me draft a finding"},
        {"label": "📜 OJK check", "query": "Check OJK compliance"},
    ]
    
    page_suggestions = {
        "📈 KRI Dashboard": [
            {"label": "📊 NPL Analysis", "query": "Analyze NPL ratio trend"},
            {"label": "📈 LDR Status", "query": "Review LDR position"},
            {"label": "⚠️ Alert summary", "query": "Summarize KRI alerts"},
        ],
        "🔄 Process Mining": [
            {"label": "🔍 Find bottlenecks", "query": "Identify process bottlenecks"},
            {"label": "⚡ Suggest automation", "query": "Suggest automation opportunities"},
            {"label": "📊 Compare variants", "query": "Compare process variants"},
        ],
        "📜 Regulatory RAG": [
            {"label": "📜 ESG check", "query": "Check ESG taxonomy compliance"},
            {"label": "🏛️ OJK regulations", "query": "Search OJK regulations"},
            {"label": "📋 POJK summary", "query": "Summarize relevant POJK"},
        ],
        "🔍 Fraud Detection": [
            {"label": "🚨 Red flags", "query": "Check for fraud red flags"},
            {"label": "📊 Benford analysis", "query": "Run Benford's law analysis"},
            {"label": "🔗 Find patterns", "query": "Find unusual patterns"},
        ],
        "📋 Findings Tracker": [
            {"label": "✍️ Draft finding", "query": "Help draft a finding"},
            {"label": "⭐ Rate risk", "query": "Recommend risk rating"},
            {"label": "💡 Remediation", "query": "Suggest remediation steps"},
        ],
    }
    
    return page_suggestions.get(current_page, base_suggestions)


def generate_copilot_response(query: str) -> str:
    """Generate AI response for copilot query."""
    query_lower = query.lower()
    
    # Context-aware responses
    active_investigation = st.session_state.get('active_investigation')
    
    responses = {
        "npl": """📊 **NPL Analysis Summary**

Based on current data, NPL Ratio is at **5.54%** (above 5% threshold).

**Key Drivers:**
1. Corporate segment: 62% of NPL
2. SME segment: 28% of NPL
3. Retail segment: 10% of NPL

**Top Debtors Contributing to NPL:**
- PT ABC Mining - IDR 150B (restructured)
- PT XYZ Commodity - IDR 120B (watch list)
- PT DEF Trading - IDR 85B (write-off candidate)

**Recommendation:** Focus audit on corporate loan restructuring processes and credit approval for mining sector.""",

        "ojk": """📜 **OJK Compliance Check**

Based on POJK 6/2022 (ESG Taxonomy) and POJK 51/2017 (Sustainable Finance):

✅ **Compliant:**
- Mandatory sustainability disclosures
- Board-level ESG oversight
- Risk management integration

⚠️ **Needs Attention:**
- Green portfolio ratio: 12% (target: 20% by 2025)
- Climate risk stress testing: Pending completion

❌ **Non-Compliant:**
- Climate risk assessment methodology: Not documented
- TCFD-aligned reporting: In progress

**Action Required:** Escalate climate risk assessment to Risk Committee by Q1.""",

        "finding": """✍️ **Draft Finding Template**

**Finding Title:** [Control Weakness - Brief Description]

**Condition (What We Found):**
[Describe the current state/observation]

**Criteria (What Should Be):**
[Reference to policy, regulation, or best practice]
- POJK No. XX/YYYY
- Internal Policy ABC
- Industry Standard XYZ

**Cause (Root Cause Analysis):**
[Why did this happen?]

**Effect (Impact Assessment):**
- Financial Impact: [IDR XXX]
- Risk Rating: [High/Medium/Low]
- Affected Areas: [List]

**Recommendation:**
1. [Immediate action]
2. [Short-term remediation]
3. [Long-term improvement]

**Management Response:** [To be completed]

**Target Date:** [DD/MM/YYYY]

Would you like me to help fill in specific sections?""",

        "bottleneck": """🔄 **Process Bottleneck Analysis**

Based on the uploaded event log:

**Primary Bottleneck:** Risk Assessment
- Average Duration: 48 hours
- Frequency: 100 events
- Severity: HIGH

**Secondary Bottlenecks:**
1. Document Verification (24 hours avg)
2. Manager Approval (8 hours avg)

**Root Causes:**
- Manual review process for risk assessment
- Limited risk officer capacity
- Complex approval hierarchy

**Recommendations:**
1. Implement automated risk scoring for standard cases
2. Add parallel processing capability
3. Establish SLA monitoring dashboard""",

        "esg": """🌱 **ESG Portfolio Status**

**Portfolio Composition:**
- Green Assets: 12% (IDR 2.4T)
- Transition Assets: 35% (IDR 7T)
- Brown Assets: 53% (IDR 10.6T)

**OJK Taxonomy Classification:**
✅ Renewable Energy: IDR 1.8T
✅ Sustainable Transport: IDR 600B
⚠️ Palm Oil (RSPO certified): IDR 1.2T
❌ Coal Mining: IDR 3.5T

**Gap to Target:**
- Current: 12% green
- Target (2025): 20% green
- Gap: 8% (≈ IDR 1.6T needed)

**Priority Actions:**
1. Develop coal phase-out timeline
2. Increase renewable energy financing
3. Require RSPO certification for palm oil""",

        "summarize": """📋 **Key Risks Summary**

**Critical (Immediate Action Required):**
1. NPL Ratio: 5.54% (breach threshold)
   - Action: Deep-dive on corporate segment

**High Priority:**
2. LDR Ratio: 94.2% (approaching limit)
   - Action: Review deposit strategy
3. ESG Gap: 8% below target
   - Action: Accelerate green financing

**Monitoring:**
4. CAR Ratio: 16.8% (healthy)
5. Operational Risk: 3 incidents this month

**Open Findings:** 12 (4 overdue)
**Upcoming Audits:** 3 scheduled this quarter"""
    }
    
    # Find matching response
    for key, response in responses.items():
        if key in query_lower:
            return response
    
    # Default response
    return f"""I understand you're asking about: *"{query}"*

I can help you with:
• **Risk Analysis** - KRI trends and anomalies
• **Compliance** - OJK, BI, BPKH regulations
• **Findings** - Draft and review audit findings
• **Process Mining** - Identify bottlenecks

What specific area would you like to explore?"""


def render_floating_copilot():
    """Render the floating copilot chat interface."""
    init_copilot_state()
    
    t = get_current_theme()
    is_open = st.session_state.copilot_open
    
    # FAB Toggle Button
    col_spacer, col_fab = st.columns([15, 1])
    with col_fab:
        fab_label = "✕" if is_open else "🤖"
        fab_help = "Close Copilot" if is_open else "Open Audit Copilot"
        
        if st.button(fab_label, key="copilot_fab", help=fab_help):
            st.session_state.copilot_open = not is_open
            st.rerun()
    
    # Chat Panel (when open)
    if is_open:
        st.markdown("---")
        
        # Header
        st.markdown(f'''
        <div style="background:linear-gradient(135deg, #1E3A5F 0%, #2E7D32 100%);
                    color:white;padding:1rem;border-radius:12px 12px 0 0;display:flex;
                    justify-content:space-between;align-items:center;">
            <div>
                <span style="font-size:1.25rem;margin-right:0.5rem;">🤖</span>
                <strong>Audit Copilot</strong>
            </div>
            <span style="font-size:0.75rem;opacity:0.8;">● Online</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # Messages container
        messages = st.session_state.copilot_messages
        
        # Welcome message if no history
        if not messages:
            st.markdown(f'''
            <div style="background:{t['bg_secondary']};padding:1rem;border-radius:8px;margin:0.5rem 0;">
                <strong>Hello, Auditor!</strong><br><br>
                I'm your AI assistant. I can help with:
                <ul style="margin:0.5rem 0;padding-left:1.2rem;">
                    <li>Analyzing KRI anomalies</li>
                    <li>Drafting audit findings</li>
                    <li>Regulatory compliance checks</li>
                    <li>Root cause analysis</li>
                </ul>
                How can I assist you today?
            </div>
            ''', unsafe_allow_html=True)
        else:
            # Show last 5 messages
            for msg in messages[-5:]:
                if msg["role"] == "user":
                    st.markdown(f'''
                    <div style="text-align:right;margin:0.5rem 0;">
                        <span style="background:#1E3A5F;color:white;padding:0.5rem 1rem;
                                     border-radius:12px;display:inline-block;max-width:80%;">
                            {msg["content"]}
                        </span>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div style="text-align:left;margin:0.5rem 0;">
                        <span style="background:{t['bg_secondary']};color:{t['text']};padding:0.5rem 1rem;
                                     border-radius:12px;display:inline-block;max-width:80%;
                                     border:1px solid {t['border']};">
                            {msg["content"]}
                        </span>
                    </div>
                    ''', unsafe_allow_html=True)
        
        # Quick suggestions
        st.markdown("**Quick Actions:**")
        suggestions = get_contextual_suggestions()
        
        cols = st.columns(len(suggestions))
        for col, sug in zip(cols, suggestions):
            with col:
                if st.button(sug["label"], key=f"sug_{sug['label']}", use_container_width=True):
                    # Add user message
                    st.session_state.copilot_messages.append({
                        "role": "user",
                        "content": sug["query"],
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Generate response
                    response = generate_copilot_response(sug["query"])
                    st.session_state.copilot_messages.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
        
        # Text input
        user_input = st.text_input(
            "Ask Copilot",
            placeholder="Ask about risks, compliance, findings...",
            key="copilot_input",
            label_visibility="collapsed"
        )
        
        if st.button("📤 Send", key="send_copilot", use_container_width=True, type="primary"):
            if user_input:
                # Add user message
                st.session_state.copilot_messages.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Generate response
                response = generate_copilot_response(user_input)
                st.session_state.copilot_messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", key="clear_copilot"):
            st.session_state.copilot_messages = []
            st.rerun()


# Export
__all__ = [
    "render_floating_copilot",
    "init_copilot_state",
    "generate_copilot_response"
]
