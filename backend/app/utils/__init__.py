from decimal import Decimal, ROUND_HALF_UP
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_amount(amount):
    """Validate and format amount for INR currency"""
    try:
        # Convert to Decimal for precise calculations
        decimal_amount = Decimal(str(amount))
        # Round to 2 decimal places (paise precision)
        rounded_amount = decimal_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # Ensure positive amount
        if rounded_amount <= 0:
            return None
        # Ensure reasonable maximum (10 crores INR)
        if rounded_amount > Decimal('100000000.00'):
            return None
        return float(rounded_amount)
    except (ValueError, TypeError):
        return None

def format_currency_response(amount):
    """Format amount for API response"""
    if amount is None:
        return 0.00
    return round(float(amount), 2)