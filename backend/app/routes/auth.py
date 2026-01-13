from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.middleware.auth import jwt_required_custom
import jwt
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    # Validation
    if not name or not email or not password:
        return jsonify({'msg': 'Please provide name, email, and password'}), 400
    
    if len(password) < 6:
        return jsonify({'msg': 'Password must be at least 6 characters long'}), 400
    
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'msg': 'Please provide a valid email'}), 400
    
    try:
        user_model = User(current_app.db)
        
        if user_model.user_exists(email):
            return jsonify({'msg': 'User already exists'}), 400
        
        user_id = user_model.create_user(name, email, password)
        
        # Create JWT token
        payload = {'user': {'id': str(user_id)}}
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'token': token}), 201
        
    except Exception as e:
        current_app.logger.error(f'Register error: {e}')
        return jsonify({'msg': 'Server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'msg': 'Please provide email and password'}), 400
    
    try:
        user_model = User(current_app.db)
        user = user_model.find_by_email(email)
        
        if not user or not user_model.verify_password(password, user['password']):
            return jsonify({'msg': 'Invalid credentials'}), 400
        
        # Create JWT token
        payload = {'user': {'id': str(user['_id'])}}
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'token': token}), 200
        
    except Exception as e:
        current_app.logger.error(f'Login error: {e}')
        return jsonify({'msg': 'Server error'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required_custom
def get_current_user():
    try:
        user = request.current_user
        # Remove password from response
        user.pop('password', None)
        # Convert ObjectId to string
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
        
    except Exception as e:
        current_app.logger.error(f'Get user error: {e}')
        return jsonify({'msg': 'Server error'}), 500