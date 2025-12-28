"""
PTCF Builder Page Module for AURIX.
Persona, Task, Context, Format - Professional prompt engineering for audit.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
import uuid

from ui.styles.css_builder import get_current_theme
from ui.components import (
    render_page_header, 
    render_footer, 
    render_badge,
    render_info_card,
    render_alert
)
from data.seeds import (
    AUDIT_UNIVERSE,
    PTCF_TEMPLATES,
    SYSTEM_PROMPTS,
    REGULATIONS,
    get_all_audit_areas
)
from app.constants import AUDIT_PERSONAS


class PTCFBuilderPage:
    """PTCF Prompt Builder page with templates and AI execution."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for PTCF builder."""
        if 'ptcf_prompts' not in st.session_state:
            st.session_state.ptcf_prompts = []
        if 'ptcf_history' not in st.session_state:
            st.session_state.ptcf_history = []
    
    def render(self):
        """Render the PTCF Builder page."""
        render_page_header("PTCF Builder", "Professional Prompt Engineering for Audit Intelligence")
        
        t = get_current_theme()
        
        # Introduction Card
        st.markdown(f'''
        <div class="pro-card" style="background:linear-gradient(135deg, {t['primary']}15, {t['accent']}15);border-left:4px solid {t['primary']};">
            <h4 style="margin:0 0 0.5rem 0;color:{t['text']} !important;">🎭 PTCF Framework</h4>
            <p style="margin:0;font-size:0.9rem;color:{t['text_secondary']} !important;">
                Build professional audit prompts using the <strong>Persona-Task-Context-Format</strong> framework.
                This methodology follows McKinsey & Big 4 best practices for optimal AI-assisted audit analysis.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📝 Build Prompt", "📚 Templates", "📜 History"])
        
        with tab1:
            self._render_prompt_builder()
        
        with tab2:
            self._render_templates()
        
        with tab3:
            self._render_history()
        
        render_footer()
    
    def _render_prompt_builder(self):
        """Render the main prompt builder interface."""
        t = get_current_theme()
        
        st.markdown("### 🔧 Build Your PTCF Prompt")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Persona Section
            st.markdown(f'''
            <div class="ptcf-item" style="border-left-color:{t['primary']};">
                <div class="ptcf-label">P - PERSONA</div>
                <div style="font-size:0.85rem;color:{t['text_secondary']} !important;">
                    Define the role and expertise AI should assume
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            persona_choice = st.selectbox(
                "Select Persona",
                options=["Custom"] + list(AUDIT_PERSONAS.values()),
                key="ptcf_persona_select"
            )
            
            if persona_choice == "Custom":
                persona_text = st.text_area(
                    "Custom Persona Description",
                    height=100,
                    placeholder="e.g., Senior Internal Auditor with 15 years of experience in credit risk...",
                    key="ptcf_persona_custom"
                )
            else:
                persona_text = persona_choice
                st.info(f"**Selected:** {persona_choice}")
            
            # Task Section
            st.markdown(f'''
            <div class="ptcf-item" style="border-left-color:{t['accent']};">
                <div class="ptcf-label" style="color:{t['accent']} !important;">T - TASK</div>
                <div style="font-size:0.85rem;color:{t['text_secondary']} !important;">
                    Clearly define what needs to be accomplished
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            task_templates = [
                "Custom Task",
                "Identify top risk areas for audit focus",
                "Assess control effectiveness",
                "Generate audit procedures",
                "Document audit finding",
                "Evaluate regulatory compliance",
                "Perform root cause analysis",
                "Develop audit recommendations"
            ]
            
            task_choice = st.selectbox(
                "Select Task Type",
                options=task_templates,
                key="ptcf_task_select"
            )
            
            if task_choice == "Custom Task":
                task_text = st.text_area(
                    "Describe the Task",
                    height=100,
                    placeholder="e.g., Analyze the credit approval process and identify control gaps...",
                    key="ptcf_task_custom"
                )
            else:
                task_text = task_choice
                # Additional task parameters
                if "risk areas" in task_choice.lower():
                    num_risks = st.slider("Number of risk areas to identify", 3, 10, 5)
                    task_text = f"{task_text} (Top {num_risks})"
        
        with col2:
            # Context Section
            st.markdown(f'''
            <div class="ptcf-item" style="border-left-color:{t['success']};">
                <div class="ptcf-label" style="color:{t['success']} !important;">C - CONTEXT</div>
                <div style="font-size:0.85rem;color:{t['text_secondary']} !important;">
                    Provide relevant background and reference materials
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Audit Area Selection
            audit_category = st.selectbox(
                "Audit Category",
                options=list(AUDIT_UNIVERSE.keys()),
                key="ptcf_audit_category"
            )
            
            audit_areas = st.multiselect(
                "Specific Audit Areas",
                options=AUDIT_UNIVERSE[audit_category],
                key="ptcf_audit_areas"
            )
            
            # Regulation References
            reg_options = []
            for cat, regs in REGULATIONS.items():
                for reg in regs:
                    reg_options.append(f"{reg['code']} - {reg['title'][:40]}...")
            
            regulations = st.multiselect(
                "Applicable Regulations",
                options=reg_options,
                key="ptcf_regulations"
            )
            
            # Additional Context
            additional_context = st.text_area(
                "Additional Context",
                height=80,
                placeholder="e.g., Audit period Q3 2024, portfolio size Rp 8.5 Trillion...",
                key="ptcf_additional_context"
            )
            
            # Format Section
            st.markdown(f'''
            <div class="ptcf-item" style="border-left-color:{t['warning']};">
                <div class="ptcf-label" style="color:{t['warning']} !important;">F - FORMAT</div>
                <div style="font-size:0.85rem;color:{t['text_secondary']} !important;">
                    Specify the expected output structure
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            format_options = [
                "Risk Assessment Matrix",
                "Control Testing Matrix",
                "Compliance Checklist",
                "Audit Procedure Table",
                "5Cs Finding Format",
                "Executive Summary",
                "Detailed Report",
                "Bullet Points",
                "Custom Format"
            ]
            
            format_choice = st.selectbox(
                "Output Format",
                options=format_options,
                key="ptcf_format_select"
            )
            
            if format_choice == "Custom Format":
                format_text = st.text_area(
                    "Custom Format Description",
                    height=80,
                    placeholder="e.g., Table with columns: Control Activity, Objective, Design Rating...",
                    key="ptcf_format_custom"
                )
            else:
                format_text = format_choice
        
        st.markdown("---")
        
        # Generate Prompt Preview
        st.markdown("### 📋 Generated PTCF Prompt")
        
        # Build context string
        context_parts = []
        if audit_areas:
            context_parts.append(f"Audit Areas: {', '.join(audit_areas)}")
        if regulations:
            context_parts.append(f"Regulations: {', '.join([r.split(' - ')[0] for r in regulations])}")
        if additional_context:
            context_parts.append(additional_context)
        
        context_string = ". ".join(context_parts) if context_parts else "General audit context"
        
        # Build final prompt
        final_prompt = self._build_ptcf_prompt(
            persona=persona_text if persona_choice == "Custom" else persona_text,
            task=task_text if task_choice == "Custom Task" else task_text,
            context=context_string,
            format_spec=format_text if format_choice == "Custom Format" else format_text
        )
        
        st.markdown(f'''
        <div class="pro-card" style="background:{t['bg_secondary']};font-family:monospace;white-space:pre-wrap;font-size:0.85rem;">
{final_prompt}
        </div>
        ''', unsafe_allow_html=True)
        
        # Action Buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(final_prompt)
                st.success("✓ Prompt displayed - copy from above")
        
        with col2:
            if st.button("💾 Save Prompt", use_container_width=True):
                self._save_prompt(final_prompt, persona_text, task_text)
        
        with col3:
            if st.button("🚀 Execute with AI", type="primary", use_container_width=True):
                self._execute_prompt(final_prompt)
    
    def _build_ptcf_prompt(self, persona: str, task: str, context: str, format_spec: str) -> str:
        """Build a complete PTCF prompt."""
        return f"""[PERSONA]
You are acting as: {persona}

[TASK]
{task}

[CONTEXT]
{context}

Consider Indonesian regulatory requirements and apply Big 4/McKinsey audit methodology best practices.

[FORMAT]
Present your response in the following format: {format_spec}

Ensure the output is:
- Professional and actionable
- Specific to the Indonesian financial industry
- Compliant with applicable regulations
- Based on risk-based audit methodology"""
    
    def _save_prompt(self, prompt: str, persona: str, task: str):
        """Save prompt to history."""
        prompt_entry = {
            'id': str(uuid.uuid4())[:8],
            'prompt': prompt,
            'persona': persona,
            'task': task,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'executed': False
        }
        st.session_state.ptcf_prompts.append(prompt_entry)
        st.success(f"✓ Prompt saved with ID: {prompt_entry['id']}")
    
    def _execute_prompt(self, prompt: str):
        """Execute prompt with AI."""
        t = get_current_theme()
        
        # Check for LLM configuration
        llm_provider = st.session_state.get('llm_provider', 'mock')
        api_key = st.session_state.get('api_key_input')
        
        with st.spinner("🤖 AI is analyzing..."):
            # Mock response for demo
            response = self._generate_mock_response(prompt)
        
        st.markdown("### 🤖 AI Response")
        st.markdown(f'''
        <div class="pro-card" style="border-left:4px solid {t['success']};">
            <div style="font-size:0.75rem;color:{t['text_muted']} !important;margin-bottom:1rem;">
                Provider: {llm_provider} | Generated: {datetime.now().strftime("%H:%M:%S")}
            </div>
            <div style="color:{t['text_secondary']} !important;white-space:pre-wrap;">
{response}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Save to history
        history_entry = {
            'id': str(uuid.uuid4())[:8],
            'prompt': prompt[:200] + "...",
            'response': response[:500] + "...",
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'provider': llm_provider
        }
        st.session_state.ptcf_history.append(history_entry)
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate mock AI response for demo."""
        if "risk" in prompt.lower():
            return """## Risk Assessment Analysis

Based on the PTCF prompt analysis, here are the identified risk areas:

### 🔴 High Risk Areas

| No | Risk Area | Inherent Risk | Key Risk Factors | Audit Focus |
|----|-----------|---------------|------------------|-------------|
| 1 | Credit Risk Management | HIGH | NPL trends, collateral valuation delays | Credit approval process, monitoring |
| 2 | IT Security Controls | HIGH | Access management gaps | User access review, change management |
| 3 | AML/CFT Compliance | HIGH | Transaction monitoring gaps | TMS effectiveness, STR filing |

### 🟡 Medium Risk Areas

| No | Risk Area | Inherent Risk | Key Risk Factors | Audit Focus |
|----|-----------|---------------|------------------|-------------|
| 4 | Operational Controls | MEDIUM | Documentation gaps | SOP compliance, segregation |
| 5 | Regulatory Reporting | MEDIUM | Timeliness issues | Reporting accuracy |

### 📋 Recommendations

1. **Immediate**: Review credit monitoring procedures per POJK 40/2019
2. **Short-term**: Implement quarterly user access review
3. **Medium-term**: Enhance transaction monitoring parameters

*Analysis based on McKinsey risk-based audit methodology*"""
        
        elif "procedure" in prompt.lower() or "audit" in prompt.lower():
            return """## Audit Test Procedures

### Audit Area: Credit Risk Management

| Step | Procedure | Nature | Sample | Evidence |
|------|-----------|--------|--------|----------|
| 1 | Review credit policy for POJK 40/2019 compliance | Document Review | All policies | Policy documents |
| 2 | Walkthrough credit approval process | Inquiry/Observation | N/A | Process notes |
| 3 | Test sample of credit approvals for proper authorization | Testing | 25 files | Approval matrix |
| 4 | Verify collateral documentation completeness | Inspection | 30 files | Checklist |
| 5 | Review NPL classification accuracy | Reperformance | 20 accounts | Calculation sheets |
| 6 | Test early warning system triggers | Analytics | 100% population | System reports |
| 7 | Evaluate credit committee effectiveness | Inquiry | 5 meetings | Meeting minutes |
| 8 | Test segregation of duties | Observation | Key controls | Access matrix |
| 9 | Review credit exception reports | Document Review | 3 months | Exception logs |
| 10 | Assess management monitoring reports | Analytical Review | 6 months | MIS reports |

### IT Control Testing
- Access control review for credit system
- Change management testing
- Data integrity verification

*Procedures aligned with IIA Standards and POJK requirements*"""
        
        else:
            return """## Analysis Results

Based on the provided context and PTCF framework:

### Key Findings

1. **Process Assessment**: Current controls require enhancement in documentation and monitoring
2. **Compliance Status**: Generally compliant with applicable regulations with minor gaps
3. **Risk Rating**: Overall MEDIUM with specific HIGH risk items identified

### Recommendations

| Priority | Recommendation | Timeline | Owner |
|----------|---------------|----------|-------|
| HIGH | Update credit monitoring procedures | Q1 2025 | Credit Division |
| HIGH | Implement automated access review | Q1 2025 | IT Security |
| MEDIUM | Enhance staff training program | Q2 2025 | HR/Compliance |

### Regulatory Considerations

- POJK 18/2016: Risk management framework compliance
- POJK 55/2016: Governance structure adequacy
- ISO 31000: Enterprise risk management integration

*Response generated using Big 4 audit methodology*"""
    
    def _render_templates(self):
        """Render PTCF templates gallery."""
        t = get_current_theme()
        
        st.markdown("### 📚 PTCF Templates Gallery")
        st.markdown(f'''
        <p style="color:{t['text_secondary']} !important;">
            Pre-built templates for common audit scenarios. Click to load into the builder.
        </p>
        ''', unsafe_allow_html=True)
        
        for template_name, template_data in PTCF_TEMPLATES.items():
            with st.expander(f"📄 {template_name}", expanded=False):
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;">
                    <div class="ptcf-item" style="border-left-color:{t['primary']};">
                        <div class="ptcf-label">PERSONA</div>
                        <div style="font-size:0.9rem;color:{t['text']} !important;">{template_data['persona']}</div>
                    </div>
                    <div class="ptcf-item" style="border-left-color:{t['accent']};">
                        <div class="ptcf-label" style="color:{t['accent']} !important;">TASK</div>
                        <div style="font-size:0.9rem;color:{t['text']} !important;">{template_data['task']}</div>
                    </div>
                    <div class="ptcf-item" style="border-left-color:{t['success']};">
                        <div class="ptcf-label" style="color:{t['success']} !important;">CONTEXT</div>
                        <div style="font-size:0.9rem;color:{t['text']} !important;">{template_data['context']}</div>
                    </div>
                    <div class="ptcf-item" style="border-left-color:{t['warning']};">
                        <div class="ptcf-label" style="color:{t['warning']} !important;">FORMAT</div>
                        <div style="font-size:0.9rem;color:{t['text']} !important;">{template_data['format']}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                if st.button(f"Use This Template", key=f"use_{template_name}"):
                    st.info(f"✓ Template '{template_name}' selected. Go to 'Build Prompt' tab to customize.")
    
    def _render_history(self):
        """Render prompt execution history."""
        t = get_current_theme()
        
        st.markdown("### 📜 Execution History")
        
        if not st.session_state.ptcf_history:
            st.info("No prompts executed yet. Build and execute a prompt to see history.")
            return
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <div class="stat-value">{len(st.session_state.ptcf_history)}</div>
                <div class="stat-label">Total Executions</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            saved_count = len(st.session_state.ptcf_prompts)
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-icon">💾</div>
                <div class="stat-value">{saved_count}</div>
                <div class="stat-label">Saved Prompts</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-icon">🤖</div>
                <div class="stat-value">Mock</div>
                <div class="stat-label">Current Provider</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # History list
        for entry in reversed(st.session_state.ptcf_history[-10:]):
            st.markdown(f'''
            <div class="pro-card" style="padding:1rem;margin-bottom:0.5rem;">
                <div style="display:flex;justify-content:space-between;align-items:start;">
                    <div style="flex:1;">
                        <div style="font-size:0.75rem;color:{t['text_muted']} !important;">
                            {entry['timestamp']} | ID: {entry['id']} | Provider: {entry['provider']}
                        </div>
                        <div style="color:{t['text']} !important;margin-top:0.5rem;font-size:0.9rem;">
                            <strong>Prompt:</strong> {entry['prompt']}
                        </div>
                        <div style="color:{t['text_secondary']} !important;margin-top:0.5rem;font-size:0.85rem;">
                            <strong>Response:</strong> {entry['response']}
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History"):
            st.session_state.ptcf_history = []
            st.rerun()


def render():
    """Entry point for the PTCF Builder page."""
    page = PTCFBuilderPage()
    page.render()
