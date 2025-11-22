"""Flask application factory."""
from flask import Flask
from app.config import config_by_name
from app.extensions import db, cache, compress
import os


def create_app(config_name=None):
    """Create and configure the Flask application."""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    config_class = config_by_name.get(config_name, config_by_name['development'])
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    cache.init_app(app)
    compress.init_app(app)
    
    # Register blueprints
    from app.routes import web_bp, api_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Add static file caching headers
    @app.after_request
    def add_cache_headers(response):
        """Add cache headers for static assets."""
        if request.path.startswith('/static/'):
            # Far-future cache headers for static assets (1 year)
            response.cache_control.max_age = 31536000
            response.cache_control.public = True
        return response
    
    # Create database tables (only if database is available)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            if app.debug:
                app.logger.warning(f"Database not available during startup: {e}")
    
    return app
