"""
Data models for the application
In production, these would be SQLAlchemy models connected to a database
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# In-memory storage (replace with database in production)
users_db = []
user_id_counter = 1

notifications_db = []
notification_id_counter = 1

fcm_tokens_db = []  # Store FCM tokens: {user_id: int, fcm_token: str, device_info: dict}

class User:
    """User model"""
    
    def __init__(self, email, password, firstName, lastName, role='student', provider='local', provider_id=None):
        global user_id_counter
        self.id = user_id_counter
        user_id_counter += 1
        self.email = email
        self.password = generate_password_hash(password) if password else None
        self.firstName = firstName
        self.lastName = lastName
        self.role = role
        self.provider = provider  # 'local', 'google', etc.
        self.provider_id = provider_id
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.is_active = True
    
    def to_dict(self):
        """Convert user to dictionary (without password)"""
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'role': self.role,
            'provider': self.provider,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def check_password(self, password):
        """Check if password matches"""
        if not self.password:
            return False
        return check_password_hash(self.password, password)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        for user in users_db:
            if isinstance(user, dict):
                if user.get('email') == email:
                    return user
            elif user.email == email:
                return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        for user in users_db:
            if isinstance(user, dict):
                if user.get('id') == user_id:
                    return user
            elif user.id == user_id:
                return user
        return None
    
    @staticmethod
    def find_by_provider(provider, provider_id):
        """Find user by OAuth provider"""
        for user in users_db:
            if isinstance(user, dict):
                # Legacy format - may not have provider fields
                if user.get('provider') == provider and user.get('provider_id') == provider_id:
                    return user
            elif hasattr(user, 'provider') and user.provider == provider and user.provider_id == provider_id:
                return user
        return None
    
    @staticmethod
    def create(user_data):
        """Create new user"""
        user = User(
            email=user_data['email'],
            password=user_data.get('password'),
            firstName=user_data['firstName'],
            lastName=user_data['lastName'],
            role=user_data.get('role', 'student'),
            provider=user_data.get('provider', 'local'),
            provider_id=user_data.get('provider_id')
        )
        users_db.append(user)
        return user

class Notification:
    """Notification model"""
    
    def __init__(self, user_id, title, body, type='info', data=None, read=False):
        global notification_id_counter
        self.id = notification_id_counter
        notification_id_counter += 1
        self.user_id = user_id
        self.title = title
        self.body = body
        self.type = type  # 'info', 'success', 'warning', 'error'
        self.data = data or {}
        self.read = read
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert notification to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'body': self.body,
            'type': self.type,
            'data': self.data,
            'read': self.read,
            'created_at': self.created_at
        }
    
    @staticmethod
    def create(notification_data):
        """Create new notification"""
        notification = Notification(
            user_id=notification_data['user_id'],
            title=notification_data['title'],
            body=notification_data['body'],
            type=notification_data.get('type', 'info'),
            data=notification_data.get('data'),
            read=notification_data.get('read', False)
        )
        notifications_db.append(notification)
        return notification
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        """Get notifications for a user"""
        notifications = []
        for n in notifications_db:
            if isinstance(n, dict):
                if n.get('user_id') == user_id:
                    notifications.append(n)
            elif hasattr(n, 'user_id') and n.user_id == user_id:
                notifications.append(n)
        
        if unread_only:
            filtered_notifications = []
            for n in notifications:
                if isinstance(n, dict):
                    if not n.get('read'):
                        filtered_notifications.append(n)
                elif hasattr(n, 'read') and not n.read:
                    filtered_notifications.append(n)
            notifications = filtered_notifications
        
        # Sort by created_at descending
        def get_created_at(n):
            """Get created_at value from notification, with fallback for sorting"""
            if isinstance(n, dict):
                return n.get('created_at', '')
            return getattr(n, 'created_at', '')
        
        notifications.sort(
            key=get_created_at,
            reverse=True
        )
        
        return [
            n.to_dict() if not isinstance(n, dict) and hasattr(n, 'to_dict') else n
            for n in notifications
        ]

