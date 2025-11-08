#!/usr/bin/env python3
"""
Entry point for running the Flask application
"""
import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Import app after adding src to path
# Type checking: app is in src/app.py
if True:  # Always executed, but helps type checker
    from src.app import create_app  # Import from src package

app = create_app()

# Application instance for gunicorn
application = app

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)

