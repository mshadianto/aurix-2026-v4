"""
Risk Assessment Page Module
Comprehensive risk evaluation with matrix visualization
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import random

from ui.components import (
    render_page_header,
    render_footer,
    render_badge,
    render_metric_card,
    render_alert,
    render_section_title
)
from ui.styles.css_builder import get_current_theme
from data.seeds import AUDIT_UNIVERSE


def render_risk_assessment_page():
    """Render the risk assessment page"""
    t = get_current_theme()
    
    render_page_header(
        "Risk Assessment",
        "Evaluate and score audit risks using industry-standard methodology"
    )
    
    # Initialize risk assessments in session state
    if 'risk_assessments' not in st.session_state:
        st.session_state.risk_assessments = {}
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 New Assessment", "📋 Assessment History", "🔥 Risk Heatmap"])
    
    with tab1:
        _render_assessment_form(t)
    
    with tab2:
        _render_assessment_history(t)
    
    with tab3:
        _render_risk_heatmap(t)
    
    render_footer()


def _render_assessment_form(t: Dict):
    """Render the risk assessment form"""
    st.markdown("### 🎯 Define Risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk identification
        st.markdown(f'''
        <div class="pro-card" style="padding: 1.5rem;">
            <h4 style="color:{t['text']} !important; margin-bottom: 1rem;">Risk Identification</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        risk_category = st.selectbox(
            "Risk Category",
            options=list(AUDIT_UNIVERSE.keys())
        )
        
        # Get areas for selected category
        risk_areas = AUDIT_UNIVERSE.get(risk_category, [])
        risk_area = st.selectbox(
            "Audit Area",
            options=risk_areas
        )
        
        risk_name = st.text_input(
            "Risk Name",
            placeholder="e.g., Credit Approval Bypass"
        )
        
        risk_description = st.text_area(
            "Risk Description",
            placeholder="Describe the risk event and its potential causes...",
            height=100
        )
    
    with col2:
        # Risk scoring
        st.markdown(f'''
        <div class="pro-card" style="padding: 1.5rem;">
            <h4 style="color:{t['text']} !important; margin-bottom: 1rem;">Risk Scoring</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        # Likelihood slider
        st.markdown("**Likelihood** (Probability of occurrence)")
        likelihood = st.select_slider(
            "Likelihood",
            options=["Very Low", "Low", "Medium", "High", "Very High"],
            value="Medium",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Impact slider
        st.markdown("**Impact** (Severity if risk materializes)")
        impact = st.select_slider(
            "Impact",
            options=["Very Low", "Low", "Medium", "High", "Very High"],
            value="Medium",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Calculate and display risk score
        score, level, color = _calculate_risk_score(likelihood, impact, t)
        
        st.markdown(f'''
        <div style="background:{color}20; border:2px solid {color}; border-radius:12px; padding:1.5rem; text-align:center;">
            <div style="font-size:3rem; font-weight:700; color:{color};">{score}</div>
            <div style="font-size:1.25rem; font-weight:600; color:{color};">{level} RISK</div>
            <div style="font-size:0.85rem; color:{t['text_muted']} !important; margin-top:0.5rem;">
                Likelihood: {likelihood} × Impact: {impact}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Control assessment section
    _render_control_assessment(t)
    
    # Save button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("💾 Save Risk Assessment", type="primary", use_container_width=True):
            if risk_name:
                _save_assessment(
                    risk_name, risk_category, risk_area, risk_description,
                    likelihood, impact, score, level
                )
            else:
                st.warning("Please enter a risk name")


def _render_control_assessment(t: Dict):
    """Render control assessment section"""
    with st.expander("🔒 Control Assessment (Optional)", expanded=False):
        st.markdown("**Evaluate existing controls to determine residual risk**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Control Factors")
            control_design = st.slider(
                "Control Design",
                min_value=1, max_value=5, value=3,
                help="How well are controls designed to mitigate the risk?"
            )
            
            operating_effectiveness = st.slider(
                "Operating Effectiveness",
                min_value=1, max_value=5, value=3,
                help="How effectively are controls operating?"
            )
            
            management_oversight = st.slider(
                "Management Oversight",
                min_value=1, max_value=5, value=3,
                help="Level of management monitoring and oversight"
            )
        
        with col2:
            st.markdown("##### Additional Factors")
            segregation = st.slider(
                "Segregation of Duties",
                min_value=1, max_value=5, value=3,
                help="Adequacy of duty segregation"
            )
            
            automation = st.slider(
                "Automation Level",
                min_value=1, max_value=5, value=3,
                help="Level of control automation"
            )
            
            # Calculate control score
            control_score = (control_design + operating_effectiveness + 
                           management_oversight + segregation + automation) / 5
            
            control_rating = "Strong" if control_score >= 4 else "Adequate" if control_score >= 3 else "Weak"
            control_color = t['success'] if control_rating == "Strong" else t['warning'] if control_rating == "Adequate" else t['danger']
            
            st.markdown(f'''
            <div style="background:{control_color}20; border:1px solid {control_color}; border-radius:8px; padding:1rem; text-align:center; margin-top:1rem;">
                <div style="font-size:1.5rem; font-weight:700; color:{control_color};">{control_score:.1f}/5</div>
                <div style="font-size:0.9rem; font-weight:600; color:{control_color};">{control_rating} Controls</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Store control assessment in session state for use in saving
        st.session_state['temp_control_score'] = control_score
        st.session_state['temp_control_rating'] = control_rating


def _calculate_risk_score(likelihood: str, impact: str, t: Dict) -> Tuple[int, str, str]:
    """Calculate risk score from likelihood and impact"""
    score_map = {
        "Very Low": 1,
        "Low": 2,
        "Medium": 3,
        "High": 4,
        "Very High": 5
    }
    
    l_score = score_map[likelihood]
    i_score = score_map[impact]
    risk_score = l_score * i_score
    
    if risk_score >= 15:
        return risk_score, "HIGH", t['danger']
    elif risk_score >= 8:
        return risk_score, "MEDIUM", t['warning']
    else:
        return risk_score, "LOW", t['success']


def _save_assessment(name: str, category: str, area: str, description: str,
                    likelihood: str, impact: str, score: int, level: str):
    """Save risk assessment to session state"""
    assessment = {
        'name': name,
        'category': category,
        'area': area,
        'description': description,
        'likelihood': likelihood,
        'impact': impact,
        'score': score,
        'level': level,
        'control_score': st.session_state.get('temp_control_score', 3.0),
        'control_rating': st.session_state.get('temp_control_rating', 'Adequate'),
        'assessed_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'assessed_by': 'Current User'
    }
    
    st.session_state.risk_assessments[name] = assessment
    st.success(f"✅ Risk assessment '{name}' saved successfully!")
    st.rerun()


def _render_assessment_history(t: Dict):
    """Render assessment history section"""
    assessments = st.session_state.risk_assessments
    
    if not assessments:
        st.info("📋 No risk assessments recorded yet. Create your first assessment above.")
        return
    
    st.markdown("### 📊 Risk Assessment History")
    
    # Summary metrics
    total = len(assessments)
    high_count = len([a for a in assessments.values() if a['level'] == 'HIGH'])
    medium_count = len([a for a in assessments.values() if a['level'] == 'MEDIUM'])
    low_count = len([a for a in assessments.values() if a['level'] == 'LOW'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(render_metric_card("Total Assessments", str(total), icon="📊"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("High Risk", str(high_count), icon="🔴"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("Medium Risk", str(medium_count), icon="🟡"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card("Low Risk", str(low_count), icon="🟢"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter options
    filter_level = st.selectbox(
        "Filter by Risk Level",
        options=["All", "HIGH", "MEDIUM", "LOW"]
    )
    
    # Display assessments
    for name, assessment in sorted(assessments.items(), 
                                    key=lambda x: x[1]['score'], 
                                    reverse=True):
        if filter_level != "All" and assessment['level'] != filter_level:
            continue
        
        _render_assessment_card(name, assessment, t)


def _render_assessment_card(name: str, assessment: Dict, t: Dict):
    """Render a single assessment card"""
    level = assessment['level']
    level_colors = {
        'HIGH': t['danger'],
        'MEDIUM': t['warning'],
        'LOW': t['success']
    }
    color = level_colors.get(level, t['text_muted'])
    
    with st.expander(f"**{name}** - {level} Risk (Score: {assessment['score']})", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f'''
            <div class="pro-card" style="padding: 1rem;">
                <div style="margin-bottom: 0.75rem;">
                    <strong>Category:</strong> {assessment['category']}
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <strong>Area:</strong> {assessment['area']}
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <strong>Description:</strong> {assessment.get('description', 'N/A')}
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <strong>Likelihood:</strong> {assessment['likelihood']} | 
                    <strong>Impact:</strong> {assessment['impact']}
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <strong>Control Rating:</strong> {assessment.get('control_rating', 'Not Assessed')}
                </div>
                <div style="font-size: 0.8rem; color: {t['text_muted']} !important;">
                    Assessed: {assessment['assessed_date']}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div style="background:{color}20; border:2px solid {color}; border-radius:12px; padding:1.5rem; text-align:center; height:100%;">
                <div style="font-size:2.5rem; font-weight:700; color:{color};">{assessment['score']}</div>
                <div style="font-size:1rem; font-weight:600; color:{color};">{level}</div>
                <div style="font-size:0.75rem; color:{t['text_muted']} !important; margin-top:0.5rem;">
                    Risk Score
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Edit", key=f"edit_{name}", use_container_width=True):
                st.info("Edit functionality coming soon")
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{name}", use_container_width=True):
                del st.session_state.risk_assessments[name]
                st.success(f"✓ Deleted '{name}'")
                st.rerun()


def _render_risk_heatmap(t: Dict):
    """Render risk heatmap visualization"""
    st.markdown("### 🔥 Risk Heat Map")
    st.markdown("Visual representation of risks across the audit universe")
    
    # Generate risk data for each category
    risk_data = []
    for cat, areas in AUDIT_UNIVERSE.items():
        # Use actual assessments if available, otherwise generate demo data
        high_risk = 0
        medium_risk = 0
        low_risk = 0
        
        for area in areas:
            # Check if there's an assessment for this area
            matching_assessments = [
                a for a in st.session_state.risk_assessments.values()
                if a.get('area') == area
            ]
            
            if matching_assessments:
                for a in matching_assessments:
                    if a['level'] == 'HIGH':
                        high_risk += 1
                    elif a['level'] == 'MEDIUM':
                        medium_risk += 1
                    else:
                        low_risk += 1
            else:
                # Demo data for unassessed areas
                r = random.random()
                if r < 0.15:
                    high_risk += 1
                elif r < 0.45:
                    medium_risk += 1
                else:
                    low_risk += 1
        
        risk_data.append({
            "category": cat,
            "high": high_risk,
            "medium": medium_risk,
            "low": low_risk,
            "total": len(areas)
        })
    
    # Display heatmap
    for item in risk_data:
        total = item['total']
        if total == 0:
            continue
        
        high_pct = (item['high'] / total) * 100
        medium_pct = (item['medium'] / total) * 100
        low_pct = (item['low'] / total) * 100
        
        st.markdown(f'''
        <div class="pro-card" style="padding: 1rem; margin-bottom: 0.75rem;">
            <div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                <strong style="color:{t['text']} !important;">{item['category']}</strong>
                <span style="color:{t['text_muted']} !important; font-size: 0.85rem;">
                    {total} areas
                </span>
            </div>
            <div style="display: flex; height: 12px; border-radius: 6px; overflow: hidden; background: {t['border']};">
                <div style="width: {high_pct}%; background: {t['danger']};"></div>
                <div style="width: {medium_pct}%; background: {t['warning']};"></div>
                <div style="width: {low_pct}%; background: {t['success']};"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.75rem;">
                <span style="color: {t['danger']} !important;">■ {item['high']} High</span>
                <span style="color: {t['warning']} !important;">■ {item['medium']} Medium</span>
                <span style="color: {t['success']} !important;">■ {item['low']} Low</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Risk Matrix Legend
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📐 Risk Matrix")
    
    _render_risk_matrix(t)


def _render_risk_matrix(t: Dict):
    """Render 5x5 risk matrix"""
    matrix_html = f'''
    <div style="overflow-x: auto;">
        <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
            <tr>
                <td style="width: 80px;"></td>
                <td colspan="5" style="text-align: center; font-weight: 600; padding: 8px; color: {t['text']} !important;">
                    IMPACT →
                </td>
            </tr>
            <tr>
                <td style="writing-mode: vertical-lr; text-orientation: mixed; text-align: center; 
                    font-weight: 600; padding: 8px; color: {t['text']} !important; transform: rotate(180deg);">
                    LIKELIHOOD
                </td>
    '''
    
    # Matrix colors based on risk score (likelihood × impact)
    for l in range(5, 0, -1):  # Likelihood from 5 to 1
        matrix_html += '<tr>'
        for i in range(1, 6):  # Impact from 1 to 5
            score = l * i
            if score >= 15:
                bg = t['danger']
                opacity = '0.9'
            elif score >= 8:
                bg = t['warning']
                opacity = '0.8'
            else:
                bg = t['success']
                opacity = '0.7'
            
            matrix_html += f'''
                <td style="width: 60px; height: 40px; text-align: center; 
                    background: {bg}{opacity.replace('0.', '')}; color: white; 
                    font-weight: 600; border: 1px solid {t['border']};">
                    {score}
                </td>
            '''
        matrix_html += '</tr>'
    
    matrix_html += '''
        </table>
    </div>
    '''
    
    st.markdown(matrix_html, unsafe_allow_html=True)
    
    # Legend
    st.markdown(f'''
    <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: {t['danger']}; border-radius: 4px;"></div>
            <span style="color: {t['text_muted']} !important; font-size: 0.85rem;">High Risk (15-25)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: {t['warning']}; border-radius: 4px;"></div>
            <span style="color: {t['text_muted']} !important; font-size: 0.85rem;">Medium Risk (8-14)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: {t['success']}; border-radius: 4px;"></div>
            <span style="color: {t['text_muted']} !important; font-size: 0.85rem;">Low Risk (1-7)</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


# Export
def render():
    """Render function called by router."""
    render_risk_assessment_page()

__all__ = ['render_risk_assessment_page', 'render']
