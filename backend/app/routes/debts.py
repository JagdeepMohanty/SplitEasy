from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId

debts_bp = Blueprint('debts', __name__)

@debts_bp.route('/debts', methods=['GET'])
def get_debts():
    try:
        if current_app.db is None:
            return jsonify({'error': 'Database not available'}), 503
            
        # Get all friends and expenses to calculate debts
        friends_collection = current_app.db.friends
        expenses_collection = current_app.db.expenses
        settlements_collection = current_app.db.settlements
        
        friends = list(friends_collection.find({}))
        expenses = list(expenses_collection.find({}))
        settlements = list(settlements_collection.find({}))
        
        # Calculate debts between friends
        debt_matrix = {}
        
        # Initialize debt matrix
        for friend in friends:
            friend_name = friend['name']
            debt_matrix[friend_name] = {}
            for other_friend in friends:
                if friend_name != other_friend['name']:
                    debt_matrix[friend_name][other_friend['name']] = 0.0
        
        # Process expenses
        for expense in expenses:
            payer = expense.get('payer')
            participants = expense.get('participants', [])
            amount = expense.get('amount', 0)
            
            if payer and participants and amount > 0:
                share_amount = round(amount / len(participants), 2)
                
                for participant in participants:
                    if participant != payer and participant in debt_matrix:
                        if payer in debt_matrix[participant]:
                            debt_matrix[participant][payer] += share_amount
        
        # Process settlements (subtract payments)
        for settlement in settlements:
            from_user = settlement.get('fromUser')
            to_user = settlement.get('toUser')
            amount = settlement.get('amount', 0)
            
            if from_user and to_user and amount > 0:
                if from_user in debt_matrix and to_user in debt_matrix[from_user]:
                    debt_matrix[from_user][to_user] -= amount
                    if debt_matrix[from_user][to_user] < 0:
                        debt_matrix[from_user][to_user] = 0
        
        # Convert to response format
        debts = []
        for debtor, creditors in debt_matrix.items():
            for creditor, amount in creditors.items():
                if amount > 0.01:  # Only include significant debts
                    debts.append({
                        'debtor': debtor,
                        'creditor': creditor,
                        'amount': round(amount, 2)
                    })
        
        return jsonify(debts), 200
        
    except Exception as e:
        current_app.logger.error(f'Get debts error: {e}')
        return jsonify({'error': 'Failed to calculate debts'}), 500