from flask import Blueprint, request, jsonify, current_app
from app.models.settlement import Settlement
from app.models.user import User
from app.middleware.auth import jwt_required_custom
from bson import ObjectId

settlements_bp = Blueprint('settlements', __name__)

@settlements_bp.route('', methods=['POST'])
@jwt_required_custom
def create_settlement():
    data = request.get_json()
    to_user_id = data.get('toUserId', '').strip()
    amount = data.get('amount')
    
    # Validation
    if not to_user_id:
        return jsonify({'msg': 'Recipient user ID is required'}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'msg': 'Amount must be positive'}), 400
    except (TypeError, ValueError):
        return jsonify({'msg': 'Invalid amount'}), 400
    
    try:
        current_user_id = request.current_user_id
        
        # Check if trying to settle with self
        if current_user_id == to_user_id:
            return jsonify({'msg': 'Cannot settle with yourself'}), 400
        
        # Verify recipient exists
        user_model = User(current_app.db)
        recipient = user_model.find_by_id(to_user_id)
        if not recipient:
            return jsonify({'msg': 'Recipient user not found'}), 404
        
        settlement_model = Settlement(current_app.db)
        settlement_id = settlement_model.create_settlement(
            from_user_id=current_user_id,
            to_user_id=to_user_id,
            amount=amount
        )
        
        return jsonify({
            '_id': str(settlement_id),
            'fromUser': current_user_id,
            'toUser': to_user_id,
            'amount': amount
        }), 201
        
    except Exception as e:
        current_app.logger.error(f'Create settlement error: {e}')
        return jsonify({'msg': 'Server error'}), 500

@settlements_bp.route('', methods=['GET'])
@jwt_required_custom
def get_settlements():
    try:
        settlement_model = Settlement(current_app.db)
        settlements = settlement_model.get_user_settlements(request.current_user_id)
        
        # Convert ObjectIds to strings
        for settlement in settlements:
            settlement['_id'] = str(settlement['_id'])
            settlement['fromUser']['_id'] = str(settlement['fromUser']['_id'])
            settlement['toUser']['_id'] = str(settlement['toUser']['_id'])
        
        return jsonify(settlements), 200
        
    except Exception as e:
        current_app.logger.error(f'Get settlements error: {e}')
        return jsonify({'msg': 'Server error'}), 500