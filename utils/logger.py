"""
Logging Configuration for AURIX.
Provides centralized logging with proper formatting and levels.
"""

import logging
import sys
from typing import Optional
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for terminal output."""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        # Add color based on level
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    use_colors: bool = True
) -> logging.Logger:
    """
    Set up a logger with the given configuration.
    
    Args:
        name: Logger name (typically __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs
        use_colors: Whether to use colored output in terminal
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    if use_colors:
        console_format = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with default configuration.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return setup_logger(name)


class AuditLogger:
    """
    Specialized logger for audit trail logging.
    Logs important audit events with structured data.
    """
    
    def __init__(self, name: str = "audit_trail"):
        self.logger = setup_logger(name, level="INFO")
    
    def log_action(
        self,
        action: str,
        user: str = "system",
        entity_type: str = "",
        entity_id: str = "",
        details: Optional[dict] = None
    ):
        """Log an audit action."""
        message = f"ACTION: {action} | USER: {user}"
        
        if entity_type:
            message += f" | ENTITY: {entity_type}"
        if entity_id:
            message += f" | ID: {entity_id}"
        if details:
            message += f" | DETAILS: {details}"
        
        self.logger.info(message)
    
    def log_access(self, page: str, user: str = "anonymous"):
        """Log page access."""
        self.logger.info(f"ACCESS: Page={page} | User={user}")
    
    def log_error(self, operation: str, error: Exception, context: Optional[dict] = None):
        """Log an error with context."""
        message = f"ERROR: Operation={operation} | Error={str(error)}"
        if context:
            message += f" | Context={context}"
        self.logger.error(message, exc_info=True)
    
    def log_security_event(self, event_type: str, details: dict):
        """Log a security-related event."""
        self.logger.warning(f"SECURITY: {event_type} | {details}")


# Global audit logger instance
audit_logger = AuditLogger()
