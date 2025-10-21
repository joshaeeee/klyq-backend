# Common helper functions
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency == "USD":
        return f"${amount:.2f}"
    elif currency == "EUR":
        return f"€{amount:.2f}"
    elif currency == "GBP":
        return f"£{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format percentage value"""
    return f"{value:.{decimals}f}%"


def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object"""
    return date.strftime(format_str)


def parse_iso_date(date_string: str) -> datetime:
    """Parse ISO date string"""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except ValueError:
        return datetime.now()


def calculate_date_range(days: int) -> tuple:
    """Calculate start and end dates for a given number of days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def group_by_date(data: List[Dict], date_field: str = "created_at") -> Dict[str, List[Dict]]:
    """Group data by date"""
    grouped = {}
    for item in data:
        date = item.get(date_field)
        if isinstance(date, str):
            date = parse_iso_date(date)
        
        date_key = date.strftime("%Y-%m-%d")
        if date_key not in grouped:
            grouped[date_key] = []
        grouped[date_key].append(item)
    
    return grouped


def calculate_growth_rate(current: float, previous: float) -> float:
    """Calculate growth rate percentage"""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def calculate_moving_average(values: List[float], window: int = 7) -> List[float]:
    """Calculate moving average for a list of values"""
    if len(values) < window:
        return values
    
    moving_avg = []
    for i in range(len(values)):
        if i < window - 1:
            moving_avg.append(values[i])
        else:
            avg = sum(values[i - window + 1:i + 1]) / window
            moving_avg.append(avg)
    
    return moving_avg


def safe_json_loads(json_string: str, default: Any = None) -> Any:
    """Safely parse JSON string"""
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Safely serialize data to JSON"""
    try:
        return json.dumps(data, default=str)
    except (TypeError, ValueError):
        return default


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""


def generate_unique_id(prefix: str = "") -> str:
    """Generate unique ID"""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{unique_id}" if prefix else unique_id


def convert_to_dict(obj: Any) -> Dict:
    """Convert object to dictionary"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    elif isinstance(obj, dict):
        return obj
    else:
        return {"value": obj}


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries"""
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def filter_none_values(data: Dict) -> Dict:
    """Remove None values from dictionary"""
    return {k: v for k, v in data.items() if v is not None}


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_nested_value(data: Dict, keys: List[str], default: Any = None) -> Any:
    """Get nested value from dictionary using key path"""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
