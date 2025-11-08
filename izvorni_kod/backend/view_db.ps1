# PowerShell script for viewing UNIZG Career Hub database
# Usage: .\view_db.ps1

Write-Host "=============================================="
Write-Host "      UNIZG CAREER HUB - DATABASE VIEWER"
Write-Host "=============================================="

# Database connection parameters
$DB_HOST = "localhost"
$DB_USER = "postgres" 
$DB_NAME = "unizg_career_hub"
$DB_PASSWORD = "postgres"  # Change this to your password

# Check if psql is available
$psqlPath = Get-Command psql -ErrorAction SilentlyContinue

if ($psqlPath) {
    Write-Host "Using psql direct connection..."
    
    # Set environment variable for password
    $env:PGPASSWORD = $DB_PASSWORD
    
    # Quick count query
    $countQuery = @"
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
        SELECT 'Udruzenja', COUNT(*) FROM associations;
"@
    
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c $countQuery
    
    Write-Host ""
    Write-Host "Detaljni pregled korisnika:"
    
    $userQuery = "SELECT id, email, first_name, last_name, role FROM users ORDER BY id;"
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c $userQuery
    
    # Clear password from environment
    Remove-Item Env:PGPASSWORD
    
} else {
    Write-Host "psql not found. Using Python fallback..."
    
    # Change to backend directory
    Set-Location "C:\Users\petar\Desktop\WEB_Trilogy\izvorni_kod\backend\src"
    
    # Python one-liner
    python -c @"
from app import create_app
from models import UserModel, JobModel, JobApplicationModel, FacultyModel, AssociationModel

app = create_app('development')
with app.app_context():
    print(f'Korisnici: {UserModel.query.count()}')
    print(f'Poslovi: {JobModel.query.count()}')
    print(f'Prijave: {JobApplicationModel.query.count()}')
    print(f'Fakulteti: {FacultyModel.query.count()}')
    print(f'Udruzenja: {AssociationModel.query.count()}')
    
    print('\nKorisnici:')
    for u in UserModel.query.all():
        print(f'  {u.id}: {u.email} ({u.role})')
"@
}

Write-Host "=============================================="