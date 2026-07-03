from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os

load_dotenv()


def create_app(config=None):
    """Flask application factory."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///event_catering.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from routes.events import events_bp
    from routes.guests import guests_bp
    from routes.dishes import dishes_bp
    from routes.menu import menu_bp
    from routes.calculate import calculate_bp
    
    app.register_blueprint(events_bp)
    app.register_blueprint(guests_bp)
    app.register_blueprint(dishes_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(calculate_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
