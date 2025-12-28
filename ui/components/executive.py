"""
Executive-Grade UI Components for AURIX Excellence 2026.

Implements "Executive-Grade" approach with:
- 5-Second Rule visual hierarchy with dominant KPI Scorecard
- So-What Auto-Narrative for strategic insights
- Flight Simulator scenario simulation
- Data Lineage transparency markers
- Export-ready reports

Author: AURIX Team
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

from ui.styles.css_builder import get_current_theme


class TrendDirection(str, Enum):
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NORMAL = "normal"


@dataclass
class KPIMetric:
    """Executive KPI metric with full context."""
    id: str
    label: str
    value: float
    unit: str = "%"
    target: Optional[float] = None
    threshold_warning: Optional[float] = None
    threshold_danger: Optional[float] = None
    trend_direction: TrendDirection = TrendDirection.STABLE
    trend_value: float = 0.0
    period: str = "MTD"
    source: str = "Core Banking System"
    last_updated: Optional[datetime] = None
    lower_is_better: bool = False


@dataclass
class SoWhatInsight:
    """Auto-generated strategic insight."""
    headline: str
    detail: str
    impact: str
    action: str
    confidence: float = 0.85
    source_metrics: List[str] = field(default_factory=list)


@dataclass
class ScenarioResult:
    """Result of a what-if scenario simulation."""
    scenario_name: str
    baseline_value: float
    projected_value: float
    impact_description: str
    risk_delta: str
    recommendations: List[str]


@dataclass
class DataLineage:
    """Data source transparency information."""
    source_system: str
    extraction_time: datetime
    transformation: str
    quality_score: float
    owner: str
    refresh_frequency: str


# =============================================================================
# EXECUTIVE KPI SCORECARD - 5-SECOND RULE
# =============================================================================

def render_executive_scorecard(
    metrics: List[KPIMetric],
    title: str = "Executive Dashboard",
    subtitle: str = "Real-time Risk & Performance Overview"
):
    """
    Render dominant KPI scorecard following 5-Second Rule.
    Key metrics visible and understood within 5 seconds.
    """
    t = get_current_theme()

    # Executive Header
    st.markdown(f'''
    <div style="
        background: linear-gradient(135deg, {t['primary']} 0%, {t['accent']} 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="color: white !important; margin: 0; font-size: 1.75rem; font-weight: 700;">
                    {title}
                </h1>
                <p style="color: rgba(255,255,255,0.85); margin: 0.5rem 0 0 0; font-size: 0.95rem;">
                    {subtitle}
                </p>
            </div>
            <div style="text-align: right;">
                <div style="color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em;">
                    Last Updated
                </div>
                <div style="color: white; font-size: 1rem; font-weight: 600;">
                    {datetime.now().strftime("%d %b %Y, %H:%M")}
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Primary KPIs - Large, dominant display (5-Second Rule)
    _render_primary_kpis(metrics[:4], t)

    # Secondary KPIs if more than 4
    if len(metrics) > 4:
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        _render_secondary_kpis(metrics[4:], t)


def _render_primary_kpis(metrics: List[KPIMetric], t: dict):
    """Render primary KPI cards - large and dominant."""
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            _render_executive_kpi_card(metric, t, is_primary=True)


def _render_secondary_kpis(metrics: List[KPIMetric], t: dict):
    """Render secondary KPI cards - smaller, supporting."""
    cols = st.columns(min(len(metrics), 6))

    for i, metric in enumerate(metrics):
        with cols[i % len(cols)]:
            _render_executive_kpi_card(metric, t, is_primary=False)


def _render_executive_kpi_card(metric: KPIMetric, t: dict, is_primary: bool = True):
    """Render individual executive KPI card."""
    # Determine status
    status = _get_metric_status(metric)
    status_color = _get_status_color(status, t)

    # Trend indicator
    trend_icon = "↑" if metric.trend_direction == TrendDirection.UP else "↓" if metric.trend_direction == TrendDirection.DOWN else "→"

    if metric.lower_is_better:
        trend_color = t['success'] if metric.trend_direction == TrendDirection.DOWN else t['danger'] if metric.trend_direction == TrendDirection.UP else t['text_muted']
    else:
        trend_color = t['success'] if metric.trend_direction == TrendDirection.UP else t['danger'] if metric.trend_direction == TrendDirection.DOWN else t['text_muted']

    # Card sizing based on primary/secondary
    padding = "1.75rem" if is_primary else "1.25rem"
    value_size = "2.75rem" if is_primary else "1.75rem"
    label_size = "0.85rem" if is_primary else "0.75rem"

    # Status indicator pulse for danger
    pulse_animation = ""
    if status == RiskLevel.CRITICAL or status == RiskLevel.HIGH:
        pulse_animation = f'''
        <style>
            @keyframes pulse-{metric.id} {{
                0% {{ box-shadow: 0 0 0 0 {status_color}40; }}
                70% {{ box-shadow: 0 0 0 10px {status_color}00; }}
                100% {{ box-shadow: 0 0 0 0 {status_color}00; }}
            }}
            .kpi-card-{metric.id} {{
                animation: pulse-{metric.id} 2s infinite;
            }}
        </style>
        '''

    # Target vs Actual indicator
    target_section = ""
    if metric.target is not None:
        variance = metric.value - metric.target
        variance_pct = (variance / metric.target * 100) if metric.target != 0 else 0
        variance_color = t['success'] if (variance >= 0 and not metric.lower_is_better) or (variance <= 0 and metric.lower_is_better) else t['danger']
        target_section = f'''
        <div style="display: flex; justify-content: space-between; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid {t['border']};">
            <span style="font-size: 0.7rem; color: {t['text_muted']};">Target: {metric.target}{metric.unit}</span>
            <span style="font-size: 0.7rem; color: {variance_color}; font-weight: 600;">
                {'+' if variance > 0 else ''}{variance:.1f}{metric.unit} ({variance_pct:+.1f}%)
            </span>
        </div>
        '''

    st.markdown(f'''
    {pulse_animation}
    <div class="kpi-card-{metric.id}" style="
        background: {t['card']};
        border: 1px solid {t['border']};
        border-left: 4px solid {status_color};
        border-radius: 12px;
        padding: {padding};
        transition: all 0.3s ease;
        height: 100%;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <div style="
                font-size: {label_size};
                color: {t['text_muted']};
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            ">
                {metric.label}
            </div>
            <div style="
                background: {status_color}20;
                color: {status_color};
                padding: 0.2rem 0.6rem;
                border-radius: 12px;
                font-size: 0.65rem;
                font-weight: 700;
                text-transform: uppercase;
            ">
                {status.value}
            </div>
        </div>

        <div style="display: flex; align-items: baseline; gap: 0.5rem;">
            <span style="
                font-size: {value_size};
                font-weight: 800;
                color: {t['text']};
                line-height: 1;
            ">
                {metric.value:,.2f}
            </span>
            <span style="font-size: 1rem; color: {t['text_muted']};">{metric.unit}</span>
        </div>

        <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
            <span style="color: {trend_color}; font-weight: 600; font-size: 0.85rem;">
                {trend_icon} {abs(metric.trend_value)}{metric.unit}
            </span>
            <span style="color: {t['text_muted']}; font-size: 0.75rem;">vs {metric.period}</span>
        </div>

        {target_section}

        <div style="margin-top: 0.75rem; font-size: 0.65rem; color: {t['text_muted']}; display: flex; align-items: center; gap: 0.25rem;">
            <span style="opacity: 0.7;">📊</span>
            <span>{metric.source}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def _get_metric_status(metric: KPIMetric) -> RiskLevel:
    """Determine metric status based on thresholds."""
    if metric.threshold_danger is not None:
        if metric.lower_is_better:
            if metric.value >= metric.threshold_danger:
                return RiskLevel.CRITICAL
            elif metric.threshold_warning and metric.value >= metric.threshold_warning:
                return RiskLevel.HIGH
        else:
            if metric.value >= metric.threshold_danger:
                return RiskLevel.CRITICAL
            elif metric.threshold_warning and metric.value >= metric.threshold_warning:
                return RiskLevel.HIGH

    if metric.threshold_warning is not None:
        if metric.lower_is_better:
            if metric.value >= metric.threshold_warning:
                return RiskLevel.MEDIUM
        else:
            if metric.value >= metric.threshold_warning:
                return RiskLevel.MEDIUM

    return RiskLevel.NORMAL


def _get_status_color(status: RiskLevel, t: dict) -> str:
    """Get color for risk level."""
    colors = {
        RiskLevel.CRITICAL: t['danger'],
        RiskLevel.HIGH: "#FF6B6B",
        RiskLevel.MEDIUM: t['warning'],
        RiskLevel.LOW: t['accent'],
        RiskLevel.NORMAL: t['success'],
    }
    return colors.get(status, t['text_muted'])


# =============================================================================
# SO-WHAT AUTO-NARRATIVE ENGINE
# =============================================================================

def generate_so_what_insight(
    metric: KPIMetric,
    context: Optional[Dict[str, Any]] = None
) -> SoWhatInsight:
    """
    Generate automatic "So-What" insight for a metric.
    Provides strategic interpretation beyond just numbers.
    """
    status = _get_metric_status(metric)

    # Generate contextual insights based on metric type and status
    insights_templates = {
        "npl_ratio": {
            RiskLevel.CRITICAL: SoWhatInsight(
                headline=f"Credit Quality Alert: NPL at {metric.value}% requires immediate attention",
                detail=f"NPL ratio has breached the {metric.threshold_danger}% danger threshold, indicating significant deterioration in loan portfolio quality.",
                impact="Potential provisioning increase of IDR 50-100B in next quarter. ROA impact estimated at -15 to -25 bps.",
                action="Recommend emergency Credit Committee meeting within 48 hours. Initiate deep-dive on top 20 delinquent accounts.",
                confidence=0.92,
                source_metrics=["npl_ratio", "provision_coverage", "watchlist_ratio"]
            ),
            RiskLevel.HIGH: SoWhatInsight(
                headline=f"Credit Risk Elevated: NPL trending toward threshold",
                detail=f"Current NPL at {metric.value}% is approaching danger zone. {metric.trend_direction.value} trend indicates continued pressure.",
                impact="If trend continues, expect threshold breach within 2-3 months. Early provision adjustment recommended.",
                action="Enhance monitoring frequency for watchlist accounts. Review new disbursement criteria.",
                confidence=0.87,
                source_metrics=["npl_ratio", "dpd_30_ratio"]
            ),
        },
        "ldr_ratio": {
            RiskLevel.CRITICAL: SoWhatInsight(
                headline=f"Liquidity Stress: LDR at {metric.value}% exceeds regulatory comfort",
                detail=f"Loan-to-Deposit ratio has exceeded regulatory threshold, indicating potential liquidity constraints.",
                impact="May trigger OJK supervisory attention. Funding cost likely to increase 25-50 bps to attract deposits.",
                action="Activate contingency funding plan. Consider wholesale funding alternatives. Slow down new loan disbursements.",
                confidence=0.89,
                source_metrics=["ldr_ratio", "lcr", "nsfr"]
            ),
        },
        "default": {
            RiskLevel.CRITICAL: SoWhatInsight(
                headline=f"{metric.label} has breached critical threshold",
                detail=f"Current value of {metric.value}{metric.unit} exceeds the {metric.threshold_danger}{metric.unit} threshold by {metric.value - metric.threshold_danger:.2f}{metric.unit}.",
                impact="Immediate management attention required. Potential regulatory and financial implications.",
                action="Convene risk committee meeting. Initiate root cause analysis. Prepare mitigation plan.",
                confidence=0.80,
                source_metrics=[metric.id]
            ),
            RiskLevel.NORMAL: SoWhatInsight(
                headline=f"{metric.label} performing within acceptable range",
                detail=f"Current value of {metric.value}{metric.unit} is within target parameters with {metric.trend_direction.value} trajectory.",
                impact="No immediate concerns. Continue monitoring for early warning signs.",
                action="Maintain current strategy. Review during next periodic assessment.",
                confidence=0.85,
                source_metrics=[metric.id]
            ),
        }
    }

    # Get appropriate insight
    metric_insights = insights_templates.get(metric.id, insights_templates["default"])
    insight = metric_insights.get(status, insights_templates["default"].get(status, insights_templates["default"][RiskLevel.NORMAL]))

    return insight


def render_so_what_panel(insight: SoWhatInsight, metric_label: str = ""):
    """Render the So-What insight panel with strategic narrative."""
    t = get_current_theme()

    confidence_color = t['success'] if insight.confidence >= 0.85 else t['warning'] if insight.confidence >= 0.70 else t['danger']

    st.markdown(f'''
    <div style="
        background: linear-gradient(135deg, {t['card']} 0%, {t['bg_secondary']} 100%);
        border: 1px solid {t['border']};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.25rem;">💡</span>
                <span style="
                    font-size: 0.7rem;
                    font-weight: 600;
                    color: {t['text_muted']};
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                ">
                    Strategic Insight
                </span>
            </div>
            <div style="
                display: flex;
                align-items: center;
                gap: 0.25rem;
                background: {confidence_color}15;
                padding: 0.25rem 0.5rem;
                border-radius: 8px;
            ">
                <span style="font-size: 0.65rem; color: {t['text_muted']};">AI Confidence:</span>
                <span style="font-size: 0.75rem; font-weight: 600; color: {confidence_color};">{insight.confidence:.0%}</span>
            </div>
        </div>

        <h4 style="color: {t['text']} !important; margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; line-height: 1.4;">
            {insight.headline}
        </h4>

        <p style="color: {t['text_secondary']}; margin: 0 0 1rem 0; font-size: 0.9rem; line-height: 1.6;">
            {insight.detail}
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="
                background: {t['danger']}10;
                border-left: 3px solid {t['danger']};
                padding: 0.75rem 1rem;
                border-radius: 0 8px 8px 0;
            ">
                <div style="font-size: 0.7rem; color: {t['danger']}; font-weight: 600; text-transform: uppercase; margin-bottom: 0.25rem;">
                    ⚠️ Impact
                </div>
                <div style="font-size: 0.85rem; color: {t['text_secondary']};">
                    {insight.impact}
                </div>
            </div>

            <div style="
                background: {t['success']}10;
                border-left: 3px solid {t['success']};
                padding: 0.75rem 1rem;
                border-radius: 0 8px 8px 0;
            ">
                <div style="font-size: 0.7rem; color: {t['success']}; font-weight: 600; text-transform: uppercase; margin-bottom: 0.25rem;">
                    ✓ Recommended Action
                </div>
                <div style="font-size: 0.85rem; color: {t['text_secondary']};">
                    {insight.action}
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


# =============================================================================
# FLIGHT SIMULATOR - SCENARIO ANALYSIS
# =============================================================================

def render_flight_simulator(
    base_metric: KPIMetric,
    scenarios: List[Dict[str, Any]] = None
):
    """
    Render Flight Simulator style scenario analysis.
    Allows executives to simulate what-if scenarios.
    """
    t = get_current_theme()

    st.markdown(f'''
    <div style="
        background: {t['card']};
        border: 1px solid {t['border']};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem;">🎮</span>
            <div>
                <div style="font-size: 1.1rem; font-weight: 600; color: {t['text']};">
                    Scenario Simulator
                </div>
                <div style="font-size: 0.75rem; color: {t['text_muted']};">
                    Explore "what-if" scenarios for proactive decision making
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"**Current {base_metric.label}:** {base_metric.value}{base_metric.unit}")

        # Scenario selection
        scenario_type = st.selectbox(
            "Select Scenario",
            [
                "📉 Economic Downturn (-20% revenue)",
                "📈 Growth Acceleration (+30% volume)",
                "⚠️ Credit Shock (+50% defaults)",
                "🏦 Interest Rate Hike (+200 bps)",
                "🎯 Custom Scenario"
            ],
            key=f"scenario_{base_metric.id}"
        )

        # Custom adjustment slider
        adjustment = st.slider(
            "Adjustment Factor",
            min_value=-50,
            max_value=50,
            value=0,
            format="%d%%",
            key=f"adjust_{base_metric.id}"
        )

        simulate_btn = st.button(
            "🚀 Run Simulation",
            key=f"sim_{base_metric.id}",
            type="primary",
            use_container_width=True
        )

    with col2:
        if simulate_btn or adjustment != 0:
            # Calculate simulated value
            factor = 1 + (adjustment / 100)

            if "Downturn" in scenario_type:
                factor *= 1.15
            elif "Growth" in scenario_type:
                factor *= 0.95
            elif "Credit Shock" in scenario_type:
                factor *= 1.50
            elif "Interest" in scenario_type:
                factor *= 1.08

            simulated_value = base_metric.value * factor
            delta = simulated_value - base_metric.value

            # Determine new status
            new_status = "NORMAL"
            status_color = t['success']
            if base_metric.threshold_danger and simulated_value >= base_metric.threshold_danger:
                new_status = "CRITICAL"
                status_color = t['danger']
            elif base_metric.threshold_warning and simulated_value >= base_metric.threshold_warning:
                new_status = "WARNING"
                status_color = t['warning']

            st.markdown(f'''
            <div style="
                background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['card']} 100%);
                border: 2px solid {status_color};
                border-radius: 12px;
                padding: 1.5rem;
            ">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 0.75rem; color: {t['text_muted']}; text-transform: uppercase; letter-spacing: 0.1em;">
                        Simulated {base_metric.label}
                    </div>
                    <div style="font-size: 3rem; font-weight: 800; color: {status_color};">
                        {simulated_value:.2f}<span style="font-size: 1.5rem;">{base_metric.unit}</span>
                    </div>
                    <div style="
                        display: inline-block;
                        background: {status_color}20;
                        color: {status_color};
                        padding: 0.25rem 0.75rem;
                        border-radius: 12px;
                        font-size: 0.75rem;
                        font-weight: 600;
                    ">
                        {new_status}
                    </div>
                </div>

                <div style="display: flex; justify-content: space-around; padding-top: 1rem; border-top: 1px solid {t['border']};">
                    <div style="text-align: center;">
                        <div style="font-size: 0.7rem; color: {t['text_muted']};">Change</div>
                        <div style="font-size: 1.25rem; font-weight: 600; color: {t['danger'] if delta > 0 else t['success']};">
                            {'+' if delta > 0 else ''}{delta:.2f}{base_metric.unit}
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 0.7rem; color: {t['text_muted']};">% Change</div>
                        <div style="font-size: 1.25rem; font-weight: 600; color: {t['danger'] if delta > 0 else t['success']};">
                            {'+' if delta > 0 else ''}{(delta/base_metric.value*100):.1f}%
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            # Recommendations based on simulation
            if new_status == "CRITICAL":
                st.error("⚠️ **Critical Alert**: This scenario would breach critical thresholds. Immediate contingency planning recommended.")
            elif new_status == "WARNING":
                st.warning("⚡ **Elevated Risk**: This scenario approaches warning levels. Enhanced monitoring advised.")
            else:
                st.success("✅ **Within Tolerance**: Metric remains within acceptable parameters under this scenario.")


# =============================================================================
# DATA LINEAGE TRANSPARENCY
# =============================================================================

def render_data_lineage(lineage: DataLineage, compact: bool = True):
    """Render data lineage transparency marker."""
    t = get_current_theme()

    quality_color = t['success'] if lineage.quality_score >= 0.95 else t['warning'] if lineage.quality_score >= 0.85 else t['danger']

    if compact:
        st.markdown(f'''
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: {t['bg_secondary']};
            border: 1px solid {t['border']};
            border-radius: 8px;
            padding: 0.35rem 0.75rem;
            font-size: 0.7rem;
            color: {t['text_muted']};
        ">
            <span style="opacity: 0.7;">📊</span>
            <span>{lineage.source_system}</span>
            <span style="color: {t['border']};">|</span>
            <span>Updated: {lineage.extraction_time.strftime("%H:%M")}</span>
            <span style="color: {t['border']};">|</span>
            <span style="color: {quality_color};">Quality: {lineage.quality_score:.0%}</span>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div style="
            background: {t['card']};
            border: 1px solid {t['border']};
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
                <span style="font-size: 1rem;">🔍</span>
                <span style="font-size: 0.75rem; font-weight: 600; color: {t['text']}; text-transform: uppercase; letter-spacing: 0.05em;">
                    Data Lineage
                </span>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; font-size: 0.8rem;">
                <div>
                    <div style="color: {t['text_muted']}; font-size: 0.65rem; text-transform: uppercase;">Source</div>
                    <div style="color: {t['text']}; font-weight: 500;">{lineage.source_system}</div>
                </div>
                <div>
                    <div style="color: {t['text_muted']}; font-size: 0.65rem; text-transform: uppercase;">Extracted</div>
                    <div style="color: {t['text']}; font-weight: 500;">{lineage.extraction_time.strftime("%d %b %Y, %H:%M")}</div>
                </div>
                <div>
                    <div style="color: {t['text_muted']}; font-size: 0.65rem; text-transform: uppercase;">Quality Score</div>
                    <div style="color: {quality_color}; font-weight: 600;">{lineage.quality_score:.1%}</div>
                </div>
                <div>
                    <div style="color: {t['text_muted']}; font-size: 0.65rem; text-transform: uppercase;">Transformation</div>
                    <div style="color: {t['text']}; font-weight: 500;">{lineage.transformation}</div>
                </div>
                <div>
                    <div style="color: {t['text_muted']}; font-size: 0.65rem; text-transform: uppercase;">Data Owner</div>
                    <div style="color: {t['text']}; font-weight: 500;">{lineage.owner}</div>
                </div>
                <div>
                    <div style="color: {t['text_muted']}; font-size: 0.65rem; text-transform: uppercase;">Refresh</div>
                    <div style="color: {t['text']}; font-weight: 500;">{lineage.refresh_frequency}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


# =============================================================================
# EXECUTIVE REPORT EXPORT
# =============================================================================

def render_export_panel(
    title: str = "Executive Report",
    metrics: List[KPIMetric] = None,
    insights: List[SoWhatInsight] = None
):
    """Render export panel for generating executive reports."""
    t = get_current_theme()

    st.markdown(f'''
    <div style="
        background: {t['card']};
        border: 1px solid {t['border']};
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.25rem;">📑</span>
                <div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: {t['text']};">
                        Export Executive Report
                    </div>
                    <div style="font-size: 0.75rem; color: {t['text_muted']};">
                        Generate presentation-ready reports
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📊 PowerPoint", use_container_width=True, key="export_ppt"):
            st.toast("📊 Generating PowerPoint report...")
            _generate_mock_export("PowerPoint")

    with col2:
        if st.button("📄 PDF Report", use_container_width=True, key="export_pdf"):
            st.toast("📄 Generating PDF report...")
            _generate_mock_export("PDF")

    with col3:
        if st.button("📈 Excel Data", use_container_width=True, key="export_excel"):
            st.toast("📈 Generating Excel export...")
            _generate_mock_export("Excel")

    with col4:
        if st.button("📧 Email Summary", use_container_width=True, key="export_email"):
            st.toast("📧 Preparing email summary...")
            _generate_mock_export("Email")


def _generate_mock_export(format_type: str):
    """Generate mock export (placeholder for actual implementation)."""
    st.success(f"✅ {format_type} report generated successfully!")
    st.info(f"📥 Download link will appear here in production environment.")


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'KPIMetric',
    'SoWhatInsight',
    'ScenarioResult',
    'DataLineage',
    'TrendDirection',
    'RiskLevel',
    'render_executive_scorecard',
    'render_so_what_panel',
    'generate_so_what_insight',
    'render_flight_simulator',
    'render_data_lineage',
    'render_export_panel',
]
