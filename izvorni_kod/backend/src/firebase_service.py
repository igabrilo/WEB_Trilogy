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
            creds_path = app.config.get('FIREBASE_CREDENTIALS_PATH', '')
            project_id = app.config.get('FIREBASE_PROJECT_ID', '')
            creds_json_env = os.environ.get('FIREBASE_CREDENTIALS_JSON', '')
            
            # Method 1: Use credentials file path
            if creds_path:
                if os.path.exists(creds_path):
                    try:
                        cred = credentials.Certificate(creds_path)
                        init_options = {}
                        if project_id:
                            init_options['projectId'] = project_id
                        firebase_admin.initialize_app(cred, init_options)
                        self.initialized = True
                        print(f"✅ Firebase initialized successfully from file: {creds_path}")
                        if project_id:
                            print(f"   Project ID: {project_id}")
                        else:
                            # Try to get project ID from credentials
                            try:
                                with open(creds_path, 'r') as f:
                                    creds_data = json.load(f)
                                    actual_project_id = creds_data.get('project_id')
                                    if actual_project_id:
                                        print(f"   Project ID: {actual_project_id}")
                            except:
                                pass
                    except Exception as e:
                        error_msg = str(e)
                        # Suppress importlib.metadata warnings for Python 3.9 compatibility
                        if 'importlib.metadata' not in error_msg and 'packages_distributions' not in error_msg:
                            print(f"❌ Firebase initialization error: {error_msg}")
                        self.initialized = False
                else:
                    print(f"⚠️  Firebase credentials file not found: {creds_path}")
                    self.initialized = False
            # Method 2: Use JSON string from environment
            elif creds_json_env:
                try:
                    creds_json = json.loads(creds_json_env)
                    cred = credentials.Certificate(creds_json)
                    init_options = {}
                    if project_id:
                        init_options['projectId'] = project_id
                    elif creds_json.get('project_id'):
                        init_options['projectId'] = creds_json.get('project_id')
                    firebase_admin.initialize_app(cred, init_options)
                    self.initialized = True
                    print("✅ Firebase initialized successfully from environment variable")
                    if project_id:
                        print(f"   Project ID: {project_id}")
                    elif creds_json.get('project_id'):
                        print(f"   Project ID: {creds_json.get('project_id')}")
                except json.JSONDecodeError as e:
                    print(f"❌ Firebase credentials JSON is invalid: {str(e)}")
                    self.initialized = False
                except Exception as e:
                    error_msg = str(e)
                    # Suppress importlib.metadata warnings for Python 3.9 compatibility
                    if 'importlib.metadata' not in error_msg and 'packages_distributions' not in error_msg:
                        print(f"❌ Firebase initialization error: {error_msg}")
                    self.initialized = False
            else:
                print("⚠️  Firebase credentials not found. Notifications will be disabled.")
                print("   Set either FIREBASE_CREDENTIALS_PATH or FIREBASE_CREDENTIALS_JSON in .env")
                self.initialized = False
        else:
            # Firebase already initialized
            self.initialized = True
            print("✅ Firebase already initialized")
    
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

