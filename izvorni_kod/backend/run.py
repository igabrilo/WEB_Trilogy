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
    from app import create_app  # type: ignore[import-untyped]

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

