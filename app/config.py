import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """
    Load application configuration from environment variables or defaults.
    
    Returns:
        dict: Dictionary containing configuration settings
    """
    config = {
        # Flask settings
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev_key_for_development_only'),
        'DEBUG': os.environ.get('DEBUG', 'True').lower() in ['true', 'yes', '1'],
        
        # Application settings
        'DEFAULT_TIME': os.environ.get('DEFAULT_TIME', '22:00:00'),  # 10 PM
        'TIMEZONE': os.environ.get('TIMEZONE', 'UTC'),
        
        # Caching settings
        'CACHE_TYPE': os.environ.get('CACHE_TYPE', 'SimpleCache'),
        'CACHE_DEFAULT_TIMEOUT': int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 86400)),  # 24 hours
        
        # Security settings
        'STRICT_TRANSPORT_SECURITY': os.environ.get('STRICT_TRANSPORT_SECURITY', 'True').lower() in ['true', 'yes', '1'],
        'CONTENT_SECURITY_POLICY': os.environ.get('CONTENT_SECURITY_POLICY', "default-src 'self'; img-src 'self' data:;"),
        'X_CONTENT_TYPE_OPTIONS': 'nosniff',
        'X_FRAME_OPTIONS': 'SAMEORIGIN',
    }
    
    return config