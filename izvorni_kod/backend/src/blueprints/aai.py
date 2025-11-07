from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
import urllib.parse
import json

# Support both absolute and relative imports
try:
    from models import User, UserModel
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
    from aai_service import AAIService, SAML_AVAILABLE, CAS_AVAILABLE
except ImportError:
    from ..models import User, UserModel
    from ..oauth2_service import OAuth2Service
    from ..firebase_service import FirebaseService
    from ..aai_service import AAIService, SAML_AVAILABLE, CAS_AVAILABLE

aai_bp = Blueprint('aai', __name__, url_prefix='/api/aai')

def get_db():
    """Get db instance from current app"""
    return current_app.extensions['sqlalchemy']

def init_aai_routes(oauth_service, firebase_service, aai_service):
    """Initialize AAI@EduHr routes with services"""
    
    @aai_bp.route('/protocols', methods=['GET'])
    def get_available_protocols():
        """Get list of available AAI authentication protocols"""
        protocols = []
        
        if SAML_AVAILABLE:
            protocols.append({
                'protocol': 'SAML',
                'name': 'SAML 2.0',
                'recommended': True,
                'available': True
            })
        
        if aai_service.oidc_available:
            protocols.append({
                'protocol': 'OIDC',
                'name': 'OpenID Connect',
                'recommended': False,
                'available': True
            })
        
        if CAS_AVAILABLE:
            protocols.append({
                'protocol': 'CAS',
                'name': 'Central Authentication Service',
                'recommended': False,
                'available': True
            })
        
        return jsonify({
            'success': True,
            'protocols': protocols,
            'current_protocol': aai_service.protocol
        }), 200
    
    @aai_bp.route('/login', methods=['GET', 'POST'])
    def aai_login():
        """Initiate AAI@EduHr login"""
        try:
            # Get protocol from request (optional, uses configured protocol if not provided)
            protocol = request.args.get('protocol') or (request.get_json() or {}).get('protocol')
            
            # Get email from request (for direct login) or redirect to AAI
            email = request.args.get('email') or (request.get_json() or {}).get('email')
            
            # Construct callback URL - use SP_ACS_URL from config or construct from request
            from flask import current_app
            callback_url = current_app.config.get('SP_ACS_URL')
            if not callback_url:
                # Fallback to url_for if SP_ACS_URL not configured
                callback_url = url_for('aai.aai_callback', _external=True)
                # Fix double port issue (localhost:5001:5000 -> localhost:5001)
                if ':5001:5000' in callback_url:
                    callback_url = callback_url.replace(':5001:5000', ':5001')
            
            if email:
                # Direct login with email - redirect to AAI
                aai_login_url = aai_service.get_login_url(
                    redirect_after_login=callback_url,
                    protocol=protocol
                )
                return redirect(aai_login_url)
            else:
                # No email provided - return AAI login URL for frontend redirect
                aai_login_url = aai_service.get_login_url(
                    redirect_after_login=callback_url,
                    protocol=protocol
                )
                return jsonify({
                    'success': True,
                    'aai_login_url': aai_login_url,
                    'protocol': protocol or aai_service.protocol,
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
            # Determine protocol from request
            protocol = request.args.get('protocol') or request.form.get('protocol')
            
            # Handle AAI callback
            user_info = aai_service.handle_callback(protocol=protocol)
            
            if not user_info:
                # Redirect to frontend with error
                error_msg = 'Failed to authenticate with AAI@EduHr'
                frontend_url = aai_service.app.config.get('FRONTEND_URL', 'http://localhost:5173')
                return redirect(f"{frontend_url}/prijava?error={urllib.parse.quote(error_msg)}")
            
            email = user_info['email']
            
            # Check if user exists by email
            db_instance = get_db()
            existing_user = db_instance.session.query(UserModel).filter_by(email=email).first()
            
            if existing_user:
                # User exists - login
                user_id = existing_user.id
                user_email = existing_user.email
                user_role = existing_user.role
            else:
                # Check if user exists by provider
                existing_user = db_instance.session.query(UserModel).filter_by(
                    provider='aai',
                    provider_id=user_info['provider_id']
                ).first()
                
                if existing_user:
                    user_id = existing_user.id
                    user_email = existing_user.email
                    user_role = existing_user.role
                else:
                    # Create new user from AAI
                    # If email is from faculty domain, set role to faculty
                    from utils import is_faculty_email
                    default_role = 'faculty' if is_faculty_email(user_info['email']) else user_info.get('role', 'student')
                    
                    # For faculty, use firstName as username (institutional name)
                    if default_role == 'faculty' or default_role == 'fakultet':
                        # For faculty, use firstName as username
                        new_user = UserModel(
                            email=user_info['email'],
                            password=None,  # No password for AAI users
                            username=user_info.get('firstName', user_info.get('email', '').split('@')[0]),
                            role=default_role,
                            provider='aai',
                            provider_id=user_info['provider_id']
                        )
                    else:
                        new_user = UserModel(
                            email=user_info['email'],
                            password=None,  # No password for AAI users
                            first_name=user_info.get('firstName', ''),
                            last_name=user_info.get('lastName', ''),
                            role=default_role,
                            provider='aai',
                            provider_id=user_info['provider_id']
                        )
                    
                    db_instance.session.add(new_user)
                    db_instance.session.commit()
                    
                    user_id = new_user.id
                    user_email = new_user.email
                    user_role = new_user.role
            
            # Generate JWT token
            token = oauth_service.generate_token(user_id, user_email, user_role)
            
            # Store SAML NameID and SessionIndex in session for Single Logout (if available)
            if user_info.get('attributes') and SAML_AVAILABLE:
                # Try to extract NameID and SessionIndex from SAML attributes
                # These are typically stored in the SAML auth object, but we'll store them in session
                session['saml_nameid'] = user_info.get('provider_id')
                session['saml_session_index'] = user_info.get('attributes', {}).get('SessionIndex', [None])[0] if isinstance(user_info.get('attributes', {}).get('SessionIndex'), list) else user_info.get('attributes', {}).get('SessionIndex')
            
            # Get redirect URL from session or use default
            redirect_url = session.pop('aai_redirect_after_login', None)
            frontend_url = aai_service.app.config.get('FRONTEND_URL', 'http://localhost:5173')
            
            # Redirect to frontend with token
            user_dict = {
                'id': user_id,
                'email': user_email,
                'firstName': user_info.get('firstName', ''),
                'lastName': user_info.get('lastName', ''),
                'role': user_role
            }
            
            # Encode user data and token for URL
            user_str = urllib.parse.quote(json.dumps(user_dict))
            token_str = urllib.parse.quote(token)
            
            redirect_to = f"{frontend_url}/prijava?token={token_str}&user={user_str}"
            
            return redirect(redirect_to)
            
        except Exception as e:
            import traceback
            print(f"AAI callback error: {str(e)}")
            print(traceback.format_exc())
            
            error_msg = f'AAI callback failed: {str(e)}'
            frontend_url = aai_service.app.config.get('FRONTEND_URL', 'http://localhost:5173')
            return redirect(f"{frontend_url}/prijava?error={urllib.parse.quote(error_msg)}")
    
    @aai_bp.route('/logout', methods=['POST'])
    @oauth_service.token_required
    def aai_logout(current_user_id, current_user_email, current_user_role):
        """Logout from AAI@EduHr"""
        try:
            # Get redirect URL after logout
            data = request.get_json() or {}
            redirect_url = data.get('redirect_url')
            protocol = data.get('protocol')
            
            # Get SAML NameID and SessionIndex from session (if available)
            name_id = session.get('saml_nameid')
            session_index = session.get('saml_session_index')
            
            # Generate AAI logout URL
            aai_logout_url = aai_service.get_logout_url(
                redirect_after_logout=redirect_url,
                protocol=protocol,
                name_id=name_id,
                session_index=session_index
            )
            
            # Clear session
            session.clear()
            
            return jsonify({
                'success': True,
                'message': 'Logout successful',
                'aai_logout_url': aai_logout_url,
                'protocol': protocol or aai_service.protocol
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'AAI logout failed: {str(e)}'
            }), 500
    
    @aai_bp.route('/metadata', methods=['GET'])
    def get_metadata():
        """Get SAML metadata for this Service Provider (if SAML is configured)"""
        if not SAML_AVAILABLE:
            return jsonify({
                'success': False,
                'message': 'SAML is not available'
            }), 400
        
        try:
            # Check if SAML settings are configured
            if not hasattr(aai_service, 'saml_settings') or not aai_service.saml_settings:
                return jsonify({
                    'success': False,
                    'message': 'SAML settings are not configured. Please check SP_ENTITY_ID, SP_ACS_URL, SP_SLS_URL, SP_X509_CERT, and SP_PRIVATE_KEY in .env file'
                }), 400
            
            # Generate SP metadata XML
            from onelogin.saml2.settings import OneLogin_Saml2_Settings
            
            # Create Settings object and generate metadata
            settings = OneLogin_Saml2_Settings(aai_service.saml_settings, sp_validation_only=True)
            metadata = settings.get_sp_metadata()
            
            return metadata, 200, {'Content-Type': 'application/xml'}
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error generating SAML metadata: {error_details}")
            return jsonify({
                'success': False,
                'message': f'Failed to generate metadata: {str(e)}'
            }), 500
