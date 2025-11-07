from flask import Flask, jsonify
from flask_cors import CORS
import os
import warnings

# Suppress known warnings
warnings.filterwarnings('ignore', message='.*importlib.metadata.*packages_distributions.*')
warnings.filterwarnings('ignore', category=FutureWarning, message='.*Python version.*past its end of life.*')

# Use absolute imports when src is in path, or relative imports when used as package
try:
    from config import config
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
    from aai_service import AAIService
    from chatbot_service import ChatbotService
    from database import init_db, create_tables, db  # Import database setup
    from blueprints.auth import auth_bp, init_auth_routes
    from blueprints.oauth import oauth_bp, init_oauth_routes
    from blueprints.notifications import notifications_bp, init_notification_routes
    from blueprints.aai import aai_bp, init_aai_routes
    from blueprints.chatbot import chatbot_bp, init_chatbot_routes
    from blueprints.search import search_bp
    from blueprints.associations import associations_bp, init_associations_routes
    from blueprints.jobs import jobs_bp, init_jobs_routes
    from blueprints.admin import admin_bp, init_admin_routes
except ImportError:
    # Fallback to relative imports if used as package
    from .config import config
    from .oauth2_service import OAuth2Service
    from .firebase_service import FirebaseService
    from .aai_service import AAIService
    from .chatbot_service import ChatbotService
    from .database import init_db, create_tables  # Import database setup
    from .blueprints.auth import auth_bp, init_auth_routes
    from .blueprints.oauth import oauth_bp, init_oauth_routes
    from .blueprints.notifications import notifications_bp, init_notification_routes
    from .blueprints.aai import aai_bp, init_aai_routes
    from .blueprints.chatbot import chatbot_bp, init_chatbot_routes
    from .blueprints.search import search_bp
    from .blueprints.associations import associations_bp, init_associations_routes
    from .blueprints.jobs import jobs_bp, init_jobs_routes
    from .blueprints.admin import admin_bp, init_admin_routes

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(config_name, config['default']))
    
    # Set session secret key FIRST (required for OAuth and AAI redirects)
    app.secret_key = app.config.get('SESSION_SECRET_KEY') or app.config.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # Initialize database
    init_db(app)
    
    # Import models after db is initialized to avoid circular imports
    with app.app_context():
        try:
            from . import models  # Import models to register them with SQLAlchemy
        except ImportError:
            import models
    
    # Create tables in development (in production, use migrations)
    if config_name == 'development':
        create_tables(app)
    
    # Initialize CORS - allow all origins in development, specific origins in production
    cors_origins = app.config.get('CORS_ORIGINS', ['*'])
    if cors_origins == ['*'] or '*' in cors_origins:
        CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    else:
        CORS(app, resources={r"/api/*": {"origins": cors_origins, "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    
    # Initialize services
    oauth_service = OAuth2Service(app)
    firebase_service = FirebaseService(app)
    aai_service = AAIService(app)
    chatbot_service = ChatbotService(app)
    
    # Initialize blueprints with services
    init_auth_routes(oauth_service, firebase_service, aai_service)
    init_oauth_routes(oauth_service, firebase_service)
    init_notification_routes(oauth_service, firebase_service)
    init_aai_routes(oauth_service, firebase_service, aai_service)
    init_chatbot_routes(oauth_service, firebase_service, chatbot_service)
    init_associations_routes(oauth_service)
    init_jobs_routes(oauth_service)
    init_admin_routes(oauth_service)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(aai_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(associations_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(admin_bp)
    
    # Root endpoint
    @app.route("/")
    def home():
        return jsonify({
            "message": "UNIZG Career Hub API",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/api/auth",
                "oauth": "/api/oauth",
                "notifications": "/api/notifications",
                "aai": "/api/aai",
                "chatbot": "/api/chatbot",
                "search": "/api/search",
                "associations": "/api/associations",
                "faculties": "/api/faculties"
            }
        })
    
    # Health check endpoint
    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "services": {
                "oauth2": oauth_service.oauth is not None,
                "firebase": firebase_service.initialized,
                "chatbot": len(chatbot_service.get_available_providers()) > 0
            }
        })
    
    return app

