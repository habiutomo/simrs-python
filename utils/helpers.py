from datetime import datetime
import re
import uuid

def generate_id():
    """Generate a unique ID"""
    return str(uuid.uuid4())

def format_date(date_str, output_format="%d %b %Y"):
    """Format date string to a readable format"""
    if not date_str:
        return ""
    
    try:
        # Handle ISO format with timezone
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            # Assume YYYY-MM-DD format
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        
        return dt.strftime(output_format)
    except ValueError:
        return date_str

def format_datetime(datetime_str, output_format="%d %b %Y %H:%M"):
    """Format datetime string to a readable format"""
    if not datetime_str:
        return ""
    
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return dt.strftime(output_format)
    except ValueError:
        return datetime_str

def calculate_age(birth_date):
    """Calculate age from birth date"""
    if not birth_date:
        return None
    
    try:
        if 'T' in birth_date:
            birth = datetime.fromisoformat(birth_date.replace('Z', '+00:00'))
        else:
            birth = datetime.strptime(birth_date, "%Y-%m-%d")
        
        today = datetime.now()
        age = today.year - birth.year
        
        # Adjust age if birthday hasn't occurred yet this year
        if (today.month, today.day) < (birth.month, birth.day):
            age -= 1
        
        return age
    except ValueError:
        return None

def format_currency(amount, currency="Rp"):
    """Format number as currency"""
    if amount is None:
        return f"{currency} 0"
    
    try:
        amount_float = float(amount)
        return f"{currency} {amount_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return f"{currency} 0"

def sanitize_input(text):
    """Sanitize user input for security"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';]', '', text)
    return sanitized
