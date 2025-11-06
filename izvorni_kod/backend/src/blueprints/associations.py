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

associations_bp = Blueprint('associations', __name__, url_prefix='/api/associations')

# In-memory storage (in production, use a database)
ASSOCIATIONS_STORAGE = []
APPLICATIONS_STORAGE = []  # For internship/job applications

def init_associations_routes(oauth_service):
    """Initialize associations routes with services"""
    
    @associations_bp.route('', methods=['POST'])
    @oauth_service.token_required
    def create_association(current_user_id, current_user_email, current_user_role):
        """Create a new association (only for faculty role or admin)"""
        try:
            # Check if user is faculty or admin
            if current_user_role not in ['faculty', 'fakultet', 'admin']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members and administrators can create associations'
                }), 403
            
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['name', 'faculty', 'shortDescription']
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
            existing = next((a for a in ASSOCIATIONS_STORAGE if a.get('slug') == slug), None)
            if existing:
                slug = f"{slug}-{len(ASSOCIATIONS_STORAGE) + 1}"
            
            # Create association
            new_association = {
                'id': len(ASSOCIATIONS_STORAGE) + 1,
                'slug': slug,
                'name': data['name'],
                'faculty': data['faculty'],
                'type': data.get('type', 'academic'),
                'logoText': data.get('logoText', data['name'][:3].upper()),
                'logoBg': data.get('logoBg', '#1e70bf'),
                'shortDescription': data['shortDescription'],
                'description': data.get('description', ''),
                'tags': data.get('tags', []),
                'links': data.get('links', {}),
                'createdBy': current_user_id,
                'createdAt': datetime.utcnow().isoformat()
            }
            
            ASSOCIATIONS_STORAGE.append(new_association)
            
            return jsonify({
                'success': True,
                'message': 'Association created successfully',
                'item': new_association
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to create association: {str(e)}'
            }), 500
    
    @associations_bp.route('/<int:association_id>', methods=['PUT'])
    @oauth_service.token_required
    def update_association(association_id, current_user_id, current_user_email, current_user_role):
        """Update an association (only for faculty role and creator)"""
        try:
            # Check if user is faculty
            if current_user_role not in ['faculty', 'fakultet']:
                return jsonify({
                    'success': False,
                    'message': 'Only faculty members can update associations'
                }), 403
            
            # Find association
            association = next((a for a in ASSOCIATIONS_STORAGE if a.get('id') == association_id), None)
            if not association:
                return jsonify({
                    'success': False,
                    'message': 'Association not found'
                }), 404
            
            # Check if user is creator
            if association.get('createdBy') != current_user_id:
                return jsonify({
                    'success': False,
                    'message': 'Only the creator can update this association'
                }), 403
            
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

