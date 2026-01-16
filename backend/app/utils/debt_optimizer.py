"""
Optimized debt settlement algorithm.
Minimizes number of transactions using net balance approach.
"""

def calculate_net_balances(expenses, settlements):
    """
    Calculate net balance for each person in paisa.
    Positive = person is owed money
    Negative = person owes money
    """
    balances = {}
    
    # Process expenses
    for expense in expenses:
        payer = expense.get('payer')
        participant_shares = expense.get('participant_shares', [])
        
        if not payer or not participant_shares:
            continue
        
        # Payer paid the full amount
        amount_paisa = expense.get('amount_paisa', 0)
        balances[payer] = balances.get(payer, 0) + amount_paisa
        
        # Each participant owes their share
        for share in participant_shares:
            participant = share['name']
            share_paisa = share['share_paisa']
            balances[participant] = balances.get(participant, 0) - share_paisa
    
    # Process settlements (reduce debts)
    for settlement in settlements:
        from_user = settlement.get('fromUser')
        to_user = settlement.get('toUser')
        amount_paisa = settlement.get('amount_paisa', 0)
        
        if from_user and to_user and amount_paisa > 0:
            # from_user paid to_user, so from_user's debt decreases
            balances[from_user] = balances.get(from_user, 0) + amount_paisa
            # to_user received payment, so what they're owed decreases
            balances[to_user] = balances.get(to_user, 0) - amount_paisa
    
    return balances


def optimize_settlements(balances):
    """
    Generate minimum number of settlements using greedy algorithm.
    
    Algorithm:
    1. Separate people into debtors (negative balance) and creditors (positive balance)
    2. Sort both lists by absolute amount
    3. Match largest debtor with largest creditor
    4. Continue until all balanced
    
    Time Complexity: O(n log n) for sorting
    Space Complexity: O(n)
    """
    # Separate debtors and creditors
    debtors = []   # People who owe money (negative balance)
    creditors = []  # People who are owed money (positive balance)
    
    for person, balance in balances.items():
        if balance < 0:
            debtors.append({'name': person, 'amount': -balance})  # Store as positive
        elif balance > 0:
            creditors.append({'name': person, 'amount': balance})
    
    # Sort by amount (largest first) for optimal matching
    debtors.sort(key=lambda x: x['amount'], reverse=True)
    creditors.sort(key=lambda x: x['amount'], reverse=True)
    
    # Generate optimized settlements
    settlements = []
    i, j = 0, 0
    
    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]
        
        # Settle the minimum of what debtor owes and creditor is owed
        settle_amount = min(debtor['amount'], creditor['amount'])
        
        if settle_amount > 0:
            settlements.append({
                'from': debtor['name'],
                'to': creditor['name'],
                'amount_paisa': settle_amount
            })
        
        # Update remaining amounts
        debtor['amount'] -= settle_amount
        creditor['amount'] -= settle_amount
        
        # Move to next person if current is settled
        if debtor['amount'] == 0:
            i += 1
        if creditor['amount'] == 0:
            j += 1
    
    return settlements


def calculate_optimized_debts(expenses, settlements):
    """
    Main function: Calculate optimized debt settlements.
    Returns list of minimum settlements needed.
    """
    # Step 1: Calculate net balances
    balances = calculate_net_balances(expenses, settlements)
    
    # Step 2: Optimize settlements
    optimized = optimize_settlements(balances)
    
    return optimized, balances
