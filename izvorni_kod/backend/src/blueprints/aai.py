from flask import Blueprint, request, jsonify, redirect, url_for, session

# Support both absolute and relative imports
try:
    from models import User
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
    from aai_service import AAIService
except ImportError:
    from ..models import User
    from ..oauth2_service import OAuth2Service
    from ..firebase_service import FirebaseService
    from ..aai_service import AAIService

aai_bp = Blueprint('aai', __name__, url_prefix='/api/aai')

def init_aai_routes(oauth_service, firebase_service, aai_service):
    """Initialize AAI@EduHr routes with services"""
    
    @aai_bp.route('/login', methods=['GET', 'POST'])
    def aai_login():
        """Initiate AAI@EduHr login"""
        try:
            # Get email from request (for direct login) or redirect to AAI
            email = request.args.get('email') or (request.get_json() or {}).get('email')
            
            if email:
                # Direct login with email - redirect to AAI
                aai_login_url = aai_service.get_login_url(
                    redirect_after_login=url_for('aai.aai_callback', _external=True)
                )
                return redirect(aai_login_url)
            else:
                # No email provided - return AAI login URL for frontend redirect
                aai_login_url = aai_service.get_login_url(
                    redirect_after_login=url_for('aai.aai_callback', _external=True)
                )
                return jsonify({
                    'success': True,
                    'aai_login_url': aai_login_url,
                    'message': 'Redirect to AAI@EduHr login'
                }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'AAI login failed: {str(e)}'
            }), 500
    
    @aai_bp.route('/callback', methods=['GET', 'POST'])
    def aai_callback():
        """Handle AAI@EduHr callback after authentication"""
        try:
            # Handle AAI callback
            user_info = aai_service.handle_callback()
            
            if not user_info:
                return jsonify({
                    'success': False,
                    'message': 'Failed to authenticate with AAI@EduHr'
                }), 400
            
            email = user_info['email']
            
            # Check if user exists by email
            existing_user = User.find_by_email(email)
            
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
                # Check if user exists by provider
                existing_user = User.find_by_provider('aai', email)
                
                if existing_user:
                    if isinstance(existing_user, dict):
                        user_id = existing_user['id']
                        user_email = existing_user['email']
                        user_role = existing_user.get('role', 'student')
                    else:
                        user_id = existing_user.id
                        user_email = existing_user.email
                        user_role = existing_user.role
                else:
                    # Create new user from AAI
                    # If email is from faculty domain, set role to faculty
                    from utils import is_faculty_email
                    default_role = 'faculty' if is_faculty_email(user_info['email']) else user_info.get('role', 'student')
                    
                    # For faculty, use firstName as username (institutional name)
                    user_data = {
                        'email': user_info['email'],
                        'password': None,  # No password for AAI users
                        'role': default_role,
                        'provider': 'aai',
                        'provider_id': user_info['provider_id']
                    }
                    
                    if default_role == 'faculty':
                        # For faculty, use firstName as username
                        user_data['username'] = user_info.get('firstName', user_info.get('email', '').split('@')[0])
                    else:
                        user_data['firstName'] = user_info.get('firstName', '')
                        user_data['lastName'] = user_info.get('lastName', '')
                    
                    new_user = User.create(user_data)
                    
                    user_id = new_user.id
                    user_email = new_user.email
                    user_role = new_user.role
            
            # Generate JWT token
            token = oauth_service.generate_token(user_id, user_email, user_role)
            
            # Get redirect URL from session or use default
            redirect_url = session.pop('aai_redirect_after_login', None)
            
            # Return success with token
            # Frontend should handle redirect
            return jsonify({
                'success': True,
                'message': 'AAI@EduHr login successful',
                'user': {
                    'id': user_id,
                    'email': user_email,
                    'firstName': user_info['firstName'],
                    'lastName': user_info['lastName'],
                    'role': user_role
                },
                'token': token,
                'redirect_url': redirect_url
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'AAI callback failed: {str(e)}'
            }), 500
    
    @aai_bp.route('/logout', methods=['POST'])
    @oauth_service.token_required
    def aai_logout(current_user_id, current_user_email, current_user_role):
        """Logout from AAI@EduHr"""
        try:
            # Get redirect URL after logout
            data = request.get_json() or {}
            redirect_url = data.get('redirect_url')
            
            # Generate AAI logout URL
            aai_logout_url = aai_service.get_logout_url(redirect_url)
            
            return jsonify({
                'success': True,
                'message': 'Logout successful',
                'aai_logout_url': aai_logout_url
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'AAI logout failed: {str(e)}'
            }), 500

