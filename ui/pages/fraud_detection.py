"""
Fraud Detection Page Module for AURIX.
Red flag analysis, fraud indicators, and investigation tools.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid
import random

from ui.styles.css_builder import get_current_theme
from ui.components import (
    render_page_header,
    render_footer,
    render_badge,
    risk_badge,
    render_metric_card,
    render_alert
)
from data.seeds import FRAUD_RED_FLAGS


class FraudDetectionPage:
    """Fraud Detection page with red flag analysis tools."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for fraud detection."""
        if 'fraud_cases' not in st.session_state:
            st.session_state.fraud_cases = self._generate_sample_cases()
        
        if 'fraud_analyses' not in st.session_state:
            st.session_state.fraud_analyses = []
    
    def _generate_sample_cases(self) -> List[Dict]:
        """Generate sample fraud cases for demo."""
        cases = []
        statuses = ['Open', 'Under Investigation', 'Escalated', 'Closed - Confirmed', 'Closed - False Positive']
        categories = list(FRAUD_RED_FLAGS.keys())
        
        for i in range(8):
            category = random.choice(categories)
            flags = FRAUD_RED_FLAGS[category]
            selected_flags = random.sample(flags, min(random.randint(2, 5), len(flags)))
            
            cases.append({
                'id': f"FRD{i+1:04d}",
                'title': f"Suspected {category.replace('_', ' ').title()} Case",
                'category': category,
                'red_flags': selected_flags,
                'risk_score': random.randint(45, 95),
                'status': random.choice(statuses),
                'amount': random.randint(50000000, 5000000000),
                'created_at': (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d'),
                'investigator': random.choice(['Ahmad F.', 'Budi S.', 'Citra D.', 'Dewi A.', 'Unassigned']),
                'notes': ''
            })
        
        return sorted(cases, key=lambda x: x['risk_score'], reverse=True)
    
    def render(self):
        """Render the Fraud Detection page."""
        render_page_header("Fraud Detection", "Red Flag Analysis & Investigation Tools")
        
        t = get_current_theme()
        
        # Summary Dashboard
        self._render_summary_dashboard()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Red Flag Scanner",
            "📋 Case Management",
            "🏴 Red Flag Library",
            "📊 Analytics"
        ])
        
        with tab1:
            self._render_red_flag_scanner()
        
        with tab2:
            self._render_case_management()
        
        with tab3:
            self._render_red_flag_library()
        
        with tab4:
            self._render_fraud_analytics()
        
        render_footer()
    
    def _render_summary_dashboard(self):
        """Render summary metrics."""
        t = get_current_theme()
        
        cases = st.session_state.fraud_cases
        
        open_cases = len([c for c in cases if c['status'] in ['Open', 'Under Investigation', 'Escalated']])
        high_risk = len([c for c in cases if c['risk_score'] >= 70])
        confirmed = len([c for c in cases if 'Confirmed' in c['status']])
        total_exposure = sum(c['amount'] for c in cases if c['status'] not in ['Closed - False Positive'])
        
        # Use Streamlit columns for metrics
        cols = st.columns(4)
        
        metrics_data = [
            ("OPEN CASES", str(open_cases), "Under investigation", t['danger'] if open_cases > 5 else t['success']),
            ("HIGH RISK", str(high_risk), "Score ≥ 70", t['danger'] if high_risk > 0 else t['success']),
            ("CONFIRMED FRAUD", str(confirmed), "This quarter", t['warning']),
            ("TOTAL EXPOSURE", f"Rp {total_exposure/1000000000:.1f}B", "Potential loss", t['danger']),
        ]
        
        for col, (label, value, change, color) in zip(cols, metrics_data):
            with col:
                st.markdown(f'''
                <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;">
                    <div style="font-size:0.75rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:{t['text_muted']} !important;margin-bottom:0.5rem;">{label}</div>
                    <div style="font-size:1.75rem;font-weight:700;color:{t['text']} !important;">{value}</div>
                    <div style="font-size:0.75rem;margin-top:0.25rem;color:{color} !important;">{change}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_red_flag_scanner(self):
        """Render the red flag scanner tool."""
        t = get_current_theme()
        
        st.markdown("### 🔍 Red Flag Scanner")
        
        st.markdown(f'''
        <div class="pro-card" style="background:{t['bg_secondary']};margin-bottom:1rem;">
            <p style="color:{t['text_secondary']} !important;margin:0;">
                Analyze transactions or activities against known fraud indicators. Select applicable red flags to calculate a risk score.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Transaction/Activity Details")
            
            case_title = st.text_input(
                "Case Title",
                placeholder="e.g., Unusual Transfer Pattern - Account XXX",
                key="scanner_title"
            )
            
            fraud_category = st.selectbox(
                "Fraud Category",
                options=list(FRAUD_RED_FLAGS.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                key="scanner_category"
            )
            
            amount = st.number_input(
                "Transaction Amount (Rp)",
                min_value=0,
                value=100000000,
                step=10000000,
                key="scanner_amount"
            )
            
            description = st.text_area(
                "Description",
                height=100,
                placeholder="Describe the suspicious activity or transaction...",
                key="scanner_description"
            )
        
        with col2:
            st.markdown("#### Red Flag Checklist")
            
            available_flags = FRAUD_RED_FLAGS.get(fraud_category, [])
            
            selected_flags = []
            for i, flag in enumerate(available_flags):
                if st.checkbox(flag, key=f"flag_{fraud_category}_{i}"):
                    selected_flags.append(flag)
            
            # Calculate risk score
            if available_flags:
                flag_ratio = len(selected_flags) / len(available_flags)
                risk_score = int(flag_ratio * 100)
                
                # Adjust based on amount
                if amount > 1000000000:
                    risk_score = min(risk_score + 15, 100)
                elif amount > 500000000:
                    risk_score = min(risk_score + 10, 100)
            else:
                risk_score = 0
        
        st.markdown("---")
        
        # Risk Score Display
        if risk_score >= 70:
            score_color = t['danger']
            risk_level = "HIGH"
        elif risk_score >= 40:
            score_color = t['warning']
            risk_level = "MEDIUM"
        else:
            score_color = t['success']
            risk_level = "LOW"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:2rem;background:linear-gradient(135deg, {score_color}15, {score_color}05);border:2px solid {score_color};">
                <div style="font-size:0.9rem;color:{t['text_muted']} !important;margin-bottom:0.5rem;">Fraud Risk Score</div>
                <div style="font-size:4rem;font-weight:700;color:{score_color} !important;">{risk_score}</div>
                <div style="font-size:1.25rem;font-weight:600;color:{score_color} !important;">{risk_level} RISK</div>
                <div style="margin-top:1rem;font-size:0.85rem;color:{t['text_secondary']} !important;">
                    {len(selected_flags)} of {len(available_flags)} red flags identified
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Action Buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Create Case", type="primary", use_container_width=True):
                if not case_title:
                    st.error("Please enter a case title.")
                elif not selected_flags:
                    st.warning("No red flags selected. Please select applicable red flags.")
                else:
                    new_case = {
                        'id': f"FRD{len(st.session_state.fraud_cases)+1:04d}",
                        'title': case_title,
                        'category': fraud_category,
                        'red_flags': selected_flags,
                        'risk_score': risk_score,
                        'status': 'Open',
                        'amount': amount,
                        'created_at': datetime.now().strftime('%Y-%m-%d'),
                        'investigator': 'Unassigned',
                        'notes': description
                    }
                    st.session_state.fraud_cases.append(new_case)
                    st.success(f"✓ Case {new_case['id']} created successfully!")
                    st.balloons()
        
        with col2:
            if st.button("💾 Save Analysis", use_container_width=True):
                analysis = {
                    'id': str(uuid.uuid4())[:8],
                    'category': fraud_category,
                    'flags': selected_flags,
                    'score': risk_score,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                st.session_state.fraud_analyses.append(analysis)
                st.success("✓ Analysis saved")
        
        with col3:
            if st.button("🔄 Clear", use_container_width=True):
                st.rerun()
    
    def _render_case_management(self):
        """Render case management interface."""
        t = get_current_theme()
        
        st.markdown("### 📋 Fraud Case Management")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", "Open", "Under Investigation", "Escalated", "Closed - Confirmed", "Closed - False Positive"],
                key="fraud_case_status"
            )
        
        with col2:
            category_filter = st.selectbox(
                "Category",
                ["All"] + [k.replace('_', ' ').title() for k in FRAUD_RED_FLAGS.keys()],
                key="fraud_case_category"
            )
        
        with col3:
            risk_filter = st.selectbox(
                "Risk Level",
                ["All", "High (≥70)", "Medium (40-69)", "Low (<40)"],
                key="fraud_case_risk"
            )
        
        st.markdown("---")
        
        # Apply filters
        cases = st.session_state.fraud_cases.copy()
        
        if status_filter != "All":
            cases = [c for c in cases if c['status'] == status_filter]
        
        if category_filter != "All":
            cat_key = category_filter.lower().replace(' ', '_')
            cases = [c for c in cases if c['category'].lower() == cat_key]
        
        if risk_filter == "High (≥70)":
            cases = [c for c in cases if c['risk_score'] >= 70]
        elif risk_filter == "Medium (40-69)":
            cases = [c for c in cases if 40 <= c['risk_score'] < 70]
        elif risk_filter == "Low (<40)":
            cases = [c for c in cases if c['risk_score'] < 40]
        
        if not cases:
            st.info("No cases match the current filters.")
            return
        
        st.markdown(f"**Showing {len(cases)} case(s)**")
        
        for case in cases:
            self._render_case_card(case)
    
    def _render_case_card(self, case: Dict):
        """Render a single fraud case card."""
        t = get_current_theme()
        
        score = case['risk_score']
        if score >= 70:
            score_color = t['danger']
        elif score >= 40:
            score_color = t['warning']
        else:
            score_color = t['success']
        
        status = case['status']
        if 'Open' in status or 'Investigation' in status:
            status_color = t['warning']
        elif 'Escalated' in status:
            status_color = t['danger']
        elif 'Confirmed' in status:
            status_color = t['danger']
        else:
            status_color = t['success']
        
        with st.expander(f"🔴 {case['id']}: {case['title']} (Score: {score})", expanded=case['status'] == 'Open'):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;">
                    <div style="display:flex;gap:1rem;margin-bottom:1rem;">
                        <span class="badge" style="background:{score_color}20;color:{score_color};">Risk: {score}</span>
                        <span class="badge" style="background:{status_color}20;color:{status_color};">{status}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Category</span>
                        <span style="color:{t['text']} !important;">{case['category'].replace('_', ' ').title()}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Amount</span>
                        <span style="font-weight:600;color:{t['text']} !important;">Rp {case['amount']:,}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Investigator</span>
                        <span style="color:{t['text']} !important;">{case['investigator']}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Created</span>
                        <span style="color:{t['text']} !important;">{case['created_at']}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Red flags identified
                st.markdown("**Red Flags Identified:**")
                for flag in case['red_flags']:
                    st.markdown(f"- 🚩 {flag}")
                
                if case['notes']:
                    st.markdown(f"**Notes:** {case['notes']}")
            
            with col2:
                st.markdown("#### Actions")
                
                new_status = st.selectbox(
                    "Update Status",
                    ["Open", "Under Investigation", "Escalated", "Closed - Confirmed", "Closed - False Positive"],
                    index=["Open", "Under Investigation", "Escalated", "Closed - Confirmed", "Closed - False Positive"].index(case['status']),
                    key=f"case_status_{case['id']}"
                )
                
                if st.button("Update", key=f"update_case_{case['id']}"):
                    case['status'] = new_status
                    st.success("✓ Status updated")
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("📝 Add Notes", key=f"notes_{case['id']}"):
                    st.session_state[f'show_notes_{case["id"]}'] = True
                
                if st.session_state.get(f'show_notes_{case["id"]}', False):
                    notes = st.text_area("Notes", value=case.get('notes', ''), key=f"notes_input_{case['id']}")
                    if st.button("Save Notes", key=f"save_notes_{case['id']}"):
                        case['notes'] = notes
                        st.success("✓ Notes saved")
    
    def _render_red_flag_library(self):
        """Render the red flag reference library."""
        t = get_current_theme()
        
        st.markdown("### 🏴 Red Flag Library")
        
        st.markdown(f'''
        <div class="pro-card" style="background:{t['bg_secondary']};margin-bottom:1rem;">
            <p style="color:{t['text_secondary']} !important;margin:0;">
                Reference library of fraud red flags organized by category. Use these indicators during audit procedures to identify potential fraud.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        for category, flags in FRAUD_RED_FLAGS.items():
            with st.expander(f"📂 {category.replace('_', ' ').title()} ({len(flags)} indicators)", expanded=False):
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;">
                ''', unsafe_allow_html=True)
                
                for i, flag in enumerate(flags, 1):
                    st.markdown(f'''
                    <div style="padding:0.5rem 0;border-bottom:1px solid {t['border']};display:flex;align-items:center;gap:0.5rem;">
                        <span style="color:{t['warning']} !important;">🚩</span>
                        <span style="color:{t['text']} !important;">{flag}</span>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_fraud_analytics(self):
        """Render fraud analytics dashboard."""
        t = get_current_theme()
        
        st.markdown("### 📊 Fraud Analytics")
        
        cases = st.session_state.fraud_cases
        
        if not cases:
            st.info("No cases available for analytics.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cases by Category
            st.markdown("#### Cases by Category")
            
            category_counts = {}
            for case in cases:
                cat = case['category'].replace('_', ' ').title()
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            total = len(cases)
            for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                pct = (count / total * 100) if total > 0 else 0
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;font-size:0.9rem;">{cat}</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{count}</span>
                    </div>
                    <div class="progress-bar" style="height:4px;">
                        <div class="progress-fill" style="width:{pct}%;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Risk Distribution
            st.markdown("#### Risk Score Distribution")
            
            high = len([c for c in cases if c['risk_score'] >= 70])
            medium = len([c for c in cases if 40 <= c['risk_score'] < 70])
            low = len([c for c in cases if c['risk_score'] < 40])
            
            for level, count, color in [("High Risk", high, t['danger']), ("Medium Risk", medium, t['warning']), ("Low Risk", low, t['success'])]:
                pct = (count / total * 100) if total > 0 else 0
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text']} !important;">{level}</span>
                        <span style="font-weight:600;color:{color} !important;">{count} ({pct:.0f}%)</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            # Case Status
            st.markdown("#### Case Status")
            
            status_counts = {}
            for case in cases:
                status = case['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
                if 'Open' in status or 'Investigation' in status:
                    color = t['warning']
                elif 'Escalated' in status or 'Confirmed' in status:
                    color = t['danger']
                else:
                    color = t['success']
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text']} !important;">{status}</span>
                        <span style="font-weight:600;color:{color} !important;">{count}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Financial Exposure
            st.markdown("#### Financial Exposure")
            
            open_exposure = sum(c['amount'] for c in cases if c['status'] in ['Open', 'Under Investigation', 'Escalated'])
            confirmed_loss = sum(c['amount'] for c in cases if 'Confirmed' in c['status'])
            
            st.markdown(f'''
            <div class="pro-card" style="padding:1rem;margin-bottom:0.5rem;">
                <div style="text-align:center;">
                    <div style="font-size:0.85rem;color:{t['text_muted']} !important;">Open Cases Exposure</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{t['warning']} !important;">
                        Rp {open_exposure/1000000000:.2f}B
                    </div>
                </div>
            </div>
            <div class="pro-card" style="padding:1rem;">
                <div style="text-align:center;">
                    <div style="font-size:0.85rem;color:{t['text_muted']} !important;">Confirmed Fraud Loss</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{t['danger']} !important;">
                        Rp {confirmed_loss/1000000000:.2f}B
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)


def render():
    """Entry point for the Fraud Detection page."""
    page = FraudDetectionPage()
    page.render()
