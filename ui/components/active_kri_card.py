"""
Active KRI Card Component for AURIX 2026.
Smart metric cards that trigger AI analysis when thresholds are breached.
"""

import streamlit as st
from typing import Optional, Dict, List, Any
from enum import Enum
from dataclasses import dataclass
import time

from ui.styles.css_builder import get_current_theme


class KRIStatus(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    DANGER = "danger"


@dataclass
class KRIAnalysisResult:
    """Result of AI-powered KRI analysis."""
    metric_name: str
    current_value: float
    threshold: float
    status: KRIStatus
    root_causes: List[Dict[str, Any]]
    recommendations: List[str]
    confidence_score: float


def get_kri_status(
    value: float,
    threshold: float,
    warning_pct: float = 0.8,
    lower_is_worse: bool = False
) -> KRIStatus:
    """Determine KRI status based on value and threshold."""
    if lower_is_worse:
        if value <= threshold:
            return KRIStatus.DANGER
        elif value <= threshold * (1 + (1 - warning_pct)):
            return KRIStatus.WARNING
        return KRIStatus.NORMAL
    else:
        if value >= threshold:
            return KRIStatus.DANGER
        elif value >= threshold * warning_pct:
            return KRIStatus.WARNING
        return KRIStatus.NORMAL


def get_status_color(status: KRIStatus, theme: dict) -> str:
    """Get color for status."""
    colors = {
        KRIStatus.NORMAL: theme.get('success', '#28A745'),
        KRIStatus.WARNING: theme.get('warning', '#FFC107'),
        KRIStatus.DANGER: theme.get('danger', '#DC3545')
    }
    return colors.get(status, theme.get('text_muted', '#6C757D'))


def run_mock_ai_analysis(
    metric_id: str,
    metric_name: str,
    value: float,
    threshold: float
) -> KRIAnalysisResult:
    """Run mock AI analysis for KRI breach."""
    time.sleep(1.5)
    
    analyses = {
        "npl_ratio": {
            "root_causes": [
                {"category": "Portfolio Concentration", "description": "High concentration in corporate segment (62% of total NPL)", "severity": "high", "evidence": "Top 10 debtors contribute 45% of NPL"},
                {"category": "Economic Factors", "description": "Commodity price downturn affecting mining sector loans", "severity": "medium", "evidence": "Mining sector NPL increased 2.3% QoQ"},
                {"category": "Underwriting Weakness", "description": "Inadequate cashflow analysis for project finance", "severity": "high", "evidence": "8 of 12 new NPLs from loans approved in 2023"}
            ],
            "recommendations": [
                "Implement enhanced due diligence for corporate loans > IDR 50B",
                "Conduct deep-dive review of mining sector exposure",
                "Strengthen cashflow projection validation in credit analysis",
                "Consider early warning system for watchlist accounts"
            ]
        },
        "ldr_ratio": {
            "root_causes": [
                {"category": "Deposit Erosion", "description": "Corporate deposits declining due to rate competition", "severity": "medium", "evidence": "Corporate time deposits down 8% QoQ"},
                {"category": "Loan Growth", "description": "Aggressive lending targets without matching funding", "severity": "high", "evidence": "Loan growth 15% YTD vs deposit growth 7%"}
            ],
            "recommendations": [
                "Review deposit pricing strategy",
                "Develop alternative funding sources",
                "Align loan growth targets with funding capacity"
            ]
        }
    }
    
    default_analysis = {
        "root_causes": [
            {"category": "Threshold Breach", "description": metric_name + " has exceeded acceptable threshold", "severity": "high", "evidence": "Current: " + str(value) + ", Threshold: " + str(threshold)}
        ],
        "recommendations": ["Conduct detailed investigation", "Review historical trends", "Escalate to Risk Committee"]
    }
    
    template = analyses.get(metric_id, default_analysis)
    
    return KRIAnalysisResult(
        metric_name=metric_name,
        current_value=value,
        threshold=threshold,
        status=get_kri_status(value, threshold),
        root_causes=template["root_causes"],
        recommendations=template["recommendations"],
        confidence_score=0.87
    )


def render_analysis_dialog(result: KRIAnalysisResult):
    """Render AI analysis results in a dialog modal."""
    t = get_current_theme()
    status_color = get_status_color(result.status, t)
    
    @st.dialog("🔍 AI Analysis: " + result.metric_name, width="large")
    def show_analysis():
        # Header using st.columns instead of complex HTML
        st.markdown("#### " + result.metric_name)
        st.caption("AI-Powered Root Cause Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Value", str(result.current_value) + "%")
        with col2:
            st.metric("Threshold", str(result.threshold) + "%")
        with col3:
            variance = result.current_value - result.threshold
            st.metric("Variance", str(round(variance, 2)) + "%")
        
        st.markdown("---")
        
        # Root Causes
        st.markdown("### 🎯 Identified Root Causes")
        
        for i, cause in enumerate(result.root_causes, 1):
            severity = cause.get("severity", "medium")
            severity_colors = {"high": t['danger'], "medium": t['warning'], "low": t['success']}
            sev_color = severity_colors.get(severity, t['text_muted'])
            
            card_html = (
                '<div style="background:' + t['bg_secondary'] + ';padding:1rem;border-radius:8px;margin-bottom:0.75rem;border-left:4px solid ' + sev_color + ';">'
                '<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                '<div>'
                '<div style="font-weight:600;color:' + t['text'] + ';margin-bottom:0.25rem;">' + str(i) + '. ' + cause["category"] + '</div>'
                '<div style="color:' + t['text_secondary'] + ';font-size:0.9rem;">' + cause["description"] + '</div>'
                '<div style="color:' + t['text_muted'] + ';font-size:0.8rem;margin-top:0.5rem;font-style:italic;">📊 Evidence: ' + cause.get("evidence", "N/A") + '</div>'
                '</div>'
                '<span style="background:' + sev_color + ';color:white;padding:0.2rem 0.5rem;border-radius:8px;font-size:0.65rem;font-weight:600;text-transform:uppercase;">' + severity + '</span>'
                '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recommendations
        st.markdown("### 💡 AI Recommendations")
        
        for rec in result.recommendations:
            rec_html = (
                '<div style="display:flex;align-items:flex-start;gap:0.75rem;padding:0.5rem 0;">'
                '<span style="color:#2E7D32;font-size:1.2rem;">✓</span>'
                '<span style="color:' + t['text_secondary'] + ';">' + rec + '</span>'
                '</div>'
            )
            st.markdown(rec_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action buttons
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📋 Create Finding", use_container_width=True):
                st.session_state['create_finding_from_kri'] = result
                st.toast("✅ Finding template created!")
        
        with col_b:
            if st.button("📊 Export Report", use_container_width=True):
                st.toast("📤 Report exported!")
        
        with col_c:
            if st.button("🔔 Set Alert", use_container_width=True):
                st.toast("🔔 Alert configured!")
    
    show_analysis()


def render_active_kri_card(
    metric_id: str,
    label: str,
    value: float,
    threshold: float,
    unit: str = "%",
    trend_value: Optional[float] = None,
    trend_direction: Optional[str] = None,
    lower_is_worse: bool = False
):
    """
    Render a smart KRI metric card with AI analysis trigger.
    """
    t = get_current_theme()
    
    # Determine status
    status = get_kri_status(value, threshold, lower_is_worse=lower_is_worse)
    status_color = get_status_color(status, t)
    is_breached = status in [KRIStatus.DANGER, KRIStatus.WARNING]
    
    # Card background
    if status == KRIStatus.DANGER:
        card_bg = t['danger'] + "10"
    elif status == KRIStatus.WARNING:
        card_bg = t['warning'] + "10"
    else:
        card_bg = t['card']
    
    # Status text color
    status_text_color = "white" if status != KRIStatus.WARNING else "#333"
    
    # Build trend section
    trend_section = ""
    if trend_value is not None and trend_direction:
        if lower_is_worse:
            trend_color = t['success'] if trend_direction == "up" else t['danger']
        else:
            trend_color = t['danger'] if trend_direction == "up" else t['success']
        trend_arrow = "↑" if trend_direction == "up" else "↓"
        trend_section = (
            '<div style="font-size:0.8rem;color:' + trend_color + ';margin-top:0.5rem;">'
            + trend_arrow + ' ' + str(trend_value) + unit + ' from last period'
            '</div>'
        )
    
    # Render card using string concatenation
    card_html = (
        '<div style="background:' + card_bg + ';border-radius:12px;padding:1.25rem;box-shadow:0 2px 12px rgba(0,0,0,0.08);border-left:4px solid ' + status_color + ';border:1px solid ' + t['border'] + ';margin-bottom:0.5rem;">'
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.75rem;">'
        '<div style="font-size:0.85rem;color:' + t['text_muted'] + ';font-weight:500;">' + label + '</div>'
        '<span style="background:' + status_color + ';color:' + status_text_color + ';font-size:0.65rem;padding:0.25rem 0.6rem;border-radius:12px;font-weight:700;">' + status.value.upper() + '</span>'
        '</div>'
        '<div style="font-size:2rem;font-weight:700;color:' + t['text'] + ';">'
        + str(value) + '<span style="font-size:1rem;color:' + t['text_muted'] + ';margin-left:2px;">' + unit + '</span>'
        '</div>'
        + trend_section +
        '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';margin-top:0.5rem;">Threshold: ' + str(threshold) + unit + '</div>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)
    
    # AI Analysis trigger button (only when breached)
    if is_breached:
        if st.button(
            "⚡ Analyze Risk",
            key="analyze_" + metric_id,
            use_container_width=True,
            type="primary"
        ):
            st.session_state['active_investigation'] = {
                "metric_id": metric_id,
                "metric_name": label,
                "value": value,
                "threshold": threshold,
                "status": status.value
            }
            
            with st.spinner("🔍 Analyzing " + label + "..."):
                result = run_mock_ai_analysis(metric_id, label, value, threshold)
            
            st.session_state['investigation_results'] = result
            render_analysis_dialog(result)


__all__ = [
    "render_active_kri_card",
    "run_mock_ai_analysis",
    "render_analysis_dialog",
    "KRIStatus",
    "KRIAnalysisResult",
    "get_kri_status"
]
