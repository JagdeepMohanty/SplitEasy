from flask import Blueprint, request, jsonify, current_app
from app.models.expense import Expense
from app.utils.sanitize import sanitize_string, sanitize_amount, sanitize_list
from bson import ObjectId

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses', methods=['POST'])
def create_expense():
    current_app.logger.info('Creating new expense')
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Request body is required'}), 400
    
    # Sanitize inputs
    description = sanitize_string(data.get('description', ''), max_length=200)
    amount = sanitize_amount(data.get('amount'))
    payer = sanitize_string(data.get('payer', ''), max_length=100)
    participants = sanitize_list(data.get('participants', []), max_items=50)
    group_id = sanitize_string(data.get('group_id', ''), max_length=50) if data.get('group_id') else None
    
    # Validation
    if not description:
        return jsonify({'success': False, 'error': 'Description is required'}), 400
    
    if amount is None:
        return jsonify({'success': False, 'error': 'Valid amount is required (max 1 crore)'}), 400
    
    if not payer:
        return jsonify({'success': False, 'error': 'Payer is required'}), 400
    
    if not participants or len(participants) == 0:
        return jsonify({'success': False, 'error': 'At least one participant is required'}), 400
    
    # Sanitize participant names
    participants = [sanitize_string(p, max_length=100) for p in participants if p]
    
    try:
        if current_app.db is None:
            current_app.logger.error('Database connection not available')
            return jsonify({'success': False, 'error': 'Database not available'}), 503
            
        expense_model = Expense(current_app.db)
        expense_id = expense_model.create_expense(
            description=description,
            amount=amount,
            payer=payer,
            participants=participants,
            group_id=group_id
        )
        
        current_app.logger.info(f'Expense created successfully with ID: {expense_id}')
        
        return jsonify({
            'success': True,
            'message': 'Expense created successfully',
            'data': {
                '_id': str(expense_id),
                'description': description,
                'amount': amount,
                'payer': payer,
                'participants': participants
            }
        }), 201
        
    except ValueError as e:
        current_app.logger.error(f'Validation error: {e}')
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f'Create expense error: {e}')
        return jsonify({'success': False, 'error': 'Failed to create expense'}), 500

@expenses_bp.route('/expenses', methods=['GET'])
def get_expenses():
    group_id = sanitize_string(request.args.get('group_id', ''), max_length=50) if request.args.get('group_id') else None
    
    try:
        if current_app.db is None:
            return jsonify({'error': 'Database not available'}), 503
            
        expense_model = Expense(current_app.db)
        expenses = expense_model.get_all_expenses(group_id)
        
        # Convert ObjectIds to strings
        for expense in expenses:
            expense['_id'] = str(expense['_id'])
            if 'date' in expense:
                expense['date'] = expense['date'].isoformat()
        
        return jsonify(expenses), 200
        
    except Exception as e:
        current_app.logger.error(f'Get expenses error: {e}')
        return jsonify({'error': 'Failed to fetch expenses'}), 500