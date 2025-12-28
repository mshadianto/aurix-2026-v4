"""
Regulatory Compliance Page Module for AURIX.
Track and monitor compliance with Indonesian financial regulations.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

from ui.styles.css_builder import get_current_theme
from ui.components import (
    render_page_header,
    render_footer,
    render_badge,
    render_metric_card,
    render_progress_bar
)
from data.seeds import REGULATIONS


class RegulatoryCompliancePage:
    """Regulatory compliance tracking and monitoring page."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for compliance tracking."""
        if 'compliance_status' not in st.session_state:
            st.session_state.compliance_status = self._generate_compliance_data()
    
    def _generate_compliance_data(self) -> Dict:
        """Generate sample compliance status data."""
        compliance = {}
        
        for category, regs in REGULATIONS.items():
            compliance[category] = {}
            for reg in regs:
                # Generate random compliance data
                status = random.choice(['Compliant', 'Partial', 'Non-Compliant', 'Under Review'])
                score = random.randint(60, 100) if status != 'Non-Compliant' else random.randint(30, 59)
                
                compliance[category][reg['code']] = {
                    'title': reg['title'],
                    'category': reg['category'],
                    'status': status,
                    'score': score,
                    'last_review': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
                    'next_review': (datetime.now() + timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d'),
                    'gaps': random.randint(0, 5),
                    'findings': random.randint(0, 3)
                }
        
        return compliance
    
    def render(self):
        """Render the Regulatory Compliance page."""
        render_page_header("Regulatory Compliance", "Track compliance with Indonesian financial regulations")
        
        t = get_current_theme()
        
        # Summary Dashboard
        self._render_summary_dashboard()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs for regulation categories
        tab_names = [f"📋 {cat}" for cat in REGULATIONS.keys()]
        tabs = st.tabs(tab_names + ["📊 Overview", "📅 Calendar"])
        
        for tab, category in zip(tabs[:-2], REGULATIONS.keys()):
            with tab:
                self._render_category_compliance(category)
        
        with tabs[-2]:
            self._render_compliance_overview()
        
        with tabs[-1]:
            self._render_compliance_calendar()
        
        render_footer()
    
    def _render_summary_dashboard(self):
        """Render summary metrics."""
        t = get_current_theme()
        
        compliance = st.session_state.compliance_status
        
        total_regs = sum(len(regs) for regs in compliance.values())
        compliant = sum(
            1 for cat in compliance.values() 
            for reg in cat.values() 
            if reg['status'] == 'Compliant'
        )
        partial = sum(
            1 for cat in compliance.values() 
            for reg in cat.values() 
            if reg['status'] == 'Partial'
        )
        non_compliant = sum(
            1 for cat in compliance.values() 
            for reg in cat.values() 
            if reg['status'] == 'Non-Compliant'
        )
        
        avg_score = sum(
            reg['score'] for cat in compliance.values() for reg in cat.values()
        ) / total_regs if total_regs > 0 else 0
        
        partial_review = partial + total_regs - compliant - non_compliant
        
        # Use Streamlit columns for metrics
        cols = st.columns(4)
        
        metrics_data = [
            ("TOTAL REGULATIONS", str(total_regs), "Tracked", t['accent']),
            ("COMPLIANT", str(compliant), f"{compliant/total_regs*100:.0f}% of total", t['success']),
            ("PARTIAL/REVIEW", str(partial_review), "Needs attention", t['danger'] if partial > 2 else t['warning']),
            ("AVERAGE SCORE", f"{avg_score:.0f}%", "Compliance score", t['success'] if avg_score >= 80 else t['warning']),
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
    
    def _render_category_compliance(self, category: str):
        """Render compliance status for a regulation category."""
        t = get_current_theme()
        
        st.markdown(f"### {category} Regulations")
        
        compliance = st.session_state.compliance_status.get(category, {})
        
        if not compliance:
            st.info("No regulations tracked for this category.")
            return
        
        for code, data in compliance.items():
            self._render_regulation_card(code, data)
    
    def _render_regulation_card(self, code: str, data: Dict):
        """Render a single regulation compliance card."""
        t = get_current_theme()
        
        status = data['status']
        score = data['score']
        
        # Status color mapping
        status_colors = {
            'Compliant': t['success'],
            'Partial': t['warning'],
            'Non-Compliant': t['danger'],
            'Under Review': t['accent']
        }
        status_color = status_colors.get(status, t['text_muted'])
        
        # Score color
        if score >= 80:
            score_color = t['success']
        elif score >= 60:
            score_color = t['warning']
        else:
            score_color = t['danger']
        
        with st.expander(f"📜 {code}: {data['title'][:50]}...", expanded=status == 'Non-Compliant'):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;">
                    <div style="margin-bottom:1rem;">
                        <span class="badge" style="background:{status_color}20;color:{status_color};">{status}</span>
                        <span style="margin-left:0.5rem;color:{t['text_muted']} !important;">{data['category']}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Full Title</span>
                        <span style="color:{t['text']} !important;">{data['title']}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Last Review</span>
                        <span style="color:{t['text']} !important;">{data['last_review']}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Next Review</span>
                        <span style="color:{t['text']} !important;">{data['next_review']}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Open Gaps</span>
                        <span style="color:{t['warning'] if data['gaps'] > 0 else t['success']} !important;">{data['gaps']}</span>
                    </div>
                    <div class="list-item">
                        <span style="color:{t['text_muted']} !important;">Related Findings</span>
                        <span style="color:{t['text']} !important;">{data['findings']}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                # Score gauge
                st.markdown(f'''
                <div class="pro-card" style="text-align:center;padding:1.5rem;">
                    <div style="font-size:0.85rem;color:{t['text_muted']} !important;margin-bottom:0.5rem;">
                        Compliance Score
                    </div>
                    <div style="font-size:2.5rem;font-weight:700;color:{score_color} !important;">
                        {score}%
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Progress bar
                st.markdown(f'''
                <div class="progress-bar" style="margin-top:0.5rem;">
                    <div class="progress-fill" style="width:{score}%;background:{score_color};"></div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Actions
                if st.button("📝 Update Status", key=f"update_{code}", use_container_width=True):
                    st.info("Opening compliance update form...")
                
                if st.button("📋 View Checklist", key=f"checklist_{code}", use_container_width=True):
                    st.info("Loading compliance checklist...")
    
    def _render_compliance_overview(self):
        """Render overall compliance overview."""
        t = get_current_theme()
        
        st.markdown("### 📊 Compliance Overview")
        
        compliance = st.session_state.compliance_status
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            st.markdown("#### Status Distribution")
            
            status_counts = {'Compliant': 0, 'Partial': 0, 'Non-Compliant': 0, 'Under Review': 0}
            
            for cat in compliance.values():
                for reg in cat.values():
                    status = reg['status']
                    if status in status_counts:
                        status_counts[status] += 1
            
            total = sum(status_counts.values())
            
            for status, count in status_counts.items():
                pct = (count / total * 100) if total > 0 else 0
                color = {
                    'Compliant': t['success'],
                    'Partial': t['warning'],
                    'Non-Compliant': t['danger'],
                    'Under Review': t['accent']
                }.get(status, t['text_muted'])
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;">{status}</span>
                        <span style="font-weight:600;color:{color} !important;">{count} ({pct:.0f}%)</span>
                    </div>
                    <div class="progress-bar" style="height:4px;">
                        <div class="progress-fill" style="width:{pct}%;background:{color};"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # By category
            st.markdown("#### By Regulation Category")
            
            for cat_name, regs in compliance.items():
                cat_total = len(regs)
                cat_compliant = len([r for r in regs.values() if r['status'] == 'Compliant'])
                cat_pct = (cat_compliant / cat_total * 100) if cat_total > 0 else 0
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;">{cat_name}</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{cat_compliant}/{cat_total}</span>
                    </div>
                    <div class="progress-bar" style="height:4px;">
                        <div class="progress-fill" style="width:{cat_pct}%;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            # Score distribution
            st.markdown("#### Score Distribution")
            
            score_ranges = {
                '90-100%': 0,
                '80-89%': 0,
                '70-79%': 0,
                '60-69%': 0,
                'Below 60%': 0
            }
            
            for cat in compliance.values():
                for reg in cat.values():
                    score = reg['score']
                    if score >= 90:
                        score_ranges['90-100%'] += 1
                    elif score >= 80:
                        score_ranges['80-89%'] += 1
                    elif score >= 70:
                        score_ranges['70-79%'] += 1
                    elif score >= 60:
                        score_ranges['60-69%'] += 1
                    else:
                        score_ranges['Below 60%'] += 1
            
            for range_name, count in score_ranges.items():
                color = t['success'] if '90' in range_name or '80' in range_name else (
                    t['warning'] if '70' in range_name or '60' in range_name else t['danger']
                )
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text']} !important;">{range_name}</span>
                        <span style="font-weight:600;color:{color} !important;">{count}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Key metrics
            st.markdown("#### Key Metrics")
            
            total_gaps = sum(reg['gaps'] for cat in compliance.values() for reg in cat.values())
            total_findings = sum(reg['findings'] for cat in compliance.values() for reg in cat.values())
            
            metrics = [
                ("Total Open Gaps", total_gaps, t['warning'] if total_gaps > 10 else t['success']),
                ("Related Findings", total_findings, t['text']),
                ("Upcoming Reviews", random.randint(3, 8), t['accent']),
                ("Overdue Reviews", random.randint(0, 2), t['danger'] if random.randint(0, 2) > 0 else t['success'])
            ]
            
            for name, value, color in metrics:
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text_secondary']} !important;">{name}</span>
                        <span style="font-weight:600;color:{color} !important;">{value}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_compliance_calendar(self):
        """Render compliance review calendar."""
        t = get_current_theme()
        
        st.markdown("### 📅 Review Calendar")
        
        compliance = st.session_state.compliance_status
        
        # Collect all review dates
        upcoming_reviews = []
        
        for cat, regs in compliance.items():
            for code, data in regs.items():
                review_date = datetime.strptime(data['next_review'], '%Y-%m-%d')
                upcoming_reviews.append({
                    'date': review_date,
                    'code': code,
                    'title': data['title'],
                    'category': cat,
                    'status': data['status']
                })
        
        # Sort by date
        upcoming_reviews.sort(key=lambda x: x['date'])
        
        # Filter options
        filter_period = st.selectbox(
            "Show reviews for",
            ["Next 30 days", "Next 60 days", "Next 90 days", "All upcoming"],
            key="calendar_filter"
        )
        
        cutoff_days = {
            "Next 30 days": 30,
            "Next 60 days": 60,
            "Next 90 days": 90,
            "All upcoming": 365
        }
        
        cutoff = datetime.now() + timedelta(days=cutoff_days[filter_period])
        filtered = [r for r in upcoming_reviews if r['date'] <= cutoff]
        
        st.markdown("---")
        
        if not filtered:
            st.info("No reviews scheduled for this period.")
            return
        
        st.markdown(f"**{len(filtered)} review(s) scheduled**")
        
        # Group by month
        current_month = None
        
        for review in filtered:
            month = review['date'].strftime('%B %Y')
            
            if month != current_month:
                current_month = month
                st.markdown(f"#### 📆 {month}")
            
            days_until = (review['date'] - datetime.now()).days
            
            if days_until < 0:
                urgency_color = t['danger']
                urgency_text = f"{abs(days_until)} days overdue"
            elif days_until <= 7:
                urgency_color = t['warning']
                urgency_text = f"{days_until} days"
            else:
                urgency_color = t['success']
                urgency_text = f"{days_until} days"
            
            st.markdown(f'''
            <div class="pro-card" style="padding:1rem;margin-bottom:0.5rem;border-left:4px solid {urgency_color};">
                <div style="display:flex;justify-content:space-between;align-items:start;">
                    <div>
                        <div style="font-weight:600;color:{t['text']} !important;">{review['code']}</div>
                        <div style="font-size:0.85rem;color:{t['text_secondary']} !important;">{review['title'][:50]}...</div>
                        <div style="font-size:0.8rem;color:{t['text_muted']} !important;margin-top:0.25rem;">
                            {review['category']} • {review['date'].strftime('%d %B %Y')}
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.8rem;color:{urgency_color} !important;font-weight:600;">
                            {urgency_text}
                        </span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)


def render():
    """Entry point for the Regulatory Compliance page."""
    page = RegulatoryCompliancePage()
    page.render()
