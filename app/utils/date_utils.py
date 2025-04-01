from datetime import date, datetime
import pytz

def get_current_date() -> date:
    """
    Get the current date.
    
    Returns:
        date: The current date
    """
    # Use UTC for consistent date calculations
    return datetime.now(pytz.UTC).date()

def format_date(date_obj: date, format_str: str = '%Y-%m-%d') -> str:
    """
    Format a date object to a string using the specified format.
    
    Args:
        date_obj: The date object to format
        format_str: The format string to use (default: '%Y-%m-%d')
        
    Returns:
        str: The formatted date string
    """
    return date_obj.strftime(format_str)