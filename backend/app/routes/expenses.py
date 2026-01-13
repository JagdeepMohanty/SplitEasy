from flask import Blueprint, request, jsonify, current_app
from app.models.expense import Expense
from app.middleware.auth import jwt_required_custom
from bson import ObjectId

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('', methods=['POST'])
@jwt_required_custom
def create_expense():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Request body is required'}), 400
    
    description = data.get('description', '').strip()
    amount = data.get('amount')
    participants = data.get('participants', [])
    
    # Validation
    if not description:
        return jsonify({'msg': 'Description is required'}), 400
    
    if len(description) > 200:
        return jsonify({'msg': 'Description too long (max 200 characters)'}), 400
    
    if not participants or len(participants) == 0:
        return jsonify({'msg': 'At least one participant is required'}), 400
    
    try:
        expense_model = Expense(current_app.db)
        current_user_id = request.current_user_id
        
        expense_id = expense_model.create_expense(
            description=description,
            amount=amount,  # Model will validate and format amount
            payer_id=current_user_id,
            participants=participants
        )
        
        return jsonify({
            '_id': str(expense_id),
            'description': description,
            'msg': 'Expense created successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f'Create expense error: {e}')
        return jsonify({'msg': 'Failed to create expense'}), 500

@expenses_bp.route('', methods=['GET'])
@jwt_required_custom
def get_expenses():
    try:
        expense_model = Expense(current_app.db)
        expenses = expense_model.get_user_expenses(request.current_user_id)
        
        # Convert ObjectIds to strings
        for expense in expenses:
            expense['_id'] = str(expense['_id'])
            for participant in expense.get('participants', []):
                participant['_id'] = str(participant['_id'])
        
        return jsonify(expenses), 200
        
    except Exception as e:
        current_app.logger.error(f'Get expenses error: {e}')
        return jsonify({'msg': 'Failed to fetch expenses'}), 500