"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║     █████╗ ██╗   ██╗██████╗ ██╗██╗  ██╗                                      ║
║    ██╔══██╗██║   ██║██╔══██╗██║╚██╗██╔╝                                      ║
║    ███████║██║   ██║██████╔╝██║ ╚███╔╝                                       ║
║    ██╔══██║██║   ██║██╔══██╗██║ ██╔██╗                                       ║
║    ██║  ██║╚██████╔╝██║  ██║██║██╔╝ ██╗                                      ║
║    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝                                      ║
║                                                                               ║
║    Intelligent Audit. Elevated Assurance.                                    ║
║    Version: 4.0.0 Enterprise                                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Main entry point for AURIX application.
This file should remain minimal - all logic is in modules.
"""

import streamlit as st
from app.config import settings, init_app
from app.router import Router
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def main():
    """Main application entry point."""
    
    # Initialize application
    init_app()
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="AURIX | Intelligent Audit Platform",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize router and render
    router = Router()
    router.render()
    
    logger.info("AURIX application rendered successfully")


if __name__ == "__main__":
    main()
