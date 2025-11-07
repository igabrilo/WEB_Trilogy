"""
SQLAlchemy data models for the application
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY

# Import db instance from database.py
try:
    from .database import db
except ImportError:
    from database import db

# Legacy in-memory storage (will be removed after migration)
users_db = []
user_id_counter = 1

notifications_db = []
notification_id_counter = 1

fcm_tokens_db = []  # Store FCM tokens: {user_id: int, fcm_token: str, device_info: dict}

class User:
    """User model"""
    
    def __init__(self, email, password, firstName=None, lastName=None, username=None, role='student', provider='local', provider_id=None):
        global user_id_counter
        self.id = user_id_counter
        user_id_counter += 1
        self.email = email
        self.password = generate_password_hash(password) if password else None
        # For institutional roles (employer, faculty), use username; otherwise use firstName/lastName
        if username:
            self.username = username
            self.firstName = username  # Store username in firstName for compatibility
            self.lastName = ''  # Empty lastName for institutional roles
        else:
            self.firstName = firstName or ''
            self.lastName = lastName or ''
            self.username = None
        self.role = role
        self.provider = provider  # 'local', 'google', etc.
        self.provider_id = provider_id
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.is_active = True
    
    def to_dict(self):
        """Convert user to dictionary (without password)"""
        result = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'provider': self.provider,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        # For institutional roles, return username; otherwise firstName/lastName
        if hasattr(self, 'username') and self.username:
            result['username'] = self.username
            result['firstName'] = self.username  # For compatibility
            result['lastName'] = ''
        else:
            result['firstName'] = self.firstName
            result['lastName'] = self.lastName
        return result
    
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
        # Check if username is provided (for institutional roles)
        username = user_data.get('username')
        if username:
            user = User(
                email=user_data['email'],
                password=user_data.get('password'),
                username=username,
                role=user_data.get('role', 'student'),
                provider=user_data.get('provider', 'local'),
                provider_id=user_data.get('provider_id')
            )
        else:
            user = User(
                email=user_data['email'],
                password=user_data.get('password'),
                firstName=user_data.get('firstName', ''),
                lastName=user_data.get('lastName', ''),
                role=user_data.get('role', 'student'),
                provider=user_data.get('provider', 'local'),
                provider_id=user_data.get('provider_id')
            )
        users_db.append(user)
        return user

# =============================================
# SQLAlchemy Models (New Database Implementation)
# =============================================

class UserModel(db.Model):
    """SQLAlchemy User model for database storage"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), nullable=True)  # For institutional roles
    role = db.Column(db.String(50), nullable=False, default='student', index=True)
    faculty = db.Column(db.String(100), nullable=True)
    interests = db.Column(db.JSON, nullable=True)  # Store as JSON array
    provider = db.Column(db.String(50), nullable=False, default='local')
    provider_id = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    notifications = db.relationship('NotificationModel', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    fcm_tokens = db.relationship('FCMTokenModel', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    created_jobs = db.relationship('JobModel', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    job_applications = db.relationship('JobApplicationModel', lazy='dynamic', cascade='all, delete-orphan')
    created_associations = db.relationship('AssociationModel', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    chat_sessions = db.relationship('ChatSessionModel', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, email, password=None, first_name=None, last_name=None, username=None, 
                 role='student', faculty=None, interests=None, provider='local', provider_id=None):
        self.email = email
        self.password_hash = generate_password_hash(password) if password else None
        
        # Handle institutional vs personal roles
        if username:
            self.username = username
            self.first_name = username  # For compatibility
            self.last_name = ''
        else:
            self.first_name = first_name or ''
            self.last_name = last_name or ''
            self.username = None
            
        self.role = role
        self.faculty = faculty
        self.interests = interests or []
        self.provider = provider
        self.provider_id = provider_id
    
    def to_dict(self):
        """Convert user to dictionary (without password)"""
        result = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'provider': self.provider,
            'faculty': self.faculty,
            'interests': self.interests or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Handle institutional vs personal roles
        if self.username:
            result['username'] = self.username
            result['firstName'] = self.username  # For compatibility
            result['lastName'] = ''
        else:
            result['firstName'] = self.first_name
            result['lastName'] = self.last_name
            
        return result
    
    def check_password(self, password):
        """Check if password matches"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Set user password"""
        self.password_hash = generate_password_hash(password)
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID"""
        return cls.query.get(user_id)
    
    @classmethod
    def find_by_provider(cls, provider, provider_id):
        """Find user by OAuth provider"""
        return cls.query.filter_by(provider=provider, provider_id=provider_id).first()
    
    @classmethod
    def create(cls, user_data):
        """Create new user"""
        user = cls(
            email=user_data['email'],
            password=user_data.get('password'),
            first_name=user_data.get('firstName'),
            last_name=user_data.get('lastName'),
            username=user_data.get('username'),
            role=user_data.get('role', 'student'),
            faculty=user_data.get('faculty'),
            interests=user_data.get('interests'),
            provider=user_data.get('provider', 'local'),
            provider_id=user_data.get('provider_id')
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def save(self):
        """Save user to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete user from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.email}>'

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

class NotificationModel(db.Model):
    """SQLAlchemy Notification model"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False, default='info')  # info, success, warning, error
    data = db.Column(db.JSON, nullable=True)
    read = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, user_id, title, body, type='info', data=None, read=False):
        self.user_id = user_id
        self.title = title
        self.body = body
        self.type = type
        self.data = data or {}
        self.read = read
    
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
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def create(cls, notification_data):
        """Create new notification"""
        notification = cls(
            user_id=notification_data['user_id'],
            title=notification_data['title'],
            body=notification_data['body'],
            type=notification_data.get('type', 'info'),
            data=notification_data.get('data'),
            read=notification_data.get('read', False)
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @classmethod
    def get_user_notifications(cls, user_id, unread_only=False):
        """Get notifications for a user"""
        query = cls.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(read=False)
        
        notifications = query.order_by(cls.created_at.desc()).all()
        return [n.to_dict() for n in notifications]
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.read = True
        db.session.commit()
    
    def save(self):
        """Save notification to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete notification from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<Notification {self.id}: {self.title}>'

class FCMTokenModel(db.Model):
    """SQLAlchemy FCM Token model for push notifications"""
    __tablename__ = 'fcm_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    fcm_token = db.Column(db.String(500), nullable=False)
    device_info = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Unique constraint for user_id + fcm_token combination
    __table_args__ = (db.UniqueConstraint('user_id', 'fcm_token', name='unique_user_token'),)
    
    def __init__(self, user_id, fcm_token, device_info=None):
        self.user_id = user_id
        self.fcm_token = fcm_token
        self.device_info = device_info or {}
    
    def to_dict(self):
        """Convert FCM token to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'fcm_token': self.fcm_token,
            'device_info': self.device_info,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def create(cls, user_id, fcm_token, device_info=None):
        """Create or update FCM token"""
        existing = cls.query.filter_by(user_id=user_id, fcm_token=fcm_token).first()
        if existing:
            existing.device_info = device_info or {}
            db.session.commit()
            return existing
        
        token = cls(user_id=user_id, fcm_token=fcm_token, device_info=device_info)
        db.session.add(token)
        db.session.commit()
        return token
    
    @classmethod
    def get_user_tokens(cls, user_id):
        """Get all FCM tokens for a user"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def remove_token(cls, user_id, fcm_token):
        """Remove FCM token"""
        token = cls.query.filter_by(user_id=user_id, fcm_token=fcm_token).first()
        if token:
            db.session.delete(token)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f'<FCMToken {self.id}: User {self.user_id}>'

class FacultyModel(db.Model):
    """SQLAlchemy Faculty model"""
    __tablename__ = 'faculties'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    abbreviation = db.Column(db.String(20), nullable=True)
    type = db.Column(db.String(50), nullable=False)  # 'faculty' or 'academy'
    contacts = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # Note: associations are linked via faculty field (string), not foreign key
    
    def __init__(self, slug, name, type, abbreviation=None, contacts=None):
        self.slug = slug
        self.name = name
        self.abbreviation = abbreviation
        self.type = type
        self.contacts = contacts or {}
    
    def to_dict(self):
        """Convert faculty to dictionary"""
        return {
            'slug': self.slug,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'type': self.type,
            'contacts': self.contacts,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create(cls, faculty_data):
        """Create new faculty"""
        faculty = cls(
            slug=faculty_data['slug'],
            name=faculty_data['name'],
            type=faculty_data['type'],
            abbreviation=faculty_data.get('abbreviation'),
            contacts=faculty_data.get('contacts')
        )
        db.session.add(faculty)
        db.session.commit()
        return faculty
    
    def save(self):
        """Save faculty to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete faculty from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<Faculty {self.name}>'

class AssociationModel(db.Model):
    """SQLAlchemy Association model"""
    __tablename__ = 'associations'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(100), nullable=True, index=True)
    type = db.Column(db.String(50), nullable=True)
    logo_text = db.Column(db.String(10), nullable=True)
    logo_bg = db.Column(db.String(20), nullable=True)
    short_description = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.JSON, nullable=True)  # Array of strings
    links = db.Column(db.JSON, nullable=True)  # Object with link types
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, slug, name, faculty=None, type=None, logo_text=None, logo_bg=None,
                 short_description=None, description=None, tags=None, links=None, created_by=None):
        self.slug = slug
        self.name = name
        self.faculty = faculty
        self.type = type
        self.logo_text = logo_text
        self.logo_bg = logo_bg
        self.short_description = short_description
        self.description = description
        self.tags = tags or []
        self.links = links or {}
        self.created_by = created_by
    
    def to_dict(self):
        """Convert association to dictionary"""
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'faculty': self.faculty,
            'type': self.type,
            'logoText': self.logo_text,
            'logoBg': self.logo_bg,
            'shortDescription': self.short_description,
            'description': self.description,
            'tags': self.tags or [],
            'links': self.links or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create(cls, association_data):
        """Create new association"""
        association = cls(
            slug=association_data['slug'],
            name=association_data['name'],
            faculty=association_data.get('faculty'),
            type=association_data.get('type'),
            logo_text=association_data.get('logoText'),
            logo_bg=association_data.get('logoBg'),
            short_description=association_data.get('shortDescription'),
            description=association_data.get('description'),
            tags=association_data.get('tags'),
            links=association_data.get('links'),
            created_by=association_data.get('created_by')
        )
        db.session.add(association)
        db.session.commit()
        return association
    
    def save(self):
        """Save association to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete association from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<Association {self.name}>'

class JobModel(db.Model):
    """SQLAlchemy Job model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False, index=True)  # internship, job, part-time, remote
    company = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    salary = db.Column(db.String(100), nullable=True)
    requirements = db.Column(db.JSON, nullable=True)  # Array of strings
    tags = db.Column(db.JSON, nullable=True)  # Array of strings
    status = db.Column(db.String(50), nullable=False, default='active', index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('JobApplicationModel', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, title, description, type, created_by, company=None, location=None,
                 salary=None, requirements=None, tags=None, status='active'):
        self.title = title
        self.description = description
        self.type = type
        self.company = company
        self.location = location
        self.salary = salary
        self.requirements = requirements or []
        self.tags = tags or []
        self.status = status
        self.created_by = created_by
    
    def to_dict(self):
        """Convert job to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'company': self.company,
            'location': self.location,
            'salary': self.salary,
            'requirements': self.requirements or [],
            'tags': self.tags or [],
            'status': self.status,
            'createdBy': self.created_by,
            'applicationCount': self.applications.count(),
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create(cls, job_data):
        """Create new job"""
        job = cls(
            title=job_data['title'],
            description=job_data['description'],
            type=job_data['type'],
            created_by=job_data['created_by'],
            company=job_data.get('company'),
            location=job_data.get('location'),
            salary=job_data.get('salary'),
            requirements=job_data.get('requirements'),
            tags=job_data.get('tags'),
            status=job_data.get('status', 'active')
        )
        db.session.add(job)
        db.session.commit()
        return job
    
    def save(self):
        """Save job to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete job from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<Job {self.title}>'

class JobApplicationModel(db.Model):
    """SQLAlchemy Job Application model"""
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending', index=True)  # pending, approved, rejected
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint for job_id + user_id combination
    __table_args__ = (db.UniqueConstraint('job_id', 'user_id', name='unique_job_application'),)
    
    # Relationships
    applicant = db.relationship('UserModel', foreign_keys=[user_id], overlaps="job_applications")
    job = db.relationship('JobModel', foreign_keys=[job_id], overlaps="applications")
    
    def __init__(self, job_id, user_id, message=None, status='pending'):
        self.job_id = job_id
        self.user_id = user_id
        self.message = message
        self.status = status
    
    def to_dict(self, include_user=False, include_job=False):
        """Convert job application to dictionary"""
        result = {
            'id': self.id,
            'jobId': self.job_id,
            'userId': self.user_id,
            'userEmail': self.applicant.email if self.applicant else None,
            'message': self.message,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_user and self.applicant:
            result['user'] = self.applicant.to_dict()
        
        if include_job and self.job:
            result['job'] = {
                'id': self.job.id,
                'title': self.job.title,
                'type': self.job.type
            }
        
        return result
    
    @classmethod
    def create(cls, application_data):
        """Create new job application"""
        application = cls(
            job_id=application_data['job_id'],
            user_id=application_data['user_id'],
            message=application_data.get('message'),
            status=application_data.get('status', 'pending')
        )
        db.session.add(application)
        db.session.commit()
        return application
    
    def update_status(self, status):
        """Update application status"""
        self.status = status
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def save(self):
        """Save job application to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete job application from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<JobApplication {self.id}: Job {self.job_id}, User {self.user_id}>'

class ChatSessionModel(db.Model):
    """SQLAlchemy Chat Session model"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.String(100), primary_key=True)  # UUID string
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    messages = db.Column(db.JSON, nullable=False, default=list)  # Array of message objects
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, id, user_id, messages=None):
        self.id = id
        self.user_id = user_id
        self.messages = messages or []
    
    def add_message(self, role, message):
        """Add message to session"""
        if not self.messages:
            self.messages = []
        
        self.messages.append({
            'role': role,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        })
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert chat session to dictionary"""
        return {
            'session_id': self.id,
            'user_id': self.user_id,
            'messages': self.messages or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create(cls, session_id, user_id):
        """Create new chat session"""
        session = cls(id=session_id, user_id=user_id)
        db.session.add(session)
        db.session.commit()
        return session
    
    def save(self):
        """Save chat session to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete chat session from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<ChatSession {self.id}: User {self.user_id}>'

class ErasmusProjectModel(db.Model):
    """SQLAlchemy Erasmus Project model"""
    __tablename__ = 'erasmus_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    faculty_slug = db.Column(db.String(100), db.ForeignKey('faculties.slug'), nullable=False, index=True)
    country = db.Column(db.String(100), nullable=True)
    university = db.Column(db.String(255), nullable=True)
    field_of_study = db.Column(db.String(255), nullable=True)  # Područje studija
    duration = db.Column(db.String(100), nullable=True)  # Trajanje (npr. "1 semestar", "1 godina")
    application_deadline = db.Column(db.Date, nullable=True)
    requirements = db.Column(db.JSON, nullable=True)  # Array of strings
    benefits = db.Column(db.JSON, nullable=True)  # Array of strings
    contact_email = db.Column(db.String(255), nullable=True)
    contact_phone = db.Column(db.String(50), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active', index=True)  # active, archived
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    faculty = db.relationship('FacultyModel', foreign_keys=[faculty_slug])
    creator = db.relationship('UserModel', foreign_keys=[created_by])
    
    def __init__(self, title, description, faculty_slug, created_by, country=None, university=None,
                 field_of_study=None, duration=None, application_deadline=None, requirements=None,
                 benefits=None, contact_email=None, contact_phone=None, website=None, status='active'):
        self.title = title
        self.description = description
        self.faculty_slug = faculty_slug
        self.created_by = created_by
        self.country = country
        self.university = university
        self.field_of_study = field_of_study
        self.duration = duration
        self.application_deadline = application_deadline
        self.requirements = requirements or []
        self.benefits = benefits or []
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.website = website
        self.status = status
    
    def to_dict(self):
        """Convert Erasmus project to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'facultySlug': self.faculty_slug,
            'facultyName': self.faculty.name if self.faculty else None,
            'country': self.country,
            'university': self.university,
            'fieldOfStudy': self.field_of_study,
            'duration': self.duration,
            'applicationDeadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'requirements': self.requirements or [],
            'benefits': self.benefits or [],
            'contactEmail': self.contact_email,
            'contactPhone': self.contact_phone,
            'website': self.website,
            'status': self.status,
            'createdBy': self.created_by,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create(cls, project_data):
        """Create new Erasmus project"""
        project = cls(
            title=project_data['title'],
            description=project_data['description'],
            faculty_slug=project_data['facultySlug'],
            created_by=project_data['created_by'],
            country=project_data.get('country'),
            university=project_data.get('university'),
            field_of_study=project_data.get('fieldOfStudy'),
            duration=project_data.get('duration'),
            application_deadline=project_data.get('applicationDeadline'),
            requirements=project_data.get('requirements'),
            benefits=project_data.get('benefits'),
            contact_email=project_data.get('contactEmail'),
            contact_phone=project_data.get('contactPhone'),
            website=project_data.get('website'),
            status=project_data.get('status', 'active')
        )
        db.session.add(project)
        db.session.commit()
        return project
    
    def save(self):
        """Save Erasmus project to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete Erasmus project from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<ErasmusProject {self.title}>'

class FavoriteFacultyModel(db.Model):
    """SQLAlchemy Favorite Faculty model (many-to-many relationship)"""
    __tablename__ = 'favorite_faculties'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    faculty_slug = db.Column(db.String(100), db.ForeignKey('faculties.slug'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Unique constraint: user can only favorite a faculty once
    __table_args__ = (db.UniqueConstraint('user_id', 'faculty_slug', name='unique_user_faculty_favorite'),)
    
    # Relationships
    user = db.relationship('UserModel', foreign_keys=[user_id])
    faculty = db.relationship('FacultyModel', foreign_keys=[faculty_slug])
    
    def __init__(self, user_id, faculty_slug):
        self.user_id = user_id
        self.faculty_slug = faculty_slug
    
    def to_dict(self):
        """Convert favorite to dictionary"""
        return {
            'id': self.id,
            'userId': self.user_id,
            'facultySlug': self.faculty_slug,
            'facultyName': self.faculty.name if self.faculty else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def create(cls, user_id, faculty_slug):
        """Create new favorite"""
        favorite = cls(user_id=user_id, faculty_slug=faculty_slug)
        db.session.add(favorite)
        db.session.commit()
        return favorite
    
    def delete(self):
        """Delete favorite from database"""
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<FavoriteFaculty User {self.user_id} -> Faculty {self.faculty_slug}>'

