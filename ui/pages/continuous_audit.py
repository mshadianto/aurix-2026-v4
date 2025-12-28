"""
Continuous Audit Page Module for AURIX.
Real-time monitoring, rule management, and alert dashboard.
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
    status_badge,
    render_metric_card,
    render_alert
)
from data.seeds import CONTINUOUS_AUDIT_RULES, AUDIT_UNIVERSE


class ContinuousAuditPage:
    """Continuous Audit monitoring and rule management page."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for continuous audit."""
        if 'ca_rules' not in st.session_state:
            # Load default rules from seeds
            st.session_state.ca_rules = [
                {**rule, 'enabled': True, 'alert_count': random.randint(0, 50)}
                for rule in CONTINUOUS_AUDIT_RULES
            ]
        
        if 'ca_alerts' not in st.session_state:
            st.session_state.ca_alerts = self._generate_sample_alerts()
    
    def _generate_sample_alerts(self) -> List[Dict]:
        """Generate sample alerts for demo."""
        alerts = []
        categories = ['AML', 'Financial', 'Security', 'Operations', 'Credit']
        severities = ['HIGH', 'MEDIUM', 'LOW']
        
        for i in range(15):
            rule = random.choice(CONTINUOUS_AUDIT_RULES)
            alerts.append({
                'id': f"ALT{i+1:04d}",
                'rule_id': rule['id'],
                'rule_name': rule['name'],
                'category': rule['category'],
                'severity': random.choice(severities),
                'description': f"Alert triggered: {rule['description']}",
                'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 72))).strftime('%Y-%m-%d %H:%M'),
                'status': random.choice(['New', 'Reviewed', 'Escalated', 'Closed']),
                'details': {
                    'transaction_id': f"TXN{random.randint(100000, 999999)}",
                    'amount': random.randint(10000, 500000),
                    'account': f"ACC{random.randint(1000, 9999)}"
                }
            })
        
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)
    
    def render(self):
        """Render the Continuous Audit page."""
        render_page_header("Continuous Audit", "Real-time monitoring and automated alerting")
        
        t = get_current_theme()
        
        # Summary Dashboard
        self._render_summary_dashboard()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🚨 Alert Dashboard",
            "⚙️ Rule Management",
            "📈 Monitoring Stats",
            "➕ Create Rule"
        ])
        
        with tab1:
            self._render_alert_dashboard()
        
        with tab2:
            self._render_rule_management()
        
        with tab3:
            self._render_monitoring_stats()
        
        with tab4:
            self._render_create_rule()
        
        render_footer()
    
    def _render_summary_dashboard(self):
        """Render summary metrics."""
        t = get_current_theme()
        
        alerts = st.session_state.ca_alerts
        rules = st.session_state.ca_rules
        
        new_alerts = len([a for a in alerts if a['status'] == 'New'])
        high_alerts = len([a for a in alerts if a['severity'] == 'HIGH' and a['status'] != 'Closed'])
        active_rules = len([r for r in rules if r.get('enabled', True)])
        alerts_24h = len([a for a in alerts if 'hours' not in a['timestamp'] or int(a['timestamp'].split()[0]) <= 24])
        
        # Use Streamlit columns for metrics
        cols = st.columns(4)
        
        metrics_data = [
            ("ACTIVE RULES", str(active_rules), f"of {len(rules)} total", t['success']),
            ("NEW ALERTS", str(new_alerts), "Requires review", t['danger'] if new_alerts > 5 else t['success']),
            ("HIGH PRIORITY", str(high_alerts), "Immediate attention", t['danger'] if high_alerts > 0 else t['success']),
            ("TOTAL ALERTS (24H)", str(alerts_24h), "Last 24 hours", t['accent']),
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
    
    def _render_alert_dashboard(self):
        """Render the alert dashboard."""
        t = get_current_theme()
        
        st.markdown("### 🚨 Alert Dashboard")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", "New", "Reviewed", "Escalated", "Closed"],
                key="ca_alert_status"
            )
        
        with col2:
            severity_filter = st.selectbox(
                "Severity",
                ["All", "HIGH", "MEDIUM", "LOW"],
                key="ca_alert_severity"
            )
        
        with col3:
            category_filter = st.selectbox(
                "Category",
                ["All"] + list(set(a['category'] for a in st.session_state.ca_alerts)),
                key="ca_alert_category"
            )
        
        with col4:
            time_filter = st.selectbox(
                "Time Range",
                ["All", "Last 24 hours", "Last 7 days", "Last 30 days"],
                key="ca_alert_time"
            )
        
        st.markdown("---")
        
        # Apply filters
        filtered_alerts = st.session_state.ca_alerts.copy()
        
        if status_filter != "All":
            filtered_alerts = [a for a in filtered_alerts if a['status'] == status_filter]
        
        if severity_filter != "All":
            filtered_alerts = [a for a in filtered_alerts if a['severity'] == severity_filter]
        
        if category_filter != "All":
            filtered_alerts = [a for a in filtered_alerts if a['category'] == category_filter]
        
        # Display alerts
        if not filtered_alerts:
            st.info("✅ No alerts match the current filters.")
            return
        
        st.markdown(f"**Showing {len(filtered_alerts)} alert(s)**")
        
        for alert in filtered_alerts[:20]:
            self._render_alert_card(alert)
    
    def _render_alert_card(self, alert: Dict):
        """Render a single alert card."""
        t = get_current_theme()
        
        severity_colors = {
            'HIGH': t['danger'],
            'MEDIUM': t['warning'],
            'LOW': t['success']
        }
        
        status_colors = {
            'New': t['danger'],
            'Reviewed': t['warning'],
            'Escalated': t['accent'],
            'Closed': t['success']
        }
        
        sev_color = severity_colors.get(alert['severity'], t['text_muted'])
        stat_color = status_colors.get(alert['status'], t['text_muted'])
        
        with st.expander(f"🔔 {alert['id']}: {alert['rule_name']}", expanded=alert['status'] == 'New'):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'''
                <div class="pro-card" style="padding:1rem;">
                    <div style="display:flex;gap:1rem;margin-bottom:1rem;">
                        <span class="badge" style="background:{sev_color}20;color:{sev_color};">{alert['severity']}</span>
                        <span class="badge" style="background:{stat_color}20;color:{stat_color};">{alert['status']}</span>
                        <span style="color:{t['text_muted']} !important;font-size:0.85rem;">Category: {alert['category']}</span>
                    </div>
                    <div style="color:{t['text']} !important;margin-bottom:1rem;">
                        {alert['description']}
                    </div>
                    <div style="background:{t['bg_secondary']};padding:1rem;border-radius:8px;font-family:monospace;font-size:0.85rem;">
                        <div style="color:{t['text_muted']} !important;margin-bottom:0.5rem;">Alert Details:</div>
                        <div style="color:{t['text']} !important;">Transaction ID: {alert['details']['transaction_id']}</div>
                        <div style="color:{t['text']} !important;">Amount: Rp {alert['details']['amount']:,}</div>
                        <div style="color:{t['text']} !important;">Account: {alert['details']['account']}</div>
                    </div>
                    <div style="margin-top:1rem;font-size:0.8rem;color:{t['text_muted']} !important;">
                        Timestamp: {alert['timestamp']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### Actions")
                
                new_status = st.selectbox(
                    "Update Status",
                    ["New", "Reviewed", "Escalated", "Closed"],
                    index=["New", "Reviewed", "Escalated", "Closed"].index(alert['status']),
                    key=f"alert_status_{alert['id']}"
                )
                
                if st.button("Update", key=f"update_alert_{alert['id']}"):
                    for a in st.session_state.ca_alerts:
                        if a['id'] == alert['id']:
                            a['status'] = new_status
                            break
                    st.success("✓ Status updated")
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("🔍 Investigate", key=f"investigate_{alert['id']}"):
                    st.info("Opening investigation workflow...")
                
                if st.button("📋 Create Finding", key=f"create_finding_{alert['id']}"):
                    st.info("Redirecting to Findings module...")
    
    def _render_rule_management(self):
        """Render rule management interface."""
        t = get_current_theme()
        
        st.markdown("### ⚙️ Rule Management")
        
        # Filter by category
        categories = list(set(r['category'] for r in st.session_state.ca_rules))
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + categories,
            key="rule_category_filter"
        )
        
        st.markdown("---")
        
        filtered_rules = st.session_state.ca_rules
        if category_filter != "All":
            filtered_rules = [r for r in filtered_rules if r['category'] == category_filter]
        
        # Display rules in a table-like format
        for rule in filtered_rules:
            enabled = rule.get('enabled', True)
            
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;">
                    <div style="display:flex;align-items:center;gap:0.5rem;">
                        <span style="font-size:1.25rem;">{'🟢' if enabled else '🔴'}</span>
                        <div>
                            <div style="font-weight:600;color:{t['text']} !important;">{rule['name']}</div>
                            <div style="font-size:0.8rem;color:{t['text_secondary']} !important;">{rule['description']}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div style="text-align:center;padding:0.5rem;">
                    <div style="font-size:0.75rem;color:{t['text_muted']} !important;">Category</div>
                    <div style="font-weight:600;color:{t['text']} !important;">{rule['category']}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'''
                <div style="text-align:center;padding:0.5rem;">
                    <div style="font-size:0.75rem;color:{t['text_muted']} !important;">Alerts</div>
                    <div style="font-weight:600;color:{t['warning'] if rule.get('alert_count', 0) > 10 else t['text']} !important;">
                        {rule.get('alert_count', 0)}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col4:
                if st.toggle("Enabled", value=enabled, key=f"rule_toggle_{rule['id']}"):
                    rule['enabled'] = True
                else:
                    rule['enabled'] = False
            
            st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)
    
    def _render_monitoring_stats(self):
        """Render monitoring statistics."""
        t = get_current_theme()
        
        st.markdown("### 📈 Monitoring Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Alerts by Category
            st.markdown("#### Alerts by Category")
            
            alerts = st.session_state.ca_alerts
            category_counts = {}
            for a in alerts:
                cat = a['category']
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            total = len(alerts)
            for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                pct = (count / total * 100) if total > 0 else 0
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <span style="color:{t['text']} !important;">{cat}</span>
                        <span style="font-weight:600;color:{t['text']} !important;">{count} ({pct:.0f}%)</span>
                    </div>
                    <div class="progress-bar" style="height:4px;">
                        <div class="progress-fill" style="width:{pct}%;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Alert Trend (mock data)
            st.markdown("#### Alert Trend (7 Days)")
            
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            values = [random.randint(5, 25) for _ in days]
            max_val = max(values)
            
            st.markdown(f'''
            <div class="pro-card" style="padding:1rem;">
                <div style="display:flex;align-items:end;gap:0.5rem;height:120px;">
            ''', unsafe_allow_html=True)
            
            bars_html = ""
            for i, (day, val) in enumerate(zip(days, values)):
                height = (val / max_val * 100) if max_val > 0 else 0
                bars_html += f'''
                <div style="flex:1;text-align:center;">
                    <div style="height:{height}px;background:{t['primary']};border-radius:4px 4px 0 0;"></div>
                    <div style="font-size:0.7rem;color:{t['text_muted']} !important;margin-top:4px;">{day}</div>
                    <div style="font-size:0.75rem;color:{t['text']} !important;">{val}</div>
                </div>
                '''
            
            st.markdown(f'''
                {bars_html}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            # Rule Performance
            st.markdown("#### Top Triggering Rules")
            
            rules = sorted(st.session_state.ca_rules, key=lambda x: x.get('alert_count', 0), reverse=True)[:5]
            
            for rule in rules:
                count = rule.get('alert_count', 0)
                st.markdown(f'''
                <div class="pro-card" style="padding:0.75rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-weight:600;color:{t['text']} !important;">{rule['name']}</div>
                            <div style="font-size:0.75rem;color:{t['text_muted']} !important;">{rule['category']}</div>
                        </div>
                        <div style="font-size:1.25rem;font-weight:700;color:{t['warning'] if count > 20 else t['text']} !important;">
                            {count}
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Response Time
            st.markdown("#### Alert Response Metrics")
            
            metrics = [
                ("Avg. Response Time", "2.5 hrs", t['success']),
                ("SLA Compliance", "94%", t['success']),
                ("False Positive Rate", "12%", t['warning']),
                ("Escalation Rate", "8%", t['text'])
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
    
    def _render_create_rule(self):
        """Render create new rule form."""
        t = get_current_theme()
        
        st.markdown("### ➕ Create New Monitoring Rule")
        
        st.markdown(f'''
        <div class="pro-card" style="background:{t['bg_secondary']};margin-bottom:1rem;">
            <p style="color:{t['text_secondary']} !important;margin:0;">
                Define custom continuous audit rules to monitor specific patterns, thresholds, or anomalies in your data.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            rule_name = st.text_input(
                "Rule Name *",
                placeholder="e.g., High Value Wire Transfer",
                key="new_rule_name"
            )
            
            rule_description = st.text_area(
                "Description *",
                height=100,
                placeholder="Describe what this rule monitors...",
                key="new_rule_desc"
            )
            
            rule_category = st.selectbox(
                "Category *",
                ["AML", "Financial", "Security", "Operations", "Credit", "IT", "Fraud", "Compliance"],
                key="new_rule_category"
            )
        
        with col2:
            rule_type = st.selectbox(
                "Rule Type *",
                ["Threshold", "Pattern", "Anomaly", "Comparison", "Sequence"],
                key="new_rule_type"
            )
            
            if rule_type == "Threshold":
                threshold_value = st.number_input(
                    "Threshold Value",
                    min_value=0,
                    value=10000,
                    key="new_rule_threshold"
                )
                
                threshold_operator = st.selectbox(
                    "Operator",
                    ["Greater than", "Less than", "Equal to", "Not equal to"],
                    key="new_rule_operator"
                )
            
            severity = st.selectbox(
                "Default Severity",
                ["HIGH", "MEDIUM", "LOW"],
                index=1,
                key="new_rule_severity"
            )
            
            enabled = st.checkbox("Enable immediately", value=True, key="new_rule_enabled")
        
        st.markdown("---")
        
        # Data Source Configuration
        st.markdown("#### Data Source Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            data_source = st.selectbox(
                "Data Source",
                ["Transaction Database", "User Activity Logs", "System Logs", "External API", "Manual Input"],
                key="new_rule_source"
            )
            
            schedule = st.selectbox(
                "Monitoring Schedule",
                ["Real-time", "Every 5 minutes", "Hourly", "Daily", "Weekly"],
                key="new_rule_schedule"
            )
        
        with col2:
            notification = st.multiselect(
                "Notification Channels",
                ["Dashboard Alert", "Email", "SMS", "Slack", "Teams"],
                default=["Dashboard Alert"],
                key="new_rule_notification"
            )
            
            escalation = st.number_input(
                "Auto-escalate after (hours)",
                min_value=0,
                value=24,
                key="new_rule_escalation"
            )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("💾 Save Rule", type="primary", use_container_width=True):
                if not rule_name or not rule_description:
                    st.error("Please fill in all required fields.")
                else:
                    new_rule = {
                        'id': len(st.session_state.ca_rules) + 1,
                        'name': rule_name,
                        'description': rule_description,
                        'category': rule_category,
                        'threshold': threshold_value if rule_type == "Threshold" else None,
                        'enabled': enabled,
                        'alert_count': 0,
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    
                    st.session_state.ca_rules.append(new_rule)
                    st.success(f"✓ Rule '{rule_name}' created successfully!")
                    st.balloons()
        
        with col2:
            if st.button("🧪 Test Rule", use_container_width=True):
                st.info("Running rule test against sample data...")
                st.success("✓ Test completed: 3 matches found in sample data")


def render():
    """Entry point for the Continuous Audit page."""
    page = ContinuousAuditPage()
    page.render()
