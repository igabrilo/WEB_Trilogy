from flask import Blueprint, request, jsonify, current_app
import re
from datetime import datetime

# Support both absolute and relative imports
try:
    from models import UserModel, FacultyModel, AssociationModel
    from oauth2_service import OAuth2Service
    from database import db
except ImportError:
    from ..models import UserModel, FacultyModel, AssociationModel
    from ..oauth2_service import OAuth2Service
    from ..database import db

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def get_db():
    """Get db instance from current app"""
    return current_app.extensions['sqlalchemy']

def init_admin_routes(oauth_service):
    """Initialize admin routes with services"""
    
    def is_admin(current_user_role):
        """Check if user is admin"""
        return current_user_role == 'admin'
    
    @admin_bp.route('/faculties', methods=['POST'])
    @oauth_service.token_required
    def create_faculty(current_user_id, current_user_email, current_user_role):
        """Create a new faculty (admin only)"""
        try:
            if not is_admin(current_user_role):
                return jsonify({
                    'success': False,
                    'message': 'Only administrators can create faculties'
                }), 403
            
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['name', 'type']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'success': False,
                        'message': f'Field {field} is required'
                    }), 400
            
            # Generate slug from name
            slug = re.sub(r'[^\w\s-]', '', data['name']).strip().lower()
            slug = re.sub(r'[-\s]+', '-', slug)
            
            # Check if slug already exists in database
            existing_faculty = get_db().session.query(FacultyModel).filter_by(slug=slug).first()
            if existing_faculty:
                faculty_count = get_db().session.query(FacultyModel).count()
                slug = f"{slug}-{faculty_count + 1}"
            
            # Create faculty object in database
            contacts = {
                'email': data.get('email'),
                'phone': data.get('phone'),
                'address': data.get('address'),
                'website': data.get('website')
            }
            
            new_faculty = FacultyModel(
                slug=slug,
                name=data['name'],
                type=data['type'],  # 'faculty' or 'academy'
                abbreviation=data.get('abbreviation', ''),
                contacts=contacts
            )
            
            # Add to database
            db.session.add(new_faculty)
            get_db().session.commit()
            
            # Convert to dict for response
            faculty_dict = new_faculty.to_dict()
            
            return jsonify({
                'success': True,
                'message': 'Faculty created successfully',
                'item': faculty_dict
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to create faculty: {str(e)}'
            }), 500
    
    @admin_bp.route('/faculties', methods=['GET'])
    @oauth_service.token_required
    def get_all_faculties(current_user_id, current_user_email, current_user_role):
        """Get all faculties (admin only)"""
        try:
            if not is_admin(current_user_role):
                return jsonify({
                    'success': False,
                    'message': 'Only administrators can view all faculties'
                }), 403
            
            # Get faculties from database
            db_faculties = get_db().session.query(FacultyModel).all()
            db_faculties_list = [faculty.to_dict() for faculty in db_faculties]
            
            return jsonify({
                'success': True,
                'count': len(db_faculties_list),
                'items': db_faculties_list
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get faculties: {str(e)}'
            }), 500
    
    @admin_bp.route('/faculties/<slug>', methods=['PUT'])
    @oauth_service.token_required
    def update_faculty(slug, current_user_id, current_user_email, current_user_role):
        """Update a faculty (admin only)"""
        try:
            if not is_admin(current_user_role):
                return jsonify({
                    'success': False,
                    'message': 'Only administrators can update faculties'
                }), 403
            
            # Find faculty in database
            faculty = get_db().session.query(FacultyModel).filter_by(slug=slug).first()
            
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found'
                }), 404
            
            data = request.get_json()
            
            # Update fields
            if 'name' in data:
                faculty.name = data['name']
            if 'abbreviation' in data:
                faculty.abbreviation = data['abbreviation']
            if 'type' in data:
                faculty.type = data['type']
            if 'email' in data:
                if faculty.contacts is None:
                    faculty.contacts = {}
                faculty.contacts['email'] = data['email']
            if 'phone' in data:
                if faculty.contacts is None:
                    faculty.contacts = {}
                faculty.contacts['phone'] = data['phone']
            if 'address' in data:
                if faculty.contacts is None:
                    faculty.contacts = {}
                faculty.contacts['address'] = data['address']
            if 'website' in data:
                if faculty.contacts is None:
                    faculty.contacts = {}
                faculty.contacts['website'] = data['website']
            
            # Commit changes to database
            get_db().session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Faculty updated successfully',
                'item': faculty.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to update faculty: {str(e)}'
            }), 500
    
    @admin_bp.route('/faculties/<slug>', methods=['DELETE'])
    @oauth_service.token_required
    def delete_faculty(slug, current_user_id, current_user_email, current_user_role):
        """Delete a faculty (admin only)"""
        try:
            if not is_admin(current_user_role):
                return jsonify({
                    'success': False,
                    'message': 'Only administrators can delete faculties'
                }), 403
            
            # Delete from database
            faculty = get_db().session.query(FacultyModel).filter_by(slug=slug).first()
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found'
                }), 404
            
            db.session.delete(faculty)
            get_db().session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Faculty deleted successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to delete faculty: {str(e)}'
            }), 500
    
    @admin_bp.route('/associations', methods=['GET'])
    @oauth_service.token_required
    def get_all_associations(current_user_id, current_user_email, current_user_role):
        """Get all associations (admin only)"""
        try:
            if not is_admin(current_user_role):
                return jsonify({
                    'success': False,
                    'message': 'Only administrators can view all associations'
                }), 403
            
            # Get associations from database
            db_associations = get_db().session.query(AssociationModel).all()
            db_associations_list = [association.to_dict() for association in db_associations]
            
            return jsonify({
                'success': True,
                'count': len(db_associations_list),
                'items': db_associations_list
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get associations: {str(e)}'
            }), 500
    
    @admin_bp.route('/associations/<int:association_id>', methods=['PUT'])
    @oauth_service.token_required
    def update_association(association_id, current_user_id, current_user_email, current_user_role):
        """Update an association (admin only)"""
        try:
            if not is_admin(current_user_role):
                return jsonify({
                    'success': False,
                    'message': 'Only administrators can update associations'
                }), 403
            
            # Find association in database
            association = get_db().session.query(AssociationModel).filter_by(id=association_id).first()
            
            if not association:
                return jsonify({
                    'success': False,
                    'message': 'Association not found'
                }), 404
            
            data = request.get_json()
            
            # Update fields
            if 'name' in data:
                association.name = data['name']
            if 'faculty' in data:
                association.faculty = data['faculty']
            if 'type' in data:
                association.type = data['type']
            if 'logoText' in data:
                association.logo_text = data['logoText']
            if 'logoBg' in data:
                association.logo_bg = data['logoBg']
            if 'shortDescription' in data:
                association.short_description = data['shortDescription']
            if 'description' in data:
                association.description = data['description']
            if 'tags' in data:
                association.tags = data['tags']
            if 'links' in data:
                association.links = data['links']
            
            # Commit changes to database
            get_db().session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Association updated successfully',
                'item': association.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to update association: {str(e)}'
            }), 500
    
    @admin_bp.route('/associations/<int:association_id>', methods=['DELETE'])
    @oauth_service.token_required
    def delete_association(association_id, current_user_id, current_user_email, current_user_role):
        """Delete an association (admin only)"""
        try:
            if not is_admin(current_user_role):
                return jsonify({
                    'success': False,
                    'message': 'Only administrators can delete associations'
                }), 403
            
            # Can only delete from database, not sample data
            association = get_db().session.query(AssociationModel).filter_by(id=association_id).first()
            if not association:
                return jsonify({
                    'success': False,
                    'message': 'Association not found or cannot be deleted (is in system data)'
                }), 404
            
            db.session.delete(association)
            get_db().session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Association deleted successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to delete association: {str(e)}'
            }), 500

