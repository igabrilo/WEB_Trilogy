from flask import Blueprint, request, jsonify
import re
from datetime import datetime

# Support both absolute and relative imports
try:
    from models import UserModel, FacultyModel, AssociationModel
    from oauth2_service import OAuth2Service
    from blueprints.search import FACULTIES_DATA
    from database import db
except ImportError:
    from ..models import UserModel, FacultyModel, AssociationModel
    from ..oauth2_service import OAuth2Service
    from ..blueprints.search import FACULTIES_DATA
    from ..database import db

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

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
            existing_faculty = FacultyModel.query.filter_by(slug=slug).first()
            if existing_faculty:
                faculty_count = FacultyModel.query.count()
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
            db.session.commit()
            
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
            db_faculties = FacultyModel.query.all()
            db_faculties_list = [faculty.to_dict() for faculty in db_faculties]
            
            # Combine with sample data
            all_faculties = FACULTIES_DATA + db_faculties_list
            
            return jsonify({
                'success': True,
                'count': len(all_faculties),
                'items': all_faculties
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
            
            # Find faculty in database first, then in mock data
            faculty = FacultyModel.query.filter_by(slug=slug).first()
            
            if not faculty:
                # Check if it's in sample data and create if needed
                sample_faculty = next((f for f in FACULTIES_DATA if f.get('slug') == slug), None)
                if sample_faculty:
                    # Create database entry from sample data
                    faculty = FacultyModel(
                        slug=sample_faculty['slug'],
                        name=sample_faculty['name'],
                        type=sample_faculty.get('type', 'faculty'),
                        abbreviation=sample_faculty.get('abbreviation', ''),
                        contacts=sample_faculty.get('contacts', {})
                    )
                    db.session.add(faculty)
                    db.session.commit()
                else:
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
            db.session.commit()
            
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
            
            # Can only delete from database, not sample data
            faculty = FacultyModel.query.filter_by(slug=slug).first()
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found or cannot be deleted (is in system data)'
                }), 404
            
            db.session.delete(faculty)
            db.session.commit()
            
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
            
            from blueprints.search import ASSOCIATIONS_DATA
            # Get associations from database
            db_associations = AssociationModel.query.all()
            db_associations_list = [association.to_dict() for association in db_associations]
            
            # Combine with sample data
            all_associations = ASSOCIATIONS_DATA + db_associations_list
            
            return jsonify({
                'success': True,
                'count': len(all_associations),
                'items': all_associations
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
            
            # Find association in database first, then in sample data
            association = AssociationModel.query.filter_by(id=association_id).first()
            
            if not association:
                # Check if it's in sample data and create if needed
                from blueprints.search import ASSOCIATIONS_DATA
                sample_association = next((a for a in ASSOCIATIONS_DATA if a.get('id') == association_id), None)
                if sample_association:
                    # Create database entry from sample data - generate slug from name
                    import re
                    slug = re.sub(r'[^\w\s-]', '', sample_association['name']).strip().lower()
                    slug = re.sub(r'[-\s]+', '-', slug)
                    
                    association = AssociationModel(
                        slug=slug,
                        name=sample_association['name'],
                        faculty=sample_association.get('faculty', ''),
                        type=sample_association.get('type', ''),
                        logo_text=sample_association.get('logoText', ''),
                        logo_bg=sample_association.get('logoBg', ''),
                        short_description=sample_association.get('shortDescription', ''),
                        description=sample_association.get('description', ''),
                        tags=sample_association.get('tags', []),
                        links=sample_association.get('links', {})
                    )
                    db.session.add(association)
                    db.session.commit()
                else:
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
            db.session.commit()
            
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
            association = AssociationModel.query.filter_by(id=association_id).first()
            if not association:
                return jsonify({
                    'success': False,
                    'message': 'Association not found or cannot be deleted (is in system data)'
                }), 404
            
            db.session.delete(association)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Association deleted successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to delete association: {str(e)}'
            }), 500

