from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.middleware.auth import jwt_required_custom
from bson import ObjectId

friends_bp = Blueprint('friends', __name__)

@friends_bp.route('/add', methods=['POST'])
@jwt_required_custom
def add_friend():
    data = request.get_json()
    friend_email = data.get('friendEmail', '').strip().lower()
    
    if not friend_email:
        return jsonify({'msg': 'Friend email is required'}), 400
    
    try:
        user_model = User(current_app.db)
        current_user_id = request.current_user_id
        
        # Find friend by email
        friend = user_model.find_by_email(friend_email)
        if not friend:
            return jsonify({'msg': 'User not found'}), 404
        
        friend_id = str(friend['_id'])
        
        # Check if trying to add self
        if current_user_id == friend_id:
            return jsonify({'msg': 'Cannot add yourself as friend'}), 400
        
        # Check if already friends
        if user_model.is_friend(current_user_id, friend_id):
            return jsonify({'msg': 'Already friends'}), 400
        
        # Add friend relationship (bidirectional)
        user_model.add_friend(current_user_id, friend_id)
        user_model.add_friend(friend_id, current_user_id)
        
        return jsonify({'msg': 'Friend added'}), 200
        
    except Exception as e:
        current_app.logger.error(f'Add friend error: {e}')
        return jsonify({'msg': 'Server error'}), 500

@friends_bp.route('', methods=['GET'])
@jwt_required_custom
def get_friends():
    try:
        user_model = User(current_app.db)
        friends = user_model.get_friends(request.current_user_id)
        
        # Convert ObjectIds to strings
        for friend in friends:
            friend['_id'] = str(friend['_id'])
        
        return jsonify(friends), 200
        
    except Exception as e:
        current_app.logger.error(f'Get friends error: {e}')
        return jsonify({'msg': 'Server error'}), 500