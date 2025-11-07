#!/bin/bash
# Quick database viewer script for UNIZG Career Hub
# Usage: ./view_db.sh

echo "=============================================="
echo "      UNIZG CAREER HUB - DATABASE VIEWER"
echo "=============================================="

# Database connection parameters
DB_HOST="localhost"
DB_USER="postgres"
DB_NAME="unizg_career_hub"

# Check if psql is available
if command -v psql &> /dev/null; then
    echo "Using psql direct connection..."
    
    # Set password if needed (you can set PGPASSWORD environment variable)
    # export PGPASSWORD="your_password"
    
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
        SELECT 
            'Korisnici' as Tabela, COUNT(*) as Broj 
        FROM users 
        UNION ALL 
        SELECT 'Poslovi', COUNT(*) FROM jobs 
        UNION ALL 
        SELECT 'Prijave', COUNT(*) FROM job_applications 
        UNION ALL 
        SELECT 'Fakulteti', COUNT(*) FROM faculties 
        UNION ALL 
        SELECT 'Udruženja', COUNT(*) FROM associations;
    "
    
    echo ""
    echo "Detaljni pregled korisnika:"
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
        SELECT id, email, first_name, last_name, role 
        FROM users 
        ORDER BY id;
    "
    
else
    echo "psql not found. Using Python fallback..."
    cd "$(dirname "$0")"
    python3 -c "
from src.app import create_app
from src.models import UserModel, JobModel, JobApplicationModel, FacultyModel, AssociationModel

app = create_app('development')
with app.app_context():
    print(f'Korisnici: {UserModel.query.count()}')
    print(f'Poslovi: {JobModel.query.count()}')
    print(f'Prijave: {JobApplicationModel.query.count()}')
    print(f'Fakulteti: {FacultyModel.query.count()}')
    print(f'Udruženja: {AssociationModel.query.count()}')
    
    print('\nKorisnici:')
    for u in UserModel.query.all():
        print(f'  {u.id}: {u.email} ({u.role})')
"
fi

echo "=============================================="