"""
AI Lab Module for AURIX.
Prompt engineering playground and AI experimentation.
"""

import streamlit as st
from datetime import datetime
import uuid

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from data.seeds import SYSTEM_PROMPTS, PTCF_TEMPLATES
from app.constants import LLM_PROVIDER_INFO


def render():
    """Render the AI Lab page."""
    t = get_current_theme()
    
    render_page_header(
        "🧪 AI Lab",
        "Experiment with prompts and AI models"
    )
    
    # Lab hero
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, {t['primary']}20, {t['accent']}20, #8b5cf620);border:1px solid {t['border']};border-radius:20px;padding:2rem;margin-bottom:2rem;text-align:center;">
        <div style="font-size:4rem;margin-bottom:1rem;">🧬</div>
        <div style="font-size:1.5rem;font-weight:700;color:{t['text']};margin-bottom:0.5rem;">AI Experimentation Lab</div>
        <div style="color:{t['text_secondary']};max-width:600px;margin:0 auto;">
            Test prompts, compare models, and discover the best AI approaches for your audit needs
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎮 Prompt Playground",
        "⚔️ Model Arena",
        "📚 Prompt Library",
        "📊 Experiments"
    ])
    
    with tab1:
        _render_playground(t)
    
    with tab2:
        _render_model_arena(t)
    
    with tab3:
        _render_prompt_library(t)
    
    with tab4:
        _render_experiments(t)
    
    render_footer()


