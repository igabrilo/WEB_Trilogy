from flask import Blueprint, request, jsonify

# Support both absolute and relative imports
try:
    from models import User
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
    from utils import is_faculty_email
    from aai_service import AAIService
except ImportError:
    from ..models import User
    from ..oauth2_service import OAuth2Service
    from ..firebase_service import FirebaseService
    from ..utils import is_faculty_email
    from ..aai_service import AAIService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def init_auth_routes(oauth_service, firebase_service, aai_service):
    """Initialize auth routes with services"""
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """Register a new user"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['email', 'password', 'firstName', 'lastName']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'success': False,
                        'message': f'Field {field} is required'
                    }), 400
            
            # Check if user already exists
            existing_user = User.find_by_email(data['email'])
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'User with this email already exists'
                }), 400
            
            # Validate password length
            if len(data['password']) < 6:
                return jsonify({
                    'success': False,
                    'message': 'Password must be at least 6 characters long'
                }), 400
            
            # Create new user
            new_user = User.create({
                'email': data['email'],
                'password': data['password'],
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'role': data.get('role', 'student'),
                'provider': 'local'
            })
            
            # Generate JWT token
            token = oauth_service.generate_token(
                new_user.id,
                new_user.email,
                new_user.role
            )
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user': new_user.to_dict(),
                'token': token
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Registration failed: {str(e)}'
            }), 500
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Login with email and password"""
        try:
            data = request.get_json()
            
            if not data or not data.get('email'):
                return jsonify({
                    'success': False,
                    'message': 'Email is required'
                }), 400
            
            email = data['email']
            
            # Check if email is from a faculty domain
            if is_faculty_email(email):
                # Redirect to AAI@EduHr login
                aai_login_url = aai_service.get_login_url()
                return jsonify({
                    'success': False,
                    'requires_aai': True,
                    'message': 'Faculty email detected. Please use AAI@EduHr login.',
                    'aai_login_url': aai_login_url
                }), 200  # Return 200 so frontend can handle redirect
            
            # Regular email/password login for non-faculty emails
            if not data.get('password'):
                return jsonify({
                    'success': False,
                    'message': 'Password is required for non-faculty emails'
                }), 400
            
            # Find user
            user = User.find_by_email(email)
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Invalid email or password'
                }), 401
            
            # Convert dict to User object if needed
            if isinstance(user, dict):
                # Legacy format - check password
                from werkzeug.security import check_password_hash
                user_password_hash = user.get('password')
                if not user_password_hash or not check_password_hash(user_password_hash, data['password']):
                    return jsonify({
                        'success': False,
                        'message': 'Invalid email or password'
                    }), 401
                
                # Generate token
                token = oauth_service.generate_token(
                    user['id'],
                    user['email'],
                    user.get('role', 'student')
                )
                
                user_response = {
                    'id': user['id'],
                    'email': user['email'],
                    'firstName': user['firstName'],
                    'lastName': user['lastName'],
                    'role': user.get('role', 'student')
                }
            else:
                # New User object
                if not user.check_password(data['password']):
                    return jsonify({
                        'success': False,
                        'message': 'Invalid email or password'
                    }), 401
                
                # Generate token
                token = oauth_service.generate_token(
                    user.id,
                    user.email,
                    user.role
                )
                
                user_response = user.to_dict()
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user_response,
                'token': token
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Login failed: {str(e)}'
            }), 500
    
    @auth_bp.route('/me', methods=['GET'])
    @oauth_service.token_required
    def get_current_user(current_user_id, current_user_email, current_user_role):
        """Get current authenticated user"""
        try:
            user = User.find_by_id(current_user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 404
            
            if isinstance(user, dict):
                user_response = {
                    'id': user['id'],
                    'email': user['email'],
                    'firstName': user['firstName'],
                    'lastName': user['lastName'],
                    'role': user.get('role', 'student')
                }
            else:
                user_response = user.to_dict()
            
            # Return user directly (not wrapped in success/message)
            return jsonify(user_response), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get user: {str(e)}'
            }), 500
    
    @auth_bp.route('/logout', methods=['POST'])
    @oauth_service.token_required
    def logout(current_user_id, current_user_email, current_user_role):
        """Logout user (client should remove token)"""
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200

