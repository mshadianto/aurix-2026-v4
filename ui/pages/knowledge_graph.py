"""
Knowledge Graph Module for AURIX.
Interactive entity relationship visualization and knowledge exploration.
"""

import streamlit as st
from datetime import datetime
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the Knowledge Graph page."""
    t = get_current_theme()
    
    render_page_header(
        "Knowledge Graph",
        "🕸️",
        "Explore relationships between audit entities, risks, and controls"
    )
    
    # Hero visualization
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);border-radius:24px;padding:2rem;margin-bottom:2rem;position:relative;overflow:hidden;">
        
        <div style="position:absolute;top:20%;left:10%;width:8px;height:8px;background:#667eea;border-radius:50%;box-shadow:0 0 20px #667eea;animation:pulse 2s infinite;"></div>
        <div style="position:absolute;top:60%;left:20%;width:6px;height:6px;background:#f093fb;border-radius:50%;box-shadow:0 0 15px #f093fb;animation:pulse 2.5s infinite;"></div>
        <div style="position:absolute;top:30%;right:15%;width:10px;height:10px;background:#4facfe;border-radius:50%;box-shadow:0 0 25px #4facfe;animation:pulse 1.8s infinite;"></div>
        <div style="position:absolute;bottom:25%;right:25%;width:7px;height:7px;background:#43e97b;border-radius:50%;box-shadow:0 0 18px #43e97b;animation:pulse 2.2s infinite;"></div>
        <div style="position:absolute;top:70%;left:40%;width:5px;height:5px;background:#fa709a;border-radius:50%;box-shadow:0 0 12px #fa709a;animation:pulse 3s infinite;"></div>
        
        <div style="position:relative;z-index:1;text-align:center;">
            <div style="font-size:3rem;margin-bottom:1rem;">🕸️</div>
            <div style="color:white;font-size:1.75rem;font-weight:800;margin-bottom:0.5rem;">
                Audit Knowledge Graph
            </div>
            <div style="color:rgba(255,255,255,0.7);max-width:500px;margin:0 auto;">
                Discover hidden connections between risks, controls, findings, and regulations
            </div>
            
            <div style="display:flex;justify-content:center;gap:2rem;margin-top:2rem;">
                <div style="text-align:center;">
                    <div style="color:#667eea;font-size:2rem;font-weight:800;">1,247</div>
                    <div style="color:rgba(255,255,255,0.6);font-size:0.75rem;">Entities</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:#f093fb;font-size:2rem;font-weight:800;">3,891</div>
                    <div style="color:rgba(255,255,255,0.6);font-size:0.75rem;">Relationships</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:#43e97b;font-size:2rem;font-weight:800;">156</div>
                    <div style="color:rgba(255,255,255,0.6);font-size:0.75rem;">Clusters</div>
                </div>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.5); }}
        }}
    </style>
    ''', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Graph Explorer",
        "🔍 Entity Search",
        "📊 Relationship Analysis",
        "🎯 Impact Tracing"
    ])
    
    with tab1:
        _render_graph_explorer(t)
    
    with tab2:
        _render_entity_search(t)
    
    with tab3:
        _render_relationship_analysis(t)
    
    with tab4:
        _render_impact_tracing(t)
    
    render_footer()


def _render_graph_explorer(t: dict):
    """Render interactive graph explorer."""
    
    st.markdown("### 🌐 Interactive Graph Explorer")
    
    # Controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        entity_type = st.multiselect(
            "Entity Types",
            ["Risks", "Controls", "Findings", "Regulations", "Processes", "Systems"],
            default=["Risks", "Controls"]
        )
    
    with col2:
        depth = st.slider("Relationship Depth", 1, 5, 2)
    
    with col3:
        layout = st.selectbox("Layout", ["Force-directed", "Hierarchical", "Radial", "Circular"])
    
    with col4:
        st.write("")
        st.write("")
        if st.button("🔄 Refresh Graph", use_container_width=True):
            pass
    
    # Graph visualization (simulated with SVG)
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1rem;position:relative;overflow:hidden;">
        <svg width="100%" height="500" viewBox="0 0 800 500">
            
            <defs>
                <radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" style="stop-color:{t['primary']};stop-opacity:0.3"/>
                    <stop offset="100%" style="stop-color:{t['primary']};stop-opacity:0"/>
                </radialGradient>
            </defs>
            
            
            <g stroke="{t['border']}" stroke-width="2" opacity="0.5">
                
                <line x1="400" y1="250" x2="200" y2="150"/>
                <line x1="400" y1="250" x2="600" y2="150"/>
                <line x1="400" y1="250" x2="200" y2="350"/>
                <line x1="400" y1="250" x2="600" y2="350"/>
                <line x1="400" y1="250" x2="400" y2="80"/>
                <line x1="400" y1="250" x2="400" y2="420"/>
                
                
                <line x1="200" y1="150" x2="100" y2="100"/>
                <line x1="200" y1="150" x2="150" y2="250"/>
                <line x1="600" y1="150" x2="700" y2="100"/>
                <line x1="600" y1="150" x2="650" y2="250"/>
                <line x1="200" y1="350" x2="100" y2="400"/>
                <line x1="200" y1="350" x2="150" y2="280"/>
                <line x1="600" y1="350" x2="700" y2="400"/>
                <line x1="600" y1="350" x2="650" y2="280"/>
                
                
                <line x1="200" y1="150" x2="400" y2="80" stroke-dasharray="4"/>
                <line x1="600" y1="150" x2="400" y2="80" stroke-dasharray="4"/>
                <line x1="200" y1="350" x2="400" y2="420" stroke-dasharray="4"/>
                <line x1="600" y1="350" x2="400" y2="420" stroke-dasharray="4"/>
            </g>
            
            
            <circle cx="400" cy="250" r="50" fill="url(#nodeGlow)"/>
            <circle cx="400" cy="250" r="40" fill="{t['danger']}" stroke="white" stroke-width="3"/>
            <text x="400" y="245" fill="white" font-size="10" text-anchor="middle" font-weight="bold">Credit</text>
            <text x="400" y="258" fill="white" font-size="10" text-anchor="middle" font-weight="bold">Risk</text>
            
            
            <circle cx="400" cy="80" r="30" fill="{t['danger']}" opacity="0.8"/>
            <text x="400" y="85" fill="white" font-size="9" text-anchor="middle">Market Risk</text>
            
            <circle cx="400" cy="420" r="30" fill="{t['danger']}" opacity="0.8"/>
            <text x="400" y="425" fill="white" font-size="9" text-anchor="middle">Liquidity</text>
            
            
            <circle cx="200" cy="150" r="35" fill="{t['primary']}"/>
            <text x="200" y="145" fill="white" font-size="9" text-anchor="middle">Credit</text>
            <text x="200" y="158" fill="white" font-size="9" text-anchor="middle">Approval</text>
            
            <circle cx="600" cy="150" r="35" fill="{t['primary']}"/>
            <text x="600" y="145" fill="white" font-size="9" text-anchor="middle">Limit</text>
            <text x="600" y="158" fill="white" font-size="9" text-anchor="middle">Monitoring</text>
            
            <circle cx="200" cy="350" r="35" fill="{t['primary']}"/>
            <text x="200" y="345" fill="white" font-size="9" text-anchor="middle">Collateral</text>
            <text x="200" y="358" fill="white" font-size="9" text-anchor="middle">Valuation</text>
            
            <circle cx="600" cy="350" r="35" fill="{t['primary']}"/>
            <text x="600" y="345" fill="white" font-size="9" text-anchor="middle">Portfolio</text>
            <text x="600" y="358" fill="white" font-size="9" text-anchor="middle">Review</text>
            
            
            <circle cx="100" cy="100" r="25" fill="{t['warning']}"/>
            <text x="100" y="105" fill="white" font-size="8" text-anchor="middle">FND-001</text>
            
            <circle cx="700" cy="100" r="25" fill="{t['warning']}"/>
            <text x="700" y="105" fill="white" font-size="8" text-anchor="middle">FND-002</text>
            
            <circle cx="100" cy="400" r="25" fill="{t['warning']}"/>
            <text x="100" y="405" fill="white" font-size="8" text-anchor="middle">FND-003</text>
            
            <circle cx="700" cy="400" r="25" fill="{t['warning']}"/>
            <text x="700" y="405" fill="white" font-size="8" text-anchor="middle">FND-004</text>
            
            
            <circle cx="150" cy="250" r="25" fill="{t['success']}"/>
            <text x="150" y="255" fill="white" font-size="8" text-anchor="middle">POJK 40</text>
            
            <circle cx="650" cy="250" r="25" fill="{t['success']}"/>
            <text x="650" y="255" fill="white" font-size="8" text-anchor="middle">POJK 55</text>
            
            <circle cx="150" cy="280" r="20" fill="{t['success']}" opacity="0.7"/>
            <text x="150" y="283" fill="white" font-size="7" text-anchor="middle">SE-15</text>
            
            <circle cx="650" cy="280" r="20" fill="{t['success']}" opacity="0.7"/>
            <text x="650" y="283" fill="white" font-size="7" text-anchor="middle">Basel III</text>
        </svg>
        
        
        <div style="position:absolute;bottom:1rem;left:1rem;background:{t['bg_secondary']};padding:1rem;border-radius:8px;">
            <div style="font-size:0.75rem;font-weight:600;color:{t['text']};margin-bottom:0.5rem;">Legend</div>
            <div style="display:flex;gap:1rem;font-size:0.7rem;">
                <span style="display:flex;align-items:center;gap:0.25rem;"><span style="width:12px;height:12px;background:{t['danger']};border-radius:50%;"></span> Risk</span>
                <span style="display:flex;align-items:center;gap:0.25rem;"><span style="width:12px;height:12px;background:{t['primary']};border-radius:50%;"></span> Control</span>
                <span style="display:flex;align-items:center;gap:0.25rem;"><span style="width:12px;height:12px;background:{t['warning']};border-radius:50%;"></span> Finding</span>
                <span style="display:flex;align-items:center;gap:0.25rem;"><span style="width:12px;height:12px;background:{t['success']};border-radius:50%;"></span> Regulation</span>
            </div>
        </div>
        
        
        <div style="position:absolute;top:1rem;right:1rem;display:flex;flex-direction:column;gap:0.25rem;">
            <button style="width:32px;height:32px;background:{t['card']};border:1px solid {t['border']};border-radius:8px;cursor:pointer;font-size:1rem;">+</button>
            <button style="width:32px;height:32px;background:{t['card']};border:1px solid {t['border']};border-radius:8px;cursor:pointer;font-size:1rem;">−</button>
            <button style="width:32px;height:32px;background:{t['card']};border:1px solid {t['border']};border-radius:8px;cursor:pointer;font-size:0.8rem;">⟲</button>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Entity details panel
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📋 Selected Entity Details")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'''
        <div style="background:{t['danger']}15;border:2px solid {t['danger']};border-radius:16px;padding:1.5rem;text-align:center;">
            <div style="width:60px;height:60px;background:{t['danger']};border-radius:50%;margin:0 auto 1rem;display:flex;align-items:center;justify-content:center;">
                <span style="color:white;font-size:1.5rem;">💰</span>
            </div>
            <div style="font-weight:700;color:{t['text']};font-size:1.1rem;">Credit Risk</div>
            <div style="color:{t['text_muted']};font-size:0.85rem;">Risk Entity</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1rem;">
                <div style="text-align:center;padding:0.75rem;background:{t['bg_secondary']};border-radius:8px;">
                    <div style="font-size:1.25rem;font-weight:700;color:{t['primary']};">12</div>
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Controls</div>
                </div>
                <div style="text-align:center;padding:0.75rem;background:{t['bg_secondary']};border-radius:8px;">
                    <div style="font-size:1.25rem;font-weight:700;color:{t['warning']};">8</div>
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Findings</div>
                </div>
                <div style="text-align:center;padding:0.75rem;background:{t['bg_secondary']};border-radius:8px;">
                    <div style="font-size:1.25rem;font-weight:700;color:{t['success']};">5</div>
                    <div style="font-size:0.7rem;color:{t['text_muted']};">Regulations</div>
                </div>
            </div>
            
            <div style="font-size:0.85rem;color:{t['text_secondary']};margin-bottom:0.5rem;">
                Credit risk encompasses potential losses from borrower defaults, concentration, and collateral inadequacy.
            </div>
            
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
                <span style="background:{t['primary']}20;color:{t['primary']};padding:0.25rem 0.5rem;border-radius:6px;font-size:0.7rem;">High Priority</span>
                <span style="background:{t['warning']}20;color:{t['warning']};padding:0.25rem 0.5rem;border-radius:6px;font-size:0.7rem;">Quarterly Review</span>
                <span style="background:{t['success']}20;color:{t['success']};padding:0.25rem 0.5rem;border-radius:6px;font-size:0.7rem;">OJK Regulated</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_entity_search(t: dict):
    """Render entity search."""
    
    st.markdown("### 🔍 Entity Search")
    
    search_query = st.text_input("Search entities...", placeholder="Type to search risks, controls, findings, regulations...")
    
    if search_query:
        results = [
            {"type": "Risk", "name": "Credit Concentration Risk", "connections": 15, "icon": "⚠️", "color": t['danger']},
            {"type": "Control", "name": "Credit Limit Approval", "connections": 8, "icon": "🛡️", "color": t['primary']},
            {"type": "Finding", "name": "FND-2024-015: Credit Policy Gap", "connections": 6, "icon": "📋", "color": t['warning']},
            {"type": "Regulation", "name": "POJK 40/2019 Credit Risk", "connections": 12, "icon": "📜", "color": t['success']},
        ]
        
        for r in results:
            st.markdown(f'''
            <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.5rem;cursor:pointer;transition:all 0.2s;">
                <div style="display:flex;align-items:center;gap:1rem;">
                    <div style="width:40px;height:40px;background:{r['color']}20;border-radius:10px;display:flex;align-items:center;justify-content:center;">
                        <span style="font-size:1.25rem;">{r['icon']}</span>
                    </div>
                    <div style="flex:1;">
                        <div style="font-weight:600;color:{t['text']};">{r['name']}</div>
                        <div style="font-size:0.8rem;color:{t['text_muted']};">{r['type']} • {r['connections']} connections</div>
                    </div>
                    <div style="color:{t['text_muted']};">→</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)


def _render_relationship_analysis(t: dict):
    """Render relationship analysis."""
    
    st.markdown("### 📊 Relationship Analysis")
    
    # Relationship matrix
    st.markdown("#### Connection Strength Matrix")
    
    entities = ["Credit Risk", "Market Risk", "Op Risk", "IT Risk", "Compliance"]
    
    matrix_html = f'<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">'
    matrix_html += f'<tr><th style="padding:0.75rem;background:{t["bg_secondary"]};color:{t["text"]};"></th>'
    
    for entity in entities:
        matrix_html += f'<th style="padding:0.75rem;background:{t["bg_secondary"]};color:{t["text"]};text-align:center;font-size:0.8rem;">{entity}</th>'
    
    matrix_html += '</tr>'
    
    connections = [
        [100, 75, 60, 45, 80],
        [75, 100, 40, 30, 55],
        [60, 40, 100, 85, 70],
        [45, 30, 85, 100, 50],
        [80, 55, 70, 50, 100],
    ]
    
    for i, entity in enumerate(entities):
        matrix_html += f'<tr><td style="padding:0.75rem;background:{t["bg_secondary"]};color:{t["text"]};font-weight:600;font-size:0.8rem;">{entity}</td>'
        
        for j, conn in enumerate(connections[i]):
            if i == j:
                bg = t['primary']
                text = 'white'
            elif conn >= 70:
                bg = f'{t["success"]}80'
                text = 'white'
            elif conn >= 50:
                bg = f'{t["warning"]}60'
                text = t['text']
            else:
                bg = f'{t["border"]}'
                text = t['text_muted']
            
            matrix_html += f'<td style="padding:0.75rem;background:{bg};color:{text};text-align:center;font-weight:600;">{conn}%</td>'
        
        matrix_html += '</tr>'
    
    matrix_html += '</table></div>'
    
    st.markdown(matrix_html, unsafe_allow_html=True)


def _render_impact_tracing(t: dict):
    """Render impact tracing."""
    
    st.markdown("### 🎯 Impact Tracing")
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;">
        <div style="font-weight:600;color:{t['text']};margin-bottom:1rem;">Trace impact of changes across the knowledge graph</div>
        <div style="display:flex;gap:1rem;align-items:end;">
            <div style="flex:1;">
                <label style="font-size:0.8rem;color:{t['text_muted']};display:block;margin-bottom:0.25rem;">Select Entity</label>
                <select style="width:100%;padding:0.75rem;border:1px solid {t['border']};border-radius:8px;background:{t['bg_secondary']};color:{t['text']};">
                    <option>POJK 40/2019 - Credit Risk Regulation</option>
                    <option>Credit Approval Control</option>
                    <option>NPL Classification Process</option>
                </select>
            </div>
            <div style="flex:1;">
                <label style="font-size:0.8rem;color:{t['text_muted']};display:block;margin-bottom:0.25rem;">Change Type</label>
                <select style="width:100%;padding:0.75rem;border:1px solid {t['border']};border-radius:8px;background:{t['bg_secondary']};color:{t['text']};">
                    <option>Regulatory Update</option>
                    <option>Control Enhancement</option>
                    <option>Risk Rating Change</option>
                </select>
            </div>
            <button style="background:{t['primary']};color:white;border:none;padding:0.75rem 1.5rem;border-radius:8px;cursor:pointer;font-weight:600;">
                🔍 Trace Impact
            </button>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Impact cascade
    st.markdown("#### 📊 Impact Cascade")
    
    impacts = [
        {"level": 1, "entity": "Credit Policy Document", "type": "Document", "impact": "High", "action": "Requires Update"},
        {"level": 1, "entity": "Loan Approval Workflow", "type": "Process", "impact": "High", "action": "Requires Modification"},
        {"level": 2, "entity": "Credit Committee Terms", "type": "Document", "impact": "Medium", "action": "Review Required"},
        {"level": 2, "entity": "Risk Rating Model", "type": "System", "impact": "Medium", "action": "Recalibration"},
        {"level": 3, "entity": "Training Materials", "type": "Document", "impact": "Low", "action": "Minor Updates"},
        {"level": 3, "entity": "Audit Program - Credit", "type": "Audit", "impact": "Medium", "action": "Scope Adjustment"},
    ]
    
    for impact in impacts:
        indent = impact['level'] * 40
        impact_colors = {"High": t['danger'], "Medium": t['warning'], "Low": t['success']}
        color = impact_colors.get(impact['impact'], t['text_muted'])
        
        st.markdown(f'''
        <div style="margin-left:{indent}px;background:{t['card']};border-left:4px solid {color};border-radius:0 12px 12px 0;padding:1rem;margin-bottom:0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-weight:600;color:{t['text']};">{impact['entity']}</div>
                    <div style="font-size:0.8rem;color:{t['text_muted']};">{impact['type']} • Level {impact['level']} Impact</div>
                </div>
                <div style="text-align:right;">
                    <div style="background:{color}20;color:{color};padding:0.25rem 0.5rem;border-radius:8px;font-size:0.7rem;font-weight:600;margin-bottom:0.25rem;">
                        {impact['impact']} Impact
                    </div>
                    <div style="font-size:0.75rem;color:{t['text_secondary']};">{impact['action']}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
