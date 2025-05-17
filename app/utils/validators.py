import re
from .errors import APIError

# Email validation regex
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
)

# Phone validation regex (E.164 format)
PHONE_REGEX = re.compile(r'^\+?[1-9]\d{1,14}$')

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not EMAIL_REGEX.match(email):
        raise APIError('Invalid email format', 400)
    return True

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not PHONE_REGEX.match(phone):
        raise APIError('Invalid phone number format. Use international format (+CountryCodeNumber)', 400)
    return True

def validate_dob(dob_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(dob_str, '%Y-%m-%d')
        return True
    except ValueError:
        raise APIError('Invalid date format. Use YYYY-MM-DD', 400)
        
def validate_password(password: str) -> bool:
    """Validate password complexity"""
    if len(password) < 8:
        raise APIError('Password must be at least 8 characters', 400)
    if not re.search(r'[A-Z]', password):
        raise APIError('Password must contain at least one uppercase letter', 400)
    if not re.search(r'[a-z]', password):
        raise APIError('Password must contain at least one lowercase letter', 400)
    if not re.search(r'[0-9]', password):
        raise APIError('Password must contain at least one number', 400)
    return True