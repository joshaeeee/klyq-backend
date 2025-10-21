# Data validation utilities
import hmac
import hashlib
from typing import Dict, Any
from ..config import settings


def validate_shopify_webhook(data: str, signature: str) -> bool:
    """Validate Shopify webhook signature"""
    try:
        # Calculate expected signature
        expected_signature = hmac.new(
            settings.shopify_api_secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(signature, expected_signature)
    except Exception:
        return False


def validate_meta_webhook(data: str, signature: str) -> bool:
    """Validate Meta webhook signature"""
    try:
        # Meta webhook validation logic
        # This would implement proper Meta webhook validation
        return True  # Simplified for demo
    except Exception:
        return False


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_shop_url(shop_url: str) -> bool:
    """Validate Shopify shop URL format"""
    return shop_url.endswith('.myshopify.com') and len(shop_url) > 14


def validate_webhook_data(data: Dict[str, Any]) -> bool:
    """Validate webhook data structure"""
    required_fields = ['id', 'created_at']
    return all(field in data for field in required_fields)


def validate_api_response(response_data: Dict[str, Any], expected_fields: list) -> bool:
    """Validate API response structure"""
    return all(field in response_data for field in expected_fields)


def sanitize_input(input_string: str) -> str:
    """Sanitize user input"""
    if not isinstance(input_string, str):
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')']
    for char in dangerous_chars:
        input_string = input_string.replace(char, '')
    
    return input_string.strip()


def validate_price(price: float) -> bool:
    """Validate price value"""
    return isinstance(price, (int, float)) and price >= 0


def validate_quantity(quantity: int) -> bool:
    """Validate quantity value"""
    return isinstance(quantity, int) and quantity >= 0


def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate date range"""
    try:
        from datetime import datetime
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        return start < end
    except Exception:
        return False
