"""
Sampling Calculator Module for AURIX.
Statistical sampling tools for audit testing.
"""

import streamlit as st
import math
from typing import Dict, List, Any

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the sampling calculator page."""
    t = get_current_theme()
    
    render_page_header(
        "🧮 Sampling Calculator",
        "Statistical sampling tools for audit testing"
    )
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Sample Size Calculator",
        "🎯 Attribute Sampling",
        "💰 MUS Sampling",
        "📖 Sampling Guide"
    ])
    
    with tab1:
        _render_sample_size_calculator(t)
    
    with tab2:
        _render_attribute_sampling(t)
    
    with tab3:
        _render_mus_sampling(t)
    
    with tab4:
        _render_sampling_guide(t)
    
    render_footer()


def _render_sample_size_calculator(t: dict):
    """Render general sample size calculator."""
    st.markdown("### 📊 Sample Size Calculator")
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <p style="color:{t['text_secondary']};margin:0;">
        Calculate the appropriate sample size based on population characteristics, 
        desired confidence level, and acceptable precision.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Input Parameters")
        
        population_size = st.number_input(
            "Population Size (N)",
            min_value=1,
            max_value=10000000,
            value=10000,
            help="Total number of items in the population"
        )
        
        confidence_level = st.select_slider(
            "Confidence Level",
            options=[90, 95, 99],
            value=95,
            help="Probability that sample results reflect the population"
        )
        
        # Z-scores for confidence levels
        z_scores = {90: 1.645, 95: 1.96, 99: 2.576}
        z_score = z_scores[confidence_level]
        
        margin_error = st.slider(
            "Margin of Error (%)",
            min_value=1,
            max_value=10,
            value=5,
            help="Acceptable precision level"
        )
        
        expected_rate = st.slider(
            "Expected Error Rate (%)",
            min_value=1,
            max_value=50,
            value=5,
            help="Estimated error/exception rate in population"
        )
    
    with col2:
        st.markdown("#### Calculation Results")
        
        # Calculate sample size using formula
        p = expected_rate / 100
        e = margin_error / 100
        
        # Infinite population formula
        n_infinite = (z_score**2 * p * (1-p)) / (e**2)
        
        # Finite population correction
        sample_size = math.ceil(n_infinite / (1 + (n_infinite - 1) / population_size))
        
        # Ensure minimum sample
        sample_size = max(sample_size, 25)
        
        # Display results
        st.markdown(f'''
        <div style="background:{t['card']};border:2px solid {t['primary']};border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
            <div style="text-align:center;">
                <div style="font-size:0.85rem;color:{t['text_muted']};text-transform:uppercase;letter-spacing:0.05em;">Recommended Sample Size</div>
                <div style="font-size:3rem;font-weight:700;color:{t['primary']};margin:0.5rem 0;">{sample_size}</div>
                <div style="font-size:0.85rem;color:{t['text_secondary']};">items from population of {population_size:,}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Additional info
        coverage_pct = (sample_size / population_size) * 100
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Coverage</div>
                    <div style="font-size:1.25rem;font-weight:600;color:{t['text']};">{coverage_pct:.2f}%</div>
                </div>
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Z-Score</div>
                    <div style="font-size:1.25rem;font-weight:600;color:{t['text']};">{z_score}</div>
                </div>
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Confidence</div>
                    <div style="font-size:1.25rem;font-weight:600;color:{t['success']};">{confidence_level}%</div>
                </div>
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Precision</div>
                    <div style="font-size:1.25rem;font-weight:600;color:{t['accent']};"> ±{margin_error}%</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sample selection method
        st.markdown("#### Recommended Selection Method")
        
        if population_size < 500:
            method = "Systematic Selection"
            method_desc = "Select every nth item from an ordered list"
        elif population_size < 5000:
            method = "Random Number Selection"
            method_desc = "Use random number generator to select items"
        else:
            method = "Stratified Random Sampling"
            method_desc = "Divide population into strata, sample from each"
        
        st.info(f"**{method}**: {method_desc}")


def _render_attribute_sampling(t: dict):
    """Render attribute sampling calculator."""
    st.markdown("### 🎯 Attribute Sampling")
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <p style="color:{t['text_secondary']};margin:0;">
        Attribute sampling is used to test controls by determining the rate 
        of deviation from a prescribed control procedure.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Test Parameters")
        
        risk_level = st.selectbox(
            "Risk of Assessing Control Risk Too Low",
            options=["5% (High Assurance)", "10% (Moderate Assurance)"],
            help="Risk that sample results support reliance on control when population deviation rate is too high"
        )
        
        tolerable_rate = st.slider(
            "Tolerable Deviation Rate (%)",
            min_value=1,
            max_value=20,
            value=5,
            help="Maximum deviation rate you can accept and still rely on control"
        )
        
        expected_deviation = st.slider(
            "Expected Deviation Rate (%)",
            min_value=0,
            max_value=10,
            value=1,
            help="Estimated deviation rate based on prior experience"
        )
        
        pop_size = st.number_input(
            "Population Size",
            min_value=100,
            max_value=10000000,
            value=5000
        )
    
    with col2:
        st.markdown("#### Sample Size Table (AICPA)")
        
        # Attribute sampling table based on AICPA guidelines
        # Simplified version
        sample_tables = {
            "5% (High Assurance)": {
                (5, 0): 59, (5, 1): 93, (5, 2): 124,
                (10, 0): 29, (10, 1): 46, (10, 2): 61,
                (15, 0): 19, (15, 1): 30, (15, 2): 40,
            },
            "10% (Moderate Assurance)": {
                (5, 0): 45, (5, 1): 77, (5, 2): 105,
                (10, 0): 22, (10, 1): 38, (10, 2): 52,
                (15, 0): 15, (15, 1): 25, (15, 2): 34,
            }
        }
        
        # Get sample size
        table = sample_tables.get(risk_level, {})
        key = (tolerable_rate, expected_deviation)
        
        # Find closest match
        sample_size = 30  # Default
        for (tol, exp), size in table.items():
            if tol >= tolerable_rate and exp >= expected_deviation:
                sample_size = size
                break
        
        st.markdown(f'''
        <div style="background:{t['card']};border:2px solid {t['success']};border-radius:12px;padding:1.5rem;text-align:center;">
            <div style="font-size:0.85rem;color:{t['text_muted']};text-transform:uppercase;">Attribute Sample Size</div>
            <div style="font-size:3rem;font-weight:700;color:{t['success']};margin:0.5rem 0;">{sample_size}</div>
            <div style="font-size:0.85rem;color:{t['text_secondary']};">control tests required</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Evaluation guide
        st.markdown("#### Evaluation Guide")
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;">
            <table style="width:100%;color:{t['text']};">
                <tr style="border-bottom:1px solid {t['border']};">
                    <th style="text-align:left;padding:0.5rem;">Deviations Found</th>
                    <th style="text-align:left;padding:0.5rem;">Conclusion</th>
                </tr>
                <tr>
                    <td style="padding:0.5rem;">0</td>
                    <td style="padding:0.5rem;color:{t['success']};">✅ Rely on control</td>
                </tr>
                <tr>
                    <td style="padding:0.5rem;">1-2</td>
                    <td style="padding:0.5rem;color:{t['warning']};">⚠️ Evaluate nature of deviations</td>
                </tr>
                <tr>
                    <td style="padding:0.5rem;">3+</td>
                    <td style="padding:0.5rem;color:{t['danger']};">❌ Do not rely - increase substantive testing</td>
                </tr>
            </table>
        </div>
        ''', unsafe_allow_html=True)


def _render_mus_sampling(t: dict):
    """Render Monetary Unit Sampling calculator."""
    st.markdown("### 💰 Monetary Unit Sampling (MUS)")
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <p style="color:{t['text_secondary']};margin:0;">
        MUS is a statistical sampling method used for substantive testing that 
        gives larger monetary items a greater chance of selection.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Parameters")
        
        book_value = st.number_input(
            "Total Book Value (Rp)",
            min_value=1000000,
            max_value=100000000000,
            value=5000000000,
            step=100000000,
            format="%d"
        )
        
        tolerable_misstatement = st.number_input(
            "Tolerable Misstatement (Rp)",
            min_value=100000,
            max_value=10000000000,
            value=250000000,
            step=10000000,
            format="%d"
        )
        
        expected_misstatement = st.number_input(
            "Expected Misstatement (Rp)",
            min_value=0,
            max_value=5000000000,
            value=50000000,
            step=10000000,
            format="%d"
        )
        
        confidence = st.select_slider(
            "Confidence Level",
            options=[80, 85, 90, 95],
            value=95
        )
        
        # Reliability factors based on confidence
        reliability_factors = {80: 1.61, 85: 1.90, 90: 2.31, 95: 3.00}
        rf = reliability_factors[confidence]
    
    with col2:
        st.markdown("#### Calculation")
        
        # MUS Sample Size calculation
        # n = (BV × RF) / (TM - EM)
        denominator = tolerable_misstatement - expected_misstatement
        if denominator > 0:
            sample_size = math.ceil((book_value * rf) / denominator)
            sampling_interval = math.floor(book_value / sample_size)
        else:
            sample_size = 0
            sampling_interval = 0
        
        st.markdown(f'''
        <div style="background:{t['card']};border:2px solid {t['accent']};border-radius:12px;padding:1.5rem;text-align:center;margin-bottom:1rem;">
            <div style="font-size:0.85rem;color:{t['text_muted']};text-transform:uppercase;">MUS Sample Size</div>
            <div style="font-size:3rem;font-weight:700;color:{t['accent']};margin:0.5rem 0;">{sample_size}</div>
            <div style="font-size:0.85rem;color:{t['text_secondary']};">monetary units to test</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Sampling Interval</div>
                    <div style="font-size:1.1rem;font-weight:600;color:{t['text']};">Rp {sampling_interval:,.0f}</div>
                </div>
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Reliability Factor</div>
                    <div style="font-size:1.1rem;font-weight:600;color:{t['text']};">{rf}</div>
                </div>
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Tolerable Misstatement</div>
                    <div style="font-size:1.1rem;font-weight:600;color:{t['warning']};">Rp {tolerable_misstatement:,.0f}</div>
                </div>
                <div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">Expected Misstatement</div>
                    <div style="font-size:1.1rem;font-weight:600;color:{t['danger']};">Rp {expected_misstatement:,.0f}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Selection method
        st.markdown("#### Selection Process")
        st.markdown(f'''
        1. Generate random start between 1 and {sampling_interval:,.0f}
        2. Select item containing that monetary unit
        3. Add sampling interval to get next selection
        4. Repeat until all {sample_size} items selected
        ''')


def _render_sampling_guide(t: dict):
    """Render sampling guide and references."""
    st.markdown("### 📖 Sampling Guide")
    
    # When to use which sampling
    st.markdown("#### When to Use Each Method")
    
    methods = [
        {
            "name": "Random Sampling",
            "use_for": "General population testing",
            "when": "All items have equal importance",
            "example": "Testing expense vouchers"
        },
        {
            "name": "Attribute Sampling",
            "use_for": "Controls testing",
            "when": "Testing Yes/No compliance",
            "example": "Authorization signatures present"
        },
        {
            "name": "MUS (Monetary Unit)",
            "use_for": "Substantive testing",
            "when": "Testing monetary amounts",
            "example": "Accounts receivable confirmation"
        },
        {
            "name": "Stratified Sampling",
            "use_for": "Heterogeneous populations",
            "when": "Population has distinct groups",
            "example": "Loans by size category"
        },
        {
            "name": "Judgmental Sampling",
            "use_for": "Specific risk areas",
            "when": "Known risk factors exist",
            "example": "High-value transactions"
        },
    ]
    
    for method in methods:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="font-weight:600;color:{t['text']};margin-bottom:0.5rem;">{method['name']}</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;font-size:0.85rem;">
                <div>
                    <span style="color:{t['text_muted']};">Use for:</span>
                    <span style="color:{t['text']};">{method['use_for']}</span>
                </div>
                <div>
                    <span style="color:{t['text_muted']};">When:</span>
                    <span style="color:{t['text']};">{method['when']}</span>
                </div>
                <div>
                    <span style="color:{t['text_muted']};">Example:</span>
                    <span style="color:{t['accent']};">{method['example']}</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # ISA references
    st.markdown("#### ISA References")
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.5rem;">
        <ul style="color:{t['text_secondary']};margin:0;padding-left:1.25rem;">
            <li><strong>ISA 530</strong> - Audit Sampling</li>
            <li><strong>ISA 500</strong> - Audit Evidence</li>
            <li><strong>ISA 520</strong> - Analytical Procedures</li>
            <li><strong>ISA 330</strong> - Auditor's Responses to Assessed Risks</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sample size factors
    st.markdown("#### Factors Affecting Sample Size")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Increases Sample Size:**")
        st.markdown("""
        - Higher confidence level required
        - Lower tolerable error rate
        - Higher expected error rate
        - Larger population
        - Greater reliance on controls
        """)
    
    with col2:
        st.markdown("**Decreases Sample Size:**")
        st.markdown("""
        - Lower confidence level acceptable
        - Higher tolerable error rate
        - Lower expected error rate
        - Smaller population
        - Less reliance on controls
        """)
