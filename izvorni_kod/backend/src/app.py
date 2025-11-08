from flask import Flask, jsonify
from flask_cors import CORS
import os
import warnings

# Suppress known warnings
warnings.filterwarnings('ignore', message='.*importlib.metadata.*packages_distributions.*')
warnings.filterwarnings('ignore', category=FutureWarning, message='.*Python version.*past its end of life.*')

# Use relative imports when used as package (default), or absolute imports when src is in path
try:
    from .config import config
    from .oauth2_service import OAuth2Service
    from .firebase_service import FirebaseService
    from .aai_service import AAIService
    from .chatbot_service import ChatbotService
    from .email_service import EmailService
    from .database import init_db, create_tables  # Import database setup
except (ImportError, ValueError):
    # Fallback to absolute imports if src is in Python path
    from config import config  # type: ignore
    from oauth2_service import OAuth2Service  # type: ignore
    from firebase_service import FirebaseService  # type: ignore
    from aai_service import AAIService  # type: ignore
    from chatbot_service import ChatbotService  # type: ignore
    from email_service import EmailService  # type: ignore
    from database import init_db, create_tables  # type: ignore  # Import database setup

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
    
    # Import models and blueprints within app context
    # This ensures SQLAlchemy is properly bound to this Flask app instance
    with app.app_context():
        # Import models after db is initialized to register them with SQLAlchemy
        try:
            from . import models  # Import models to register them with SQLAlchemy
        except ImportError:
            import models
        
        # Create tables in development (in production, use migrations)
        if config_name == 'development':
            create_tables(app)
        
        # Import blueprints AFTER db is initialized and models are imported
        # This ensures that when blueprints import models, db is already initialized
        try:
            from .blueprints.auth import auth_bp, init_auth_routes
            from .blueprints.oauth import oauth_bp, init_oauth_routes
            from .blueprints.notifications import notifications_bp, init_notification_routes
            from .blueprints.aai import aai_bp, init_aai_routes
            from .blueprints.chatbot import chatbot_bp, init_chatbot_routes
            from .blueprints.search import search_bp
            from .blueprints.associations import associations_bp, init_associations_routes
            from .blueprints.jobs import jobs_bp, init_jobs_routes
            from .blueprints.admin import admin_bp, init_admin_routes
            from .blueprints.erasmus import erasmus_bp, init_erasmus_routes
            from .blueprints.favorites import favorites_bp, init_favorites_routes
            from .blueprints.inquiries import inquiries_bp, init_inquiries_routes
        except ImportError:
            # Fallback to absolute imports if src is in Python path
            from blueprints.auth import auth_bp, init_auth_routes  # type: ignore
            from blueprints.oauth import oauth_bp, init_oauth_routes  # type: ignore
            from blueprints.notifications import notifications_bp, init_notification_routes  # type: ignore
            from blueprints.aai import aai_bp, init_aai_routes  # type: ignore
            from blueprints.chatbot import chatbot_bp, init_chatbot_routes  # type: ignore
            from blueprints.search import search_bp  # type: ignore
            from blueprints.associations import associations_bp, init_associations_routes  # type: ignore
            from blueprints.jobs import jobs_bp, init_jobs_routes  # type: ignore
            from blueprints.admin import admin_bp, init_admin_routes  # type: ignore
            from blueprints.erasmus import erasmus_bp, init_erasmus_routes  # type: ignore
            from blueprints.favorites import favorites_bp, init_favorites_routes  # type: ignore
            from blueprints.inquiries import inquiries_bp, init_inquiries_routes  # type: ignore
    
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
    email_service = EmailService(app)
    
    # Initialize and register blueprints with services (within app context for proper SQLAlchemy binding)
    with app.app_context():
        # Initialize blueprints with services
        init_auth_routes(oauth_service, firebase_service, aai_service)
        init_oauth_routes(oauth_service, firebase_service)
        init_notification_routes(oauth_service, firebase_service)
        init_aai_routes(oauth_service, firebase_service, aai_service)
        init_chatbot_routes(oauth_service, firebase_service, chatbot_service)
        init_associations_routes(oauth_service)
        init_jobs_routes(oauth_service, email_service, firebase_service)
        init_admin_routes(oauth_service)
        init_erasmus_routes(oauth_service)
        init_favorites_routes(oauth_service)
        init_inquiries_routes(oauth_service, email_service)
        
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
        app.register_blueprint(erasmus_bp)
        app.register_blueprint(favorites_bp)
        app.register_blueprint(inquiries_bp)
    
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
                "faculties": "/api/faculties",
                "inquiries": "/api/inquiries",
                "erasmus": "/api/erasmus",
                "favorites": "/api/favorites"
            }
        })
    
    # Health check endpoint
    @app.route("/health")
    def health():
        firebase_status = "initialized" if firebase_service.initialized else "not_initialized"
        firebase_message = "Ready" if firebase_service.initialized else "Credentials not configured"
        
        return jsonify({
            "status": "healthy",
            "services": {
                "oauth2": {
                    "available": oauth_service.oauth is not None,
                    "status": "ready" if oauth_service.oauth else "not_configured"
                },
                "firebase": {
                    "available": firebase_service.initialized,
                    "status": firebase_status,
                    "message": firebase_message
                },
                "email": {
                    "available": email_service.initialized,
                    "status": "initialized" if email_service.initialized else "not_initialized",
                    "message": "Ready" if email_service.initialized else "Not configured (MAIL_USERNAME and MAIL_PASSWORD required)"
                },
                "chatbot": {
                    "available": len(chatbot_service.get_available_providers()) > 0,
                    "providers": chatbot_service.get_available_providers(),
                    "count": len(chatbot_service.get_available_providers())
                }
            }
        })
    
    return app

