"""
Executive Dashboard for AURIX Excellence 2026.

Premium executive-grade dashboard featuring:
- 5-Second Rule KPI Scorecard
- So-What Auto-Narrative insights
- Flight Simulator scenario analysis
- Data Lineage transparency
- Export-ready reports

Designed for C-Suite and Senior Management.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import List

from ui.styles.css_builder import get_current_theme
from ui.components import render_footer
from ui.components.executive import (
    KPIMetric,
    TrendDirection,
    DataLineage,
    render_executive_scorecard,
    render_so_what_panel,
    generate_so_what_insight,
    render_flight_simulator,
    render_data_lineage,
    render_export_panel,
)
from services.visitor_service import track_page_view


def render():
    """Render the Executive Dashboard."""
    t = get_current_theme()

    # Track page view
    track_page_view("Executive Dashboard")

    # Define executive KPIs
    kpis = _get_executive_kpis()

    # Render Executive Scorecard (5-Second Rule)
    render_executive_scorecard(
        metrics=kpis,
        title="Executive Command Center",
        subtitle="Real-time Risk & Performance Intelligence | AURIX Excellence 2026"
    )

    # Data Lineage for transparency
    lineage = DataLineage(
        source_system="Core Banking System (T24)",
        extraction_time=datetime.now() - timedelta(minutes=15),
        transformation="ETL Pipeline v3.2 → Data Warehouse → AURIX Analytics",
        quality_score=0.97,
        owner="Risk Management Division",
        refresh_frequency="Every 15 minutes"
    )
    render_data_lineage(lineage, compact=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main content in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Strategic Insights",
        "🎮 Scenario Simulator",
        "📈 Detailed Analytics",
        "📑 Reports"
    ])

    with tab1:
        _render_strategic_insights(kpis, t)

    with tab2:
        _render_scenario_simulator(kpis, t)

    with tab3:
        _render_detailed_analytics(kpis, t)

    with tab4:
        _render_reports_section(kpis, t)

    # Footer
    render_footer()


def _get_executive_kpis() -> List[KPIMetric]:
    """Get executive KPI metrics with sample data."""
    return [
        KPIMetric(
            id="npl_ratio",
            label="NPL Ratio",
            value=5.54,
            unit="%",
            target=3.50,
            threshold_warning=4.00,
            threshold_danger=5.00,
            trend_direction=TrendDirection.UP,
            trend_value=0.82,
            period="vs Last Month",
            source="Core Banking - Credit Module",
            lower_is_better=True
        ),
        KPIMetric(
            id="ldr_ratio",
            label="LDR",
            value=94.32,
            unit="%",
            target=85.00,
            threshold_warning=90.00,
            threshold_danger=100.00,
            trend_direction=TrendDirection.UP,
            trend_value=2.15,
            period="vs Last Month",
            source="Treasury Management System",
            lower_is_better=True
        ),
        KPIMetric(
            id="car_ratio",
            label="CAR",
            value=18.45,
            unit="%",
            target=14.00,
            threshold_warning=12.00,
            threshold_danger=10.00,
            trend_direction=TrendDirection.DOWN,
            trend_value=0.35,
            period="vs Last Month",
            source="Risk Management System",
            lower_is_better=False
        ),
        KPIMetric(
            id="roa",
            label="ROA",
            value=2.18,
            unit="%",
            target=2.50,
            threshold_warning=1.50,
            threshold_danger=1.00,
            trend_direction=TrendDirection.STABLE,
            trend_value=0.05,
            period="vs Last Month",
            source="Finance & Accounting System",
            lower_is_better=False
        ),
        KPIMetric(
            id="lcr",
            label="LCR",
            value=142.50,
            unit="%",
            target=120.00,
            threshold_warning=110.00,
            threshold_danger=100.00,
            trend_direction=TrendDirection.UP,
            trend_value=5.20,
            period="vs Last Month",
            source="Treasury Management System",
            lower_is_better=False
        ),
        KPIMetric(
            id="cost_income",
            label="Cost-to-Income",
            value=48.75,
            unit="%",
            target=45.00,
            threshold_warning=50.00,
            threshold_danger=55.00,
            trend_direction=TrendDirection.DOWN,
            trend_value=1.25,
            period="vs Last Month",
            source="Finance & Accounting System",
            lower_is_better=True
        ),
    ]


def _render_strategic_insights(kpis: List[KPIMetric], t: dict):
    """Render strategic insights with So-What narratives."""
    st.markdown("### 💡 Strategic Intelligence")
    st.markdown(
        f"<p style='color: {t['text_muted']}; font-size: 0.9rem;'>"
        "AI-generated insights explaining the business impact of each metric. "
        "Click on any metric to explore root causes and recommended actions."
        "</p>",
        unsafe_allow_html=True
    )

    # Find metrics that need attention (breaching thresholds)
    critical_kpis = [k for k in kpis if k.threshold_danger and (
        (k.lower_is_better and k.value >= k.threshold_danger) or
        (not k.lower_is_better and k.value <= k.threshold_danger)
    )]

    warning_kpis = [k for k in kpis if k.threshold_warning and k not in critical_kpis and (
        (k.lower_is_better and k.value >= k.threshold_warning) or
        (not k.lower_is_better and k.value <= k.threshold_warning)
    )]

    # Render insights for critical metrics first
    if critical_kpis:
        st.markdown(f"#### 🚨 Critical Alerts ({len(critical_kpis)})")
        for kpi in critical_kpis:
            insight = generate_so_what_insight(kpi)
            render_so_what_panel(insight, kpi.label)

    if warning_kpis:
        st.markdown(f"#### ⚠️ Elevated Risk ({len(warning_kpis)})")
        for kpi in warning_kpis:
            insight = generate_so_what_insight(kpi)
            render_so_what_panel(insight, kpi.label)

    # Show positive performers
    healthy_kpis = [k for k in kpis if k not in critical_kpis and k not in warning_kpis]
    if healthy_kpis:
        with st.expander(f"✅ Healthy Metrics ({len(healthy_kpis)})", expanded=False):
            for kpi in healthy_kpis:
                st.markdown(f'''
                <div style="
                    background: {t['success']}10;
                    border-left: 3px solid {t['success']};
                    padding: 0.75rem 1rem;
                    margin-bottom: 0.5rem;
                    border-radius: 0 8px 8px 0;
                ">
                    <strong style="color: {t['text']};">{kpi.label}</strong>
                    <span style="color: {t['text_muted']}; margin-left: 0.5rem;">
                        {kpi.value}{kpi.unit} - Within target range
                    </span>
                </div>
                ''', unsafe_allow_html=True)


def _render_scenario_simulator(kpis: List[KPIMetric], t: dict):
    """Render Flight Simulator for scenario analysis."""
    st.markdown("### 🎮 Risk Scenario Simulator")
    st.markdown(
        f"<p style='color: {t['text_muted']}; font-size: 0.9rem;'>"
        "Explore 'what-if' scenarios to understand potential impacts and prepare contingency plans. "
        "Adjust parameters to simulate various market conditions and stress scenarios."
        "</p>",
        unsafe_allow_html=True
    )

    # Select metric to simulate
    selected_metric_id = st.selectbox(
        "Select Metric to Simulate",
        options=[k.id for k in kpis],
        format_func=lambda x: next((k.label for k in kpis if k.id == x), x)
    )

    selected_metric = next((k for k in kpis if k.id == selected_metric_id), kpis[0])

    render_flight_simulator(selected_metric)

    # Scenario presets
    st.markdown("#### 📋 Pre-built Stress Scenarios")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'''
        <div style="
            background: {t['card']};
            border: 1px solid {t['border']};
            border-radius: 12px;
            padding: 1rem;
        ">
            <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">🌪️</div>
            <div style="font-weight: 600; color: {t['text']}; margin-bottom: 0.25rem;">
                OJK Stress Test 2024
            </div>
            <div style="font-size: 0.8rem; color: {t['text_muted']};">
                Regulatory stress scenario with GDP -5%, NPL +3%
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div style="
            background: {t['card']};
            border: 1px solid {t['border']};
            border-radius: 12px;
            padding: 1rem;
        ">
            <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">📉</div>
            <div style="font-weight: 600; color: {t['text']}; margin-bottom: 0.25rem;">
                Commodity Crash
            </div>
            <div style="font-size: 0.8rem; color: {t['text_muted']};">
                Mining & Palm Oil sector shock scenario
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
        <div style="
            background: {t['card']};
            border: 1px solid {t['border']};
            border-radius: 12px;
            padding: 1rem;
        ">
            <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">💹</div>
            <div style="font-weight: 600; color: {t['text']}; margin-bottom: 0.25rem;">
                Rate Normalization
            </div>
            <div style="font-size: 0.8rem; color: {t['text_muted']};">
                BI Rate increase +150bps impact analysis
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_detailed_analytics(kpis: List[KPIMetric], t: dict):
    """Render detailed analytics with trends and comparisons."""
    st.markdown("### 📈 Detailed Performance Analytics")

    # KPI comparison table
    st.markdown("#### KPI Performance Summary")

    # Build comparison data
    table_html = f'''
    <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
        <thead>
            <tr style="background: {t['bg_secondary']};">
                <th style="padding: 0.75rem; text-align: left; color: {t['text_muted']}; font-weight: 600; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.05em;">Metric</th>
                <th style="padding: 0.75rem; text-align: right; color: {t['text_muted']}; font-weight: 600; text-transform: uppercase; font-size: 0.7rem;">Current</th>
                <th style="padding: 0.75rem; text-align: right; color: {t['text_muted']}; font-weight: 600; text-transform: uppercase; font-size: 0.7rem;">Target</th>
                <th style="padding: 0.75rem; text-align: right; color: {t['text_muted']}; font-weight: 600; text-transform: uppercase; font-size: 0.7rem;">Variance</th>
                <th style="padding: 0.75rem; text-align: center; color: {t['text_muted']}; font-weight: 600; text-transform: uppercase; font-size: 0.7rem;">Trend</th>
                <th style="padding: 0.75rem; text-align: center; color: {t['text_muted']}; font-weight: 600; text-transform: uppercase; font-size: 0.7rem;">Status</th>
            </tr>
        </thead>
        <tbody>
    '''

    for kpi in kpis:
        # Calculate variance
        if kpi.target:
            variance = kpi.value - kpi.target
            variance_pct = (variance / kpi.target * 100) if kpi.target != 0 else 0

            if kpi.lower_is_better:
                variance_color = t['success'] if variance <= 0 else t['danger']
            else:
                variance_color = t['success'] if variance >= 0 else t['danger']
        else:
            variance = 0
            variance_pct = 0
            variance_color = t['text_muted']

        # Trend icon
        trend_icon = "↑" if kpi.trend_direction == TrendDirection.UP else "↓" if kpi.trend_direction == TrendDirection.DOWN else "→"

        # Status badge
        if kpi.threshold_danger:
            if (kpi.lower_is_better and kpi.value >= kpi.threshold_danger) or \
               (not kpi.lower_is_better and kpi.value <= kpi.threshold_danger):
                status = "CRITICAL"
                status_bg = t['danger']
            elif kpi.threshold_warning and ((kpi.lower_is_better and kpi.value >= kpi.threshold_warning) or \
                 (not kpi.lower_is_better and kpi.value <= kpi.threshold_warning)):
                status = "WARNING"
                status_bg = t['warning']
            else:
                status = "NORMAL"
                status_bg = t['success']
        else:
            status = "NORMAL"
            status_bg = t['success']

        table_html += f'''
            <tr style="border-bottom: 1px solid {t['border']};">
                <td style="padding: 0.75rem; color: {t['text']}; font-weight: 500;">{kpi.label}</td>
                <td style="padding: 0.75rem; text-align: right; color: {t['text']}; font-weight: 600;">{kpi.value:.2f}{kpi.unit}</td>
                <td style="padding: 0.75rem; text-align: right; color: {t['text_muted']};">{kpi.target:.2f}{kpi.unit if kpi.target else '-'}</td>
                <td style="padding: 0.75rem; text-align: right; color: {variance_color}; font-weight: 500;">{'+' if variance > 0 else ''}{variance:.2f}{kpi.unit}</td>
                <td style="padding: 0.75rem; text-align: center; font-size: 1.1rem;">{trend_icon}</td>
                <td style="padding: 0.75rem; text-align: center;">
                    <span style="background: {status_bg}20; color: {status_bg}; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.65rem; font-weight: 600;">{status}</span>
                </td>
            </tr>
        '''

    table_html += '''
        </tbody>
    </table>
    '''

    st.markdown(table_html, unsafe_allow_html=True)

    # Data Lineage - Full detail
    st.markdown("#### 🔍 Data Governance & Lineage")

    lineage = DataLineage(
        source_system="Core Banking System (T24 Temenos)",
        extraction_time=datetime.now() - timedelta(minutes=15),
        transformation="ETL Pipeline v3.2 (Airflow) → Snowflake DWH → dbt Models → AURIX Analytics Layer",
        quality_score=0.97,
        owner="Chief Risk Officer (CRO) Office",
        refresh_frequency="Near Real-time (15-minute intervals)"
    )
    render_data_lineage(lineage, compact=False)


def _render_reports_section(kpis: List[KPIMetric], t: dict):
    """Render reports and export section."""
    st.markdown("### 📑 Executive Reports")
    st.markdown(
        f"<p style='color: {t['text_muted']}; font-size: 0.9rem;'>"
        "Generate presentation-ready reports for Board meetings, Risk Committee, and regulatory submissions."
        "</p>",
        unsafe_allow_html=True
    )

    # Export panel
    render_export_panel(
        title="Executive Dashboard Report",
        metrics=kpis
    )

    st.markdown("#### 📋 Available Report Templates")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'''
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem;">📊</span>
                <div style="font-weight: 600; color: {t['text']};">Board Risk Report</div>
            </div>
            <div style="font-size: 0.85rem; color: {t['text_muted']}; margin-bottom: 0.75rem;">
                Comprehensive risk overview for Board of Directors with key metrics, trends, and strategic recommendations.
            </div>
            <div style="font-size: 0.7rem; color: {t['accent']};">
                📄 20-25 slides | ⏱️ ~2 min to generate
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem;">📈</span>
                <div style="font-weight: 600; color: {t['text']};">KRI Dashboard Summary</div>
            </div>
            <div style="font-size: 0.85rem; color: {t['text_muted']}; margin-bottom: 0.75rem;">
                One-page executive summary of all Key Risk Indicators with threshold breaches highlighted.
            </div>
            <div style="font-size: 0.7rem; color: {t['accent']};">
                📄 1 page | ⏱️ ~30 sec to generate
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem;">🏛️</span>
                <div style="font-weight: 600; color: {t['text']};">OJK Regulatory Report</div>
            </div>
            <div style="font-size: 0.85rem; color: {t['text_muted']}; margin-bottom: 0.75rem;">
                Pre-formatted report following OJK submission guidelines for monthly risk reporting.
            </div>
            <div style="font-size: 0.7rem; color: {t['accent']};">
                📄 Standard format | ⏱️ ~1 min to generate
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="background: {t['card']}; border: 1px solid {t['border']}; border-radius: 12px; padding: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem;">⚠️</span>
                <div style="font-weight: 600; color: {t['text']};">Incident Alert Report</div>
            </div>
            <div style="font-size: 0.85rem; color: {t['text_muted']}; margin-bottom: 0.75rem;">
                Detailed analysis of threshold breaches with root cause analysis and remediation timeline.
            </div>
            <div style="font-size: 0.7rem; color: {t['accent']};">
                📄 3-5 pages | ⏱️ ~45 sec to generate
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Schedule reports
    st.markdown("#### ⏰ Scheduled Reports")
    st.info("💡 Configure automated report generation and distribution to stakeholders. Reports can be scheduled daily, weekly, or on-demand.")
