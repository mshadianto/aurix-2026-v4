"""
Interactive Risk Universe Module for AURIX.
Visual exploration of audit universe and risk relationships.
"""

import streamlit as st
from datetime import datetime
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer
from data.seeds import AUDIT_UNIVERSE, RISK_FACTORS


def render():
    """Render the risk universe page."""
    t = get_current_theme()
    
    render_page_header(
        "🌐 Risk Universe Explorer",
        "Interactive exploration of your audit universe and risk landscape"
    )
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Universe Map",
        "🔗 Risk Network",
        "📊 Risk Matrix",
        "🎯 Focus Areas"
    ])
    
    with tab1:
        _render_universe_map(t)
    
    with tab2:
        _render_risk_network(t)
    
    with tab3:
        _render_risk_matrix(t)
    
    with tab4:
        _render_focus_areas(t)
    
    render_footer()


def _render_universe_map(t: dict):
    """Render interactive universe map."""
    st.markdown("### 🌐 Audit Universe Map")
    st.markdown("Click on any domain to explore its audit areas and associated risks.")
    
    categories = list(AUDIT_UNIVERSE.keys())
    colors = [t['primary'], t['accent'], t['success'], t['warning'], t['danger'], "#8b5cf6"]
    icons = ["⚖️", "⚠️", "💰", "⚙️", "💻", "🛡️"]
    labels = ["Governance", "Risk Mgmt", "Financial", "Operations", "Technology", "AML/CFT"]
    
    st.markdown("---")
    
    # Center hub
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        hub_html = (
            '<div style="text-align:center;padding:2rem;">'
            '<div style="display:inline-block;width:120px;height:120px;background:linear-gradient(135deg, ' + t['primary'] + ', ' + t['accent'] + ');border-radius:50%;line-height:120px;box-shadow:0 0 40px ' + t['primary'] + '40;">'
            '<span style="color:white;font-size:2rem;">🏛️</span>'
            '</div>'
            '<div style="margin-top:0.5rem;font-weight:700;color:' + t['text'] + ';">AUDIT UNIVERSE</div>'
            '</div>'
        )
        st.markdown(hub_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Domain circles in grid
    cols = st.columns(6)
    
    for i, col in enumerate(cols):
        with col:
            color = colors[i]
            icon = icons[i]
            label = labels[i]
            
            card_html = (
                '<div style="text-align:center;padding:1rem;">'
                '<div style="width:80px;height:80px;margin:0 auto;background:linear-gradient(135deg, ' + color + ', ' + color + 'dd);border-radius:50%;line-height:80px;box-shadow:0 4px 15px ' + color + '40;cursor:pointer;">'
                '<span style="color:white;font-size:1.5rem;">' + icon + '</span>'
                '</div>'
                '<div style="font-size:0.75rem;font-weight:600;color:' + t['text'] + ';margin-top:0.75rem;">' + label + '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Category selection
    selected_category = st.selectbox("Select Domain to Explore", options=categories)
    
    if selected_category:
        areas = AUDIT_UNIVERSE[selected_category]
        st.markdown("#### 📋 " + selected_category + " - Audit Areas")
        
        cols = st.columns(3)
        for i, area in enumerate(areas):
            risk_level = random.choice(["High", "Medium", "Low"])
            risk_colors = {"High": t['danger'], "Medium": t['warning'], "Low": t['success']}
            risk_color = risk_colors[risk_level]
            last_audit = str(random.randint(1, 18)) + " months ago"
            
            with cols[i % 3]:
                html = (
                    '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:12px;padding:1rem;margin-bottom:0.75rem;">'
                    '<div style="font-weight:600;color:' + t['text'] + ';margin-bottom:0.5rem;">' + area + '</div>'
                    '<div style="display:flex;justify-content:space-between;align-items:center;">'
                    '<span style="font-size:0.7rem;color:' + t['text_muted'] + ';">Last: ' + last_audit + '</span>'
                    '<span style="background:' + risk_color + '20;color:' + risk_color + ';padding:0.2rem 0.5rem;border-radius:4px;font-size:0.7rem;font-weight:600;">' + risk_level + '</span>'
                    '</div>'
                    '</div>'
                )
                st.markdown(html, unsafe_allow_html=True)


def _render_risk_network(t: dict):
    """Render risk relationship network using simple layout."""
    st.markdown("### 🔗 Risk Relationship Network")
    st.markdown("Visualize how different risks are interconnected across your organization.")
    
    # Instead of complex CSS positioning, use a simple grid layout
    risks_data = [
        {"name": "Credit Risk", "icon": "💳", "color": t['danger'], "connections": 6},
        {"name": "Market Risk", "icon": "📈", "color": t['warning'], "connections": 4},
        {"name": "Liquidity Risk", "icon": "💧", "color": t['primary'], "connections": 5},
        {"name": "Operational Risk", "icon": "⚙️", "color": t['accent'], "connections": 5},
        {"name": "Compliance Risk", "icon": "📋", "color": t['success'], "connections": 4},
        {"name": "Cyber Risk", "icon": "🔐", "color": "#8b5cf6", "connections": 5},
    ]
    
    st.markdown("#### Risk Nodes")
    cols = st.columns(3)
    
    for i, risk in enumerate(risks_data):
        with cols[i % 3]:
            card_html = (
                '<div style="background:' + t['card'] + ';border:2px solid ' + risk['color'] + ';border-radius:16px;padding:1.5rem;text-align:center;margin-bottom:1rem;">'
                '<div style="font-size:2.5rem;margin-bottom:0.5rem;">' + risk['icon'] + '</div>'
                '<div style="font-weight:700;color:' + t['text'] + ';margin-bottom:0.25rem;">' + risk['name'] + '</div>'
                '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">' + str(risk['connections']) + ' connections</div>'
                '<div style="width:60px;height:4px;background:' + risk['color'] + ';border-radius:2px;margin:0.5rem auto 0;"></div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Risk correlation matrix
    st.markdown("#### 📊 Risk Correlation Matrix")
    
    risks = ["Credit", "Market", "Liquidity", "Operational", "Compliance", "Cyber"]
    correlations = [
        [1.0, 0.6, 0.8, 0.4, 0.5, 0.3],
        [0.6, 1.0, 0.7, 0.3, 0.2, 0.4],
        [0.8, 0.7, 1.0, 0.4, 0.3, 0.3],
        [0.4, 0.3, 0.4, 1.0, 0.6, 0.7],
        [0.5, 0.2, 0.3, 0.6, 1.0, 0.5],
        [0.3, 0.4, 0.3, 0.7, 0.5, 1.0],
    ]
    
    # Build table
    table_html = '<table style="width:100%;border-collapse:collapse;font-size:0.8rem;">'
    table_html += '<tr><th style="padding:0.5rem;background:' + t['bg_secondary'] + ';color:' + t['text'] + ';"></th>'
    
    for risk in risks:
        table_html += '<th style="padding:0.5rem;background:' + t['bg_secondary'] + ';color:' + t['text'] + ';text-align:center;">' + risk + '</th>'
    
    table_html += '</tr>'
    
    for i, row_risk in enumerate(risks):
        table_html += '<tr>'
        table_html += '<td style="padding:0.5rem;background:' + t['bg_secondary'] + ';color:' + t['text'] + ';font-weight:600;">' + row_risk + '</td>'
        
        for j, corr in enumerate(correlations[i]):
            if corr >= 0.7:
                bg = t['danger'] + '30'
            elif corr >= 0.5:
                bg = t['warning'] + '30'
            else:
                bg = t['success'] + '30'
            
            table_html += '<td style="padding:0.5rem;background:' + bg + ';color:' + t['text'] + ';text-align:center;">' + str(corr) + '</td>'
        
        table_html += '</tr>'
    
    table_html += '</table>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Legend
    st.markdown("<br>", unsafe_allow_html=True)
    legend_html = (
        '<div style="display:flex;gap:2rem;justify-content:center;font-size:0.8rem;">'
        '<div><span style="display:inline-block;width:16px;height:16px;background:' + t['danger'] + '30;border-radius:4px;vertical-align:middle;margin-right:0.5rem;"></span>High (≥0.7)</div>'
        '<div><span style="display:inline-block;width:16px;height:16px;background:' + t['warning'] + '30;border-radius:4px;vertical-align:middle;margin-right:0.5rem;"></span>Medium (0.5-0.7)</div>'
        '<div><span style="display:inline-block;width:16px;height:16px;background:' + t['success'] + '30;border-radius:4px;vertical-align:middle;margin-right:0.5rem;"></span>Low (<0.5)</div>'
        '</div>'
    )
    st.markdown(legend_html, unsafe_allow_html=True)


def _render_risk_matrix(t: dict):
    """Render risk assessment matrix."""
    st.markdown("### 📊 Risk Assessment Matrix")
    st.markdown("Traditional 5x5 risk matrix for impact vs likelihood assessment.")
    
    # Create matrix header
    impacts = ["Negligible", "Minor", "Moderate", "Major", "Severe"]
    likelihoods = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]
    
    # Risk matrix colors (5x5)
    matrix_colors = [
        [t['success'], t['success'], t['warning'], t['warning'], t['danger']],
        [t['success'], t['warning'], t['warning'], t['danger'], t['danger']],
        [t['warning'], t['warning'], t['danger'], t['danger'], t['danger']],
        [t['warning'], t['danger'], t['danger'], t['danger'], t['danger']],
        [t['danger'], t['danger'], t['danger'], t['danger'], t['danger']],
    ]
    
    # Build matrix
    matrix_html = '<table style="width:100%;border-collapse:collapse;text-align:center;">'
    
    # Header row
    matrix_html += '<tr><th style="padding:0.75rem;background:' + t['bg_secondary'] + ';"></th>'
    for impact in impacts:
        matrix_html += '<th style="padding:0.75rem;background:' + t['bg_secondary'] + ';color:' + t['text'] + ';font-size:0.75rem;">' + impact + '</th>'
    matrix_html += '</tr>'
    
    # Data rows
    for i, likelihood in enumerate(reversed(likelihoods)):
        row_idx = 4 - i
        matrix_html += '<tr>'
        matrix_html += '<td style="padding:0.75rem;background:' + t['bg_secondary'] + ';color:' + t['text'] + ';font-size:0.75rem;font-weight:600;">' + likelihood + '</td>'
        
        for j, impact in enumerate(impacts):
            color = matrix_colors[row_idx][j]
            matrix_html += '<td style="padding:1rem;background:' + color + '40;border:1px solid ' + t['border'] + ';"></td>'
        
        matrix_html += '</tr>'
    
    matrix_html += '</table>'
    
    st.markdown(matrix_html, unsafe_allow_html=True)
    
    # Legend
    st.markdown("<br>", unsafe_allow_html=True)
    
    legend_cols = st.columns(3)
    with legend_cols[0]:
        st.markdown(
            '<div style="background:' + t['success'] + '40;padding:0.5rem;border-radius:8px;text-align:center;">'
            '<div style="font-weight:600;color:' + t['text'] + ';">Low Risk</div>'
            '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">Accept / Monitor</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with legend_cols[1]:
        st.markdown(
            '<div style="background:' + t['warning'] + '40;padding:0.5rem;border-radius:8px;text-align:center;">'
            '<div style="font-weight:600;color:' + t['text'] + ';">Medium Risk</div>'
            '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">Mitigate / Control</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with legend_cols[2]:
        st.markdown(
            '<div style="background:' + t['danger'] + '40;padding:0.5rem;border-radius:8px;text-align:center;">'
            '<div style="font-weight:600;color:' + t['text'] + ';">High Risk</div>'
            '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">Urgent Action</div>'
            '</div>',
            unsafe_allow_html=True
        )


def _render_focus_areas(t: dict):
    """Render focus areas for audit attention."""
    st.markdown("### 🎯 Priority Focus Areas")
    st.markdown("Areas requiring immediate audit attention based on risk assessment.")
    
    focus_areas = [
        {"area": "Credit Underwriting", "score": 92, "category": "Credit Risk", "status": "Critical"},
        {"area": "AML Transaction Monitoring", "score": 88, "category": "Compliance", "status": "Critical"},
        {"area": "IT Access Controls", "score": 75, "category": "IT/Cyber", "status": "High"},
        {"area": "Treasury Operations", "score": 70, "category": "Operational", "status": "High"},
        {"area": "Vendor Management", "score": 65, "category": "Operational", "status": "Medium"},
        {"area": "Business Continuity", "score": 60, "category": "Operational", "status": "Medium"},
    ]
    
    for item in focus_areas:
        if item['status'] == "Critical":
            status_color = t['danger']
        elif item['status'] == "High":
            status_color = t['warning']
        else:
            status_color = t['accent']
        
        card_html = (
            '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-left:4px solid ' + status_color + ';border-radius:0 12px 12px 0;padding:1rem;margin-bottom:0.75rem;">'
            '<div style="display:flex;justify-content:space-between;align-items:center;">'
            '<div>'
            '<div style="font-weight:600;color:' + t['text'] + ';">' + item['area'] + '</div>'
            '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">' + item['category'] + '</div>'
            '</div>'
            '<div style="text-align:right;">'
            '<div style="font-size:1.5rem;font-weight:700;color:' + status_color + ';">' + str(item['score']) + '</div>'
            '<span style="background:' + status_color + '20;color:' + status_color + ';padding:0.2rem 0.5rem;border-radius:4px;font-size:0.7rem;font-weight:600;">' + item['status'] + '</span>'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
