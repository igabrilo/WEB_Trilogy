from flask import Blueprint, request, jsonify, session

# Support both absolute and relative imports
try:
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
    from chatbot_service import ChatbotService
    from models import User
except ImportError:
    from ..oauth2_service import OAuth2Service
    from ..firebase_service import FirebaseService
    from ..chatbot_service import ChatbotService
    from ..models import User
import uuid
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Store conversation sessions (in production, use database)
conversation_sessions = {}

def init_chatbot_routes(oauth_service, firebase_service, chatbot_service):
    """Initialize chatbot routes with services"""
    
    @chatbot_bp.route('/send', methods=['POST'])
    @oauth_service.optional_token
    def send_message(current_user_id=None, current_user_email=None, current_user_role=None, is_authenticated=False):
        """Send a message to the chatbot (works with or without authentication)"""
        try:
            data = request.get_json()
            
            if not data or not data.get('message'):
                return jsonify({
                    'success': False,
                    'message': 'Message is required'
                }), 400
            
            message = data['message']
            provider_name = data.get('provider', 'smotra')  # Default to smotra
            session_id = data.get('session_id') or session.get('chatbot_session_id')
            
            # Create new session if needed
            if not session_id:
                session_id = str(uuid.uuid4())
                session['chatbot_session_id'] = session_id
                conversation_sessions[session_id] = {
                    'user_id': current_user_id,  # Can be None for anonymous users
                    'created_at': datetime.now().isoformat(),
                    'messages': []
                }
            
            # Get context from session (include user data if authenticated)
            context = {
                'session_id': session_id
            }
            if is_authenticated and current_user_id:
                context['user_id'] = current_user_id
                context['user_email'] = current_user_email
                context['user_role'] = current_user_role
            
            # Send message to chatbot
            response = chatbot_service.send_message(
                message=message,
                provider_name=provider_name,
                context=context,
                session_id=session_id
            )
            
            # Store conversation in session
            if session_id in conversation_sessions:
                conversation_sessions[session_id]['messages'].append({
                    'role': 'user',
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                })
                
                if response.get('success'):
                    bot_response = response.get('response', {}).get('message', '') or \
                                 response.get('response', {}).get('response', '')
                    conversation_sessions[session_id]['messages'].append({
                        'role': 'assistant',
                        'message': bot_response,
                        'timestamp': datetime.now().isoformat()
                    })
            
            return jsonify({
                'success': response.get('success', False),
                'message': response.get('response', {}).get('message') or 
                          response.get('response', {}).get('response') or 
                          response.get('error', 'Unknown error'),
                'session_id': session_id,
                'provider': response.get('provider', provider_name),
                'error': response.get('error') if not response.get('success') else None
            }), 200 if response.get('success') else 500
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to send message: {str(e)}'
            }), 500
    
    @chatbot_bp.route('/providers', methods=['GET'])
    @oauth_service.optional_token
    def get_providers(current_user_id=None, current_user_email=None, current_user_role=None, is_authenticated=False):
        """Get list of available chatbot providers (works with or without authentication)"""
        try:
            providers = chatbot_service.get_available_providers()
            
            return jsonify({
                'success': True,
                'providers': providers,
                'count': len(providers)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get providers: {str(e)}'
            }), 500
    
    @chatbot_bp.route('/history', methods=['GET'])
    @oauth_service.optional_token
    def get_conversation_history(current_user_id=None, current_user_email=None, current_user_role=None, is_authenticated=False):
        """Get conversation history for current session (works with or without authentication)"""
        try:
            session_id = request.args.get('session_id') or session.get('chatbot_session_id')
            
            if not session_id:
                return jsonify({
                    'success': True,
                    'messages': [],
                    'message': 'No active session'
                }), 200
            
            # Get conversation from session storage
            if session_id in conversation_sessions:
                conversation = conversation_sessions[session_id]
                
                # Verify session belongs to user (if authenticated)
                # Anonymous sessions can be accessed by anyone with the session_id
                if is_authenticated and current_user_id:
                    if conversation['user_id'] and conversation['user_id'] != current_user_id:
                        return jsonify({
                            'success': False,
                            'message': 'Unauthorized: Session does not belong to user'
                        }), 403
                
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'messages': conversation['messages'],
                    'created_at': conversation['created_at']
                }), 200
            else:
                return jsonify({
                    'success': True,
                    'messages': [],
                    'message': 'Session not found'
                }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get history: {str(e)}'
            }), 500
    
    @chatbot_bp.route('/session', methods=['POST'])
    @oauth_service.optional_token
    def create_session(current_user_id=None, current_user_email=None, current_user_role=None, is_authenticated=False):
        """Create a new chatbot conversation session (works with or without authentication)"""
        try:
            session_id = str(uuid.uuid4())
            session['chatbot_session_id'] = session_id
            
            conversation_sessions[session_id] = {
                'user_id': current_user_id if is_authenticated else None,
                'created_at': datetime.now().isoformat(),
                'messages': []
            }
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'message': 'Session created successfully'
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to create session: {str(e)}'
            }), 500
    
    @chatbot_bp.route('/session/<session_id>', methods=['DELETE'])
    @oauth_service.token_required
    def delete_session(current_user_id, current_user_email, current_user_role, session_id):
        """Delete a conversation session"""
        try:
            if session_id in conversation_sessions:
                conversation = conversation_sessions[session_id]
                
                # Verify session belongs to user
                if conversation['user_id'] != current_user_id:
                    return jsonify({
                        'success': False,
                        'message': 'Unauthorized: Session does not belong to user'
                    }), 403
                
                del conversation_sessions[session_id]
                
                if session.get('chatbot_session_id') == session_id:
                    session.pop('chatbot_session_id', None)
                
                return jsonify({
                    'success': True,
                    'message': 'Session deleted successfully'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Session not found'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to delete session: {str(e)}'
            }), 500
    
    @chatbot_bp.route('/career-office/query', methods=['POST'])
    @oauth_service.token_required
    def query_career_office(current_user_id, current_user_email, current_user_role):
        """Query Career Development Office chatbot specifically"""
        try:
            data = request.get_json()
            
            if not data or not data.get('message'):
                return jsonify({
                    'success': False,
                    'message': 'Message is required'
                }), 400
            
            message = data['message']
            session_id = data.get('session_id') or session.get('chatbot_session_id')
            
            # Create context for career office
            context = {
                'user_id': current_user_id,
                'user_email': current_user_email,
                'user_role': current_user_role,
                'source': 'career_hub',
                'session_id': session_id
            }
            
            # Send to career office chatbot
            response = chatbot_service.send_message(
                message=message,
                provider_name='career_office',
                context=context,
                session_id=session_id
            )
            
            return jsonify({
                'success': response.get('success', False),
                'message': response.get('response', {}).get('message') or 
                          response.get('response', {}).get('response') or 
                          response.get('error', 'Unknown error'),
                'provider': 'career_development_office',
                'error': response.get('error') if not response.get('success') else None
            }), 200 if response.get('success') else 500
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to query career office: {str(e)}'
            }), 500

