from flask import Blueprint, request, jsonify, current_app

# Support both absolute and relative imports
try:
    from models import FacultyInquiryModel, FacultyModel, UserModel
    from oauth2_service import OAuth2Service
    from email_service import EmailService
except ImportError:
    from ..models import FacultyInquiryModel, FacultyModel, UserModel
    from ..oauth2_service import OAuth2Service
    from ..email_service import EmailService

inquiries_bp = Blueprint('inquiries', __name__, url_prefix='/api/inquiries')

def get_db():
    """Get db instance from current app"""
    return current_app.extensions['sqlalchemy']

def init_inquiries_routes(oauth_service, email_service=None):
    """Initialize inquiries routes with services"""
    
    @inquiries_bp.route('/faculties', methods=['POST'])
    @oauth_service.optional_token
    def send_faculty_inquiry(current_user_id=None, current_user_email=None, current_user_role=None, is_authenticated=False):
        """Send an inquiry to a faculty (works with or without authentication)"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data or not data.get('facultySlug'):
                return jsonify({
                    'success': False,
                    'message': 'Faculty slug is required'
                }), 400
            
            if not data.get('senderName') or not data.get('senderEmail'):
                return jsonify({
                    'success': False,
                    'message': 'Sender name and email are required'
                }), 400
            
            if not data.get('subject') or not data.get('message'):
                return jsonify({
                    'success': False,
                    'message': 'Subject and message are required'
                }), 400
            
            faculty_slug = data['facultySlug']
            sender_name = data['senderName']
            sender_email = data['senderEmail']
            subject = data['subject']
            message = data['message']
            
            # Verify faculty exists
            db_instance = get_db()
            faculty = db_instance.session.query(FacultyModel).filter_by(slug=faculty_slug).first()
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found'
                }), 404
            
            # If user is authenticated, use their user_id and email
            if is_authenticated and current_user_id:
                user_id = current_user_id
                # Optionally override with provided email if different
                if current_user_email and current_user_email != sender_email:
                    sender_email = current_user_email
            else:
                user_id = None
            
            # Create inquiry
            inquiry = FacultyInquiryModel(
                faculty_slug=faculty_slug,
                sender_name=sender_name,
                sender_email=sender_email,
                subject=subject,
                message=message,
                user_id=user_id
            )
            
            db_instance.session.add(inquiry)
            db_instance.session.commit()
            
            # Send email notification to faculty (if email service is configured)
            if email_service and email_service.initialized:
                try:
                    # Get faculty contact email
                    faculty_email = None
                    if faculty.contacts and isinstance(faculty.contacts, dict):
                        faculty_email = faculty.contacts.get('email')
                    
                    if faculty_email:
                        email_service.send_email(
                            to=faculty_email,
                            subject=f'Novi upit: {subject}',
                            body=f'''
Dobili ste novi upit od {sender_name} ({sender_email}).

Fakultet: {faculty.name}
Predmet: {subject}

Poruka:
{message}

---
Ovaj upit možete vidjeti i odgovoriti preko sustava.
'''
                        )
                except Exception as e:
                    # Log error but don't fail the request
                    print(f"Failed to send email notification: {str(e)}")
            
            return jsonify({
                'success': True,
                'message': 'Inquiry sent successfully',
                'item': inquiry.to_dict()
            }), 201
            
        except Exception as e:
            get_db().session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to send inquiry: {str(e)}'
            }), 500
    
    @inquiries_bp.route('/faculties/<faculty_slug>', methods=['GET'])
    @oauth_service.token_required
    def get_faculty_inquiries(faculty_slug, current_user_id, current_user_email, current_user_role):
        """Get inquiries for a faculty (only for faculty members)"""
        try:
            # Check if user is faculty or admin
            if current_user_role not in ['faculty', 'fakultet', 'admin']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members can view inquiries'
                }), 403
            
            db_instance = get_db()
            
            # Verify faculty exists
            faculty = db_instance.session.query(FacultyModel).filter_by(slug=faculty_slug).first()
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found'
                }), 404
            
            # Get user's faculty (if not admin)
            if current_user_role != 'admin':
                user = db_instance.session.query(UserModel).get(current_user_id)
                if not user:
                    return jsonify({
                        'success': False,
                        'message': 'User not found'
                    }), 404
                
                # Check if user's email domain matches faculty domain
                # For now, allow all faculty users to see inquiries for any faculty
                # In production, you might want to restrict this further
                pass
            
            # Get inquiries for this faculty
            status_filter = request.args.get('status')  # pending, read, replied, or all
            inquiries_query = db_instance.session.query(FacultyInquiryModel).filter_by(
                faculty_slug=faculty_slug
            )
            
            if status_filter and status_filter != 'all':
                inquiries_query = inquiries_query.filter_by(status=status_filter)
            
            inquiries = inquiries_query.order_by(FacultyInquiryModel.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'count': len(inquiries),
                'items': [inquiry.to_dict(include_user=True) for inquiry in inquiries]
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get inquiries: {str(e)}'
            }), 500
    
    @inquiries_bp.route('/<int:inquiry_id>/read', methods=['PUT'])
    @oauth_service.token_required
    def mark_inquiry_read(inquiry_id, current_user_id, current_user_email, current_user_role):
        """Mark inquiry as read (only for faculty members)"""
        try:
            # Check if user is faculty or admin
            if current_user_role not in ['faculty', 'fakultet', 'admin']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members can mark inquiries as read'
                }), 403
            
            db_instance = get_db()
            inquiry = db_instance.session.query(FacultyInquiryModel).get(inquiry_id)
            
            if not inquiry:
                return jsonify({
                    'success': False,
                    'message': 'Inquiry not found'
                }), 404
            
            inquiry.mark_as_read()
            db_instance.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Inquiry marked as read',
                'item': inquiry.to_dict()
            }), 200
            
        except Exception as e:
            get_db().session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to mark inquiry as read: {str(e)}'
            }), 500
    
    @inquiries_bp.route('/<int:inquiry_id>/reply', methods=['POST'])
    @oauth_service.token_required
    def reply_to_inquiry(inquiry_id, current_user_id, current_user_email, current_user_role):
        """Reply to an inquiry (only for faculty members)"""
        try:
            # Check if user is faculty or admin
            if current_user_role not in ['faculty', 'fakultet', 'admin']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members can reply to inquiries'
                }), 403
            
            data = request.get_json()
            if not data or not data.get('replyMessage'):
                return jsonify({
                    'success': False,
                    'message': 'Reply message is required'
                }), 400
            
            db_instance = get_db()
            inquiry = db_instance.session.query(FacultyInquiryModel).get(inquiry_id)
            
            if not inquiry:
                return jsonify({
                    'success': False,
                    'message': 'Inquiry not found'
                }), 404
            
            reply_message = data['replyMessage']
            
            # Mark as replied
            inquiry.mark_as_replied(reply_message)
            db_instance.session.commit()
            
            # Send email reply to sender (if email service is configured)
            if email_service and email_service.initialized:
                try:
                    # Get faculty info
                    faculty = db_instance.session.query(FacultyModel).filter_by(slug=inquiry.faculty_slug).first()
                    faculty_name = faculty.name if faculty else 'Fakultet'
                    
                    email_service.send_email(
                        to=inquiry.sender_email,
                        subject=f'Odgovor na vaš upit: {inquiry.subject}',
                        body=f'''
Poštovani/a {inquiry.sender_name},

Hvala vam na upitu. Evo odgovora od {faculty_name}:

---
{reply_message}
---

Vaš originalni upit:
{inquiry.message}

---
S poštovanjem,
{faculty_name}
'''
                    )
                except Exception as e:
                    # Log error but don't fail the request
                    print(f"Failed to send email reply: {str(e)}")
            
            return jsonify({
                'success': True,
                'message': 'Reply sent successfully',
                'item': inquiry.to_dict()
            }), 200
            
        except Exception as e:
            get_db().session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to send reply: {str(e)}'
            }), 500
    
    @inquiries_bp.route('/my', methods=['GET'])
    @oauth_service.token_required
    def get_my_inquiries(current_user_id, current_user_email, current_user_role):
        """Get inquiries sent by the current user"""
        try:
            db_instance = get_db()
            inquiries = db_instance.session.query(FacultyInquiryModel).filter_by(
                user_id=current_user_id
            ).order_by(FacultyInquiryModel.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'count': len(inquiries),
                'items': [inquiry.to_dict(include_faculty=True) for inquiry in inquiries]
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get inquiries: {str(e)}'
            }), 500

