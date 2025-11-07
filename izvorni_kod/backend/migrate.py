"""
Database migration utility
Run this script to initialize the database with sample data
"""
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def init_database(app):
    """Initialize database with tables"""
    print("Creating database tables...")
    with app.app_context():
        # Get the db instance from the app
        from flask import current_app
        db = current_app.extensions['sqlalchemy']
        db.create_all()
    print("Database tables created successfully!")

def seed_database(app):
    """Seed database with sample data"""
    with app.app_context():
        # Get the db instance from the app
        from flask import current_app
        db = current_app.extensions['sqlalchemy']
        
        # Import models within app context to avoid redefinition
        from src.models import (
            UserModel, NotificationModel, FCMTokenModel, FacultyModel,
            AssociationModel, JobModel, JobApplicationModel, ChatSessionModel
        )
        
        print("Seeding database with sample data...")
        
        # Create sample faculties
        faculties_data = [
            {
                'slug': 'fer',
                'name': 'Fakultet elektrotehnike i računarstva',
                'type': 'faculty',
                'abbreviation': 'FER',
                'contacts': {
                    'email': 'info@fer.hr',
                    'phone': '+385 1 6129 700',
                    'address': 'Unska 3, 10000 Zagreb',
                    'website': 'https://www.fer.unizg.hr'
                }
            },
            {
                'slug': 'ffzg',
                'name': 'Filozofski fakultet',
                'type': 'faculty',
                'abbreviation': 'FFZG',
                'contacts': {
                    'email': 'info@ffzg.hr',
                    'phone': '+385 1 4092 100',
                    'address': 'Ivana Lučića 3, 10000 Zagreb',
                    'website': 'https://www.ffzg.unizg.hr'
                }
            },
            {
                'slug': 'pmf',
                'name': 'Prirodoslovno-matematički fakultet',
                'type': 'faculty',
                'abbreviation': 'PMF',
                'contacts': {
                    'email': 'info@pmf.hr',
                    'phone': '+385 1 4605 900',
                    'address': 'Horvatovac 102a, 10000 Zagreb',
                    'website': 'https://www.pmf.unizg.hr'
                }
            }
        ]
        
        for faculty_data in faculties_data:
            existing = FacultyModel.query.filter_by(slug=faculty_data['slug']).first()
            if not existing:
                faculty = FacultyModel(**faculty_data)
                db.session.add(faculty)
        
        # Create admin user
        admin_email = 'ivan.gabrilo@gmail.com'
        existing_admin = UserModel.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin_user = UserModel(
                email=admin_email,
                password='ivan55',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            db.session.add(admin_user)
        
        # Create sample associations
        associations_data = [
            {
                'slug': 'aiesec-fer',
                'name': 'AIESEC FER',
                'faculty': 'FER',
                'type': 'international',
                'logo_text': 'AIESEC',
                'logo_bg': '#1e70bf',
                'short_description': 'Međunarodna studentska organizacija za razvoj mladih lidera',
                'description': 'AIESEC je najveća studentska organizacija na svijetu koja pruža prilike za međunarodnu razmjenu i razvoj vještina.',
                'tags': ['leadership', 'international', 'exchange', 'networking'],
                'links': {
                    'website': 'https://aiesec.hr',
                    'facebook': 'https://facebook.com/aiesecfer',
                    'instagram': 'https://instagram.com/aiesecfer'
                }
            },
            {
                'slug': 'best-fer',
                'name': 'BEST Zagreb',
                'faculty': 'FER',
                'type': 'academic',
                'logo_text': 'BEST',
                'logo_bg': '#ff6b35',
                'short_description': 'Studentska organizacija za tehničke studente',
                'description': 'BEST pruža prilike za razvoj tehničkih vještina kroz razne projekte i događaje.',
                'tags': ['technical', 'engineering', 'workshops', 'competitions'],
                'links': {
                    'website': 'https://best.hr',
                    'facebook': 'https://facebook.com/bestzagreb'
                }
            }
        ]
        
        for assoc_data in associations_data:
            existing = AssociationModel.query.filter_by(slug=assoc_data['slug']).first()
            if not existing:
                association = AssociationModel(**assoc_data)
                db.session.add(association)
        
        db.session.commit()
        print("Database seeded successfully!")

def reset_database(app):
    """Reset database (drop and recreate)"""
    print("Dropping all tables...")
    with app.app_context():
        # Get the db instance from the app
        from flask import current_app
        db = current_app.extensions['sqlalchemy']
        db.drop_all()
    
    print("Creating new tables...")
    with app.app_context():
        # Get the db instance from the app
        from flask import current_app
        db = current_app.extensions['sqlalchemy']
        db.create_all()
    print("Database reset successfully!")

if __name__ == '__main__':
    from src.app import create_app
    app = create_app('development')
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        with app.app_context():
            if command == 'init':
                init_database(app)
            elif command == 'seed':
                seed_database(app)
            elif command == 'reset':
                reset_database(app)
                seed_database(app)
            else:
                print("Available commands: init, seed, reset")
    else:
        print("Usage: python migrate.py [init|seed|reset]")
        print("  init  - Create database tables")
        print("  seed  - Add sample data")
        print("  reset - Drop and recreate tables with sample data")