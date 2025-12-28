"""
Gamification Center Module for AURIX.
Achievements, badges, XP system, and team leaderboard.
"""

import streamlit as st
from datetime import datetime, timedelta
import random

from ui.styles.css_builder import get_current_theme
from ui.components import render_page_header, render_footer


def render():
    """Render the gamification center page."""
    t = get_current_theme()
    
    render_page_header(
        "🎮 Gamification Center",
        "Track achievements, earn badges, and compete with your team!"
    )
    
    # Initialize gamification state
    _init_gamification_state()
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 My Progress",
        "🎖️ Badges",
        "📊 Leaderboard",
        "🎯 Challenges",
        "🎁 Rewards"
    ])
    
    with tab1:
        _render_my_progress(t)
    
    with tab2:
        _render_badges(t)
    
    with tab3:
        _render_leaderboard(t)
    
    with tab4:
        _render_challenges(t)
    
    with tab5:
        _render_rewards(t)
    
    render_footer()


def _init_gamification_state():
    """Initialize gamification session state."""
    if 'user_xp' not in st.session_state:
        st.session_state.user_xp = 2450
    if 'user_level' not in st.session_state:
        st.session_state.user_level = 12
    if 'user_badges' not in st.session_state:
        st.session_state.user_badges = ['first_audit', 'risk_hunter', 'speed_demon', 'perfectionist', 'team_player']
    if 'daily_streak' not in st.session_state:
        st.session_state.daily_streak = 7
    if 'weekly_goals' not in st.session_state:
        st.session_state.weekly_goals = {'findings': 8, 'workpapers': 5, 'reviews': 12}


