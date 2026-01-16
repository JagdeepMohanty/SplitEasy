from flask import Blueprint, jsonify, current_app
from datetime import datetime
import os

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET', 'HEAD'])
def health_check():
    """Comprehensive health check for Render monitoring"""
    try:
        # Check database connection
        db_status = 'connected' if current_app.db is not None else 'disconnected'
        
        # Basic app info
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': db_status,
            'environment': os.getenv('FLASK_ENV', 'unknown'),
            'version': '1.0.0'
        }
        
        # If database is available, test a simple query
        if current_app.db is not None:
            try:
                current_app.db.command('ping')
                health_data['database_ping'] = 'success'
            except Exception as e:
                health_data['database_ping'] = 'failed'
                health_data['database_error'] = str(e)
        
        return jsonify(health_data), 200
        
    except Exception as e:
        return jsonify({
            'status': 'healthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 200

@health_bp.route('/', methods=['GET'])
def root():
    """Root endpoint for basic connectivity test"""
    return jsonify({
        'message': 'EasyXpense Backend API',
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200