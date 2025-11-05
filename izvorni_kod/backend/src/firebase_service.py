import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

class FirebaseService:
    """Firebase Cloud Messaging Service for Push Notifications"""
    
    def __init__(self, app=None):
        self.app = None
        self.initialized = False
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize Firebase Admin SDK"""
        self.app = app
        
        # Suppress importlib.metadata warnings
        import warnings
        warnings.filterwarnings('ignore', message='.*importlib.metadata.*packages_distributions.*')
        warnings.filterwarnings('ignore', category=FutureWarning, message='.*Python version.*past its end of life.*')
        
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            creds_path = app.config.get('FIREBASE_CREDENTIALS_PATH')
            project_id = app.config.get('FIREBASE_PROJECT_ID')
            
            if creds_path and os.path.exists(creds_path):
                try:
                    cred = credentials.Certificate(creds_path)
                    firebase_admin.initialize_app(cred, {
                        'projectId': project_id or None
                    })
                    self.initialized = True
                except Exception as e:
                    # Suppress importlib.metadata warnings for Python 3.9 compatibility
                    if 'importlib.metadata' not in str(e) and 'packages_distributions' not in str(e):
                        print(f"Firebase initialization error: {str(e)}")
                    self.initialized = False
            elif os.environ.get('FIREBASE_CREDENTIALS_JSON'):
                # Alternative: use JSON string from environment
                try:
                    firebase_creds_json_str = os.environ.get('FIREBASE_CREDENTIALS_JSON')
                    if firebase_creds_json_str:
                        creds_json = json.loads(firebase_creds_json_str)
                        cred = credentials.Certificate(creds_json)
                        firebase_admin.initialize_app(cred, {
                            'projectId': project_id or creds_json.get('project_id')
                        })
                        self.initialized = True
                    else:
                        self.initialized = False
                except Exception as e:
                    # Suppress importlib.metadata warnings for Python 3.9 compatibility
                    if 'importlib.metadata' not in str(e) and 'packages_distributions' not in str(e):
                        print(f"Firebase initialization error: {str(e)}")
                    self.initialized = False
            else:
                print("Warning: Firebase credentials not found. Notifications will be disabled.")
                self.initialized = False
    
    def send_notification(self, fcm_token, title, body, data=None):
        """Send push notification to a single device"""
        if not self.initialized:
            return {'success': False, 'message': 'Firebase not initialized'}
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=fcm_token
            )
            
            response = messaging.send(message)
            return {
                'success': True,
                'message_id': response,
                'message': 'Notification sent successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to send notification: {str(e)}'
            }
    
    def send_multicast_notification(self, fcm_tokens, title, body, data=None):
        """Send push notification to multiple devices"""
        if not self.initialized:
            return {'success': False, 'message': 'Firebase not initialized'}
        
        if not fcm_tokens:
            return {'success': False, 'message': 'No FCM tokens provided'}
        
        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                tokens=fcm_tokens
            )
            
            response = messaging.send_multicast(message)
            return {
                'success': True,
                'success_count': response.success_count,
                'failure_count': response.failure_count,
                'responses': [
                    {
                        'success': resp.success,
                        'message_id': resp.message_id if resp.success else None,
                        'error': str(resp.exception) if resp.exception else None
                    }
                    for resp in response.responses
                ]
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to send multicast notification: {str(e)}'
            }
    
    def send_topic_notification(self, topic, title, body, data=None):
        """Send push notification to all devices subscribed to a topic"""
        if not self.initialized:
            return {'success': False, 'message': 'Firebase not initialized'}
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                topic=topic
            )
            
            response = messaging.send(message)
            return {
                'success': True,
                'message_id': response,
                'message': 'Topic notification sent successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to send topic notification: {str(e)}'
            }
    
    def subscribe_to_topic(self, fcm_tokens, topic):
        """Subscribe devices to a topic"""
        if not self.initialized:
            return {'success': False, 'message': 'Firebase not initialized'}
        
        try:
            response = messaging.subscribe_to_topic(fcm_tokens, topic)
            return {
                'success': True,
                'success_count': response.success_count,
                'failure_count': response.failure_count
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to subscribe to topic: {str(e)}'
            }
    
    def unsubscribe_from_topic(self, fcm_tokens, topic):
        """Unsubscribe devices from a topic"""
        if not self.initialized:
            return {'success': False, 'message': 'Firebase not initialized'}
        
        try:
            response = messaging.unsubscribe_from_topic(fcm_tokens, topic)
            return {
                'success': True,
                'success_count': response.success_count,
                'failure_count': response.failure_count
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to unsubscribe from topic: {str(e)}'
            }

