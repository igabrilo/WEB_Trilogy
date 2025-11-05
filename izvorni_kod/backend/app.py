from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Secret key for JWT (in production, use environment variable)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# In-memory database (replace with real database in production)
users_db = []
user_id_counter = 1

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = next((u for u in users_db if u['id'] == data['user_id']), None)
        except:
            return jsonify({'success': False, 'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/")
def home():
    return jsonify({"message": "Hello, Flask API!"})

@app.route("/api/auth/register", methods=['POST'])
def register():
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
        if any(user['email'] == data['email'] for user in users_db):
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
        global user_id_counter
        new_user = {
            'id': user_id_counter,
            'email': data['email'],
            'password': generate_password_hash(data['password']),
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'role': data.get('role', 'student'),
            'created_at': datetime.datetime.now().isoformat()
        }
        users_db.append(new_user)
        user_id_counter += 1
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': new_user['id'],
            'email': new_user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Return user data (without password)
        user_response = {
            'id': new_user['id'],
            'email': new_user['email'],
            'firstName': new_user['firstName'],
            'lastName': new_user['lastName'],
            'role': new_user['role']
        }
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user_response,
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@app.route("/api/auth/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user = next((u for u in users_db if u['email'] == data['email']), None)
        
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Return user data (without password)
        user_response = {
            'id': user['id'],
            'email': user['email'],
            'firstName': user['firstName'],
            'lastName': user['lastName'],
            'role': user['role']
        }
        
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

@app.route("/api/auth/me", methods=['GET'])
@token_required
def get_current_user(current_user):
    user_response = {
        'id': current_user['id'],
        'email': current_user['email'],
        'firstName': current_user['firstName'],
        'lastName': current_user['lastName'],
        'role': current_user['role']
    }
    return jsonify(user_response), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
