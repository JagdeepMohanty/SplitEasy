"""
Money handling utilities using integer paisa (paise) to avoid floating-point errors.
All amounts stored as integers (1 rupee = 100 paisa).
"""

def rupees_to_paisa(rupees):
    """Convert rupees (float/int) to paisa (integer)"""
    if rupees is None:
        raise ValueError("Amount cannot be None")
    
    try:
        # Handle both float and int inputs
        amount_float = float(rupees)
        # Convert to paisa (multiply by 100 and round to nearest integer)
        amount_paisa = round(amount_float * 100)
        return amount_paisa
    except (ValueError, TypeError):
        raise ValueError(f"Invalid amount: {rupees}")


def paisa_to_rupees(paisa):
    """Convert paisa (integer) to rupees (float) for display"""
    if paisa is None:
        return 0.0
    return round(paisa / 100, 2)


def validate_amount_paisa(amount_paisa):
    """Validate amount in paisa"""
    if not isinstance(amount_paisa, int):
        raise ValueError("Amount must be an integer in paisa")
    
    if amount_paisa <= 0:
        raise ValueError("Amount must be positive")
    
    if amount_paisa > 100000000:  # 10 lakh rupees = 100 crore paisa
        raise ValueError("Amount too large (max 10,00,000 INR)")
    
    return True


def split_equally(amount_paisa, num_people):
    """
    Split amount equally among people using integer division.
    Distributes remainder to first N people to ensure exact total.
    
    Returns list of shares in paisa (integers).
    """
    if num_people <= 0:
        raise ValueError("Number of people must be positive")
    
    base_share = amount_paisa // num_people
    remainder = amount_paisa % num_people
    
    shares = []
    for i in range(num_people):
        # First 'remainder' people get base_share + 1
        if i < remainder:
            shares.append(base_share + 1)
        else:
            shares.append(base_share)
    
    # Verify total matches exactly
    assert sum(shares) == amount_paisa, "Split calculation error"
    
    return shares
