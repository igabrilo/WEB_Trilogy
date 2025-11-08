import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, use environment variables directly
    pass

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OAuth2 Configuration
    OAUTH2_CLIENT_ID = os.environ.get('OAUTH2_CLIENT_ID', '')
    OAUTH2_CLIENT_SECRET = os.environ.get('OAUTH2_CLIENT_SECRET', '')
    OAUTH2_ACCESS_TOKEN_URL = os.environ.get('OAUTH2_ACCESS_TOKEN_URL', '')
    OAUTH2_AUTHORIZE_URL = os.environ.get('OAUTH2_AUTHORIZE_URL', '')
    OAUTH2_API_BASE_URL = os.environ.get('OAUTH2_API_BASE_URL', '')
    
    # Firebase Configuration
    # Option 1: Path to Firebase service account JSON file
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', '')
    # Option 2: Firebase credentials as JSON string (alternative to file path)
    # Set FIREBASE_CREDENTIALS_JSON in environment if not using file path
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', '')
    
    # JWT Configuration
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_DAYS = 30
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Database Configuration
    # Heroku provides DATABASE_URL automatically when using Postgres addon
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # Handle Heroku Postgres connection string format
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # AAI@EduHr Configuration
    # Protocol: SAML (recommended), OIDC, or CAS
    AAI_PROTOCOL = os.environ.get('AAI_PROTOCOL', 'SAML').upper()
    
    # SAML 2.0 Configuration
    AAI_ENTITY_ID = os.environ.get('AAI_ENTITY_ID', 'https://aai.fer.hr/idp/shibboleth')
    AAI_LOGIN_URL = os.environ.get('AAI_LOGIN_URL', 'https://aai.fer.hr/idp/profile/SAML2/Redirect/SSO')
    AAI_LOGOUT_URL = os.environ.get('AAI_LOGOUT_URL', 'https://aai.fer.hr/idp/profile/Logout')
    AAI_METADATA_URL = os.environ.get('AAI_METADATA_URL', 'https://aai.fer.hr/idp/shibboleth')
    
    # Service Provider (SP) Configuration for AAI/SAML
    SP_ENTITY_ID = os.environ.get('SP_ENTITY_ID', '')
    SP_ACS_URL = os.environ.get('SP_ACS_URL', '')  # Assertion Consumer Service URL
    SP_SLS_URL = os.environ.get('SP_SLS_URL', '')  # Single Logout Service URL
    SP_X509_CERT = os.environ.get('SP_X509_CERT', '')  # SP certificate (PEM format)
    SP_PRIVATE_KEY = os.environ.get('SP_PRIVATE_KEY', '')  # SP private key (PEM format)
    IDP_X509_CERT = os.environ.get('IDP_X509_CERT', '')  # IdP certificate from metadata (PEM format)
    
    # OpenID Connect (OIDC) Configuration
    AAI_OIDC_CLIENT_ID = os.environ.get('AAI_OIDC_CLIENT_ID', '')
    AAI_OIDC_CLIENT_SECRET = os.environ.get('AAI_OIDC_CLIENT_SECRET', '')
    AAI_OIDC_DISCOVERY_URL = os.environ.get('AAI_OIDC_DISCOVERY_URL', 'https://aai.fer.hr/.well-known/openid-configuration')
    AAI_OIDC_END_SESSION_URL = os.environ.get('AAI_OIDC_END_SESSION_URL', 'https://aai.fer.hr/oidc/end_session')
    
    # CAS Configuration
    AAI_CAS_SERVER_URL = os.environ.get('AAI_CAS_SERVER_URL', 'https://aai.fer.hr/cas')
    AAI_CAS_VERSION = os.environ.get('AAI_CAS_VERSION', '2')  # CAS protocol version: 1, 2, or 3
    SP_CAS_SERVICE_URL = os.environ.get('SP_CAS_SERVICE_URL', '')
    
    # Session configuration (needed for AAI redirects)
    SESSION_SECRET_KEY = os.environ.get('SESSION_SECRET_KEY', SECRET_KEY)
    
    # Frontend URL for redirects after authentication
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
    
    # Chatbot Configuration
    # Smotra UNIZG Chatbot
    SMOTRA_CHATBOT_API_KEY = os.environ.get('SMOTRA_CHATBOT_API_KEY', '')
    SMOTRA_BASE_URL = os.environ.get('SMOTRA_BASE_URL', 'https://smotra.unizg.hr')
    
    # Career Development Office Chatbot
    CAREER_OFFICE_CHATBOT_API_KEY = os.environ.get('CAREER_OFFICE_CHATBOT_API_KEY', '')
    CAREER_OFFICE_BASE_URL = os.environ.get('CAREER_OFFICE_BASE_URL', 'https://www.unizg.hr')
    
    # OpenAI/Generic Chatbot (optional)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL', '')
    
    # Email Configuration (for notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME', ''))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

