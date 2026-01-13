from app import create_app
import os

# Create Flask application
app = create_app()

if __name__ == "__main__":
    # For development
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)