"""
Visitor Service for AURIX.
Handles visitor tracking and analytics.
"""

import streamlit as st
import random
from datetime import datetime
from typing import Dict, Any, Optional

from utils.logger import get_logger

logger = get_logger(__name__)


def get_visitor_stats() -> Dict[str, Any]:
    """
    Get visitor statistics.
    Falls back to mock data if database is not available.
    
    Returns:
        Dictionary containing visitor statistics
    """
    # Try to get from database
    stats = _get_stats_from_database()
    
    if stats:
        return stats
    
    # Fallback to mock data
    logger.warning("Database not connected - using mock visitor data")
    return _get_mock_stats()


def _get_stats_from_database() -> Optional[Dict[str, Any]]:
    """Attempt to get stats from database."""
    try:
        from infrastructure.database.postgres import get_db_connection, return_db_connection
        
        conn = get_db_connection()
        if not conn:
            return None
        
        cur = conn.cursor()
        
        # Total visits
        cur.execute("SELECT SUM(total_visits) FROM daily_stats")
        total_visits = cur.fetchone()[0] or 0
        
        # Unique visitors
        cur.execute("SELECT COUNT(DISTINCT visitor_id) FROM visitor_sessions")
        unique_visitors = cur.fetchone()[0] or 0
        
        # Total page views
        cur.execute("SELECT COUNT(*) FROM page_views")
        total_page_views = cur.fetchone()[0] or 0
        
        # Average session duration
        cur.execute("SELECT AVG(session_duration) FROM page_views WHERE session_duration > 0")
        avg_duration = cur.fetchone()[0] or 0
        
        # Today's stats
        today = datetime.now().date()
        cur.execute("SELECT total_visits, unique_visitors FROM daily_stats WHERE stat_date = %s", (today,))
        today_stats = cur.fetchone()
        today_visits = today_stats[0] if today_stats else 0
        today_visitors = today_stats[1] if today_stats else 0
        
        # Popular pages
        cur.execute("""
            SELECT page_name, COUNT(*) as views
            FROM page_views
            GROUP BY page_name
            ORDER BY views DESC
            LIMIT 5
        """)
        popular_pages = cur.fetchall()
        
        # Hourly traffic
        cur.execute("""
            SELECT EXTRACT(HOUR FROM view_timestamp) as hour, COUNT(*) as views
            FROM page_views
            WHERE view_timestamp > NOW() - INTERVAL '24 hours'
            GROUP BY hour
            ORDER BY hour
        """)
        hourly_data = cur.fetchall()
        hourly_traffic = [0] * 24
        for hour, views in hourly_data:
            hourly_traffic[int(hour)] = views
        
        cur.close()
        return_db_connection(conn)
        
        logger.info(f"Real data retrieved: {total_visits} visits, {unique_visitors} unique visitors")
        
        return {
            'total_visits': total_visits,
            'unique_visitors': unique_visitors,
            'total_page_views': total_page_views,
            'avg_session_duration': int(avg_duration) if avg_duration else 0,
            'today_visits': today_visits,
            'today_visitors': today_visitors,
            'popular_pages': popular_pages,
            'hourly_traffic': hourly_traffic,
            'is_mock': False
        }
        
    except Exception as e:
        logger.error(f"Error getting stats from database: {e}")
        return None


def _get_mock_stats() -> Dict[str, Any]:
    """Generate mock visitor statistics."""
    return {
        'total_visits': random.randint(1000, 5000),
        'unique_visitors': random.randint(100, 500),
        'total_page_views': random.randint(5000, 20000),
        'avg_session_duration': random.randint(300, 1800),
        'today_visits': random.randint(50, 200),
        'today_visitors': random.randint(10, 50),
        'popular_pages': [
            ('Dashboard', random.randint(100, 500)),
            ('KRI Monitor', random.randint(80, 300)),
            ('Fraud Detection', random.randint(60, 200)),
            ('Data Analytics', random.randint(50, 150)),
            ('Documents', random.randint(40, 100))
        ],
        'hourly_traffic': [random.randint(10, 50) for _ in range(24)],
        'is_mock': True
    }


def track_page_view(page_name: str):
    """
    Track a page view.
    
    Args:
        page_name: Name of the page being viewed
    """
    # Update session state
    st.session_state.page_views = st.session_state.get('page_views', 0) + 1
    
    if 'visited_pages' not in st.session_state:
        st.session_state.visited_pages = []
    
    st.session_state.visited_pages.append({
        'page': page_name,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Try to track in database
    _track_in_database(page_name)


def _track_in_database(page_name: str):
    """Track page view in database."""
    try:
        from infrastructure.database.postgres import get_db_connection, return_db_connection
        
        conn = get_db_connection()
        if not conn:
            return
        
        cur = conn.cursor()
        
        session_duration = int(
            (datetime.now() - st.session_state.get('session_start', datetime.now())).total_seconds()
        )
        
        cur.execute("""
            INSERT INTO page_views (visitor_id, page_name, session_duration)
            VALUES (%s, %s, %s)
        """, (st.session_state.get('visitor_id', 'unknown'), page_name, session_duration))
        
        # Update daily stats
        today = datetime.now().date()
        cur.execute("""
            INSERT INTO daily_stats (stat_date, total_visits, unique_visitors, total_page_views)
            VALUES (%s, 1, 1, 1)
            ON CONFLICT (stat_date)
            DO UPDATE SET
                total_visits = daily_stats.total_visits + 1,
                total_page_views = daily_stats.total_page_views + 1,
                updated_at = CURRENT_TIMESTAMP
        """, (today,))
        
        conn.commit()
        cur.close()
        return_db_connection(conn)
        
    except Exception as e:
        logger.debug(f"Could not track page view in database: {e}")