def _render_playground(t: dict):
    """Render prompt playground."""
    st.markdown("### 🎮 Prompt Playground")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input")
        
        # System prompt
        system_preset = st.selectbox(
            "System Prompt Preset",
            options=["Custom"] + list(SYSTEM_PROMPTS.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if system_preset == "Custom":
            system_prompt = st.text_area(
                "System Prompt",
                height=100,
                placeholder="You are an expert audit assistant..."
            )
        else:
            system_prompt = st.text_area(
                "System Prompt",
                value=SYSTEM_PROMPTS.get(system_preset, ""),
                height=100
            )
        
        # User prompt
        user_prompt = st.text_area(
            "User Prompt",
            height=150,
            placeholder="Enter your prompt here..."
        )
        
        # Variables
        with st.expander("📝 Variables (optional)"):
            var1_name = st.text_input("Variable 1 Name", value="audit_area")
            var1_value = st.text_input("Variable 1 Value", value="Credit Risk")
            var2_name = st.text_input("Variable 2 Name", value="regulation")
            var2_value = st.text_input("Variable 2 Value", value="POJK 40/2019")
        
        # Parameters
        with st.expander("⚙️ Parameters"):
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
            top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
        
        # Model selection
        model = st.selectbox(
            "Model",
            options=["Groq (Llama 3.3)", "Google (Gemini)", "Together (Mixtral)", "Mock (Demo)"]
        )
        
        if st.button("🚀 Run Prompt", type="primary", use_container_width=True):
            st.session_state['playground_result'] = True
    
    with col2:
        st.markdown("#### Output")
        
        if st.session_state.get('playground_result'):
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['success']};border-radius:12px;padding:1.5rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                    <span style="color:{t['success']};font-weight:600;">✅ Response Generated</span>
                    <span style="font-size:0.75rem;color:{t['text_muted']};">1.2s • 487 tokens</span>
                </div>
                <div style="color:{t['text']};white-space:pre-wrap;font-family:monospace;font-size:0.85rem;background:{t['bg_secondary']};padding:1rem;border-radius:8px;max-height:400px;overflow-y:auto;">
## Risk Assessment Analysis

Based on the {var1_value} focus area and {var2_value} requirements:

### Key Risk Areas

1. **Credit Quality Deterioration**
   - NPL ratio monitoring
   - Watchlist account tracking
   - Early warning indicators

2. **Concentration Risk**
   - Top borrower exposure
   - Sector concentration
   - Geographic distribution

3. **Collateral Risk**
   - Valuation accuracy
   - Coverage adequacy
   - Legal enforceability

### Recommended Audit Procedures

| # | Procedure | Sample |
|---|-----------|--------|
| 1 | Review credit policy compliance | 25 files |
| 2 | Test credit approval process | 15 cases |
| 3 | Verify collateral valuations | 10 assets |

### Regulatory Considerations

Per {var2_value}, ensure:
- Asset quality classification
- CKPN adequacy
- Reporting timeliness
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Actions
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.button("📋 Copy", use_container_width=True)
            with col_b:
                st.button("💾 Save", use_container_width=True)
            with col_c:
                st.button("🔄 Regenerate", use_container_width=True)
        else:
            st.markdown(f'''
            <div style="background:{t['card']};border:2px dashed {t['border']};border-radius:12px;padding:3rem;text-align:center;">
                <div style="font-size:3rem;margin-bottom:1rem;opacity:0.5;">🧪</div>
                <div style="color:{t['text_muted']};">Run a prompt to see results here</div>
            </div>
            ''', unsafe_allow_html=True)


def _render_model_arena(t: dict):
    """Render model comparison arena."""
    st.markdown("### ⚔️ Model Arena")
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:2rem;">
        <div style="display:flex;align-items:center;gap:1rem;">
            <div style="font-size:2.5rem;">🏟️</div>
            <div>
                <div style="font-weight:600;color:{t['text']};">Compare Multiple Models</div>
                <div style="color:{t['text_secondary']};font-size:0.9rem;">Test the same prompt across different AI models side-by-side</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Prompt input
    arena_prompt = st.text_area(
        "Test Prompt",
        height=100,
        placeholder="Enter a prompt to test across models...",
        value="Generate 5 audit procedures for testing vendor payment controls, including sample sizes and expected evidence."
    )
    
    # Model selection
    st.markdown("#### Select Models to Compare")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        model1 = st.checkbox("🦙 Groq Llama 3.3", value=True)
    with col2:
        model2 = st.checkbox("💎 Google Gemini", value=True)
    with col3:
        model3 = st.checkbox("🌀 Together Mixtral", value=False)
    with col4:
        model4 = st.checkbox("🎭 Mock Demo", value=True)
    
    if st.button("⚔️ Start Battle", type="primary", use_container_width=True):
        st.session_state['arena_running'] = True
    
    if st.session_state.get('arena_running'):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Results")
        
        # Show results
        models_results = [
            ("🦙 Groq Llama 3.3", 0.8, 4.5, 89),
            ("💎 Google Gemini", 1.2, 4.2, 85),
            ("🎭 Mock Demo", 0.5, 4.0, 80),
        ]
        
        cols = st.columns(3)
        
        for col, (name, time, rating, relevance) in zip(cols, models_results):
            with col:
                st.markdown(f'''
                <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.25rem;">
                    <div style="font-weight:700;color:{t['text']};margin-bottom:1rem;text-align:center;">{name}</div>
                    
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-bottom:1rem;">
                        <div style="text-align:center;background:{t['bg_secondary']};padding:0.5rem;border-radius:8px;">
                            <div style="font-size:0.7rem;color:{t['text_muted']};">Time</div>
                            <div style="font-weight:600;color:{t['text']};">{time}s</div>
                        </div>
                        <div style="text-align:center;background:{t['bg_secondary']};padding:0.5rem;border-radius:8px;">
                            <div style="font-size:0.7rem;color:{t['text_muted']};">Relevance</div>
                            <div style="font-weight:600;color:{t['success']};">{relevance}%</div>
                        </div>
                    </div>
                    
                    <div style="background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;font-size:0.8rem;color:{t['text_secondary']};max-height:200px;overflow-y:auto;">
                        <strong>Sample Output:</strong><br><br>
                        1. Review vendor master data changes (n=25)<br>
                        2. Test payment approval workflow (n=15)<br>
                        3. Verify three-way matching (n=20)<br>
                        4. Check duplicate payment controls<br>
                        5. Validate bank account verification
                    </div>
                    
                    <div style="text-align:center;margin-top:1rem;">
                        <span style="font-size:1.5rem;">{'⭐' * int(rating)}</span>
                        <div style="font-size:0.75rem;color:{t['text_muted']};">{rating}/5.0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Winner announcement
        st.markdown(f'''
        <div style="background:linear-gradient(135deg, {t['warning']}20, {t['warning']}10);border:2px solid {t['warning']};border-radius:16px;padding:1.5rem;margin-top:1.5rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">🏆</div>
            <div style="font-weight:700;color:{t['warning']};font-size:1.2rem;">Winner: Groq Llama 3.3</div>
            <div style="color:{t['text_secondary']};font-size:0.9rem;">Best combination of speed and quality</div>
        </div>
        ''', unsafe_allow_html=True)


def _render_prompt_library(t: dict):
    """Render prompt library."""
    st.markdown("### 📚 Prompt Library")
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search prompts", placeholder="Search by name or keyword...")
    with col2:
        category = st.selectbox("Category", ["All", "Risk Assessment", "Procedures", "Compliance", "Findings", "General"])
    
    # Prompt cards
    prompts = [
        {
            "name": "Risk Identification Matrix",
            "category": "Risk Assessment",
            "description": "Generate comprehensive risk identification for any audit area",
            "uses": 156,
            "rating": 4.8,
            "template": PTCF_TEMPLATES.get('risk_identification', {})
        },
        {
            "name": "Audit Procedure Generator",
            "category": "Procedures",
            "description": "Create detailed audit procedures with testing approach",
            "uses": 243,
            "rating": 4.9,
            "template": PTCF_TEMPLATES.get('procedure_generation', {})
        },
        {
            "name": "Control Assessment",
            "category": "Risk Assessment",
            "description": "Evaluate control design and operating effectiveness",
            "uses": 128,
            "rating": 4.7,
            "template": PTCF_TEMPLATES.get('control_assessment', {})
        },
        {
            "name": "Compliance Gap Analysis",
            "category": "Compliance",
            "description": "Identify regulatory compliance gaps",
            "uses": 95,
            "rating": 4.6,
            "template": PTCF_TEMPLATES.get('compliance_review', {})
        },
        {
            "name": "Finding Documentation (5Cs)",
            "category": "Findings",
            "description": "Document audit findings using the 5Cs methodology",
            "uses": 312,
            "rating": 4.9,
            "template": PTCF_TEMPLATES.get('finding_documentation', {})
        },
    ]
    
    for prompt in prompts:
        if search and search.lower() not in prompt['name'].lower() and search.lower() not in prompt['description'].lower():
            continue
        if category != "All" and prompt['category'] != category:
            continue
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:start;">
                <div style="flex:1;">
                    <div style="font-weight:700;color:{t['text']};font-size:1.1rem;">{prompt['name']}</div>
                    <div style="color:{t['text_secondary']};margin:0.5rem 0;">{prompt['description']}</div>
                    <div style="display:flex;gap:1rem;font-size:0.8rem;color:{t['text_muted']};">
                        <span>📁 {prompt['category']}</span>
                        <span>🔄 {prompt['uses']} uses</span>
                        <span>⭐ {prompt['rating']}</span>
                    </div>
                </div>
                <div style="display:flex;gap:0.5rem;">
                    <button style="background:{t['primary']};color:white;border:none;padding:0.5rem 1rem;border-radius:8px;cursor:pointer;">
                        Use
                    </button>
                    <button style="background:{t['bg_secondary']};color:{t['text']};border:1px solid {t['border']};padding:0.5rem 1rem;border-radius:8px;cursor:pointer;">
                        View
                    </button>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_experiments(t: dict):
    """Render experiments history."""
    st.markdown("### 📊 Experiments History")
    
    # Stats
    cols = st.columns(4)
    
    stats = [
        ("Total Experiments", "47", t['primary']),
        ("This Week", "12", t['accent']),
        ("Avg. Quality", "4.5/5", t['success']),
        ("Prompts Saved", "23", t['warning']),
    ]
    
    for col, (label, value, color) in zip(cols, stats):
        with col:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:{color};">{value}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{label}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Experiment list
    experiments = [
        {"name": "Credit Risk Procedures v3", "date": "Today", "models": 3, "winner": "Llama 3.3", "status": "completed"},
        {"name": "AML Alert Analysis", "date": "Yesterday", "models": 2, "winner": "Gemini", "status": "completed"},
        {"name": "IT Controls Testing", "date": "2 days ago", "models": 4, "winner": "Mixtral", "status": "completed"},
        {"name": "Fraud Detection Prompts", "date": "3 days ago", "models": 3, "winner": "Llama 3.3", "status": "completed"},
    ]
    
    for exp in experiments:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.5rem;display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="font-weight:600;color:{t['text']};">{exp['name']}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">
                    {exp['date']} • {exp['models']} models tested
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:1rem;">
                <span style="background:{t['success']}20;color:{t['success']};padding:0.25rem 0.75rem;border-radius:12px;font-size:0.75rem;">
                    🏆 {exp['winner']}
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
