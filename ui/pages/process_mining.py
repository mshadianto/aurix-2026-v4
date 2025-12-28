"""
Process Mining Page for AURIX 2026.
Interactive process discovery and bottleneck analysis.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer

# Import process mining module
import sys
sys.path.insert(0, '/home/claude/aurix_integrated')
from modules.process_mining import (
    generate_sample_event_log,
    parse_event_log,
    calculate_dfg,
    calculate_activity_durations,
    detect_bottlenecks,
    get_process_variants,
    generate_dfg_graphviz,
    calculate_process_metrics
)


class ProcessMiningPage:
    """Process Mining with DFG visualization and bottleneck detection."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for process mining."""
        if 'pm_event_log' not in st.session_state:
            st.session_state.pm_event_log = None
        if 'pm_dfg' not in st.session_state:
            st.session_state.pm_dfg = None
        if 'pm_bottlenecks' not in st.session_state:
            st.session_state.pm_bottlenecks = []
    
    def render(self):
        """Render the Process Mining page."""
        render_page_header(
            "Process Mining",
            "Automated Process Discovery & Bottleneck Analysis"
        )
        
        t = get_current_theme()
        
        # Introduction
        st.markdown(f'''
        <div style="background:linear-gradient(135deg, {t['primary']}15, {t['accent']}10);
                    padding:1.5rem;border-radius:12px;margin-bottom:1.5rem;
                    border:1px solid {t['border']};">
            <div style="display:flex;align-items:center;gap:1rem;">
                <span style="font-size:2.5rem;">🔄</span>
                <div>
                    <h3 style="margin:0;color:{t['text']};">Discover Process Inefficiencies</h3>
                    <p style="margin:0.5rem 0 0 0;color:{t['text_secondary']};">
                        Upload event logs to automatically discover process flows, identify bottlenecks, 
                        and find optimization opportunities using process mining algorithms.
                    </p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs([
            "📤 Data Upload",
            "🔍 Process Discovery",
            "📊 Analysis Results"
        ])
        
        with tab1:
            self._render_upload_section()
        
        with tab2:
            self._render_discovery_section()
        
        with tab3:
            self._render_analysis_section()
        
        render_footer()
    
    def _render_upload_section(self):
        """Render data upload section."""
        t = get_current_theme()
        
        st.markdown("### 📤 Upload Event Log")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f'''
            <div style="background:{t['bg_secondary']};padding:1rem;border-radius:8px;margin-bottom:1rem;">
                <strong>Required Columns:</strong>
                <ul style="margin:0.5rem 0;padding-left:1.2rem;">
                    <li><code>case_id</code> - Unique process instance identifier</li>
                    <li><code>activity</code> - Activity/task name</li>
                    <li><code>timestamp</code> - Event timestamp (YYYY-MM-DD HH:MM:SS)</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload CSV Event Log",
                type=["csv"],
                key="pm_upload"
            )
            
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"✅ Loaded {len(df)} events")
                    
                    # Column mapping
                    st.markdown("#### Map Columns")
                    cols = df.columns.tolist()
                    
                    case_col = st.selectbox("Case ID Column", cols, key="case_col")
                    activity_col = st.selectbox("Activity Column", cols, key="activity_col")
                    timestamp_col = st.selectbox("Timestamp Column", cols, key="timestamp_col")
                    
                    if st.button("🔄 Process Event Log", type="primary"):
                        with st.spinner("Processing event log..."):
                            parsed_df = parse_event_log(df, case_col, activity_col, timestamp_col)
                            st.session_state.pm_event_log = parsed_df
                            st.success(f"✅ Processed {parsed_df['case_id'].nunique()} cases")
                            st.rerun()
                
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        
        with col2:
            st.markdown("#### 🎲 Or Use Demo Data")
            
            if st.button("📊 Load Sample Data", use_container_width=True):
                with st.spinner("Generating sample event log..."):
                    sample_df = generate_sample_event_log(100)
                    st.session_state.pm_event_log = sample_df
                    st.success("✅ Loaded 100 sample loan approval cases")
                    st.rerun()
            
            st.markdown(f'''
            <div style="background:{t['bg_secondary']};padding:1rem;border-radius:8px;margin-top:1rem;">
                <strong>Sample Process:</strong><br>
                Loan Approval Workflow
                <ul style="margin:0.5rem 0;padding-left:1.2rem;font-size:0.85rem;">
                    <li>Application Received</li>
                    <li>Document Verification</li>
                    <li>Credit Check</li>
                    <li>Risk Assessment</li>
                    <li>Manager Approval</li>
                    <li>Final Review</li>
                    <li>Loan Disbursement</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
        
        # Show current data preview
        if st.session_state.pm_event_log is not None:
            st.markdown("---")
            st.markdown("### 📋 Data Preview")
            st.dataframe(
                st.session_state.pm_event_log.head(20),
                use_container_width=True
            )
    
    def _render_discovery_section(self):
        """Render process discovery section with DFG."""
        t = get_current_theme()
        
        if st.session_state.pm_event_log is None:
            st.info("👆 Please upload event log data first")
            return
        
        df = st.session_state.pm_event_log
        
        st.markdown("### 🔍 Process Discovery")
        
        # Calculate metrics
        metrics = calculate_process_metrics(df)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Cases", metrics['total_cases'])
        with col2:
            st.metric("Total Events", metrics['total_events'])
        with col3:
            st.metric("Unique Activities", metrics['unique_activities'])
        with col4:
            avg_dur = metrics['avg_case_duration_hours']
            if avg_dur >= 24:
                dur_str = f"{avg_dur/24:.1f} days"
            else:
                dur_str = f"{avg_dur:.1f} hours"
            st.metric("Avg Case Duration", dur_str)
        
        st.markdown("---")
        
        # Generate DFG
        st.markdown("### 📊 Directly-Follows Graph (DFG)")
        
        dfg, activity_counts = calculate_dfg(df)
        durations = calculate_activity_durations(df)
        bottlenecks = detect_bottlenecks(df)
        
        # Store in session
        st.session_state.pm_dfg = dfg
        st.session_state.pm_bottlenecks = bottlenecks
        
        # Get bottleneck activity names
        bottleneck_names = [b.activity for b in bottlenecks]
        
        # Generate and display graph
        dot_string = generate_dfg_graphviz(dfg, activity_counts, durations, bottleneck_names)
        
        try:
            st.graphviz_chart(dot_string, use_container_width=True)
        except Exception as e:
            st.warning(f"Graphviz visualization not available: {e}")
            st.code(dot_string, language="dot")
        
        # Legend
        st.markdown(f'''
        <div style="display:flex;gap:2rem;justify-content:center;margin:1rem 0;
                    padding:0.75rem;background:{t['bg_secondary']};border-radius:8px;">
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <div style="width:20px;height:20px;background:#E3F2FD;border:2px solid #1565C0;border-radius:4px;"></div>
                <span style="font-size:0.85rem;">Normal Activity</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <div style="width:20px;height:20px;background:#FFCDD2;border:3px solid #C62828;border-radius:4px;"></div>
                <span style="font-size:0.85rem;">Bottleneck Activity</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span style="font-size:0.85rem;">Edge thickness = frequency</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    def _render_analysis_section(self):
        """Render analysis results section."""
        t = get_current_theme()
        
        if st.session_state.pm_event_log is None:
            st.info("👆 Please upload event log data first")
            return
        
        df = st.session_state.pm_event_log
        bottlenecks = st.session_state.pm_bottlenecks or detect_bottlenecks(df)
        
        # Bottleneck Analysis
        st.markdown("### ⚠️ Bottleneck Analysis")
        
        if bottlenecks:
            for bn in bottlenecks:
                severity_colors = {
                    "high": t['danger'],
                    "medium": t['warning'],
                    "low": t['success']
                }
                sev_color = severity_colors.get(bn.severity, t['text_muted'])
                
                # Format duration
                if bn.avg_duration_hours >= 24:
                    dur_str = f"{bn.avg_duration_hours/24:.1f} days"
                else:
                    dur_str = f"{bn.avg_duration_hours:.1f} hours"
                
                st.markdown(f'''
                <div style="background:{t['card']};border-left:4px solid {sev_color};
                            padding:1rem;border-radius:0 8px 8px 0;margin-bottom:0.75rem;
                            border:1px solid {t['border']};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:{t['text']};font-size:1.1rem;">{bn.activity}</strong>
                            <div style="color:{t['text_secondary']};font-size:0.9rem;margin-top:0.25rem;">
                                Avg Duration: <strong>{dur_str}</strong> | 
                                Events: <strong>{bn.event_count}</strong> |
                                Percentile: {bn.percentile_rank}%
                            </div>
                        </div>
                        <span style="background:{sev_color};color:white;padding:0.25rem 0.75rem;
                                     border-radius:12px;font-size:0.75rem;font-weight:600;
                                     text-transform:uppercase;">
                            {bn.severity}
                        </span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # AI Analysis trigger
            if st.button("🤖 Generate AI Recommendations", type="primary"):
                with st.spinner("Analyzing bottlenecks..."):
                    import time
                    time.sleep(1.5)
                
                st.markdown(f'''
                <div style="background:{t['success']}15;border:1px solid {t['success']};
                            padding:1.5rem;border-radius:12px;margin-top:1rem;">
                    <h4 style="margin:0 0 1rem 0;color:{t['text']};">💡 AI Recommendations</h4>
                    
                    <div style="margin-bottom:1rem;">
                        <strong>1. Risk Assessment Optimization</strong>
                        <p style="margin:0.25rem 0;color:{t['text_secondary']};">
                            Consider implementing automated risk scoring for standard cases to reduce 
                            manual review time. This could reduce duration by 40-60%.
                        </p>
                    </div>
                    
                    <div style="margin-bottom:1rem;">
                        <strong>2. Parallel Processing</strong>
                        <p style="margin:0.25rem 0;color:{t['text_secondary']};">
                            Credit Check and Document Verification can run in parallel rather than 
                            sequentially. Estimated time savings: 8-12 hours per case.
                        </p>
                    </div>
                    
                    <div>
                        <strong>3. SLA Monitoring</strong>
                        <p style="margin:0.25rem 0;color:{t['text_secondary']};">
                            Implement real-time SLA monitoring dashboard with escalation triggers 
                            when activities exceed expected duration.
                        </p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.success("✅ No significant bottlenecks detected")
        
        st.markdown("---")
        
        # Process Variants
        st.markdown("### 🔀 Process Variants")
        
        variants = get_process_variants(df, top_n=5)
        
        for var in variants:
            st.markdown(f'''
            <div style="background:{t['bg_secondary']};padding:1rem;border-radius:8px;margin-bottom:0.5rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                    <strong style="color:{t['accent']};">Variant #{var['rank']}</strong>
                    <span style="color:{t['text_muted']};">{var['count']} cases ({var['percentage']}%)</span>
                </div>
                <div style="font-size:0.85rem;color:{t['text_secondary']};font-family:monospace;">
                    {var['trace']}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Activity durations table
        st.markdown("---")
        st.markdown("### ⏱️ Activity Durations")
        
        durations = calculate_activity_durations(df)
        dur_df = pd.DataFrame([
            {"Activity": act, "Avg Duration (hours)": round(dur, 2)}
            for act, dur in sorted(durations.items(), key=lambda x: -x[1])
        ])
        
        st.dataframe(dur_df, use_container_width=True, hide_index=True)
        
        render_footer()


def render():
    """Entry point for the Process Mining page."""
    page = ProcessMiningPage()
    page.render()
