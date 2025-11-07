#!/usr/bin/env python3
"""
Simple database viewer script
Usage: python view_database.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import create_app
from src.models import UserModel, JobModel, JobApplicationModel, FacultyModel, AssociationModel

def main():
    """View current database contents"""
    try:
        app = create_app('development')
        with app.app_context():
            from flask import current_app
            db = current_app.extensions['sqlalchemy']
            
            print("=" * 60)
            print("           UNIZG CAREER HUB - BAZA PODATAKA")
            print("=" * 60)
            
            # Korisnici
            users = UserModel.query.all()
            print(f"\n👥 KORISNICI ({len(users)}):")
            if users:
                for user in users:
                    print(f"  • ID: {user.id} | {user.email} | {user.first_name} {user.last_name} | {user.role}")
            else:
                print("  (Nema korisnika)")
            
            # Poslovi
            jobs = JobModel.query.all()
            print(f"\n💼 POSLOVI I PRAKSE ({len(jobs)}):")
            if jobs:
                for job in jobs:
                    print(f"  • ID: {job.id} | {job.title} | {job.company} | {job.type} | Kreirao: {job.created_by}")
            else:
                print("  (Nema poslova)")
            
            # Prijave za posao
            applications = JobApplicationModel.query.all()
            print(f"\n📝 PRIJAVE ZA POSAO ({len(applications)}):")
            if applications:
                for app in applications:
                    applicant = app.applicant.email if app.applicant else "Nepoznat"
                    job_title = app.job.title if app.job else "Nepoznat posao"
                    print(f"  • ID: {app.id} | {applicant} → {job_title} | Status: {app.status}")
            else:
                print("  (Nema prijava)")
            
            # Fakulteti
            faculties = FacultyModel.query.all()
            print(f"\n🏛️ FAKULTETI ({len(faculties)}):")
            if faculties:
                for faculty in faculties:
                    print(f"  • ID: {faculty.id} | {faculty.name} | {faculty.slug} | {faculty.type}")
            else:
                print("  (Nema fakulteta)")
            
            # Udruženja
            associations = AssociationModel.query.all()
            print(f"\n🤝 STUDENTSKA UDRUŽENJA ({len(associations)}):")
            if associations:
                for assoc in associations:
                    print(f"  • ID: {assoc.id} | {assoc.name} | Fakultet: {assoc.faculty}")
            else:
                print("  (Nema udruženja)")
            
            print("\n" + "=" * 60)
            print("✅ Database connection successful!")
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()