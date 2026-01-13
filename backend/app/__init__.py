from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
import sys

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Enhanced logging configuration
    if os.getenv('FLASK_ENV') == 'production':
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    
    app.logger.info('Starting EasyXpense Backend...')
    
    # Configuration
    mongo_uri = os.getenv('MONGO_URI')
    
    if not mongo_uri:
        app.logger.error('MONGO_URI environment variable is required')
        raise ValueError('MONGO_URI environment variable is required')
    
    app.logger.info(f'Flask environment: {os.getenv("FLASK_ENV", "development")}')
    
    # CORS configuration for production
    cors_origins = ['https://easyxpense.netlify.app']
    if os.getenv('FLASK_ENV') == 'development':
        cors_origins.extend(['http://localhost:3000', 'http://localhost:5173'])
    
    app.logger.info(f'CORS origins: {cors_origins}')
    CORS(app, origins=cors_origins, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # MongoDB connection with enhanced error handling
    try:
        app.logger.info('Connecting to MongoDB...')
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        app.db = client.get_default_database()
        # Test connection
        app.db.command('ping')
        app.logger.info('MongoDB connection successful')
    except Exception as e:
        app.logger.error(f'MongoDB connection failed: {e}')
        app.db = None
    
    # Global request validation
    @app.before_request
    def validate_json():
        if request.method in ['POST', 'PUT'] and request.content_type:
            if 'application/json' not in request.content_type:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    # Register blueprints
    try:
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
        
        app.logger.info('All blueprints registered successfully')
    except Exception as e:
        app.logger.error(f'Failed to register blueprints: {e}')
        raise
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint for backend status"""
        app.logger.info('Root endpoint accessed')
        return jsonify({
            'status': 'ok',
            'service': 'EasyXpense Backend',
            'environment': os.getenv('FLASK_ENV', 'development')
        }), 200
    
    # Health endpoint for monitoring
    @app.route('/health', methods=['GET'])
    def health():
        """Simple health check for Render monitoring"""
        app.logger.info('Health endpoint accessed')
        try:
            db_status = 'connected' if app.db else 'disconnected'
            return jsonify({
                'status': 'healthy',
                'database': db_status
            }), 200
        except Exception as e:
            app.logger.error(f'Health check failed: {e}')
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 503
    
    # Enhanced error handlers
    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning(f'Bad request: {error}')
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        # Don't log warnings for expected endpoints
        if request.path not in ['/', '/health']:
            app.logger.warning(f'Endpoint not found: {request.url}')
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        app.logger.warning(f'Method not allowed: {request.method} {request.url}')
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        app.logger.error(f'Service unavailable: {error}')
        return jsonify({'error': 'Service temporarily unavailable'}), 503
    
    app.logger.info('EasyXpense Backend initialized successfully')
    return app