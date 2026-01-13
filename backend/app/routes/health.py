from flask import Blueprint, jsonify, current_app
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    try:
        # Test MongoDB connection
        current_app.db.command('ping')
        mongodb_status = 'connected'
    except Exception:
        mongodb_status = 'disconnected'
    
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat(),
        'mongodb': mongodb_status
    }), 200

@health_bp.route('/', methods=['GET'])
def root():
    return 'Hello from Flask backend!', 200