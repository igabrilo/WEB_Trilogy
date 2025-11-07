from flask import Blueprint, request, jsonify
import re
from datetime import datetime
from sqlalchemy import or_, func, text

# Support both absolute and relative imports
try:
    from models import UserModel, JobModel, JobApplicationModel
    from oauth2_service import OAuth2Service
    from database import db
except ImportError:
    from ..models import UserModel, JobModel, JobApplicationModel
    from ..oauth2_service import OAuth2Service
    from ..database import db

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

def init_jobs_routes(oauth_service):
    """Initialize jobs routes with services"""
    
    @jobs_bp.route('', methods=['POST'])
    @oauth_service.token_required
    def create_job(current_user_id, current_user_email, current_user_role):
        """Create a new job/internship posting (only for employer role)"""
        try:
            # Check if user is employer
            if current_user_role not in ['employer', 'poslodavac']:
                return jsonify({
                    'success': False,
                    'message': 'Only employers can create job postings'
                }), 403
            
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['title', 'description', 'type']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'success': False,
                        'message': f'Field {field} is required'
                    }), 400
            
            # Create job posting using JobModel
            new_job = JobModel(
                title=data['title'],
                description=data['description'],
                type=data['type'],  # 'internship', 'job', 'part-time', 'remote'
                company=data.get('company', ''),
                location=data.get('location', ''),
                salary=data.get('salary', ''),
                requirements=data.get('requirements', []),
                tags=data.get('tags', []),
                created_by=current_user_id,
                status='active'
            )
            
            new_job.save()
            
            return jsonify({
                'success': True,
                'message': 'Job posting created successfully',
                'item': new_job.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to create job posting: {str(e)}'
            }), 500
    
    @jobs_bp.route('', methods=['GET'])
    def get_jobs():
        """Get all job postings"""
        try:
            type_filter = request.args.get('type')
            query = request.args.get('q', '').strip()
            
            # Start with all active jobs
            jobs_query = JobModel.query.filter_by(status='active')
            
            # Filter by type
            if type_filter:
                jobs_query = jobs_query.filter_by(type=type_filter)
            
            # Search by query
            if query:
                search_term = f"%{query.lower()}%"
                jobs_query = jobs_query.filter(
                    or_(
                        text("LOWER(title) LIKE :search"),
                        text("LOWER(description) LIKE :search"),
                        text("LOWER(company) LIKE :search")
                    ).params(search=search_term)
                )
            
            jobs = jobs_query.all()
            jobs_list = [job.to_dict() for job in jobs]
            
            return jsonify({
                'success': True,
                'count': len(jobs_list),
                'items': jobs_list
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get jobs: {str(e)}'
            }), 500
    
    @jobs_bp.route('/<int:job_id>', methods=['GET'])
    def get_job(job_id):
        """Get a single job posting by ID"""
        try:
            job = JobModel.query.get(job_id)
            if not job:
                return jsonify({
                    'success': False,
                    'message': 'Job not found'
                }), 404
            
            return jsonify({
                'success': True,
                'item': job.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get job: {str(e)}'
            }), 500
    
    @jobs_bp.route('/<int:job_id>/apply', methods=['POST'])
    @oauth_service.token_required
    def apply_to_job(job_id, current_user_id, current_user_email, current_user_role):
        """Apply to a job/internship (only for students)"""
        try:
            # Check if user is student
            if current_user_role not in ['student', 'alumni']:
                return jsonify({
                    'success': False,
                    'message': 'Only students and alumni can apply to jobs'
                }), 403
            
            # Find job
            job = JobModel.query.get(job_id)
            if not job:
                return jsonify({
                    'success': False,
                    'message': 'Job not found'
                }), 404
            
            # Check if already applied
            existing_application = JobApplicationModel.query.filter_by(
                job_id=job_id,
                user_id=current_user_id
            ).first()
            
            if existing_application:
                return jsonify({
                    'success': False,
                    'message': 'You have already applied to this job'
                }), 400
            
            data = request.get_json()
            
            # Create application
            application = JobApplicationModel(
                job_id=job_id,
                user_id=current_user_id,
                message=data.get('message', ''),
                status='pending'
            )
            
            application.save()
            
            return jsonify({
                'success': True,
                'message': 'Application submitted successfully',
                'item': application.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to apply: {str(e)}'
            }), 500
    
    @jobs_bp.route('/<int:job_id>/applications', methods=['GET'])
    @oauth_service.token_required
    def get_job_applications(job_id, current_user_id, current_user_email, current_user_role):
        """Get applications for a job (only for employer who created it)"""
        try:
            # Check if user is employer
            if current_user_role not in ['employer', 'poslodavac']:
                return jsonify({
                    'success': False,
                    'message': 'Only employers can view applications'
                }), 403
            
            # Find job
            job = JobModel.query.get(job_id)
            if not job:
                return jsonify({
                    'success': False,
                    'message': 'Job not found'
                }), 404
            
            # Check if user is creator
            if job.created_by != current_user_id:
                return jsonify({
                    'success': False,
                    'message': 'You can only view applications for your own job postings'
                }), 403
            
            # Get applications for this job
            applications = JobApplicationModel.query.filter_by(job_id=job_id).all()
            
            applications_list = [app.to_dict(include_user=True) for app in applications]
            
            return jsonify({
                'success': True,
                'count': len(applications_list),
                'items': applications_list
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get applications: {str(e)}'
            }), 500
    
    @jobs_bp.route('/applications', methods=['GET'])
    @oauth_service.token_required
    def get_all_applications(current_user_id, current_user_email, current_user_role):
        """Get all applications for all jobs created by employer"""
        try:
            # Check if user is employer
            if current_user_role not in ['employer', 'poslodavac']:
                return jsonify({
                    'success': False,
                    'message': 'Only employers can view applications'
                }), 403
            
            # Get all jobs created by this employer and their applications
            employer_jobs = JobModel.query.filter_by(created_by=current_user_id).all()
            
            all_applications = []
            for job in employer_jobs:
                applications = JobApplicationModel.query.filter_by(job_id=job.id).all()
                for app in applications:
                    all_applications.append(app.to_dict(include_user=True, include_job=True))
            
            return jsonify({
                'success': True,
                'count': len(all_applications),
                'items': all_applications
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get applications: {str(e)}'
            }), 500
    
    @jobs_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
    @oauth_service.token_required
    def update_application_status(application_id, current_user_id, current_user_email, current_user_role):
        """Update application status (approve/reject) - only for employer"""
        try:
            # Check if user is employer
            if current_user_role not in ['employer', 'poslodavac']:
                return jsonify({
                    'success': False,
                    'message': 'Only employers can update application status'
                }), 403
            
            # Find application
            application = JobApplicationModel.query.get(application_id)
            if not application:
                return jsonify({
                    'success': False,
                    'message': 'Application not found'
                }), 404
            
            # Find job and check if user is job creator
            job = JobModel.query.get(application.job_id)
            if not job or job.created_by != current_user_id:
                return jsonify({
                    'success': False,
                    'message': 'You can only update applications for your own job postings'
                }), 403
            
            data = request.get_json()
            new_status = data.get('status')
            
            if new_status not in ['pending', 'approved', 'rejected']:
                return jsonify({
                    'success': False,
                    'message': 'Invalid status. Must be pending, approved, or rejected'
                }), 400
            
            # Update application status
            application.status = new_status
            application.save()
            
            return jsonify({
                'success': True,
                'message': f'Application {new_status} successfully',
                'item': application.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to update application status: {str(e)}'
            }), 500
    
    @jobs_bp.route('/applications/<int:application_id>/send-email', methods=['POST'])
    @oauth_service.token_required
    def send_email_to_applicant(application_id, current_user_id, current_user_email, current_user_role):
        """Send email to applicant - only for employer"""
        try:
            # Check if user is employer
            if current_user_role not in ['employer', 'poslodavac']:
                return jsonify({
                    'success': False,
                    'message': 'Only employers can send emails to applicants'
                }), 403
            
            # Find application
            application = JobApplicationModel.query.get(application_id)
            if not application:
                return jsonify({
                    'success': False,
                    'message': 'Application not found'
                }), 404
            
            # Find job and check if user is job creator
            job = JobModel.query.get(application.job_id)
            if not job or job.created_by != current_user_id:
                return jsonify({
                    'success': False,
                    'message': 'You can only send emails for your own job postings'
                }), 403
            
            data = request.get_json()
            subject = data.get('subject', '')
            message = data.get('message', '')
            
            if not subject or not message:
                return jsonify({
                    'success': False,
                    'message': 'Subject and message are required'
                }), 400
            
            # Get applicant user info
            applicant = UserModel.query.get(application.user_id)
            if not applicant:
                return jsonify({
                    'success': False,
                    'message': 'Applicant not found'
                }), 404
            
            # In production, send actual email here
            # For now, just return success
            # TODO: Integrate with email service (SMTP, SendGrid, etc.)
            
            return jsonify({
                'success': True,
                'message': f'Email sent to {applicant.email}',
                'email': {
                    'to': applicant.email,
                    'subject': subject,
                    'message': message,
                    'sentAt': datetime.utcnow().isoformat()
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to send email: {str(e)}'
            }), 500

