from flask import Blueprint, request, jsonify
import re
from datetime import datetime
from sqlalchemy import func

# Support both absolute and relative imports
try:
    from models import UserModel, AssociationModel
    from oauth2_service import OAuth2Service
    from database import db
except ImportError:
    from ..models import UserModel, AssociationModel
    from ..oauth2_service import OAuth2Service
    from ..database import db

associations_bp = Blueprint('associations', __name__, url_prefix='/api/associations')

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
            
            # Check if slug already exists and make it unique
            existing = AssociationModel.query.filter_by(slug=slug).first()
            if existing:
                # Simple unique slug generation
                import uuid
                slug = f"{slug}-{str(uuid.uuid4())[:8]}"
            
            # Create association
            new_association = AssociationModel(
                slug=slug,
                name=data['name'],
                faculty=data['faculty'],
                type=data.get('type', 'academic'),
                logo_text=data.get('logoText', data['name'][:3].upper()),
                logo_bg=data.get('logoBg', '#1e70bf'),
                short_description=data['shortDescription'],
                description=data.get('description', ''),
                tags=data.get('tags', []),
                links=data.get('links', {}),
                created_by=current_user_id
            )
            
            new_association.save()
            
            return jsonify({
                'success': True,
                'message': 'Association created successfully',
                'item': new_association.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
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
            association = AssociationModel.query.get(association_id)
            if not association:
                return jsonify({
                    'success': False,
                    'message': 'Association not found'
                }), 404
            
            # Check if user is creator
            if association.created_by != current_user_id:
                return jsonify({
                    'success': False,
                    'message': 'Only the creator can update this association'
                }), 403
            
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
            
            association.save()
            
            return jsonify({
                'success': True,
                'message': 'Association updated successfully',
                'item': association.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to update association: {str(e)}'
            }), 500