def _render_my_progress(t: dict):
    """Render user progress dashboard."""
    
    xp = st.session_state.user_xp
    level = st.session_state.user_level
    xp_for_next = level * 250
    xp_progress = int((xp % 250) / 250 * 100)
    daily_streak = st.session_state.daily_streak
    
    # Progress header card
    header_html = (
        '<div style="background:linear-gradient(135deg, ' + t['primary'] + ', ' + t['accent'] + ');border-radius:20px;padding:2rem;margin-bottom:2rem;color:white;">'
        '<div style="text-align:center;margin-bottom:1rem;">'
        '<div style="font-size:3rem;margin-bottom:0.5rem;">👨‍💼</div>'
        '<div style="font-size:0.9rem;opacity:0.9;text-transform:uppercase;">Senior Auditor</div>'
        '<div style="font-size:2.5rem;font-weight:700;">Level ' + str(level) + '</div>'
        '</div>'
        '<div style="max-width:400px;margin:0 auto;">'
        '<div style="font-size:0.9rem;opacity:0.8;margin-bottom:0.5rem;text-align:center;">' + str(xp) + ' / ' + str(xp_for_next) + ' XP to next level</div>'
        '<div style="height:12px;background:rgba(255,255,255,0.2);border-radius:6px;overflow:hidden;">'
        '<div style="width:' + str(xp_progress) + '%;height:100%;background:rgba(255,255,255,0.9);border-radius:6px;"></div>'
        '</div>'
        '</div>'
        '<div style="text-align:center;margin-top:1.5rem;">'
        '<span style="background:rgba(255,255,255,0.2);padding:0.75rem 1.5rem;border-radius:12px;">'
        '🔥 ' + str(daily_streak) + ' Day Streak'
        '</span>'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Stats Grid
    stats = [
        ("🎯", "Audits Completed", "47", "+3 this week", t['success']),
        ("📋", "Findings Documented", "156", "+12 this week", t['primary']),
        ("⏱️", "Hours Logged", "1,248", "+42 this week", t['accent']),
        ("⭐", "Quality Score", "94%", "+2% vs last month", t['warning']),
    ]
    
    cols = st.columns(4)
    for col, (icon, label, value, change, color) in zip(cols, stats):
        with col:
            html = (
                '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:16px;padding:1.25rem;text-align:center;">'
                '<div style="font-size:2rem;margin-bottom:0.5rem;">' + icon + '</div>'
                '<div style="font-size:1.75rem;font-weight:700;color:' + color + ';">' + value + '</div>'
                '<div style="font-size:0.8rem;color:' + t['text_muted'] + ';margin-bottom:0.25rem;">' + label + '</div>'
                '<div style="font-size:0.7rem;color:' + t['success'] + ';">📈 ' + change + '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Weekly Goals
    st.markdown("### 🎯 Weekly Goals")
    
    goals = [
        ("Document Findings", 8, 12, "📋"),
        ("Complete Workpapers", 5, 8, "📝"),
        ("Review Documents", 12, 15, "👁️"),
        ("AI Consultations", 20, 20, "🤖"),
    ]
    
    for label, current, target, icon in goals:
        progress = min(int(current / target * 100), 100)
        is_complete = current >= target
        status_text = str(current) + "/" + str(target)
        if is_complete:
            status_text += " ✅"
        
        html = (
            '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:12px;padding:1rem;margin-bottom:0.75rem;">'
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
            '<span style="color:' + t['text'] + ';font-weight:500;">' + icon + ' ' + label + '</span>'
            '<span style="color:' + (t['success'] if is_complete else t['text_muted']) + ';font-weight:600;">' + status_text + '</span>'
            '</div>'
            '<div style="height:8px;background:' + t['border'] + ';border-radius:4px;overflow:hidden;">'
            '<div style="width:' + str(progress) + '%;height:100%;background:' + (t['success'] if is_complete else t['primary']) + ';border-radius:4px;"></div>'
            '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def _render_badges(t: dict):
    """Render badges collection."""
    st.markdown("### 🎖️ Badge Collection")
    
    badges = [
        {"id": "first_audit", "name": "First Audit", "icon": "🌟", "desc": "Complete your first audit", "earned": True},
        {"id": "risk_hunter", "name": "Risk Hunter", "icon": "🎯", "desc": "Identify 50 risks", "earned": True},
        {"id": "speed_demon", "name": "Speed Demon", "icon": "⚡", "desc": "Complete audit in record time", "earned": True},
        {"id": "perfectionist", "name": "Perfectionist", "icon": "💎", "desc": "100% quality score", "earned": True},
        {"id": "team_player", "name": "Team Player", "icon": "🤝", "desc": "Help 10 colleagues", "earned": True},
        {"id": "ai_master", "name": "AI Master", "icon": "🤖", "desc": "Use AI 100 times", "earned": False},
        {"id": "doc_ninja", "name": "Doc Ninja", "icon": "📄", "desc": "Process 500 documents", "earned": False},
        {"id": "streak_king", "name": "Streak King", "icon": "🔥", "desc": "30-day login streak", "earned": False},
    ]
    
    cols = st.columns(4)
    for i, badge in enumerate(badges):
        with cols[i % 4]:
            opacity = "1" if badge['earned'] else "0.4"
            border_color = t['accent'] if badge['earned'] else t['border']
            
            html = (
                '<div style="background:' + t['card'] + ';border:2px solid ' + border_color + ';border-radius:16px;padding:1.5rem;text-align:center;margin-bottom:1rem;opacity:' + opacity + ';">'
                '<div style="font-size:3rem;margin-bottom:0.5rem;">' + badge['icon'] + '</div>'
                '<div style="font-weight:700;color:' + t['text'] + ';margin-bottom:0.25rem;">' + badge['name'] + '</div>'
                '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">' + badge['desc'] + '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)


def _render_leaderboard(t: dict):
    """Render team leaderboard."""
    st.markdown("### 📊 Team Leaderboard")
    
    leaderboard = [
        {"rank": 1, "name": "Ahmad R.", "xp": 15420, "level": 18, "badge": "🥇"},
        {"rank": 2, "name": "Citra D.", "xp": 12850, "level": 16, "badge": "🥈"},
        {"rank": 3, "name": "Budi S.", "xp": 11200, "level": 15, "badge": "🥉"},
        {"rank": 4, "name": "You", "xp": 2450, "level": 12, "badge": ""},
        {"rank": 5, "name": "Dewi P.", "xp": 2100, "level": 11, "badge": ""},
        {"rank": 6, "name": "Eko P.", "xp": 1850, "level": 10, "badge": ""},
    ]
    
    for entry in leaderboard:
        is_you = entry['name'] == "You"
        bg_color = t['primary'] + "20" if is_you else t['card']
        border = "2px solid " + t['primary'] if is_you else "1px solid " + t['border']
        
        html = (
            '<div style="background:' + bg_color + ';border:' + border + ';border-radius:12px;padding:1rem;margin-bottom:0.5rem;">'
            '<div style="display:flex;align-items:center;gap:1rem;">'
            '<div style="font-size:1.5rem;font-weight:700;color:' + t['text'] + ';width:40px;">#' + str(entry['rank']) + '</div>'
            '<div style="font-size:1.5rem;">' + entry['badge'] + '</div>'
            '<div style="flex:1;">'
            '<div style="font-weight:600;color:' + t['text'] + ';">' + entry['name'] + '</div>'
            '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';">Level ' + str(entry['level']) + '</div>'
            '</div>'
            '<div style="text-align:right;">'
            '<div style="font-weight:700;color:' + t['accent'] + ';">' + str(entry['xp']) + ' XP</div>'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def _render_challenges(t: dict):
    """Render active challenges."""
    st.markdown("### 🎯 Active Challenges")
    
    challenges = [
        {"name": "Speed Auditor", "desc": "Complete 3 audits this week", "progress": 2, "target": 3, "reward": "500 XP", "deadline": "3 days"},
        {"name": "Risk Master", "desc": "Identify 10 high risks", "progress": 7, "target": 10, "reward": "300 XP", "deadline": "5 days"},
        {"name": "Documentation Pro", "desc": "Create 20 workpapers", "progress": 15, "target": 20, "reward": "400 XP", "deadline": "1 week"},
        {"name": "AI Explorer", "desc": "Use AI assistant 50 times", "progress": 35, "target": 50, "reward": "250 XP", "deadline": "2 weeks"},
    ]
    
    for challenge in challenges:
        progress_pct = int(challenge['progress'] / challenge['target'] * 100)
        
        html = (
            '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:12px;padding:1.25rem;margin-bottom:1rem;">'
            '<div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.75rem;">'
            '<div>'
            '<div style="font-weight:700;color:' + t['text'] + ';">' + challenge['name'] + '</div>'
            '<div style="font-size:0.8rem;color:' + t['text_muted'] + ';">' + challenge['desc'] + '</div>'
            '</div>'
            '<div style="text-align:right;">'
            '<div style="font-weight:600;color:' + t['accent'] + ';">🎁 ' + challenge['reward'] + '</div>'
            '<div style="font-size:0.7rem;color:' + t['text_muted'] + ';">⏰ ' + challenge['deadline'] + '</div>'
            '</div>'
            '</div>'
            '<div style="height:8px;background:' + t['border'] + ';border-radius:4px;overflow:hidden;margin-bottom:0.5rem;">'
            '<div style="width:' + str(progress_pct) + '%;height:100%;background:' + t['primary'] + ';border-radius:4px;"></div>'
            '</div>'
            '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';text-align:right;">' + str(challenge['progress']) + '/' + str(challenge['target']) + ' completed</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def _render_rewards(t: dict):
    """Render rewards shop."""
    st.markdown("### 🎁 Rewards Shop")
    
    st.info("💡 Earn XP by completing audits, documenting findings, and helping your team!")
    
    rewards = [
        {"name": "Extra Day Off", "cost": 5000, "icon": "🏖️", "desc": "Redeem for 1 additional PTO day"},
        {"name": "Premium Training", "cost": 3000, "icon": "📚", "desc": "Access to premium audit courses"},
        {"name": "Coffee Voucher", "cost": 500, "icon": "☕", "desc": "Free coffee for a week"},
        {"name": "Custom Badge", "cost": 2000, "icon": "🎨", "desc": "Create your own profile badge"},
        {"name": "Team Lunch", "cost": 4000, "icon": "🍕", "desc": "Free lunch for your team"},
        {"name": "Early Leave Pass", "cost": 1000, "icon": "🚪", "desc": "Leave 2 hours early (once)"},
    ]
    
    user_xp = st.session_state.user_xp
    
    cols = st.columns(3)
    for i, reward in enumerate(rewards):
        with cols[i % 3]:
            can_afford = user_xp >= reward['cost']
            opacity = "1" if can_afford else "0.6"
            
            html = (
                '<div style="background:' + t['card'] + ';border:1px solid ' + t['border'] + ';border-radius:16px;padding:1.5rem;text-align:center;margin-bottom:1rem;opacity:' + opacity + ';">'
                '<div style="font-size:3rem;margin-bottom:0.75rem;">' + reward['icon'] + '</div>'
                '<div style="font-weight:700;color:' + t['text'] + ';margin-bottom:0.25rem;">' + reward['name'] + '</div>'
                '<div style="font-size:0.75rem;color:' + t['text_muted'] + ';margin-bottom:0.75rem;min-height:36px;">' + reward['desc'] + '</div>'
                '<div style="background:' + t['accent'] + ';color:white;padding:0.5rem 1rem;border-radius:8px;font-weight:600;">'
                + str(reward['cost']) + ' XP'
                '</div>'
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)
