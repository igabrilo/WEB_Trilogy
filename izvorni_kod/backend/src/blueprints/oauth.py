from flask import Blueprint, request, jsonify, redirect, url_for, session

# Support both absolute and relative imports
try:
    from models import User
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
except ImportError:
    from ..models import User
    from ..oauth2_service import OAuth2Service
    from ..firebase_service import FirebaseService

oauth_bp = Blueprint('oauth', __name__, url_prefix='/api/oauth')

def init_oauth_routes(oauth_service, firebase_service):
    """Initialize OAuth routes with services"""
    
    @oauth_bp.route('/login/<provider>', methods=['GET'])
    def oauth_login(provider):
        """Initiate OAuth2 login"""
        try:
            if provider == 'google':
                redirect_uri = url_for('oauth.oauth_callback', provider='google', _external=True)
                return oauth_service.oauth.google.authorize_redirect(redirect_uri)
            else:
                return jsonify({
                    'success': False,
                    'message': f'Provider {provider} not supported'
                }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'OAuth login failed: {str(e)}'
            }), 500
    
    @oauth_bp.route('/callback/<provider>', methods=['GET'])
    def oauth_callback(provider):
        """Handle OAuth2 callback"""
        try:
            if provider == 'google':
                user_info = oauth_service.handle_callback('google')
                
                if not user_info:
                    return jsonify({
                        'success': False,
                        'message': 'Failed to authenticate with OAuth provider'
                    }), 400
                
                # Check if user exists by provider
                existing_user = User.find_by_provider('google', user_info['provider_id'])
                
                if existing_user:
                    # User exists - login
                    if isinstance(existing_user, dict):
                        user_id = existing_user['id']
                        user_email = existing_user['email']
                        user_role = existing_user.get('role', 'student')
                    else:
                        user_id = existing_user.id
                        user_email = existing_user.email
                        user_role = existing_user.role
                else:
                    # Check if user exists by email
                    existing_user = User.find_by_email(user_info['email'])
                    
                    if existing_user:
                        # User exists with this email but different provider
                        return jsonify({
                            'success': False,
                            'message': 'An account with this email already exists. Please use email/password login.'
                        }), 400
                    
                    # Create new user
                    new_user = User.create({
                        'email': user_info['email'],
                        'password': None,  # No password for OAuth users
                        'firstName': user_info['firstName'],
                        'lastName': user_info['lastName'],
                        'role': 'student',
                        'provider': 'google',
                        'provider_id': user_info['provider_id']
                    })
                    
                    user_id = new_user.id
                    user_email = new_user.email
                    user_role = new_user.role
                
                # Generate JWT token
                token = oauth_service.generate_token(user_id, user_email, user_role)
                
                # Return success with token (frontend should handle redirect)
                return jsonify({
                    'success': True,
                    'message': 'OAuth login successful',
                    'user': {
                        'id': user_id,
                        'email': user_email,
                        'firstName': user_info['firstName'],
                        'lastName': user_info['lastName'],
                        'role': user_role
                    },
                    'token': token
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': f'Provider {provider} not supported'
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'OAuth callback failed: {str(e)}'
            }), 500

