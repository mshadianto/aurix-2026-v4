"""
Team Hub Module for AURIX.
Collaboration, team chat, and knowledge sharing.
"""

import streamlit as st
from datetime import datetime, timedelta
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the team hub page."""
    t = get_current_theme()
    
    render_page_header(
        "👥 Team Hub",
        "Collaborate, share knowledge, and connect with your team"
    )
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Team Chat",
        "📢 Announcements",
        "📚 Knowledge Base",
        "🏅 Recognition",
        "📅 Team Calendar"
    ])
    
    with tab1:
        _render_team_chat(t)
    
    with tab2:
        _render_announcements(t)
    
    with tab3:
        _render_knowledge_base(t)
    
    with tab4:
        _render_recognition(t)
    
    with tab5:
        _render_team_calendar(t)
    
    render_footer()


def _render_team_chat(t: dict):
    """Render team chat interface."""
    st.markdown("### 💬 Team Chat")
    
    # Channel selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;">
            <div style="font-weight:600;color:{t['text']};margin-bottom:1rem;">Channels</div>
        </div>
        ''', unsafe_allow_html=True)
        
        channels = [
            ("# general", 3),
            ("# credit-audit", 5),
            ("# it-audit", 2),
            ("# aml-team", 0),
            ("# random", 1),
        ]
        
        for channel, unread in channels:
            bg = t['primary'] + '20' if channel == "# general" else 'transparent'
            st.markdown(f'''
            <div style="padding:0.5rem;border-radius:8px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;background:{bg};">
                <span style="color:{t['text']};font-size:0.85rem;">{channel}</span>
                {f'<span style="background:{t["danger"]};color:white;padding:0.1rem 0.4rem;border-radius:10px;font-size:0.65rem;">{unread}</span>' if unread > 0 else ''}
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f'''
        <div style="font-weight:600;color:{t['text']};margin-bottom:0.5rem;">Direct Messages</div>
        ''', unsafe_allow_html=True)
        
        dms = [
            ("Ahmad R.", "online", 0),
            ("Budi S.", "away", 2),
            ("Citra D.", "online", 0),
            ("Dewi P.", "offline", 0),
        ]
        
        for name, status, unread in dms:
            status_color = {"online": t['success'], "away": t['warning'], "offline": t['text_muted']}[status]
            st.markdown(f'''
            <div style="padding:0.5rem;display:flex;align-items:center;gap:0.5rem;cursor:pointer;">
                <div style="position:relative;">
                    <div style="width:28px;height:28px;background:{t['primary']}30;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;">{name[0]}</div>
                    <div style="position:absolute;bottom:0;right:0;width:8px;height:8px;background:{status_color};border-radius:50%;border:2px solid {t['card']};"></div>
                </div>
                <span style="color:{t['text']};font-size:0.85rem;flex:1;">{name}</span>
                {f'<span style="background:{t["danger"]};color:white;padding:0.1rem 0.4rem;border-radius:10px;font-size:0.65rem;">{unread}</span>' if unread > 0 else ''}
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        # Chat header
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px 12px 0 0;padding:1rem;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-weight:600;color:{t['text']};"># general</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">8 members • General discussions</div>
            </div>
            <div style="display:flex;gap:0.5rem;">
                <span style="cursor:pointer;">📌</span>
                <span style="cursor:pointer;">🔍</span>
                <span style="cursor:pointer;">⚙️</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Messages
        messages = [
            {"user": "Ahmad R.", "time": "09:15", "text": "Good morning team! Reminder: Credit Risk draft report due this Friday 🎯", "reactions": [("👍", 3), ("✅", 2)]},
            {"user": "Budi S.", "time": "09:22", "text": "Thanks for the reminder! I'll have my section ready by Thursday.", "reactions": []},
            {"user": "Citra D.", "time": "09:30", "text": "FYI - I found a great template for IT control testing in the knowledge base. Check it out! 📚", "reactions": [("🙏", 2)]},
            {"user": "System", "time": "09:45", "text": "🤖 AI Assistant generated 5 new audit procedures for Credit Risk review", "reactions": [("👀", 4)], "is_system": True},
            {"user": "Dewi P.", "time": "10:00", "text": "Has anyone used the new sampling calculator? It's amazing! 🧮", "reactions": [("❤️", 3), ("🔥", 2)]},
        ]
        
        st.markdown(f'''
        <div style="background:{t['bg_secondary']};border-left:1px solid {t['border']};border-right:1px solid {t['border']};padding:1rem;height:350px;overflow-y:auto;">
        ''', unsafe_allow_html=True)
        
        for msg in messages:
            is_system = msg.get('is_system', False)
            
            if is_system:
                st.markdown(f'''
                <div style="text-align:center;margin:1rem 0;">
                    <span style="background:{t['primary']}20;color:{t['primary']};padding:0.5rem 1rem;border-radius:20px;font-size:0.8rem;">
                        {msg['text']}
                    </span>
                </div>
                ''', unsafe_allow_html=True)
            else:
                reactions_html = ' '.join([f'<span style="background:{t["card"]};padding:0.1rem 0.4rem;border-radius:10px;font-size:0.7rem;margin-right:0.25rem;">{r} {c}</span>' for r, c in msg['reactions']])
                
                st.markdown(f'''
                <div style="margin-bottom:1rem;">
                    <div style="display:flex;align-items:start;gap:0.75rem;">
                        <div style="width:36px;height:36px;background:{t['primary']}30;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:600;flex-shrink:0;">
                            {msg['user'][0]}
                        </div>
                        <div style="flex:1;">
                            <div style="display:flex;align-items:center;gap:0.5rem;">
                                <span style="font-weight:600;color:{t['text']};">{msg['user']}</span>
                                <span style="font-size:0.7rem;color:{t['text_muted']};">{msg['time']}</span>
                            </div>
                            <div style="color:{t['text_secondary']};margin-top:0.25rem;">{msg['text']}</div>
                            {f'<div style="margin-top:0.5rem;">{reactions_html}</div>' if reactions_html else ''}
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Message input
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            st.text_input("Message", placeholder="Type a message...", label_visibility="collapsed")
        with col_btn:
            st.button("Send", type="primary", use_container_width=True)


def _render_announcements(t: dict):
    """Render announcements section."""
    st.markdown("### 📢 Announcements")
    
    announcements = [
        {
            "title": "🎉 AURIX v4.2 Released!",
            "content": "We're excited to announce the release of AURIX v4.2 with new features including Gamification, AI Lab, and Command Center. Check out what's new!",
            "author": "System Admin",
            "date": "Today",
            "priority": "high",
            "pinned": True
        },
        {
            "title": "📅 Q1 Audit Committee Meeting",
            "content": "Reminder: Q1 Audit Committee presentation scheduled for March 31, 2025. Please ensure all reports are finalized by March 25.",
            "author": "CAE Office",
            "date": "Yesterday",
            "priority": "high",
            "pinned": True
        },
        {
            "title": "📚 New Training: AI-Assisted Auditing",
            "content": "Sign up for our upcoming workshop on leveraging AI tools in audit work. Limited seats available!",
            "author": "L&D Team",
            "date": "2 days ago",
            "priority": "medium",
            "pinned": False
        },
        {
            "title": "🏆 Employee of the Month: Ahmad R.",
            "content": "Congratulations to Ahmad for outstanding performance in the Credit Risk audit! Well deserved! 👏",
            "author": "HR",
            "date": "3 days ago",
            "priority": "low",
            "pinned": False
        },
    ]
    
    priority_colors = {"high": t['danger'], "medium": t['warning'], "low": t['success']}
    
    for ann in announcements:
        color = priority_colors.get(ann['priority'], t['text_muted'])
        
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-left:4px solid {color};border-radius:0 16px 16px 0;padding:1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.75rem;">
                <div style="font-weight:700;color:{t['text']};font-size:1.1rem;">
                    {'📌 ' if ann['pinned'] else ''}{ann['title']}
                </div>
                <span style="background:{color}20;color:{color};padding:0.2rem 0.6rem;border-radius:12px;font-size:0.7rem;text-transform:uppercase;">{ann['priority']}</span>
            </div>
            <div style="color:{t['text_secondary']};margin-bottom:1rem;">{ann['content']}</div>
            <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:{t['text_muted']};">
                <span>👤 {ann['author']}</span>
                <span>🕐 {ann['date']}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_knowledge_base(t: dict):
    """Render knowledge base section."""
    st.markdown("### 📚 Knowledge Base")
    
    # Search
    search = st.text_input("🔍 Search knowledge base", placeholder="Search articles, templates, guides...")
    
    # Categories
    categories = [
        ("📋", "Audit Procedures", 45, t['primary']),
        ("📝", "Templates", 32, t['accent']),
        ("📖", "Guidelines", 28, t['success']),
        ("🎓", "Training Materials", 15, t['warning']),
        ("❓", "FAQs", 52, t['danger']),
    ]
    
    cols = st.columns(5)
    for col, (icon, name, count, color) in zip(cols, categories):
        with col:
            st.markdown(f'''
            <div style="background:{color}15;border:1px solid {color};border-radius:12px;padding:1rem;text-align:center;cursor:pointer;transition:transform 0.2s;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:600;color:{t['text']};font-size:0.85rem;">{name}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{count} items</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Popular articles
    st.markdown("#### 🔥 Popular Articles")
    
    articles = [
        {"title": "Complete Guide to Risk-Based Auditing", "category": "Guidelines", "views": 1250, "rating": 4.9},
        {"title": "AI Prompt Templates for Audit", "category": "Templates", "views": 980, "rating": 4.8},
        {"title": "POJK Compliance Checklist 2024", "category": "Audit Procedures", "views": 875, "rating": 4.7},
        {"title": "Sampling Methodology Best Practices", "category": "Guidelines", "views": 720, "rating": 4.6},
    ]
    
    for article in articles:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.5rem;display:flex;justify-content:space-between;align-items:center;cursor:pointer;transition:background 0.2s;">
            <div>
                <div style="font-weight:600;color:{t['text']};">{article['title']}</div>
                <div style="font-size:0.8rem;color:{t['text_muted']};">📁 {article['category']} • 👁️ {article['views']} views</div>
            </div>
            <div style="display:flex;align-items:center;gap:0.25rem;">
                <span style="color:{t['warning']};">⭐</span>
                <span style="font-weight:600;color:{t['text']};">{article['rating']}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def _render_recognition(t: dict):
    """Render recognition wall."""
    st.markdown("### 🏅 Recognition Wall")
    
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, {t['warning']}20, {t['warning']}10);border:1px solid {t['warning']};border-radius:16px;padding:2rem;margin-bottom:2rem;text-align:center;">
        <div style="font-size:3rem;margin-bottom:1rem;">🏆</div>
        <div style="font-size:1.25rem;font-weight:700;color:{t['text']};margin-bottom:0.5rem;">Employee of the Month</div>
        <div style="font-size:2rem;font-weight:700;color:{t['warning']};">Ahmad Ramadhan</div>
        <div style="color:{t['text_secondary']};margin-top:0.5rem;">Outstanding performance in Credit Risk Audit</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Kudos feed
    st.markdown("#### 👏 Recent Kudos")
    
    kudos = [
        {"from": "Budi S.", "to": "Citra D.", "message": "Great work on the IT controls documentation!", "badge": "⭐ Quality Star"},
        {"from": "CAE", "to": "AML Team", "message": "Excellent job on the regulatory examination prep!", "badge": "🏅 Team Excellence"},
        {"from": "Dewi P.", "to": "Ahmad R.", "message": "Thanks for the mentoring sessions!", "badge": "🎓 Mentor"},
        {"from": "Citra D.", "to": "Budi S.", "message": "Amazing analytical skills on the fraud case!", "badge": "🔍 Sharp Eye"},
    ]
    
    for k in kudos:
        st.markdown(f'''
        <div style="background:{t['card']};border:1px solid {t['border']};border-radius:12px;padding:1rem;margin-bottom:0.5rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                <span style="background:{t['success']}20;color:{t['success']};padding:0.2rem 0.6rem;border-radius:12px;font-size:0.75rem;">{k['badge']}</span>
            </div>
            <div style="color:{t['text']};">
                <strong>{k['from']}</strong> recognized <strong>{k['to']}</strong>
            </div>
            <div style="color:{t['text_secondary']};font-style:italic;margin-top:0.25rem;">"{k['message']}"</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Give kudos
    st.markdown("#### 🎁 Give Kudos")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("To", ["Ahmad R.", "Budi S.", "Citra D.", "Dewi P."])
    with col2:
        st.selectbox("Badge", ["⭐ Quality Star", "🏅 Team Excellence", "🎓 Mentor", "🔍 Sharp Eye", "🚀 Innovator"])
    st.text_input("Message", placeholder="Write your appreciation...")
    st.button("🎉 Send Kudos", type="primary")


def _render_team_calendar(t: dict):
    """Render team calendar."""
    st.markdown("### 📅 Team Calendar")
    
    # Calendar header
    st.markdown(f'''
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
        <div style="display:flex;gap:0.5rem;">
            <button style="background:{t['card']};border:1px solid {t['border']};padding:0.5rem 1rem;border-radius:8px;cursor:pointer;">◀</button>
            <button style="background:{t['card']};border:1px solid {t['border']};padding:0.5rem 1rem;border-radius:8px;cursor:pointer;">▶</button>
        </div>
        <div style="font-size:1.25rem;font-weight:700;color:{t['text']};">January 2025</div>
        <button style="background:{t['primary']};color:white;border:none;padding:0.5rem 1rem;border-radius:8px;cursor:pointer;">+ Add Event</button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Calendar grid
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    st.markdown(f'''
    <div style="background:{t['card']};border:1px solid {t['border']};border-radius:16px;overflow:hidden;">
        
        <div style="display:grid;grid-template-columns:repeat(7, 1fr);background:{t['bg_secondary']};">
            {''.join([f'<div style="padding:1rem;text-align:center;font-weight:600;color:{t["text"]};border-right:1px solid {t["border"]};">{d}</div>' for d in days])}
        </div>
        
        
        <div style="display:grid;grid-template-columns:repeat(7, 1fr);">
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text_muted']};">30</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text_muted']};">31</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text']};">1</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text']};">2</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text']};">3</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text_muted']};">4</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text_muted']};">5</div>
        </div>
        
        
        <div style="display:grid;grid-template-columns:repeat(7, 1fr);">
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text']};">6</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text']};">7</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text']};">8
                <div style="background:{t['primary']};color:white;padding:0.2rem 0.4rem;border-radius:4px;font-size:0.65rem;margin-top:0.25rem;">Credit Audit</div>
            </div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text']};">9</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};background:{t['primary']}10;color:{t['text']};font-weight:600;">10
                <div style="background:{t['warning']};color:white;padding:0.2rem 0.4rem;border-radius:4px;font-size:0.65rem;margin-top:0.25rem;">Team Meeting</div>
            </div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text_muted']};">11</div>
            <div style="padding:0.5rem;min-height:80px;border:1px solid {t['border']};color:{t['text_muted']};">12</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Upcoming events
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📌 Upcoming Events")
    
    events = [
        {"date": "Jan 10", "time": "09:00", "title": "Weekly Team Meeting", "type": "meeting"},
        {"date": "Jan 12", "time": "14:00", "title": "Credit Audit Kickoff", "type": "audit"},
        {"date": "Jan 15", "time": "10:00", "title": "OJK Liaison Call", "type": "external"},
    ]
    
    type_colors = {"meeting": t['primary'], "audit": t['success'], "external": t['warning']}
    
    for event in events:
        color = type_colors.get(event['type'], t['text_muted'])
        st.markdown(f'''
        <div style="display:flex;align-items:center;gap:1rem;padding:0.75rem;background:{t['card']};border:1px solid {t['border']};border-left:4px solid {color};border-radius:0 8px 8px 0;margin-bottom:0.5rem;">
            <div style="text-align:center;min-width:60px;">
                <div style="font-weight:700;color:{t['text']};">{event['date']}</div>
                <div style="font-size:0.75rem;color:{t['text_muted']};">{event['time']}</div>
            </div>
            <div style="font-weight:500;color:{t['text']};">{event['title']}</div>
        </div>
        ''', unsafe_allow_html=True)
