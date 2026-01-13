from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    mongo_uri = os.getenv('MONGO_URI')
    
    if not mongo_uri:
        raise ValueError('MONGO_URI environment variable is required')
    
    # CORS configuration for production
    cors_origins = ['https://easyxpense.netlify.app']
    if os.getenv('FLASK_ENV') == 'development':
        cors_origins.extend(['http://localhost:3000', 'http://localhost:5173'])
    
    CORS(app, origins=cors_origins, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # MongoDB connection with graceful error handling
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        app.db = client.get_default_database()
        print('✅ MongoDB connection initialized')
    except Exception as e:
        print(f'⚠️ MongoDB connection warning: {e}')
        app.db = None
    
    # Configure logging
    if os.getenv('FLASK_ENV') == 'production':
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Global request validation
    @app.before_request
    def validate_json():
        if request.method in ['POST', 'PUT'] and request.content_type:
            if 'application/json' not in request.content_type:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    # Register blueprints with correct URL structure
    from app.routes.friends import friends_bp
    from app.routes.expenses import expenses_bp
    from app.routes.settlements import settlements_bp
    from app.routes.debts import debts_bp
    from app.routes.health import health_bp
    
    app.register_blueprint(friends_bp, url_prefix='/api')
    app.register_blueprint(expenses_bp, url_prefix='/api')
    app.register_blueprint(settlements_bp, url_prefix='/api')
    app.register_blueprint(debts_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # Enhanced error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({'error': 'Service temporarily unavailable'}), 503
    
    return app