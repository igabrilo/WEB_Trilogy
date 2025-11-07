from authlib.integrations.flask_client import OAuth
from flask import Flask, session, redirect, url_for
from functools import wraps
import jwt
import datetime
import os

class OAuth2Service:
    """OAuth2 Authentication Service"""
    
    def __init__(self, app=None):
        self.oauth = None
        self.app = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize OAuth2 with Flask app"""
        self.app = app
        self.oauth = OAuth(app)
        
        # Register OAuth providers
        # Example: Google OAuth (can add more providers)
        if app.config.get('OAUTH2_CLIENT_ID'):
            self.oauth.register(
                name='google',
                client_id=app.config.get('OAUTH2_CLIENT_ID'),
                client_secret=app.config.get('OAUTH2_CLIENT_SECRET'),
                server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
                client_kwargs={
                    'scope': 'openid email profile'
                }
            )
    
    def generate_token(self, user_id, email, role='student'):
        """Generate JWT token for user"""
        if not self.app:
            raise RuntimeError("OAuth2Service not initialized with Flask app")
        secret_key = self.app.config.get('SECRET_KEY')
        expiration_days = self.app.config.get('JWT_EXPIRATION_DAYS', 30)
        
        token = jwt.encode({
            'user_id': user_id,
            'email': email,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days)
        }, secret_key, algorithm='HS256')
        
        return token
    
    def verify_token(self, token):
        """Verify JWT token"""
        if not self.app:
            raise RuntimeError("OAuth2Service not initialized with Flask app")
        try:
            secret_key = self.app.config.get('SECRET_KEY')
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            return data
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_authorization_url(self, provider='google', redirect_uri=None):
        """Get OAuth2 authorization URL"""
        if not self.oauth:
            return None
        
        if provider == 'google' and self.oauth.google:
            redirect_uri = redirect_uri or url_for('oauth_callback', provider='google', _external=True)
            return self.oauth.google.authorize_redirect(redirect_uri)
        
        return None
    
    def handle_callback(self, provider='google'):
        """Handle OAuth2 callback"""
        if not self.oauth:
            return None
        
        if provider == 'google' and self.oauth.google:
            try:
                token = self.oauth.google.authorize_access_token()
                user_info = token.get('userinfo')
                
                if user_info:
                    return {
                        'email': user_info.get('email'),
                        'firstName': user_info.get('given_name', ''),
                        'lastName': user_info.get('family_name', ''),
                        'picture': user_info.get('picture', ''),
                        'provider': 'google',
                        'provider_id': user_info.get('sub')
                    }
            except Exception as e:
                print(f"OAuth callback error: {str(e)}")
                return None
        
        return None
    
    def token_required(self, f):
        """Decorator for routes requiring authentication"""
        from functools import wraps
        
        @wraps(f)
        def decorated(*args, **kwargs):
            from flask import request, jsonify
            
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({'success': False, 'message': 'Token is missing'}), 401
            
            try:
                if token.startswith('Bearer '):
                    token = token[7:]
                
                data = self.verify_token(token)
                if not data:
                    return jsonify({'success': False, 'message': 'Token is invalid or expired'}), 401
                
                # Add user data to kwargs
                kwargs['current_user_id'] = data.get('user_id')
                kwargs['current_user_email'] = data.get('email')
                kwargs['current_user_role'] = data.get('role')
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Token verification failed: {str(e)}'}), 401
            
            return f(*args, **kwargs)
        return decorated
    
    def optional_token(self, f):
        """Decorator for routes that work with or without authentication"""
        from functools import wraps
        
        @wraps(f)
        def decorated(*args, **kwargs):
            from flask import request
            
            token = request.headers.get('Authorization')
            
            # Try to get user data if token is provided, but don't require it
            if token:
                try:
                    if token.startswith('Bearer '):
                        token = token[7:]
                    
                    data = self.verify_token(token)
                    if data:
                        # Add user data to kwargs if token is valid
                        kwargs['current_user_id'] = data.get('user_id')
                        kwargs['current_user_email'] = data.get('email')
                        kwargs['current_user_role'] = data.get('role')
                        kwargs['is_authenticated'] = True
                    else:
                        # Token is invalid, but continue without auth
                        kwargs['current_user_id'] = None
                        kwargs['current_user_email'] = None
                        kwargs['current_user_role'] = None
                        kwargs['is_authenticated'] = False
                except Exception:
                    # Token verification failed, continue without auth
                    kwargs['current_user_id'] = None
                    kwargs['current_user_email'] = None
                    kwargs['current_user_role'] = None
                    kwargs['is_authenticated'] = False
            else:
                # No token provided, continue without auth
                kwargs['current_user_id'] = None
                kwargs['current_user_email'] = None
                kwargs['current_user_role'] = None
                kwargs['is_authenticated'] = False
            
            return f(*args, **kwargs)
        return decorated

