"""
Database configuration and setup
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy extension
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    migrate.init_app(app, db)
    return db

def create_tables(app, db_instance=None):
    """Create all database tables"""
    if db_instance is None:
        db_instance = db
    with app.app_context():
        db_instance.create_all()

def drop_tables(app, db_instance=None):
    """Drop all database tables (use carefully!)"""
    if db_instance is None:
        db_instance = db
    with app.app_context():
        db_instance.drop_all()