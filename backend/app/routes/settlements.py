from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime

settlements_bp = Blueprint('settlements', __name__)

@settlements_bp.route('/settlements', methods=['POST'])
def create_settlement():
    current_app.logger.info('Creating new settlement')
    data = request.get_json()
    current_app.logger.info(f'Settlement data received: {data}')
    
    if not data:
        return jsonify({'success': False, 'error': 'Request body is required'}), 400
        
    from_user = data.get('fromUser', '').strip()
    to_user = data.get('toUser', '').strip()
    amount = data.get('amount')
    
    # Validation
    if not from_user or not to_user:
        return jsonify({'success': False, 'error': 'From user and to user are required'}), 400
    
    if from_user == to_user:
        return jsonify({'success': False, 'error': 'Cannot settle with yourself'}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'success': False, 'error': 'Amount must be positive'}), 400
        if amount > 1000000:  # 10 lakh INR limit
            return jsonify({'success': False, 'error': 'Amount too large'}), 400
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Invalid amount'}), 400
    
    try:
        if current_app.db is None:
            return jsonify({'error': 'Database not available'}), 503
            
        settlements_collection = current_app.db.settlements
        
        settlement_data = {
            'fromUser': from_user,
            'toUser': to_user,
            'amount': round(amount, 2),
            'date': datetime.utcnow(),
            'currency': 'INR'
        }
        
        result = settlements_collection.insert_one(settlement_data)
        
        return jsonify({
            'success': True,
            'message': 'Settlement created successfully',
            'data': {
                '_id': str(result.inserted_id),
                'fromUser': from_user,
                'toUser': to_user,
                'amount': round(amount, 2)
            }
        }), 201
        
    except Exception as e:
        current_app.logger.error(f'Create settlement error: {e}')
        return jsonify({'success': False, 'error': 'Failed to create settlement'}), 500

@settlements_bp.route('/settlements', methods=['GET'])
def get_settlements():
    try:
        if current_app.db is None:
            return jsonify({'error': 'Database not available'}), 503
            
        settlements_collection = current_app.db.settlements
        settlements = list(settlements_collection.find({}).sort('date', -1))
        
        # Convert ObjectIds to strings and format dates
        for settlement in settlements:
            settlement['_id'] = str(settlement['_id'])
            if 'date' in settlement:
                settlement['date'] = settlement['date'].isoformat()
        
        return jsonify(settlements), 200
        
    except Exception as e:
        current_app.logger.error(f'Get settlements error: {e}')
        return jsonify({'error': 'Failed to fetch settlements'}), 500