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
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', '')
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', '')
    
    # JWT Configuration
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_DAYS = 30
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # AAI@EduHr Configuration
    AAI_ENTITY_ID = os.environ.get('AAI_ENTITY_ID', 'https://aai.fer.hr/idp/shibboleth')
    AAI_LOGIN_URL = os.environ.get('AAI_LOGIN_URL', 'https://aai.fer.hr/idp/profile/SAML2/Redirect/SSO')
    AAI_LOGOUT_URL = os.environ.get('AAI_LOGOUT_URL', 'https://aai.fer.hr/idp/profile/Logout')
    AAI_METADATA_URL = os.environ.get('AAI_METADATA_URL', 'https://aai.fer.hr/idp/shibboleth')
    
    # Service Provider (SP) Configuration for AAI
    SP_ENTITY_ID = os.environ.get('SP_ENTITY_ID', '')
    SP_ACS_URL = os.environ.get('SP_ACS_URL', '')  # Assertion Consumer Service URL
    SP_SLS_URL = os.environ.get('SP_SLS_URL', '')  # Single Logout Service URL
    
    # Session configuration (needed for AAI redirects)
    SESSION_SECRET_KEY = os.environ.get('SESSION_SECRET_KEY', SECRET_KEY)
    
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

