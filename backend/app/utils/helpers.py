"""
Helper utilities for the Hogwarts application.
"""
from datetime import datetime, timezone
from typing import Dict, Any

def get_current_utc_time() -> datetime:
    """
    Returns the current time in UTC.
    
    Returns:
        datetime: The current time in UTC
    """
    return datetime.now(timezone.utc)

def format_date(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formats a datetime object to a string.
    
    Args:
        dt: The datetime to format
        format_str: The format string to use
        
    Returns:
        str: The formatted datetime string
    """
    return dt.strftime(format_str)

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes input data to prevent XSS and other attacks.
    
    Args:
        data: The input data to sanitize
        
    Returns:
        Dict[str, Any]: The sanitized data
    """
    # This is a simple implementation - for production, use a library like bleach
    if not isinstance(data, dict):
        return data
        
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Remove potentially dangerous HTML content
            sanitized[key] = value.replace('<', '&lt;').replace('>', '&gt;')
        elif isinstance(value, dict):
            sanitized[key] = sanitize_input(value)
        else:
            sanitized[key] = value
            
    return sanitized 