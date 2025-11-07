from flask import Blueprint, request, jsonify
from typing import Optional

# Support both absolute and relative imports
try:
    from models import AssociationModel, FacultyModel
    from database import db
except ImportError:
    from ..models import AssociationModel, FacultyModel
    from ..database import db

search_bp = Blueprint('search', __name__, url_prefix='/api')

# Note: Mock data has been migrated to database. See migrate.py for seed data.

def search_associations(query: str, faculty: Optional[str] = None):
    """Search associations by query and optionally filter by faculty"""
    query_lower = query.lower()
    results = []
    
    # Get all associations from database
    associations_query = AssociationModel.query
    
    # Filter by faculty if specified
    if faculty:
        associations_query = associations_query.filter_by(faculty=faculty)
    
    db_associations = associations_query.all()
    
    for assoc in db_associations:
        assoc_dict = assoc.to_dict()
        # Search in name, description, tags
        name_match = query_lower in assoc_dict.get('name', '').lower()
        desc_match = query_lower in assoc_dict.get('shortDescription', '').lower() or query_lower in assoc_dict.get('description', '').lower()
        tags_match = any(query_lower in tag.lower() for tag in assoc_dict.get('tags', []))
        
        if name_match or desc_match or tags_match:
            results.append(assoc_dict)
    
    return results

def search_faculties(query: str, faculty: Optional[str] = None):
    """Search faculties by query"""
    query_lower = query.lower()
    results = []
    
    # Get all faculties from database
    faculties_query = FacultyModel.query
    
    # Filter by faculty abbreviation if specified (for filtering by user's faculty)
    if faculty:
        faculties_query = faculties_query.filter_by(abbreviation=faculty)
    
    db_faculties = faculties_query.all()
    
    for fac in db_faculties:
        fac_dict = fac.to_dict()
        # Search in name, abbreviation
        name_match = query_lower in fac_dict.get('name', '').lower()
        abbrev_match = query_lower in fac_dict.get('abbreviation', '').lower()
        address_match = query_lower in fac_dict.get('contacts', {}).get('address', '').lower() if fac_dict.get('contacts') else False
        
        if name_match or abbrev_match or address_match:
            results.append(fac_dict)
    
    return results

@search_bp.route('/search', methods=['GET'])
def search_all():
    """Search both associations and faculties"""
    query = request.args.get('q', '').strip()
    faculty = request.args.get('faculty', '').strip() or None
    
    if not query:
        return jsonify({
            'success': True,
            'query': query,
            'results': {
                'associations': [],
                'faculties': []
            }
        }), 200
    
    associations = search_associations(query, faculty)
    faculties = search_faculties(query, faculty)
    
    return jsonify({
        'success': True,
        'query': query,
        'results': {
            'associations': associations,
            'faculties': faculties
        }
    }), 200

@search_bp.route('/associations', methods=['GET'])
def get_associations():
    """Get all associations, optionally filtered by faculty and search query"""
    faculty = request.args.get('faculty', '').strip() or None
    query = request.args.get('q', '').strip() or None
    
    # Get associations from database
    associations_query = AssociationModel.query
    
    # Filter by faculty
    if faculty:
        associations_query = associations_query.filter_by(faculty=faculty)
    
    # Search by query
    if query:
        results = search_associations(query, faculty)
    else:
        db_associations = associations_query.all()
        results = [assoc.to_dict() for assoc in db_associations]
    
    return jsonify({
        'success': True,
        'count': len(results),
        'items': results
    }), 200

@search_bp.route('/associations/<slug>', methods=['GET'])
def get_association(slug):
    """Get a single association by slug"""
    # Get from database
    db_assoc = AssociationModel.query.filter_by(slug=slug).first()
    if not db_assoc:
        return jsonify({
            'success': False,
            'message': 'Association not found'
        }), 404
    
    return jsonify({
        'success': True,
        'item': db_assoc.to_dict()
    }), 200

@search_bp.route('/faculties', methods=['GET'])
def get_faculties():
    """Get all faculties, optionally filtered by search query"""
    query = request.args.get('q', '').strip() or None
    
    # Get faculties from database
    if query:
        results = search_faculties(query)
    else:
        db_faculties = FacultyModel.query.all()
        results = [fac.to_dict() for fac in db_faculties]
    
    return jsonify({
        'success': True,
        'count': len(results),
        'items': results
    }), 200

@search_bp.route('/faculties/<slug>', methods=['GET'])
def get_faculty(slug):
    """Get a single faculty by slug"""
    # Get from database
    db_faculty = FacultyModel.query.filter_by(slug=slug).first()
    if not db_faculty:
        return jsonify({
            'success': False,
            'message': 'Faculty not found'
        }), 404
    
    return jsonify({
        'success': True,
        'item': db_faculty.to_dict()
    }), 200

