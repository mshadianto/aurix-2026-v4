"""
Predictive Analytics Module for AURIX.
AI-powered forecasting, trend analysis, and risk predictions.
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import math

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the Predictive Analytics page."""
    t = get_current_theme()
    
    render_page_header(
        "Predictive Analytics",
        "🔮",
        "AI-powered forecasting and trend predictions"
    )
    
    # Stunning animated header
    st.markdown(f'''
    <style>
        @keyframes gradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
    </style>
    
    <div style="background:linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);background-size:400% 400%;animation:gradient 15s ease infinite;border-radius:24px;padding:2.5rem;margin-bottom:2rem;position:relative;overflow:hidden;">
        <div style="position:absolute;top:20px;right:20px;font-size:6rem;opacity:0.2;animation:float 3s ease-in-out infinite;">🔮</div>
        
        <div style="position:relative;z-index:1;">
            <div style="color:white;font-size:2rem;font-weight:800;margin-bottom:0.5rem;">
                AI Prediction Engine
            </div>
            <div style="color:rgba(255,255,255,0.9);font-size:1rem;max-width:500px;">
                Harness the power of machine learning to predict risks, forecast trends, and make data-driven decisions
            </div>
            
            <div style="display:flex;gap:2rem;margin-top:2rem;">
                <div style="text-align:center;">
                    <div style="color:white;font-size:2.5rem;font-weight:800;">94.7%</div>
                    <div style="color:rgba(255,255,255,0.8);font-size:0.8rem;">Prediction Accuracy</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:white;font-size:2.5rem;font-weight:800;">156</div>
                    <div style="color:rgba(255,255,255,0.8);font-size:0.8rem;">Risks Predicted</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:white;font-size:2.5rem;font-weight:800;">23</div>
                    <div style="color:rgba(255,255,255,0.8);font-size:0.8rem;">Prevented Issues</div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Risk Forecast",
        "🎯 Finding Predictions",
        "⏰ Timeline Projections",
        "🧠 AI Insights"
    ])
    
    with tab1:
        _render_risk_forecast(t)
    
    with tab2:
        _render_finding_predictions(t)
    
    with tab3:
        _render_timeline_projections(t)
    
    with tab4:
        _render_ai_insights(t)
    
    render_footer()


def _render_risk_forecast(t: dict):
    """Render risk forecasting."""
    
    st.markdown("### 📈 Risk Trend Forecast")
    
    # Time range selector
    col1, col2 = st.columns([2, 1])
    with col1:
        forecast_range = st.select_slider(
            "Forecast Period",
            options=["1 Month", "3 Months", "6 Months", "12 Months"],
            value="6 Months"
        )
    
    # Risk trend visualization
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:2rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
            <div style="font-weight:700;color:{t['text']};">Credit Risk Trend Forecast</div>
            <div style="display:flex;gap:1rem;font-size:0.75rem;">
                <span style="color:{t['text_muted']};">● Historical</span>
                <span style="color:{t['primary']};">● Predicted</span>
                <span style="color:{t['danger']};">● Alert Zone</span>
            </div>
        </div>
        
        
        <svg width="100%" height="250" viewBox="0 0 800 250">
            
            <g stroke="{t['border']}" stroke-width="1">
                <line x1="50" y1="30" x2="50" y2="200" stroke-dasharray="4"/>
                <line x1="50" y1="200" x2="750" y2="200"/>
                <line x1="50" y1="115" x2="750" y2="115" stroke-dasharray="4" opacity="0.5"/>
                <line x1="50" y1="30" x2="750" y2="30" stroke-dasharray="4" opacity="0.5"/>
            </g>
            
            
            <rect x="50" y="30" width="700" height="50" fill="{t['danger']}" opacity="0.1"/>
            
            
            <path d="M 50 150 L 150 140 L 250 155 L 350 130 L 400 125" 
                  stroke="{t['text_muted']}" stroke-width="3" fill="none"/>
            
            
            <path d="M 400 125 L 500 110 L 600 95 L 700 70 L 750 60" 
                  stroke="{t['primary']}" stroke-width="3" fill="none" stroke-dasharray="8,4"/>
            
            
            <path d="M 400 125 L 500 100 L 600 80 L 700 55 L 750 45 L 750 75 L 700 85 L 600 110 L 500 120 L 400 125" 
                  fill="{t['primary']}" opacity="0.2"/>
            
            
            <circle cx="50" cy="150" r="6" fill="{t['text_muted']}"/>
            <circle cx="150" cy="140" r="6" fill="{t['text_muted']}"/>
            <circle cx="250" cy="155" r="6" fill="{t['text_muted']}"/>
            <circle cx="350" cy="130" r="6" fill="{t['text_muted']}"/>
            <circle cx="400" cy="125" r="8" fill="{t['warning']}" stroke="white" stroke-width="2"/>
            
            
            <circle cx="500" cy="110" r="6" fill="{t['primary']}" opacity="0.7"/>
            <circle cx="600" cy="95" r="6" fill="{t['primary']}" opacity="0.7"/>
            <circle cx="700" cy="70" r="6" fill="{t['danger']}" opacity="0.7"/>
            <circle cx="750" cy="60" r="6" fill="{t['danger']}" opacity="0.7"/>
            
            
            <text x="50" y="220" fill="{t['text_muted']}" font-size="10">Jan</text>
            <text x="150" y="220" fill="{t['text_muted']}" font-size="10">Feb</text>
            <text x="250" y="220" fill="{t['text_muted']}" font-size="10">Mar</text>
            <text x="350" y="220" fill="{t['text_muted']}" font-size="10">Apr</text>
            <text x="400" y="220" fill="{t['warning']}" font-size="10" font-weight="bold">Now</text>
            <text x="500" y="220" fill="{t['primary']}" font-size="10">Jun</text>
            <text x="600" y="220" fill="{t['primary']}" font-size="10">Jul</text>
            <text x="700" y="220" fill="{t['danger']}" font-size="10">Aug</text>
            <text x="750" y="220" fill="{t['danger']}" font-size="10">Sep</text>
            
            
            <text x="40" y="35" fill="{t['text_muted']}" font-size="10" text-anchor="end">High</text>
            <text x="40" y="120" fill="{t['text_muted']}" font-size="10" text-anchor="end">Med</text>
            <text x="40" y="205" fill="{t['text_muted']}" font-size="10" text-anchor="end">Low</text>
            
            
            <rect x="620" y="35" width="120" height="40" rx="8" fill="{t['danger']}" opacity="0.9"/>
            <text x="680" y="55" fill="white" font-size="10" text-anchor="middle">⚠️ Risk Alert</text>
            <text x="680" y="68" fill="white" font-size="8" text-anchor="middle">Aug-Sep 2025</text>
        </svg>
    </div>
    ''', unsafe_allow_html=True)
    
    # Risk predictions by category
    st.markdown("#### 🎯 Risk Predictions by Category")
    
    risks = [
        {"name": "Credit Risk", "current": 65, "predicted": 78, "change": 13, "direction": "up", "confidence": 92},
        {"name": "Operational Risk", "current": 45, "predicted": 42, "change": -3, "direction": "down", "confidence": 88},
        {"name": "Compliance Risk", "current": 55, "predicted": 70, "change": 15, "direction": "up", "confidence": 85},
        {"name": "Cyber Risk", "current": 70, "predicted": 85, "change": 15, "direction": "up", "confidence": 91},
        {"name": "Liquidity Risk", "current": 35, "predicted": 38, "change": 3, "direction": "up", "confidence": 79},
    ]
    
    for risk in risks:
        direction_icon = "📈" if risk['direction'] == 'up' else "📉"
        change_color = t['danger'] if risk['direction'] == 'up' else t['success']
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="flex:1;">
                    <div style="font-weight:600;color:{t['text']};margin-bottom:0.5rem;">{risk['name']}</div>
                    <div style="display:flex;gap:2rem;align-items:center;">
                        <div>
                            <div style="font-size:0.7rem;color:{t['text_muted']};">Current</div>
                            <div style="font-size:1.25rem;font-weight:700;color:{t['text']};">{risk['current']}</div>
                        </div>
                        <div style="font-size:1.5rem;color:{t['text_muted']};">→</div>
                        <div>
                            <div style="font-size:0.7rem;color:{t['text_muted']};">Predicted</div>
                            <div style="font-size:1.25rem;font-weight:700;color:{change_color};">{risk['predicted']}</div>
                        </div>
                    </div>
                </div>
                <div style="text-align:center;padding:0 1.5rem;border-left:1px solid {t['border']};">
                    <div style="font-size:1.5rem;">{direction_icon}</div>
                    <div style="color:{change_color};font-weight:700;">{'+' if risk['change'] > 0 else ''}{risk['change']}</div>
                </div>
                <div style="text-align:center;padding-left:1.5rem;border-left:1px solid {t['border']};">
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Confidence</div>
                    <div style="font-size:1.25rem;font-weight:700;color:{t['primary']};">{risk['confidence']}%</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_finding_predictions(t: dict):
    """Render finding predictions."""
    
    st.markdown("### 🎯 Predicted Audit Findings")
    
    st.markdown(f'''
    <div style="background:{t['warning']}15;border:1px solid {t['warning']};border-radius:12px;padding:1rem;margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:0.75rem;">
            <span style="font-size:1.5rem;">🧠</span>
            <div>
                <div style="font-weight:600;color:{t['text']};">AI Analysis Complete</div>
                <div style="color:{t['text_secondary']};font-size:0.85rem;">Based on historical patterns, current KRIs, and industry trends</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Predicted findings
    predictions = [
        {
            "title": "Credit Concentration Breach",
            "probability": 87,
            "timing": "Within 60 days",
            "impact": "High",
            "basis": "Top 10 borrower exposure approaching 35% limit",
            "mitigation": "Review portfolio diversification strategy",
            "icon": "💰"
        },
        {
            "title": "KYC Documentation Gaps",
            "probability": 72,
            "timing": "Within 90 days",
            "impact": "Medium",
            "basis": "15% of high-risk customers missing updated documents",
            "mitigation": "Initiate customer outreach program",
            "icon": "📋"
        },
        {
            "title": "Cyber Security Vulnerability",
            "probability": 65,
            "timing": "Within 45 days",
            "impact": "Critical",
            "basis": "Patch management delays + increased threat landscape",
            "mitigation": "Accelerate patch deployment schedule",
            "icon": "🔒"
        },
        {
            "title": "Regulatory Reporting Delay",
            "probability": 58,
            "timing": "Within 30 days",
            "impact": "Medium",
            "basis": "System upgrade timeline conflicts with reporting deadline",
            "mitigation": "Prepare manual backup procedures",
            "icon": "📊"
        },
    ]
    
    cols = st.columns(2)
    
    for i, pred in enumerate(predictions):
        impact_colors = {"Critical": t['danger'], "High": t['warning'], "Medium": t['accent'], "Low": t['success']}
        impact_color = impact_colors.get(pred['impact'], t['text_muted'])
        
        with cols[i % 2]:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:1rem;position:relative;overflow:hidden;">
                <div style="position:absolute;top:0;right:0;width:100px;height:100px;background:{impact_color}10;border-radius:0 0 0 100px;"></div>
                
                <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:1rem;">
                    <div style="display:flex;gap:0.75rem;align-items:center;">
                        <span style="font-size:2rem;">{pred['icon']}</span>
                        <div>
                            <div style="font-weight:700;color:{t['text']};">{pred['title']}</div>
                            <div style="font-size:0.8rem;color:{t['text_muted']};">⏰ {pred['timing']}</div>
                        </div>
                    </div>
                    <div style="background:{impact_color};color:white;padding:0.25rem 0.75rem;border-radius:12px;font-size:0.7rem;font-weight:600;">
                        {pred['impact']} Impact
                    </div>
                </div>
                
                
                <div style="margin-bottom:1rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">
                        <span style="font-size:0.8rem;color:{t['text_muted']};">Probability</span>
                        <span style="font-weight:700;color:{t['primary']};">{pred['probability']}%</span>
                    </div>
                    <div style="height:8px;background:{t['border']};border-radius:4px;overflow:hidden;">
                        <div style="width:{pred['probability']}%;height:100%;background:linear-gradient(90deg, {t['success']}, {t['warning']}, {t['danger']});border-radius:4px;"></div>
                    </div>
                </div>
                
                <div style="background:{t['bg_secondary']};padding:0.75rem;border-radius:8px;margin-bottom:0.75rem;">
                    <div style="font-size:0.7rem;color:{t['text_muted']};margin-bottom:0.25rem;">📊 Analysis Basis</div>
                    <div style="font-size:0.85rem;color:{t['text']};">{pred['basis']}</div>
                </div>
                
                <div style="background:{t['success']}15;padding:0.75rem;border-radius:8px;">
                    <div style="font-size:0.7rem;color:{t['success']};margin-bottom:0.25rem;">💡 Recommended Mitigation</div>
                    <div style="font-size:0.85rem;color:{t['text']};">{pred['mitigation']}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)


def _render_timeline_projections(t: dict):
    """Render timeline projections."""
    
    st.markdown("### ⏰ Audit Timeline Projections")
    
    # Current audits with AI predictions
    audits = [
        {"name": "Credit Risk Assessment", "progress": 65, "planned_end": "Jan 30", "predicted_end": "Feb 5", "delay_days": 6, "confidence": 85},
        {"name": "IT General Controls", "progress": 45, "planned_end": "Feb 15", "predicted_end": "Feb 12", "delay_days": -3, "confidence": 78},
        {"name": "AML Compliance Review", "progress": 80, "planned_end": "Jan 20", "predicted_end": "Jan 22", "delay_days": 2, "confidence": 92},
        {"name": "Treasury Operations", "progress": 30, "planned_end": "Mar 1", "predicted_end": "Mar 15", "delay_days": 14, "confidence": 71},
    ]
    
    for audit in audits:
        status_color = t['success'] if audit['delay_days'] <= 0 else (t['warning'] if audit['delay_days'] <= 7 else t['danger'])
        delay_text = f"{audit['delay_days']} days late" if audit['delay_days'] > 0 else f"{abs(audit['delay_days'])} days early"
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                <div style="font-weight:700;color:{t['text']};">{audit['name']}</div>
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <div style="background:{status_color}20;color:{status_color};padding:0.25rem 0.75rem;border-radius:12px;font-size:0.75rem;font-weight:600;">
                        {delay_text}
                    </div>
                    <div style="font-size:0.75rem;color:{t['text_muted']};">
                        {audit['confidence']}% confidence
                    </div>
                </div>
            </div>
            
            <div style="height:24px;background:{t['border']};border-radius:12px;overflow:hidden;position:relative;margin-bottom:1rem;">
                <div style="width:{audit['progress']}%;height:100%;background:linear-gradient(90deg, {t['primary']}, {t['accent']});border-radius:12px;"></div>
                <div style="position:absolute;top:50%;left:{audit['progress']}%;transform:translate(-50%,-50%);background:white;padding:0.1rem 0.5rem;border-radius:8px;font-size:0.7rem;font-weight:600;color:{t['primary']};">
                    {audit['progress']}%
                </div>
            </div>
            
            <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                <div>
                    <span style="color:{t['text_muted']};">Planned: </span>
                    <span style="color:{t['text']};">{audit['planned_end']}</span>
                </div>
                <div>
                    <span style="color:{t['text_muted']};">AI Predicted: </span>
                    <span style="color:{status_color};font-weight:600;">{audit['predicted_end']}</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_ai_insights(t: dict):
    """Render AI-generated insights."""
    
    st.markdown("### 🧠 AI-Generated Insights")
    
    # Insight cards with different types
    insights = [
        {
            "type": "trend",
            "icon": "📈",
            "title": "Emerging Risk Pattern",
            "content": "AI detected a correlation between recent market volatility and increased credit defaults in the SME segment. Similar patterns preceded 2019 NPL spike.",
            "action": "Review SME Portfolio",
            "confidence": 89,
            "color": t['warning']
        },
        {
            "type": "anomaly",
            "icon": "🔍",
            "title": "Anomaly Detected",
            "content": "Unusual transaction pattern in Branch #45 - 340% increase in high-value transfers over past 2 weeks, deviating from historical baseline.",
            "action": "Investigate Branch",
            "confidence": 94,
            "color": t['danger']
        },
        {
            "type": "opportunity",
            "icon": "💡",
            "title": "Efficiency Opportunity",
            "content": "Based on similar audits, implementing data analytics for loan testing could reduce fieldwork by 40% while improving coverage.",
            "action": "View Approach",
            "confidence": 82,
            "color": t['success']
        },
        {
            "type": "regulatory",
            "icon": "📜",
            "title": "Regulatory Impact",
            "content": "New POJK draft regulation on cyber resilience expected Q2 2025. AI predicts significant control enhancement requirements.",
            "action": "Prepare Assessment",
            "confidence": 76,
            "color": t['primary']
        },
    ]
    
    cols = st.columns(2)
    
    for i, insight in enumerate(insights):
        with cols[i % 2]:
            st.markdown(f'''
            <div style="background:linear-gradient(135deg, {insight['color']}10, {t['card']});border:1px solid {insight['color']}40;border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:1rem;">
                    <div style="display:flex;gap:0.75rem;align-items:center;">
                        <div style="width:45px;height:45px;background:{insight['color']}20;border-radius:12px;display:flex;align-items:center;justify-content:center;">
                            <span style="font-size:1.5rem;">{insight['icon']}</span>
                        </div>
                        <div style="font-weight:700;color:{t['text']};">{insight['title']}</div>
                    </div>
                    <div style="background:{insight['color']};color:white;padding:0.2rem 0.6rem;border-radius:8px;font-size:0.65rem;font-weight:600;">
                        {insight['confidence']}%
                    </div>
                </div>
                
                <div style="color:{t['text_secondary']};font-size:0.9rem;margin-bottom:1rem;line-height:1.5;">
                    {insight['content']}
                </div>
                
                <button style="background:{insight['color']};color:white;border:none;padding:0.5rem 1rem;border-radius:8px;cursor:pointer;font-weight:600;font-size:0.85rem;width:100%;">
                    {insight['action']} →
                </button>
            </div>
            ''', unsafe_allow_html=True)
