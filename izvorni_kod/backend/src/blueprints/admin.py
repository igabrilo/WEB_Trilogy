from flask import Blueprint, request, jsonify
import re
from datetime import datetime

# Support both absolute and relative imports
try:
    from models import User
    from oauth2_service import OAuth2Service
    from blueprints.search import FACULTIES_DATA
    from blueprints.associations import ASSOCIATIONS_STORAGE
except ImportError:
    from ..models import User
    from ..oauth2_service import OAuth2Service
    from ..blueprints.search import FACULTIES_DATA
    from ..blueprints.associations import ASSOCIATIONS_STORAGE

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# In-memory storage for faculties (in production, use database)
# Export this so search.py can use it
FACULTIES_STORAGE = []

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
            
            # Check if slug already exists
            all_faculties = FACULTIES_DATA + FACULTIES_STORAGE
            existing = next((f for f in all_faculties if f.get('slug') == slug), None)
            if existing:
                slug = f"{slug}-{len(FACULTIES_STORAGE) + 1}"
            
            # Create faculty
            new_faculty = {
                'slug': slug,
                'name': data['name'],
                'abbreviation': data.get('abbreviation', ''),
                'type': data['type'],  # 'faculty' or 'academy'
                'contacts': {
                    'email': data.get('email'),
                    'phone': data.get('phone'),
                    'address': data.get('address'),
                    'website': data.get('website')
                },
                'createdAt': datetime.utcnow().isoformat()
            }
            
            FACULTIES_STORAGE.append(new_faculty)
            
            return jsonify({
                'success': True,
                'message': 'Faculty created successfully',
                'item': new_faculty
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
            
            all_faculties = FACULTIES_DATA + FACULTIES_STORAGE
            
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
            
            # Find faculty in storage first, then in mock data
            faculty = next((f for f in FACULTIES_STORAGE if f.get('slug') == slug), None)
            if not faculty:
                faculty = next((f for f in FACULTIES_DATA if f.get('slug') == slug), None)
                if faculty:
                    # Copy to storage for editing
                    faculty = faculty.copy()
                    FACULTIES_STORAGE.append(faculty)
            
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found'
                }), 404
            
            data = request.get_json()
            
            # Update fields
            if 'name' in data:
                faculty['name'] = data['name']
            if 'abbreviation' in data:
                faculty['abbreviation'] = data['abbreviation']
            if 'type' in data:
                faculty['type'] = data['type']
            if 'email' in data:
                if 'contacts' not in faculty:
                    faculty['contacts'] = {}
                faculty['contacts']['email'] = data['email']
            if 'phone' in data:
                if 'contacts' not in faculty:
                    faculty['contacts'] = {}
                faculty['contacts']['phone'] = data['phone']
            if 'address' in data:
                if 'contacts' not in faculty:
                    faculty['contacts'] = {}
                faculty['contacts']['address'] = data['address']
            if 'website' in data:
                if 'contacts' not in faculty:
                    faculty['contacts'] = {}
                faculty['contacts']['website'] = data['website']
            
            faculty['updatedAt'] = datetime.utcnow().isoformat()
            
            return jsonify({
                'success': True,
                'message': 'Faculty updated successfully',
                'item': faculty
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
            
            # Can only delete from storage, not mock data
            faculty = next((f for f in FACULTIES_STORAGE if f.get('slug') == slug), None)
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found or cannot be deleted (is in system data)'
                }), 404
            
            FACULTIES_STORAGE.remove(faculty)
            
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
            all_associations = ASSOCIATIONS_DATA + ASSOCIATIONS_STORAGE
            
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
            
            # Find association
            association = next((a for a in ASSOCIATIONS_STORAGE if a.get('id') == association_id), None)
            if not association:
                from blueprints.search import ASSOCIATIONS_DATA
                association = next((a for a in ASSOCIATIONS_DATA if a.get('id') == association_id), None)
                if not association:
                    return jsonify({
                        'success': False,
                        'message': 'Association not found'
                    }), 404
            
            data = request.get_json()
            
            # Update fields
            if 'name' in data:
                association['name'] = data['name']
            if 'faculty' in data:
                association['faculty'] = data['faculty']
            if 'type' in data:
                association['type'] = data['type']
            if 'logoText' in data:
                association['logoText'] = data['logoText']
            if 'logoBg' in data:
                association['logoBg'] = data['logoBg']
            if 'shortDescription' in data:
                association['shortDescription'] = data['shortDescription']
            if 'description' in data:
                association['description'] = data['description']
            if 'tags' in data:
                association['tags'] = data['tags']
            if 'links' in data:
                association['links'] = data['links']
            
            association['updatedAt'] = datetime.utcnow().isoformat()
            
            return jsonify({
                'success': True,
                'message': 'Association updated successfully',
                'item': association
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
            
            # Can only delete from storage, not mock data
            association = next((a for a in ASSOCIATIONS_STORAGE if a.get('id') == association_id), None)
            if not association:
                return jsonify({
                    'success': False,
                    'message': 'Association not found or cannot be deleted (is in system data)'
                }), 404
            
            ASSOCIATIONS_STORAGE.remove(association)
            
            return jsonify({
                'success': True,
                'message': 'Association deleted successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to delete association: {str(e)}'
            }), 500

