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
            
            # Validate required fields based on role
            requested_role = data.get('role', 'student')
            is_institutional = requested_role in ['employer', 'poslodavac', 'faculty', 'fakultet']
            
            # Check basic required fields
            if not data.get('email') or not data.get('password'):
                return jsonify({
                    'success': False,
                    'message': 'Email and password are required'
                }), 400
            
            # For institutional roles, require username; for others, require firstName/lastName
            if is_institutional:
                if not data.get('username'):
                    return jsonify({
                        'success': False,
                        'message': 'Korisničko ime je obavezno'
                    }), 400
            else:
                if not data.get('firstName') or not data.get('lastName'):
                    return jsonify({
                        'success': False,
                        'message': 'Ime i prezime su obavezni'
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
            
            # Validate role-specific requirements
            email = data['email']
            
            # If registering as faculty, email must be from faculty domain
            if requested_role in ['faculty', 'fakultet']:
                if not is_faculty_email(email):
                    return jsonify({
                        'success': False,
                        'message': 'Fakulteti se moraju registrirati s email adresom s fakultetske domene'
                    }), 400
            
            # If email is from faculty domain but role is not faculty, suggest faculty role
            if is_faculty_email(email) and requested_role not in ['faculty', 'fakultet']:
                return jsonify({
                    'success': False,
                    'message': 'Email adresa s fakultetske domene zahtijeva registraciju kao fakultet. Fakulteti se prijavljuju preko AAI@EduHr sustava.'
                }), 400
            
            # Create new user
            user_data = {
                'email': data['email'],
                'password': data['password'],
                'role': requested_role,
                'provider': 'local'
            }
            
            if is_institutional:
                user_data['username'] = data['username']
            else:
                user_data['firstName'] = data['firstName']
                user_data['lastName'] = data['lastName']
                if 'faculty' in data:
                    user_data['faculty'] = data['faculty']
                if 'interests' in data:
                    user_data['interests'] = data['interests']
            
            new_user = User.create(user_data)
            
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
            
            # Check if this is admin login
            ADMIN_EMAIL = 'ivan.gabrilo@gmail.com'
            ADMIN_PASSWORD = 'ivan55'
            
            if email == ADMIN_EMAIL:
                # Admin login - check password
                if not data.get('password'):
                    return jsonify({
                        'success': False,
                        'message': 'Password is required'
                    }), 400
                
                if data['password'] != ADMIN_PASSWORD:
                    return jsonify({
                        'success': False,
                        'message': 'Invalid email or password'
                    }), 401
                
                # Find or create admin user
                admin_user = User.find_by_email(ADMIN_EMAIL)
                if not admin_user:
                    # Create admin user if doesn't exist
                    admin_user = User.create({
                        'email': ADMIN_EMAIL,
                        'password': ADMIN_PASSWORD,
                        'firstName': 'Admin',
                        'lastName': 'User',
                        'role': 'admin',
                        'provider': 'local'
                    })
                
                # Ensure user has admin role and get user data
                if isinstance(admin_user, dict):
                    admin_user['role'] = 'admin'
                    user_id = admin_user['id']
                    user_response = {
                        'id': admin_user['id'],
                        'email': admin_user['email'],
                        'firstName': admin_user.get('firstName', 'Admin'),
                        'lastName': admin_user.get('lastName', 'User'),
                        'role': 'admin'
                    }
                else:
                    admin_user.role = 'admin'
                    user_id = admin_user.id
                    user_response = admin_user.to_dict()
                
                # Generate token
                token = oauth_service.generate_token(
                    user_id,
                    ADMIN_EMAIL,
                    'admin'
                )
                
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'user': user_response,
                    'token': token
                }), 200
            
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

