from flask import Blueprint, request, jsonify

# Support both absolute and relative imports
try:
    from models import NotificationModel, UserModel, FCMTokenModel
    from database import db
except ImportError:
    from ..models import NotificationModel, UserModel, FCMTokenModel
    from ..database import db

try:
    from oauth2_service import OAuth2Service
    from firebase_service import FirebaseService
except ImportError:
    from ..oauth2_service import OAuth2Service
    from ..firebase_service import FirebaseService

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

def init_notification_routes(oauth_service, firebase_service):
    """Initialize notification routes with services"""
    
    @notifications_bp.route('/register-token', methods=['POST'])
    @oauth_service.token_required
    def register_fcm_token(current_user_id, current_user_email, current_user_role):
        """Register FCM token for push notifications"""
        try:
            data = request.get_json()
            
            if not data or not data.get('fcm_token'):
                return jsonify({
                    'success': False,
                    'message': 'FCM token is required'
                }), 400
            
            fcm_token = data['fcm_token']
            device_info = data.get('device_info', {})
            
            # Create or update FCM token
            FCMTokenModel.create(
                user_id=current_user_id,
                fcm_token=fcm_token,
                device_info=device_info
            )
            
            return jsonify({
                'success': True,
                'message': 'FCM token registered successfully'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to register token: {str(e)}'
            }), 500
    
    @notifications_bp.route('/unregister-token', methods=['POST'])
    @oauth_service.token_required
    def unregister_fcm_token(current_user_id, current_user_email, current_user_role):
        """Unregister FCM token"""
        try:
            data = request.get_json()
            
            if not data or not data.get('fcm_token'):
                return jsonify({
                    'success': False,
                    'message': 'FCM token is required'
                }), 400
            
            fcm_token = data['fcm_token']
            
            # Remove FCM token
            FCMTokenModel.remove_token(current_user_id, fcm_token)
            
            return jsonify({
                'success': True,
                'message': 'FCM token unregistered successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to unregister token: {str(e)}'
            }), 500
    
    @notifications_bp.route('/', methods=['GET'])
    @oauth_service.token_required
    def get_notifications(current_user_id, current_user_email, current_user_role):
        """Get user notifications"""
        try:
            unread_only = request.args.get('unread_only', 'false').lower() == 'true'
            
            notifications = NotificationModel.get_user_notifications(current_user_id, unread_only)
            
            return jsonify({
                'success': True,
                'notifications': notifications,
                'count': len(notifications)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get notifications: {str(e)}'
            }), 500
    
    @notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
    @oauth_service.token_required
    def mark_notification_read(current_user_id, current_user_email, current_user_role, notification_id):
        """Mark notification as read"""
        try:
            # Find notification
            notification = NotificationModel.query.filter_by(
                id=notification_id,
                user_id=current_user_id
            ).first()
            
            if not notification:
                return jsonify({
                    'success': False,
                    'message': 'Notification not found'
                }), 404
            
            # Mark as read
            notification.read = True
            notification.save()
            
            return jsonify({
                'success': True,
                'message': 'Notification marked as read'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to mark notification as read: {str(e)}'
            }), 500
    
    @notifications_bp.route('/send', methods=['POST'])
    @oauth_service.token_required
    def send_notification(current_user_id, current_user_email, current_user_role):
        """Send notification (admin only)"""
        try:
            # Check if user is admin (in production, use proper role checking)
            if current_user_role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Unauthorized: Admin access required'
                }), 403
            
            data = request.get_json()
            
            if not data or not data.get('user_id') or not data.get('title') or not data.get('body'):
                return jsonify({
                    'success': False,
                    'message': 'user_id, title, and body are required'
                }), 400
            
            # Create notification
            notification = NotificationModel.create({
                'user_id': data['user_id'],
                'title': data['title'],
                'body': data['body'],
                'type': data.get('type', 'info'),
                'data': data.get('data', {})
            })
            
            # Send push notification if FCM token exists
            user_tokens = FCMTokenModel.get_user_tokens(data['user_id'])
            
            if user_tokens and firebase_service.initialized:
                fcm_tokens = [token.fcm_token for token in user_tokens]
                firebase_service.send_multicast_notification(
                    fcm_tokens,
                    notification.title,
                    notification.body,
                    {'notification_id': str(notification.id), **notification.data}
                )
            
            return jsonify({
                'success': True,
                'message': 'Notification sent successfully',
                'notification': notification.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to send notification: {str(e)}'
            }), 500

