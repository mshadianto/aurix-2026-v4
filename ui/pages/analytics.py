"""
Analytics Page Module for AURIX.
Comprehensive audit analytics and reporting dashboard.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

from ui.styles.css_builder import get_current_theme
from ui.components import (
    render_page_header,
    render_footer,
    render_metric_card,
    render_progress_bar
)
from data.seeds import AUDIT_UNIVERSE


class AnalyticsPage:
    """Analytics and reporting dashboard page."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for analytics."""
        if 'analytics_data' not in st.session_state:
            st.session_state.analytics_data = self._generate_analytics_data()
    
    def _generate_analytics_data(self) -> Dict:
        """Generate sample analytics data."""
        return {
            'audits_completed': random.randint(15, 30),
            'audits_in_progress': random.randint(3, 8),
            'findings_this_year': random.randint(50, 120),
            'high_risk_findings': random.randint(10, 30),
            'closure_rate': random.randint(75, 95),
            'avg_audit_days': random.randint(15, 45),
            'coverage_score': random.randint(70, 95),
            'resource_utilization': random.randint(60, 90)
        }
    
    def render(self):
        """Render the Analytics page."""
        render_page_header("Analytics", "Comprehensive audit analytics and insights")
        
        t = get_current_theme()
        
        # Time period selector
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            period = st.selectbox(
                "Time Period",
                ["This Year", "Last 12 Months", "Last Quarter", "Last Month"],
                key="analytics_period"
            )
        
        with col2:
            comparison = st.checkbox("Show Year-over-Year", value=True, key="show_yoy")
        
        st.markdown("---")
        
        # Summary Metrics
        self._render_summary_metrics()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs for different analytics views
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Performance",
            "🎯 Coverage",
            "📈 Trends",
            "📋 Reports"
        ])
        
        with tab1:
            self._render_performance_analytics()
        
        with tab2:
            self._render_coverage_analytics()
        
        with tab3:
            self._render_trend_analytics()
        
        with tab4:
            self._render_reports()
        
        render_footer()
    
    def _render_summary_metrics(self):
        """Render summary metrics."""
        t = get_current_theme()
        data = st.session_state.analytics_data
        
        # Use Streamlit columns for metrics
        cols = st.columns(4)
        
        metrics_data = [
            ("AUDITS COMPLETED", str(data['audits_completed']), "+12% vs LY", t['success']),
            ("IN PROGRESS", str(data['audits_in_progress']), "On track", t['accent']),
            ("TOTAL FINDINGS", str(data['findings_this_year']), f"{data['high_risk_findings']} high risk", t['danger'] if data['high_risk_findings'] > 20 else t['warning']),
            ("CLOSURE RATE", f"{data['closure_rate']}%", "+5% improvement", t['success']),
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
    
    def _render_performance_analytics(self):
        """Render performance analytics."""
        t = get_current_theme()
        data = st.session_state.analytics_data
        
        st.markdown("### 📊 Audit Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Audit efficiency
            st.markdown("#### Efficiency Metrics")
            
            efficiency_metrics = [
                ("Average Audit Duration", f"{data['avg_audit_days']} days", 30),
                ("On-Time Completion", f"{random.randint(80, 95)}%", 85),
                ("Resource Utilization", f"{data['resource_utilization']}%", 80),
                ("Documentation Quality", f"{random.randint(75, 95)}%", 80)
            ]
            
            for name, value, target in efficiency_metrics:
                actual = int(value.replace('%', '').replace(' days', ''))
                pct = min((actual / target * 100), 100) if 'days' not in value else (target / actual * 100)
                color = t['success'] if pct >= 90 else (t['warning'] if pct >= 70 else t['danger'])
                
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;margin-bottom:0.75rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;">{name}</span>
                        <span style="font-weight:600;color:{color} !important;">{value}</span>
                    </div>
                    <div class="progress-bar" style="height:6px;">
                        <div class="progress-fill" style="width:{min(pct, 100)}%;background:{color};"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Team performance
            st.markdown("#### Team Performance")
            
            team_members = [
                ("Ahmad Fauzi", 12, 95),
                ("Budi Santoso", 10, 88),
                ("Citra Dewi", 8, 92),
                ("Dewi Anggraeni", 11, 85),
                ("Eko Prasetyo", 9, 90)
            ]
            
            for name, audits, quality in team_members:
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-weight:600;color:{t['text']} !important;">{name}</div>
                            <div style="font-size:0.8rem;color:{t['text_muted']} !important;">{audits} audits completed</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.25rem;font-weight:700;color:{t['success'] if quality >= 90 else t['warning']} !important;">
                                {quality}%
                            </div>
                            <div style="font-size:0.7rem;color:{t['text_muted']} !important;">Quality</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            # Finding trends
            st.markdown("#### Findings by Severity")
            
            severity_data = [
                ("Critical", random.randint(2, 8), t['danger']),
                ("High", random.randint(10, 25), t['danger']),
                ("Medium", random.randint(30, 50), t['warning']),
                ("Low", random.randint(20, 40), t['success'])
            ]
            
            total_findings = sum(x[1] for x in severity_data)
            
            for severity, count, color in severity_data:
                pct = (count / total_findings * 100) if total_findings > 0 else 0
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;">{severity}</span>
                        <span style="font-weight:600;color:{color} !important;">{count} ({pct:.0f}%)</span>
                    </div>
                    <div class="progress-bar" style="height:8px;">
                        <div class="progress-fill" style="width:{pct}%;background:{color};"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Finding status
            st.markdown("#### Findings by Status")
            
            status_data = [
                ("Open", random.randint(15, 30), t['warning']),
                ("In Progress", random.randint(10, 25), t['accent']),
                ("Closed", random.randint(40, 70), t['success']),
                ("Overdue", random.randint(3, 10), t['danger'])
            ]
            
            for status, count, color in status_data:
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{t['text']} !important;">{status}</span>
                        <span style="font-weight:600;color:{color} !important;">{count}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_coverage_analytics(self):
        """Render audit coverage analytics."""
        t = get_current_theme()
        
        st.markdown("### 🎯 Audit Coverage")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Coverage by audit universe
            st.markdown("#### Coverage by Audit Universe")
            
            for category, areas in AUDIT_UNIVERSE.items():
                total = len(areas)
                covered = random.randint(int(total * 0.5), total)
                pct = (covered / total * 100) if total > 0 else 0
                
                color = t['success'] if pct >= 80 else (t['warning'] if pct >= 50 else t['danger'])
                
                with st.expander(f"📂 {category} ({covered}/{total})", expanded=False):
                    for area in areas:
                        is_covered = random.random() > 0.3
                        st.markdown(f'''
                        <div style="display:flex;align-items:center;gap:0.5rem;padding:0.25rem 0;">
                            <span style="color:{'#10b981' if is_covered else '#6b7280'} !important;">
                                {'✓' if is_covered else '○'}
                            </span>
                            <span style="color:{t['text'] if is_covered else t['text_muted']} !important;">{area}</span>
                        </div>
                        ''', unsafe_allow_html=True)
            
            # Overall coverage score
            st.markdown("#### Overall Coverage Score")
            
            coverage_score = st.session_state.analytics_data['coverage_score']
            score_color = t['success'] if coverage_score >= 80 else (t['warning'] if coverage_score >= 60 else t['danger'])
            
            st.markdown(f'''
            <div class="pro-card" style="text-align:center;padding:2rem;">
                <div style="font-size:4rem;font-weight:700;color:{score_color} !important;">{coverage_score}%</div>
                <div style="color:{t['text_secondary']} !important;">Audit Universe Coverage</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            # Risk coverage matrix
            st.markdown("#### Risk-Based Coverage")
            
            risk_coverage = [
                ("High Risk Areas", random.randint(85, 100), t['danger']),
                ("Medium Risk Areas", random.randint(60, 85), t['warning']),
                ("Low Risk Areas", random.randint(40, 70), t['success'])
            ]
            
            for risk, coverage, color in risk_coverage:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;margin-bottom:0.75rem;border-left:4px solid {color};">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;">{risk}</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{coverage}%</span>
                    </div>
                    <div class="progress-bar" style="height:8px;">
                        <div class="progress-fill" style="width:{coverage}%;background:{color};"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Cycle coverage
            st.markdown("#### Audit Cycle Coverage")
            
            cycle_data = {
                "Mandatory (Annual)": 100,
                "High Risk (18 months)": 85,
                "Medium Risk (24 months)": 70,
                "Low Risk (36 months)": 55
            }
            
            for cycle, pct in cycle_data.items():
                color = t['success'] if pct >= 90 else (t['warning'] if pct >= 70 else t['danger'])
                
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;font-size:0.9rem;">{cycle}</span>
                        <span style="font-weight:600;color:{color} !important;">{pct}%</span>
                    </div>
                    <div class="progress-bar" style="height:4px;">
                        <div class="progress-fill" style="width:{pct}%;background:{color};"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_trend_analytics(self):
        """Render trend analytics."""
        t = get_current_theme()
        
        st.markdown("### 📈 Trend Analysis")
        
        # Monthly trends
        st.markdown("#### Monthly Audit Activity (Last 12 Months)")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        audits = [random.randint(2, 6) for _ in months]
        findings = [random.randint(5, 20) for _ in months]
        
        max_val = max(max(audits), max(findings))
        
        # Simple bar chart
        st.markdown(f'''
        <div class="pro-card" style="padding:1rem;">
            <div style="display:flex;align-items:end;gap:8px;height:200px;margin-bottom:1rem;">
        ''', unsafe_allow_html=True)
        
        bars_html = ""
        for i, (month, audit, finding) in enumerate(zip(months, audits, findings)):
            audit_height = (audit / max_val * 150) if max_val > 0 else 0
            finding_height = (finding / max_val * 150) if max_val > 0 else 0
            
            bars_html += f'''
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;">
                <div style="display:flex;gap:2px;align-items:end;height:150px;">
                    <div style="width:12px;height:{audit_height}px;background:{t['primary']};border-radius:2px 2px 0 0;"></div>
                    <div style="width:12px;height:{finding_height}px;background:{t['warning']};border-radius:2px 2px 0 0;"></div>
                </div>
                <div style="font-size:0.7rem;color:{t['text_muted']} !important;">{month}</div>
            </div>
            '''
        
        st.markdown(f'''
            {bars_html}
            </div>
            <div style="display:flex;justify-content:center;gap:2rem;margin-top:1rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:12px;height:12px;background:{t['primary']};border-radius:2px;"></div>
                    <span style="font-size:0.8rem;color:{t['text_muted']} !important;">Audits Completed</span>
                </div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="width:12px;height:12px;background:{t['warning']};border-radius:2px;"></div>
                    <span style="font-size:0.8rem;color:{t['text_muted']} !important;">Findings Raised</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Year-over-year comparison
        st.markdown("#### Year-over-Year Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            yoy_metrics = [
                ("Audits Completed", 28, 25, "+12%"),
                ("Findings Raised", 95, 110, "-14%"),
                ("High Risk Findings", 18, 25, "-28%"),
                ("Average Audit Days", 32, 38, "-16%")
            ]
            
            for metric, current, previous, change in yoy_metrics:
                is_positive = '+' in change or (metric in ['High Risk Findings', 'Average Audit Days'] and '-' in change)
                color = t['success'] if is_positive else t['danger']
                
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;margin-bottom:0.5rem;">
                    <div style="font-size:0.85rem;color:{t['text_muted']} !important;">{metric}</div>
                    <div style="display:flex;justify-content:space-between;align-items:end;margin-top:0.5rem;">
                        <div>
                            <span style="font-size:1.5rem;font-weight:700;color:{t['text']} !important;">{current}</span>
                            <span style="font-size:0.8rem;color:{t['text_muted']} !important;"> vs {previous}</span>
                        </div>
                        <span style="font-weight:600;color:{color} !important;">{change}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Trend Indicators")
            
            indicators = [
                ("Finding Closure Rate", "↑", "Improving", t['success']),
                ("Audit Efficiency", "↑", "Improving", t['success']),
                ("Risk Coverage", "→", "Stable", t['warning']),
                ("Documentation Quality", "↑", "Improving", t['success'])
            ]
            
            for name, arrow, status, color in indicators:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:{t['text']} !important;">{name}</span>
                        <div style="display:flex;align-items:center;gap:0.5rem;">
                            <span style="font-size:1.5rem;color:{color} !important;">{arrow}</span>
                            <span style="color:{color} !important;font-weight:600;">{status}</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    def _render_reports(self):
        """Render reports section."""
        t = get_current_theme()
        
        st.markdown("### 📋 Generate Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Standard Reports")
            
            reports = [
                ("📊 Quarterly Audit Summary", "Executive summary of audit activities"),
                ("📈 Annual Audit Report", "Comprehensive yearly audit report"),
                ("🎯 Coverage Report", "Audit universe coverage analysis"),
                ("📋 Findings Tracker", "Open findings status report"),
                ("⏱️ Audit Plan Status", "Progress against annual plan")
            ]
            
            for name, desc in reports:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-weight:600;color:{t['text']} !important;">{name}</div>
                            <div style="font-size:0.8rem;color:{t['text_muted']} !important;">{desc}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                if st.button(f"Generate", key=f"gen_{name[:10]}", use_container_width=True):
                    st.info(f"Generating {name}...")
        
        with col2:
            st.markdown("#### Custom Report Builder")
            
            report_type = st.selectbox(
                "Report Type",
                ["Summary Dashboard", "Detailed Analysis", "Trend Report", "Comparison Report"],
                key="custom_report_type"
            )
            
            date_range = st.date_input(
                "Date Range",
                value=(datetime.now() - timedelta(days=90), datetime.now()),
                key="report_date_range"
            )
            
            include_sections = st.multiselect(
                "Include Sections",
                ["Executive Summary", "Performance Metrics", "Findings Analysis", 
                 "Coverage Analysis", "Trend Charts", "Recommendations"],
                default=["Executive Summary", "Performance Metrics"],
                key="report_sections"
            )
            
            export_format = st.selectbox(
                "Export Format",
                ["PDF", "Excel", "PowerPoint", "Word"],
                key="report_export_format"
            )
            
            if st.button("📥 Generate Custom Report", type="primary", use_container_width=True):
                with st.spinner("Generating report..."):
                    import time
                    time.sleep(2)
                    st.success("✓ Report generated successfully!")
                    st.download_button(
                        "💾 Download Report",
                        "Sample report content",
                        file_name=f"aurix_report_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )


def render():
    """Entry point for the Analytics page."""
    page = AnalyticsPage()
    page.render()
