from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.models.expense import Expense
from app.models.settlement import Settlement
from app.middleware.auth import jwt_required_custom
from bson import ObjectId

debts_bp = Blueprint('debts', __name__)

@debts_bp.route('', methods=['GET'])
@jwt_required_custom
def get_debts():
    try:
        current_user_id = request.current_user_id
        
        user_model = User(current_app.db)
        expense_model = Expense(current_app.db)
        settlement_model = Settlement(current_app.db)
        
        # Get user's friends
        friends = user_model.get_friends(current_user_id)
        debts = []
        
        for friend in friends:
            friend_id = str(friend['_id'])
            friend_name = friend['name']
            
            # Calculate net amount (positive = friend owes me, negative = I owe friend)
            net_amount = 0.0
            
            # 1. Expenses I paid where friend participated
            expenses_i_paid = expense_model.get_expenses_with_participant(current_user_id, friend_id)
            for expense in expenses_i_paid:
                share_amount = expense['amount'] / len(expense['participants'])
                net_amount += share_amount
            
            # 2. Expenses friend paid where I participated
            expenses_friend_paid = expense_model.get_expenses_with_participant(friend_id, current_user_id)
            for expense in expenses_friend_paid:
                share_amount = expense['amount'] / len(expense['participants'])
                net_amount -= share_amount
            
            # 3. Settlements from friend to me (friend paid me)
            settlements_friend_to_me = settlement_model.get_settlements_from_user(friend_id, current_user_id)
            for settlement in settlements_friend_to_me:
                net_amount -= settlement['amount']
            
            # 4. Settlements from me to friend (I paid friend)
            settlements_me_to_friend = settlement_model.get_settlements_from_user(current_user_id, friend_id)
            for settlement in settlements_me_to_friend:
                net_amount += settlement['amount']
            
            # Round to 2 decimal places
            net_amount = round(net_amount, 2)
            
            debts.append({
                'friendId': friend_id,
                'friendName': friend_name,
                'amount': net_amount
            })
        
        return jsonify(debts), 200
        
    except Exception as e:
        current_app.logger.error(f'Get debts error: {e}')
        return jsonify({'msg': 'Server error'}), 500