from flask import Blueprint, request, jsonify, current_app

# Support both absolute and relative imports
try:
    from models import FavoriteFacultyModel, FacultyModel
    from oauth2_service import OAuth2Service
    from database import db
except ImportError:
    from ..models import FavoriteFacultyModel, FacultyModel
    from ..oauth2_service import OAuth2Service
    from ..database import db

favorites_bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')

def get_db():
    """Get db instance from current app"""
    return current_app.extensions['sqlalchemy']

def init_favorites_routes(oauth_service):
    """Initialize favorites routes with services"""
    
    @favorites_bp.route('/faculties', methods=['POST'])
    @oauth_service.token_required
    def add_favorite_faculty(current_user_id, current_user_email, current_user_role):
        """Add a faculty to user's favorites (only for ucenik and student)"""
        try:
            # Check if user is ucenik or student
            if current_user_role not in ['ucenik', 'student']:
                return jsonify({
                    'success': False,
                    'message': 'Only students and ucenik can favorite faculties'
                }), 403
            
            data = request.get_json()
            faculty_slug = data.get('facultySlug')
            
            if not faculty_slug:
                return jsonify({
                    'success': False,
                    'message': 'facultySlug is required'
                }), 400
            
            # Verify faculty exists
            faculty = get_db().session.query(FacultyModel).filter_by(slug=faculty_slug).first()
            if not faculty:
                return jsonify({
                    'success': False,
                    'message': 'Faculty not found'
                }), 404
            
            # Check if already favorited
            existing = get_db().session.query(FavoriteFacultyModel).filter_by(
                user_id=current_user_id,
                faculty_slug=faculty_slug
            ).first()
            
            if existing:
                return jsonify({
                    'success': False,
                    'message': 'Faculty is already in your favorites'
                }), 400
            
            # Create favorite
            favorite = FavoriteFacultyModel.create(current_user_id, faculty_slug)
            
            return jsonify({
                'success': True,
                'message': 'Faculty added to favorites',
                'item': favorite.to_dict()
            }), 201
            
        except Exception as e:
            get_db().session.rollback()
            return jsonify({
                'success': False,
                'message': f'Failed to add favorite: {str(e)}'
            }), 500
    
    @favorites_bp.route('/faculties', methods=['GET'])
    @oauth_service.token_required
    def get_favorite_faculties(current_user_id, current_user_email, current_user_role):
        """Get user's favorite faculties"""
        try:
            favorites = get_db().session.query(FavoriteFacultyModel).filter_by(user_id=current_user_id).all()
            favorites_list = [fav.to_dict() for fav in favorites]
            
            return jsonify({
                'success': True,
                'count': len(favorites_list),
                'items': favorites_list
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get favorites: {str(e)}'
            }), 500
    
    @favorites_bp.route('/faculties/<faculty_slug>', methods=['DELETE'])
    @oauth_service.token_required
    def remove_favorite_faculty(faculty_slug, current_user_id, current_user_email, current_user_role):
        """Remove a faculty from user's favorites"""
        try:
            favorite = get_db().session.query(FavoriteFacultyModel).filter_by(
                user_id=current_user_id,
                faculty_slug=faculty_slug
            ).first()
            
            if not favorite:
                return jsonify({
                    'success': False,
                    'message': 'Favorite not found'
                }), 404
            
            favorite.delete()
            
            return jsonify({
                'success': True,
                'message': 'Faculty removed from favorites'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to remove favorite: {str(e)}'
            }), 500
    
    @favorites_bp.route('/faculties/<faculty_slug>/check', methods=['GET'])
    @oauth_service.token_required
    def check_favorite_faculty(faculty_slug, current_user_id, current_user_email, current_user_role):
        """Check if a faculty is in user's favorites"""
        try:
            favorite = get_db().session.query(FavoriteFacultyModel).filter_by(
                user_id=current_user_id,
                faculty_slug=faculty_slug
            ).first()
            
            return jsonify({
                'success': True,
                'isFavorite': favorite is not None
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to check favorite: {str(e)}'
            }), 500

