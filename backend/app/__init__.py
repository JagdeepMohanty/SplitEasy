from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
from datetime import timedelta

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'fallback-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/spliteasy')
    
    # Initialize extensions
    jwt = JWTManager(app)
    CORS(app, origins=[os.getenv('CLIENT_URL', 'http://localhost:5173')])
    
    # MongoDB connection
    try:
        client = MongoClient(app.config['MONGODB_URI'])
        app.db = client.get_default_database()
        # Test connection
        client.admin.command('ping')
        print('✅ MongoDB connected successfully')
    except Exception as e:
        print(f'❌ MongoDB connection error: {e}')
        raise
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.friends import friends_bp
    from app.routes.expenses import expenses_bp
    from app.routes.settlements import settlements_bp
    from app.routes.debts import debts_bp
    from app.routes.health import health_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/users')
    app.register_blueprint(friends_bp, url_prefix='/api/friends')
    app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
    app.register_blueprint(settlements_bp, url_prefix='/api/settlements')
    app.register_blueprint(debts_bp, url_prefix='/api/debts')
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return {'msg': 'Bad request'}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'msg': 'Unauthorized'}, 401
    
    @app.errorhandler(404)
    def not_found(error):
        return {'msg': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'msg': 'Internal server error'}, 500
    
    return app