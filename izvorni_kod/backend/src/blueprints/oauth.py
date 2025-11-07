from flask import Blueprint, request, jsonify, redirect, url_for, session
import json

# Support both absolute and relative imports
try:
    from models import UserModel
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
except ImportError:
    from ..models import UserModel
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
                if not oauth_service.oauth or not oauth_service.oauth.google:
                    return jsonify({
                        'success': False,
                        'message': 'OAuth2 service not properly configured'
                    }), 500
                
                redirect_uri = url_for('oauth.oauth_callback', provider='google', _external=True)
                return oauth_service.oauth.google.authorize_redirect(redirect_uri)
            else:
                return jsonify({
                    'success': False,
                    'message': f'Provider {provider} not supported'
                }), 400
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"OAuth login error: {str(e)}")
            print(f"Traceback: {error_details}")
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
                    import urllib.parse
                    frontend_url = request.headers.get('Origin') or request.args.get('frontend_url') or 'http://localhost:5173'
                    redirect_url = f"{frontend_url}/prijava?error=oauth_failed"
                    return redirect(redirect_url)
                
                # Check if user exists by provider (SQLAlchemy)
                existing_user = UserModel.find_by_provider('google', user_info['provider_id'])
                
                if existing_user:
                    # User exists - login
                    user_id = existing_user.id
                    user_email = existing_user.email
                    user_role = existing_user.role
                    user_provider = existing_user.provider
                    
                    # IMPORTANT: If user logged in via Google OAuth, don't auto-assign admin role
                    # Admin role should only be assigned via email/password login with specific credentials
                    # This prevents Google OAuth users from getting admin access
                    if user_role == 'admin' and user_provider == 'google':
                        # Reset to student role for Google OAuth users (admin should use email/password)
                        if not isinstance(existing_user, dict):
                            existing_user.role = 'student'
                            existing_user.save()
                        user_role = 'student'
                else:
                    # Check if user exists by email (SQLAlchemy)
                    existing_user = UserModel.find_by_email(user_info['email'])
                    
                    if existing_user:
                        # User exists with this email but different provider
                        # If user is admin, don't allow Google OAuth login (security measure)
                        existing_user_role = existing_user.role
                        if existing_user_role == 'admin':
                            import urllib.parse
                            frontend_url = request.headers.get('Origin') or request.args.get('frontend_url') or 'http://localhost:5173'
                            error_msg = urllib.parse.quote('Admin accounts must use email/password login. Google OAuth is not allowed for admin accounts.')
                            redirect_url = f"{frontend_url}/prijava?error={error_msg}"
                            return redirect(redirect_url)
                        
                        # For non-admin users, ask them to use email/password login
                        import urllib.parse
                        frontend_url = request.headers.get('Origin') or request.args.get('frontend_url') or 'http://localhost:5173'
                        error_msg = urllib.parse.quote('An account with this email already exists. Please use email/password login.')
                        redirect_url = f"{frontend_url}/prijava?error={error_msg}"
                        return redirect(redirect_url)
                    
                    # Check if email is from faculty domain - don't allow Google login for faculty
                    from utils import is_faculty_email
                    if is_faculty_email(user_info['email']):
                        import urllib.parse
                        frontend_url = request.headers.get('Origin') or request.args.get('frontend_url') or 'http://localhost:5173'
                        error_msg = urllib.parse.quote('Fakulteti se prijavljuju isključivo preko AAI@EduHr sustava. Google prijava nije dostupna za fakultetske email adrese.')
                        redirect_url = f"{frontend_url}/prijava?error={error_msg}"
                        return redirect(redirect_url)
                    
                    # Create new user in database (default role student)
                    new_user = UserModel.create({
                        'email': user_info['email'],
                        'password': None,  # No password for OAuth users
                        'firstName': user_info['firstName'],
                        'lastName': user_info['lastName'],
                        'role': 'student',  # Default role, can be changed in profile
                        'provider': 'google',
                        'provider_id': user_info['provider_id']
                    })
                    user_id = new_user.id
                    user_email = new_user.email
                    user_role = new_user.role
                
                # Generate JWT token
                token = oauth_service.generate_token(user_id, user_email, user_role)
                
                # Prepare user data for frontend
                # Use DB user info if available, fallback to OAuth user_info
                db_user = UserModel.find_by_id(user_id)
                user_data = db_user.to_dict() if db_user else {
                    'id': user_id,
                    'email': user_email,
                    'firstName': user_info.get('firstName', ''),
                    'lastName': user_info.get('lastName', ''),
                    'role': user_role
                }
                
                # Redirect to frontend with token and user data in URL
                import urllib.parse
                frontend_url = request.headers.get('Origin') or request.args.get('frontend_url') or 'http://localhost:5173'
                user_json = urllib.parse.quote(json.dumps(user_data))
                redirect_url = f"{frontend_url}/prijava?token={token}&user={user_json}"
                return redirect(redirect_url)
            else:
                return jsonify({
                    'success': False,
                    'message': f'Provider {provider} not supported'
                }), 400
                
        except Exception as e:
            import urllib.parse
            frontend_url = request.headers.get('Origin') or request.args.get('frontend_url') or 'http://localhost:5173'
            error_msg = urllib.parse.quote(f'OAuth callback failed: {str(e)}')
            redirect_url = f"{frontend_url}/prijava?error={error_msg}"
            return redirect(redirect_url)

