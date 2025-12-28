"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║     █████╗ ██╗   ██╗██████╗ ██╗██╗  ██╗                                      ║
║    ██╔══██╗██║   ██║██╔══██╗██║╚██╗██╔╝                                      ║
║    ███████║██║   ██║██████╔╝██║ ╚███╔╝                                       ║
║    ██╔══██║██║   ██║██╔══██╗██║ ██╔██╗                                       ║
║    ██║  ██║╚██████╔╝██║  ██║██║██╔╝ ██╗                                      ║
║    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝                                      ║
║                                                                               ║
║    AUdit Risk Intelligence eXcellence                                        ║
║    Intelligent Audit. Elevated Assurance.                                    ║
║    Version: 4.2 Excellence 2026                                              ║
║                                                                               ║
║    🆕 2026 Features:                                                          ║
║    • Grouped Navigation + Floating AI Copilot                                ║
║    • Active KRI Cards with AI Analysis                                       ║
║    • Process Mining with DFG Visualization                                   ║
║    • Regulatory RAG (OJK/BI/BPKH)                                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Streamlit entry point for AURIX application.
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add app to path for imports
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import after path setup
from app.config import settings, init_app
from app.router import Router
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="AURIX | Intelligent Audit Platform",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/mshadianto/aurix',
            'Report a bug': 'https://github.com/mshadianto/aurix/issues',
            'About': f"""
            ## AURIX v{settings.app_version}
            
            **AUdit Risk Intelligence eXcellence**
            
            A comprehensive AI-powered Internal Audit platform for the Indonesian financial industry.
            
            Built with ❤️ by Sopian
            """
        }
    )


def main():
    """Main application entry point."""
    try:
        # Configure page first (must be first Streamlit command)
        configure_page()
        
        # Initialize application state
        init_app()
        
        # Create and render router
        router = Router()
        router.render()
        
        logger.debug("AURIX rendered successfully")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error(f"An unexpected error occurred: {str(e)}")
        st.info("Please refresh the page. If the problem persists, contact support.")


if __name__ == "__main__":
    main()
