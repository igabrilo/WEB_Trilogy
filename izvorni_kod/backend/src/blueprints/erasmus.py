from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

# Support both absolute and relative imports
try:
    from models import ErasmusProjectModel, FacultyModel
    from oauth2_service import OAuth2Service
    from database import db
except ImportError:
    from ..models import ErasmusProjectModel, FacultyModel
    from ..oauth2_service import OAuth2Service
    from ..database import db

erasmus_bp = Blueprint('erasmus', __name__, url_prefix='/api/erasmus')

def get_db():
    """Get db instance from current app"""
    return current_app.extensions['sqlalchemy']

def init_erasmus_routes(oauth_service):
    """Initialize Erasmus routes with services"""
    
    @erasmus_bp.route('', methods=['POST'])
    @oauth_service.token_required
    def create_erasmus_project(current_user_id, current_user_email, current_user_role):
        """Create a new Erasmus project (only for faculty role)"""
        try:
            # Check if user is faculty
            if current_user_role not in ['faculty', 'fakultet']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members can create Erasmus projects'
                }), 403
            
            data = request.get_json()
            
            db_instance = get_db()
            
            # Validate required fields
            required_fields = ['title', 'description', 'facultySlug']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'success': False,
                        'message': f'Field {field} is required'
                    }), 400
            
            # Verify faculty exists
            faculty = db_instance.session.query(FacultyModel).filter_by(slug=data['facultySlug']).first()
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found'
                }), 404
            
            # Parse application deadline if provided
            application_deadline = None
            if data.get('applicationDeadline'):
                try:
                    application_deadline = datetime.strptime(data['applicationDeadline'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Invalid application deadline format. Use YYYY-MM-DD'
                    }), 400
            
            # Create Erasmus project
            project = ErasmusProjectModel(
                title=data['title'],
                description=data['description'],
                faculty_slug=data['facultySlug'],
                created_by=current_user_id,
                country=data.get('country'),
                university=data.get('university'),
                field_of_study=data.get('fieldOfStudy'),
                duration=data.get('duration'),
                application_deadline=application_deadline,
                requirements=data.get('requirements', []),
                benefits=data.get('benefits', []),
                contact_email=data.get('contactEmail'),
                contact_phone=data.get('contactPhone'),
                website=data.get('website'),
                status='active'
            )
            
            db_instance.session.add(project)
            db_instance.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Erasmus project created successfully',
                'item': project.to_dict()
            }), 201
            
        except Exception as e:
            db_instance = get_db()
            db_instance.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to create Erasmus project: {str(e)}'
            }), 500
    
    @erasmus_bp.route('', methods=['GET'])
    def get_erasmus_projects():
        """Get all active Erasmus projects, optionally filtered by faculty"""
        try:
            faculty_slug = request.args.get('faculty')
            field_of_study = request.args.get('fieldOfStudy')
            
            # Start with all active projects
            projects_query = get_db().session.query(ErasmusProjectModel).filter_by(status='active')
            
            # Filter by faculty
            if faculty_slug:
                projects_query = projects_query.filter_by(faculty_slug=faculty_slug)
            
            # Filter by field of study
            if field_of_study:
                projects_query = projects_query.filter_by(field_of_study=field_of_study)
            
            projects = projects_query.order_by(ErasmusProjectModel.created_at.desc()).all()
            projects_list = [project.to_dict() for project in projects]
            
            return jsonify({
                'success': True,
                'count': len(projects_list),
                'items': projects_list
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get Erasmus projects: {str(e)}'
            }), 500
    
    @erasmus_bp.route('/<int:project_id>', methods=['GET'])
    def get_erasmus_project(project_id):
        """Get a single Erasmus project by ID"""
        try:
            project = get_db().session.query(ErasmusProjectModel).get(project_id)
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Erasmus project not found'
                }), 404
            
            return jsonify({
                'success': True,
                'item': project.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get Erasmus project: {str(e)}'
            }), 500
    
    @erasmus_bp.route('/<int:project_id>', methods=['PUT'])
    @oauth_service.token_required
    def update_erasmus_project(project_id, current_user_id, current_user_email, current_user_role):
        """Update an Erasmus project (only for faculty who created it or admin)"""
        try:
            # Check if user is faculty or admin
            if current_user_role not in ['faculty', 'fakultet', 'admin']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members and administrators can update Erasmus projects'
                }), 403
            
            db_instance = get_db()
            project = db_instance.session.query(ErasmusProjectModel).get(project_id)
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Erasmus project not found'
                }), 404
            
            # Check if user is creator or admin
            if project.created_by != current_user_id and current_user_role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'You can only update your own Erasmus projects'
                }), 403
            
            data = request.get_json()
            
            # Update fields
            if 'title' in data:
                project.title = data['title']
            if 'description' in data:
                project.description = data['description']
            if 'facultySlug' in data:
                # Verify faculty exists
                faculty = db_instance.session.query(FacultyModel).filter_by(slug=data['facultySlug']).first()
                if not faculty:
                    return jsonify({
                        'success': False,
                        'message': 'Faculty not found'
                    }), 404
                project.faculty_slug = data['facultySlug']
            if 'country' in data:
                project.country = data['country']
            if 'university' in data:
                project.university = data['university']
            if 'fieldOfStudy' in data:
                project.field_of_study = data['fieldOfStudy']
            if 'duration' in data:
                project.duration = data['duration']
            if 'applicationDeadline' in data:
                if data['applicationDeadline']:
                    try:
                        project.application_deadline = datetime.strptime(data['applicationDeadline'], '%Y-%m-%d').date()
                    except ValueError:
                        return jsonify({
                            'success': False,
                            'message': 'Invalid application deadline format. Use YYYY-MM-DD'
                        }), 400
                else:
                    project.application_deadline = None
            if 'requirements' in data:
                project.requirements = data['requirements']
            if 'benefits' in data:
                project.benefits = data['benefits']
            if 'contactEmail' in data:
                project.contact_email = data['contactEmail']
            if 'contactPhone' in data:
                project.contact_phone = data['contactPhone']
            if 'website' in data:
                project.website = data['website']
            if 'status' in data:
                project.status = data['status']
            
            db_instance.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Erasmus project updated successfully',
                'item': project.to_dict()
            }), 200
            
        except Exception as e:
            db_instance = get_db()
            db_instance.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to update Erasmus project: {str(e)}'
            }), 500
    
    @erasmus_bp.route('/<int:project_id>', methods=['DELETE'])
    @oauth_service.token_required
    def delete_erasmus_project(project_id, current_user_id, current_user_email, current_user_role):
        """Delete an Erasmus project (only for faculty who created it or admin)"""
        try:
            # Check if user is faculty or admin
            if current_user_role not in ['faculty', 'fakultet', 'admin']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members and administrators can delete Erasmus projects'
                }), 403
            
            project = get_db().session.query(ErasmusProjectModel).get(project_id)
            if not project:
                return jsonify({
                    'success': False,
                    'message': 'Erasmus project not found'
                }), 404
            
            # Check if user is creator or admin
            if project.created_by != current_user_id and current_user_role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'You can only delete your own Erasmus projects'
                }), 403
            
            project.delete()
            
            return jsonify({
                'success': True,
                'message': 'Erasmus project deleted successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to delete Erasmus project: {str(e)}'
            }), 500

