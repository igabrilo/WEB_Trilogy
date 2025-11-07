@echo off
REM Windows batch script for viewing database
REM Usage: view_db.bat

echo ==============================================
echo       UNIZG CAREER HUB - DATABASE VIEWER
echo ==============================================

REM Try psql first
where psql >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using psql direct connection...
    set PGPASSWORD=postgres
    psql -h localhost -U postgres -d unizg_career_hub -c "SELECT 'Korisnici' as Tabela, COUNT(*) as Broj FROM users UNION ALL SELECT 'Poslovi', COUNT(*) FROM jobs UNION ALL SELECT 'Prijave', COUNT(*) FROM job_applications UNION ALL SELECT 'Fakulteti', COUNT(*) FROM faculties UNION ALL SELECT 'Udruzenja', COUNT(*) FROM associations;"
    set PGPASSWORD=
) else (
    echo psql not found. Using Python...
    cd /d "C:\Users\petar\Desktop\WEB_Trilogy\izvorni_kod\backend\src"
    python -c "from app import create_app; from models import *; app = create_app('development'); app.app_context().push(); print('Korisnici:', UserModel.query.count()); print('Poslovi:', JobModel.query.count()); print('Prijave:', JobApplicationModel.query.count()); print('Fakulteti:', FacultyModel.query.count()); print('Udruzenja:', AssociationModel.query.count())"
)

echo ==============================================
pause