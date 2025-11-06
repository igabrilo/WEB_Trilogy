from flask import Blueprint, request, jsonify
import re
from datetime import datetime

# Support both absolute and relative imports
try:
    from models import User
    from oauth2_service import OAuth2Service
except ImportError:
    from ..models import User
    from ..oauth2_service import OAuth2Service

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

# In-memory storage (in production, use a database)
JOBS_STORAGE = []
APPLICATIONS_STORAGE = []

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
            
            # Create job posting
            new_job = {
                'id': len(JOBS_STORAGE) + 1,
                'title': data['title'],
                'description': data['description'],
                'type': data['type'],  # 'internship', 'job', 'part-time', 'remote'
                'company': data.get('company', ''),
                'location': data.get('location', ''),
                'salary': data.get('salary', ''),
                'requirements': data.get('requirements', []),
                'tags': data.get('tags', []),
                'createdBy': current_user_id,
                'createdAt': datetime.utcnow().isoformat(),
                'status': 'active',
                'applications': []
            }
            
            JOBS_STORAGE.append(new_job)
            
            return jsonify({
                'success': True,
                'message': 'Job posting created successfully',
                'item': new_job
            }), 201
            
        except Exception as e:
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
            
            jobs = JOBS_STORAGE.copy()
            
            # Filter by type
            if type_filter:
                jobs = [j for j in jobs if j.get('type') == type_filter]
            
            # Search by query
            if query:
                query_lower = query.lower()
                jobs = [j for j in jobs if 
                       query_lower in j.get('title', '').lower() or
                       query_lower in j.get('description', '').lower() or
                       query_lower in j.get('company', '').lower()]
            
            # Remove applications from response (only show count)
            for job in jobs:
                if 'applications' in job:
                    job['applicationCount'] = len(job['applications'])
                    del job['applications']
            
            return jsonify({
                'success': True,
                'count': len(jobs),
                'items': jobs
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get jobs: {str(e)}'
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
            job = next((j for j in JOBS_STORAGE if j.get('id') == job_id), None)
            if not job:
                return jsonify({
                    'success': False,
                    'message': 'Job not found'
                }), 404
            
            # Check if already applied
            existing_application = next(
                (a for a in job.get('applications', []) if a.get('userId') == current_user_id),
                None
            )
            if existing_application:
                return jsonify({
                    'success': False,
                    'message': 'You have already applied to this job'
                }), 400
            
            data = request.get_json()
            
            # Create application
            application = {
                'id': len(APPLICATIONS_STORAGE) + 1,
                'jobId': job_id,
                'userId': current_user_id,
                'userEmail': current_user_email,
                'message': data.get('message', ''),
                'status': 'pending',  # pending, approved, rejected
                'createdAt': datetime.utcnow().isoformat()
            }
            
            APPLICATIONS_STORAGE.append(application)
            job['applications'].append(application)
            
            return jsonify({
                'success': True,
                'message': 'Application submitted successfully',
                'item': application
            }), 201
            
        except Exception as e:
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
            job = next((j for j in JOBS_STORAGE if j.get('id') == job_id), None)
            if not job:
                return jsonify({
                    'success': False,
                    'message': 'Job not found'
                }), 404
            
            # Check if user is creator
            if job.get('createdBy') != current_user_id:
                return jsonify({
                    'success': False,
                    'message': 'You can only view applications for your own job postings'
                }), 403
            
            applications = job.get('applications', [])
            
            # Get user info for each application
            for app in applications:
                user = User.find_by_id(app.get('userId'))
                if user:
                    if isinstance(user, dict):
                        app['user'] = {
                            'id': user.get('id'),
                            'email': user.get('email'),
                            'firstName': user.get('firstName'),
                            'lastName': user.get('lastName')
                        }
                    else:
                        app['user'] = user.to_dict()
            
            return jsonify({
                'success': True,
                'count': len(applications),
                'items': applications
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
            
            # Get all jobs created by this employer
            employer_jobs = [j for j in JOBS_STORAGE if j.get('createdBy') == current_user_id]
            
            all_applications = []
            for job in employer_jobs:
                for app in job.get('applications', []):
                    app_with_job = app.copy()
                    app_with_job['job'] = {
                        'id': job.get('id'),
                        'title': job.get('title'),
                        'type': job.get('type')
                    }
                    # Get user info
                    user = User.find_by_id(app.get('userId'))
                    if user:
                        if isinstance(user, dict):
                            app_with_job['user'] = {
                                'id': user.get('id'),
                                'email': user.get('email'),
                                'firstName': user.get('firstName'),
                                'lastName': user.get('lastName')
                            }
                        else:
                            app_with_job['user'] = user.to_dict()
                    all_applications.append(app_with_job)
            
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
            application = next((a for a in APPLICATIONS_STORAGE if a.get('id') == application_id), None)
            if not application:
                return jsonify({
                    'success': False,
                    'message': 'Application not found'
                }), 404
            
            # Find job
            job = next((j for j in JOBS_STORAGE if j.get('id') == application.get('jobId')), None)
            if not job:
                return jsonify({
                    'success': False,
                    'message': 'Job not found'
                }), 404
            
            # Check if user is job creator
            if job.get('createdBy') != current_user_id:
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
            application['status'] = new_status
            application['updatedAt'] = datetime.utcnow().isoformat()
            
            # Update in job's applications list
            job_app = next((a for a in job.get('applications', []) if a.get('id') == application_id), None)
            if job_app:
                job_app['status'] = new_status
                job_app['updatedAt'] = application['updatedAt']
            
            return jsonify({
                'success': True,
                'message': f'Application {new_status} successfully',
                'item': application
            }), 200
            
        except Exception as e:
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
            application = next((a for a in APPLICATIONS_STORAGE if a.get('id') == application_id), None)
            if not application:
                return jsonify({
                    'success': False,
                    'message': 'Application not found'
                }), 404
            
            # Find job
            job = next((j for j in JOBS_STORAGE if j.get('id') == application.get('jobId')), None)
            if not job:
                return jsonify({
                    'success': False,
                    'message': 'Job not found'
                }), 404
            
            # Check if user is job creator
            if job.get('createdBy') != current_user_id:
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
            
            # In production, send actual email here
            # For now, just return success
            # TODO: Integrate with email service (SMTP, SendGrid, etc.)
            
            return jsonify({
                'success': True,
                'message': f'Email sent to {application.get("userEmail")}',
                'email': {
                    'to': application.get('userEmail'),
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

