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
        # Import models first to register them
        from src import models
        # Use the db instance that was initialized with the app
        db = app.extensions['sqlalchemy']
        db.create_all()
    print("Database tables created successfully!")

def seed_database(app):
    """Seed database with sample data"""
    with app.app_context():
        # Import models first to register them with db
        from src import models
        # Use the db instance that was initialized with the app
        db = app.extensions['sqlalchemy']
        
        # Import model classes
        from src.models import (
            UserModel, NotificationModel, FCMTokenModel, FacultyModel,
            AssociationModel, JobModel, JobApplicationModel, ChatSessionModel,
            ErasmusProjectModel, FavoriteFacultyModel
        )
        
        print("Seeding database with sample data...")
        
        # Create all faculties from mock data
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
            },
            {
                'slug': 'efzg',
                'name': 'Ekonomski fakultet',
                'type': 'faculty',
                'abbreviation': 'EFZG',
                'contacts': {
                    'email': 'info@efzg.hr',
                    'phone': '+385 1 2383 333',
                    'address': 'Trg J. F. Kennedyja 6, 10000 Zagreb',
                    'website': 'https://www.efzg.unizg.hr'
                }
            },
            {
                'slug': 'fsb',
                'name': 'Fakultet strojarstva i brodogradnje',
                'type': 'faculty',
                'abbreviation': 'FSB',
                'contacts': {
                    'email': 'info@fsb.hr',
                    'phone': '+385 1 6168 222',
                    'address': 'Ivana Lučića 5, 10000 Zagreb',
                    'website': 'https://www.fsb.unizg.hr'
                }
            },
            {
                'slug': 'grad',
                'name': 'Građevinski fakultet',
                'type': 'faculty',
                'abbreviation': 'GRAD',
                'contacts': {
                    'email': 'info@grad.hr',
                    'phone': '+385 1 4639 200',
                    'address': 'Kačićeva 26, 10000 Zagreb',
                    'website': 'https://www.grad.unizg.hr'
                }
            },
            {
                'slug': 'arhitekt',
                'name': 'Arhitektonski fakultet',
                'type': 'faculty',
                'abbreviation': 'ARH',
                'contacts': {
                    'email': 'info@arhitekt.hr',
                    'phone': '+385 1 4639 000',
                    'address': 'Kačićeva 26, 10000 Zagreb',
                    'website': 'https://www.arhitekt.unizg.hr'
                }
            },
            {
                'slug': 'agr',
                'name': 'Agronomski fakultet',
                'type': 'faculty',
                'abbreviation': 'AGR',
                'contacts': {
                    'email': 'info@agr.hr',
                    'phone': '+385 1 2393 777',
                    'address': 'Svetošimunska cesta 25, 10000 Zagreb',
                    'website': 'https://www.agr.unizg.hr'
                }
            },
            {
                'slug': 'pf',
                'name': 'Pravni fakultet',
                'type': 'faculty',
                'abbreviation': 'PF',
                'contacts': {
                    'email': 'info@pravo.hr',
                    'phone': '+385 1 4896 500',
                    'address': 'Trg Republike Hrvatske 14, 10000 Zagreb',
                    'website': 'https://www.pravo.unizg.hr'
                }
            },
            {
                'slug': 'foi',
                'name': 'Fakultet organizacije i informatike',
                'type': 'faculty',
                'abbreviation': 'FOI',
                'contacts': {
                    'email': 'info@foi.hr',
                    'phone': '+385 1 2457 600',
                    'address': 'Pavlinska 2, 42000 Varaždin',
                    'website': 'https://www.foi.unizg.hr'
                }
            },
            {
                'slug': 'fbf',
                'name': 'Farmaceutsko-biokemijski fakultet',
                'type': 'faculty',
                'abbreviation': 'FBF',
                'contacts': {
                    'email': 'info@fbf.unizg.hr',
                    'phone': '+385 1 6394 400',
                    'address': 'Schrottova 20, 10000 Zagreb',
                    'website': 'https://www.fbf.unizg.hr'
                }
            },
            {
                'slug': 'veterina',
                'name': 'Veterinarski fakultet',
                'type': 'faculty',
                'abbreviation': 'VEF',
                'contacts': {
                    'email': 'info@vef.unizg.hr',
                    'phone': '+385 1 2390 116',
                    'address': 'Heinzelova 55, 10000 Zagreb',
                    'website': 'https://www.vef.unizg.hr'
                }
            },
            {
                'slug': 'kif',
                'name': 'Kineziološki fakultet',
                'type': 'faculty',
                'abbreviation': 'KIF',
                'contacts': {
                    'email': 'dekanat@kif.hr',
                    'phone': '+385 1 3658 677',
                    'address': 'Horvaćanska cesta 15, 10000 Zagreb',
                    'website': 'https://www.kif.unizg.hr'
                }
            },
            {
                'slug': 'rgn',
                'name': 'Rudarsko-geološko-naftni fakultet',
                'type': 'faculty',
                'abbreviation': 'RGN',
                'contacts': {
                    'email': 'info@rgn.unizg.hr',
                    'phone': '+385 1 5535 800',
                    'address': 'Pierottijeva 6, 10000 Zagreb',
                    'website': 'https://www.rgn.unizg.hr'
                }
            },
            {
                'slug': 'tekstil',
                'name': 'Tekstilno-tehnološki fakultet',
                'type': 'faculty',
                'abbreviation': 'TTF',
                'contacts': {
                    'email': 'info@ttf.unizg.hr',
                    'phone': '+385 1 3712 555',
                    'address': 'Prilaz baruna Filipovića 28a, 10000 Zagreb',
                    'website': 'https://www.ttf.unizg.hr'
                }
            },
            {
                'slug': 'kemija',
                'name': 'Fakultet kemijskog inženjerstva i tehnologije',
                'type': 'faculty',
                'abbreviation': 'FKIT',
                'contacts': {
                    'email': 'info@fkit.unizg.hr',
                    'phone': '+385 1 4597 111',
                    'address': 'Marulićev trg 19, 10000 Zagreb',
                    'website': 'https://www.fkit.unizg.hr'
                }
            },
            {
                'slug': 'geodezija',
                'name': 'Geodetski fakultet',
                'type': 'faculty',
                'abbreviation': 'GEOF',
                'contacts': {
                    'email': 'info@geof.hr',
                    'phone': '+385 1 4639 200',
                    'address': 'Kačićeva 26, 10000 Zagreb',
                    'website': 'https://www.geof.unizg.hr'
                }
            },
            {
                'slug': 'promet',
                'name': 'Fakultet prometnih znanosti',
                'type': 'faculty',
                'abbreviation': 'FPZ',
                'contacts': {
                    'email': 'info@fpz.unizg.hr',
                    'phone': '+385 1 2384 222',
                    'address': 'Vukelićeva 4, 10000 Zagreb',
                    'website': 'https://www.fpz.unizg.hr'
                }
            },
            {
                'slug': 'stomatologija',
                'name': 'Stomatološki fakultet',
                'type': 'faculty',
                'abbreviation': 'SFZG',
                'contacts': {
                    'email': 'info@sfzg.hr',
                    'phone': '+385 1 4802 111',
                    'address': 'Gundulićeva 5, 10000 Zagreb',
                    'website': 'https://www.sfzg.unizg.hr'
                }
            },
            {
                'slug': 'medicina',
                'name': 'Medicinski fakultet',
                'type': 'faculty',
                'abbreviation': 'MFZG',
                'contacts': {
                    'email': 'info@mef.hr',
                    'phone': '+385 1 4566 777',
                    'address': 'Šalata 3, 10000 Zagreb',
                    'website': 'https://www.mef.unizg.hr'
                }
            },
            {
                'slug': 'ufzg',
                'name': 'Učiteljski fakultet',
                'type': 'faculty',
                'abbreviation': 'UFZG',
                'contacts': {
                    'email': 'info@ufzg.hr',
                    'phone': '+385 1 2394 300',
                    'address': 'Savska cesta 77, 10000 Zagreb',
                    'website': 'https://www.ufzg.unizg.hr'
                }
            },
            {
                'slug': 'teoloski',
                'name': 'Katolički bogoslovni fakultet',
                'type': 'faculty',
                'abbreviation': 'KBF',
                'contacts': {
                    'email': 'info@kbf.unizg.hr',
                    'phone': '+385 1 4890 577',
                    'address': 'Vlaška 38, 10000 Zagreb',
                    'website': 'https://www.kbf.unizg.hr'
                }
            },
            {
                'slug': 'hrstud',
                'name': 'Hrvatski studiji',
                'type': 'faculty',
                'abbreviation': 'HS',
                'contacts': {
                    'email': 'info@hrstud.unizg.hr',
                    'phone': '+385 1 6112 700',
                    'address': 'Borongajska cesta 83d, 10000 Zagreb',
                    'website': 'https://www.hrstud.unizg.hr'
                }
            },
            {
                'slug': 'pbf',
                'name': 'Prehrambeno-biotehnološki fakultet',
                'type': 'faculty',
                'abbreviation': 'PBF',
                'contacts': {
                    'email': 'info@pbf.unizg.hr',
                    'phone': '+385 1 4605 027',
                    'address': 'Pierottijeva 6, 10000 Zagreb',
                    'website': 'https://www.pbf.unizg.hr'
                }
            },
            {
                'slug': 'simet',
                'name': 'Metalurški fakultet',
                'type': 'faculty',
                'abbreviation': 'SMS',
                'contacts': {
                    'email': 'info@simet.unizg.hr',
                    'phone': '+385 1 5536 400',
                    'address': 'Aleja narodnih heroja 3, 44000 Sisak',
                    'website': 'https://www.simet.unizg.hr'
                }
            },
            {
                'slug': 'sumfak',
                'name': 'Šumarski fakultet',
                'type': 'faculty',
                'abbreviation': 'ŠUMFAK',
                'contacts': {
                    'email': 'info@sumfak.unizg.hr',
                    'phone': '+385 1 2352 533',
                    'address': 'Svetošimunska cesta 25, 10000 Zagreb',
                    'website': 'https://www.sumfak.unizg.hr'
                }
            },
            {
                'slug': 'fpzg',
                'name': 'Fakultet političkih znanosti',
                'type': 'faculty',
                'abbreviation': 'FPZG',
                'contacts': {
                    'email': 'info@fpzg.hr',
                    'phone': '+385 1 4904 888',
                    'address': 'Lepušićeva 6, 10000 Zagreb',
                    'website': 'https://www.fpzg.unizg.hr'
                }
            },
            {
                'slug': 'erf',
                'name': 'Edukacijsko-rehabilitacijski fakultet',
                'type': 'faculty',
                'abbreviation': 'ERF',
                'contacts': {
                    'email': 'info@erf.unizg.hr',
                    'phone': '+385 1 2457 609',
                    'address': 'Borcinska 83f, 10000 Zagreb',
                    'website': 'https://www.erf.unizg.hr'
                }
            },
            {
                'slug': 'grf',
                'name': 'Grafički fakultet',
                'type': 'faculty',
                'abbreviation': 'GF',
                'contacts': {
                    'email': 'info@grf.unizg.hr',
                    'phone': '+385 1 2371 500',
                    'address': 'Getaldićeva 2, 10000 Zagreb',
                    'website': 'https://www.grf.unizg.hr'
                }
            },
            {
                'slug': 'alu',
                'name': 'Akademija likovnih umjetnosti',
                'type': 'academy',
                'abbreviation': 'ALU',
                'contacts': {
                    'email': 'info@alu.unizg.hr',
                    'phone': '+385 1 4828 200',
                    'address': 'Ilica 85, 10000 Zagreb',
                    'website': 'https://www.alu.unizg.hr'
                }
            },
            {
                'slug': 'muza',
                'name': 'Muzička akademija',
                'type': 'academy',
                'abbreviation': 'MA',
                'contacts': {
                    'email': 'info@muza.unizg.hr',
                    'phone': '+385 1 4837 500',
                    'address': 'Trg Republike Hrvatske 12, 10000 Zagreb',
                    'website': 'https://www.muza.unizg.hr'
                }
            },
            {
                'slug': 'adu',
                'name': 'Akademija dramske umjetnosti',
                'type': 'academy',
                'abbreviation': 'ADU',
                'contacts': {
                    'email': 'info@adu.hr',
                    'phone': '+385 1 4871 444',
                    'address': 'Trg Republike Hrvatske 5, 10000 Zagreb',
                    'website': 'https://www.adu.hr'
                }
            }
        ]
        
        faculties_added = 0
        faculties_existing = 0
        for faculty_data in faculties_data:
            existing = db.session.query(FacultyModel).filter_by(slug=faculty_data['slug']).first()
            if not existing:
                faculty = FacultyModel(**faculty_data)
                db.session.add(faculty)
                faculties_added += 1
                print(f"  ✓ Added: {faculty_data['name']} ({faculty_data['slug']})")
            else:
                faculties_existing += 1
        
        db.session.commit()
        total_faculties = db.session.query(FacultyModel).count()
        print(f"\nFaculties: {faculties_added} added, {faculties_existing} already exist, {total_faculties} total in database")
        
        # Create admin user
        admin_email = 'ivan.gabrilo@gmail.com'
        existing_admin = db.session.query(UserModel).filter_by(email=admin_email).first()
        if not existing_admin:
            admin_user = UserModel(
                email=admin_email,
                password='ivan55',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            db.session.add(admin_user)
        
        # Create test faculty user (mock for testing)
        # Using non-faculty email domain so it can use email/password login
        test_faculty_email = 'test-fakultet@example.com'
        existing_faculty = db.session.query(UserModel).filter_by(email=test_faculty_email).first()
        if not existing_faculty:
            test_faculty_user = UserModel(
                email=test_faculty_email,
                password='fakultet123',
                username='FER - Test Fakultet',  # Institutional role uses username
                first_name='FER - Test Fakultet',
                last_name='',
                role='faculty'
            )
            db.session.add(test_faculty_user)
            print(f"  ✓ Added test faculty user: {test_faculty_email} (password: fakultet123)")
        
        # Create all associations from mock data
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
            },
            {
                'slug': 'efsa-fer',
                'name': 'EFSA FER',
                'faculty': 'FER',
                'type': 'academic',
                'logo_text': 'EFSA',
                'logo_bg': '#2d5016',
                'short_description': 'Europska federacija studentskih udruga',
                'description': 'EFSA promiče suradnju između studentskih organizacija diljem Europe.',
                'tags': ['european', 'academic', 'networking'],
                'links': {
                    'website': 'https://efsa.hr'
                }
            },
            {
                'slug': 'ieee-student-branch',
                'name': 'IEEE Student Branch Zagreb',
                'faculty': 'FER',
                'type': 'professional',
                'logo_text': 'IEEE',
                'logo_bg': '#00629b',
                'short_description': 'Profesionalna organizacija za elektrotehničare i računarce',
                'description': 'IEEE Student Branch pruža prilike za profesionalni razvoj i networking u području elektrotehnike i računarstva.',
                'tags': ['professional', 'engineering', 'technology', 'networking'],
                'links': {
                    'website': 'https://ieee.hr',
                    'facebook': 'https://facebook.com/ieeezagreb'
                }
            },
            {
                'slug': 'hackathons-fer',
                'name': 'Hackathons FER',
                'faculty': 'FER',
                'type': 'technical',
                'logo_text': 'HACK',
                'logo_bg': '#1a1a1a',
                'short_description': 'Organizacija hackathona i programerskih natjecanja',
                'description': 'Organiziramo hackathone i programerska natjecanja za studente.',
                'tags': ['hackathon', 'programming', 'competition', 'coding'],
                'links': {
                    'website': 'https://hackathons.fer.hr'
                }
            },
            {
                'slug': 'ffzg-studentski-savjet',
                'name': 'Studentski savjet FFZG',
                'faculty': 'FFZG',
                'type': 'academic',
                'logo_text': 'SS FFZG',
                'logo_bg': '#8b4513',
                'short_description': 'Studentska samouprava Filozofskog fakulteta',
                'description': 'Zastupamo interese studentata Filozofskog fakulteta.',
                'tags': ['student-government', 'academic', 'representation'],
                'links': {
                    'website': 'https://ss.ffzg.hr'
                }
            },
            {
                'slug': 'pmf-studentski-klub',
                'name': 'Studentski klub PMF',
                'faculty': 'PMF',
                'type': 'academic',
                'logo_text': 'SK PMF',
                'logo_bg': '#006400',
                'short_description': 'Studentska organizacija Prirodoslovno-matematičkog fakulteta',
                'description': 'Organiziramo događaje i aktivnosti za studente PMF-a.',
                'tags': ['academic', 'science', 'mathematics', 'events'],
                'links': {
                    'website': 'https://sk.pmf.hr'
                }
            }
        ]
        
        for assoc_data in associations_data:
            existing = db.session.query(AssociationModel).filter_by(slug=assoc_data['slug']).first()
            if not existing:
                association = AssociationModel(**assoc_data)
                db.session.add(association)
        
        # Create test employer user for jobs
        employer_user = db.session.query(UserModel).filter_by(email='employer@test.hr').first()
        if not employer_user:
            # Create user without password first to avoid scrypt issue in Python 3.9
            employer_user = UserModel(
                email='employer@test.hr',
                password=None,  # Set password later
                username='TestPoslodavac',
                role='employer',
                provider='local'
            )
            db.session.add(employer_user)
            db.session.flush()  # Get the ID
            # Set password using pbkdf2 method (works in Python 3.9)
            from werkzeug.security import generate_password_hash
            employer_user.password_hash = generate_password_hash('test123', method='pbkdf2:sha256')
            db.session.commit()
        
        # Create jobs and internships
        jobs_data = [
            {
                'title': 'Backend Developer Internship',
                'description': 'Tražimo studenta za praksu u backend razvoju. Radit ćete na razvoju REST API-ja koristeći Python i Flask. Praksa traje 3 mjeseca, mogućnost zaposlenja nakon prakse.',
                'type': 'internship',
                'company': 'Tech Solutions d.o.o.',
                'location': 'Zagreb, Remote',
                'salary': 'Neplaćeno (praksa)',
                'requirements': [
                    'Poznavanje Python programskog jezika',
                    'Osnovno poznavanje REST API-ja',
                    'Poznavanje Git-a',
                    'Dobar engleski jezik'
                ],
                'tags': ['python', 'flask', 'backend', 'internship', 'remote'],
                'status': 'active',
                'created_by': employer_user.id
            },
            {
                'title': 'Frontend Developer - Junior',
                'description': 'Pozivamo mlade developere da se pridruže našem timu. Radit ćete na modernim web aplikacijama koristeći React i TypeScript. Nudimo mentorstvo i mogućnost profesionalnog razvoja.',
                'type': 'job',
                'company': 'Digital Agency Zagreb',
                'location': 'Zagreb',
                'salary': '8.000 - 12.000 kn',
                'requirements': [
                    'Poznavanje React-a i TypeScript-a',
                    'Iskustvo s CSS i responsive designom',
                    'Poznavanje Git-a',
                    'Komunikacijske vještine'
                ],
                'tags': ['react', 'typescript', 'frontend', 'junior', 'zagreb'],
                'status': 'active',
                'created_by': employer_user.id
            },
            {
                'title': 'Data Science Praksa',
                'description': 'Pružamo priliku studentima da steknu praktično iskustvo u području data science-a. Radit ćete na analizi podataka, izradi modela i vizualizaciji rezultata.',
                'type': 'internship',
                'company': 'Data Analytics Lab',
                'location': 'Zagreb',
                'salary': 'Neplaćeno (praksa)',
                'requirements': [
                    'Poznavanje Python-a (pandas, numpy)',
                    'Osnovno poznavanje statistike',
                    'Interes za machine learning',
                    'Dobar engleski jezik'
                ],
                'tags': ['python', 'data-science', 'machine-learning', 'internship', 'analytics'],
                'status': 'active',
                'created_by': employer_user.id
            },
            {
                'title': 'Full Stack Developer - Part Time',
                'description': 'Tražimo studenta za part-time poziciju full stack developera. Radit ćete na razvoju web aplikacija od frontenda do backenda. Fleksibilno radno vrijeme.',
                'type': 'part-time',
                'company': 'StartupHub',
                'location': 'Zagreb, Hybrid',
                'salary': '4.000 - 6.000 kn',
                'requirements': [
                    'Poznavanje JavaScript-a (Node.js, React)',
                    'Osnovno poznavanje baza podataka',
                    'Mogućnost rada 20h tjedno',
                    'Komunikacijske vještine'
                ],
                'tags': ['javascript', 'nodejs', 'react', 'fullstack', 'part-time', 'hybrid'],
                'status': 'active',
                'created_by': employer_user.id
            },
            {
                'title': 'DevOps Engineer - Remote',
                'description': 'Pozivamo DevOps inženjere da se pridruže našem timu. Radit ćete na automatizaciji deployment procesa, upravljanju cloud infrastrukturom i CI/CD pipeline-ima.',
                'type': 'remote',
                'company': 'Cloud Services Inc.',
                'location': 'Remote',
                'salary': '15.000 - 20.000 kn',
                'requirements': [
                    'Iskustvo s Docker i Kubernetes',
                    'Poznavanje AWS ili Azure',
                    'Poznavanje CI/CD alata (GitHub Actions, GitLab CI)',
                    'Poznavanje Linux-a',
                    'Engleski jezik'
                ],
                'tags': ['devops', 'docker', 'kubernetes', 'aws', 'remote', 'ci-cd'],
                'status': 'active',
                'created_by': employer_user.id
            },
            {
                'title': 'Mobile App Developer Praksa',
                'description': 'Tražimo studente za praksu u razvoju mobilnih aplikacija. Radit ćete na iOS ili Android aplikacijama koristeći moderne tehnologije. Praksa traje 2-3 mjeseca.',
                'type': 'internship',
                'company': 'MobileFirst Solutions',
                'location': 'Zagreb',
                'salary': 'Neplaćeno (praksa)',
                'requirements': [
                    'Poznavanje Swift-a (iOS) ili Kotlin-a (Android)',
                    'Osnovno poznavanje mobile development-a',
                    'Interes za UI/UX design',
                    'Dobar engleski jezik'
                ],
                'tags': ['mobile', 'ios', 'android', 'swift', 'kotlin', 'internship'],
                'status': 'active',
                'created_by': employer_user.id
            },
            {
                'title': 'QA Engineer - Junior',
                'description': 'Tražimo junior QA inženjera za testiranje web i mobilnih aplikacija. Radit ćete na pisanju test planova, izvršavanju testova i prijavljivanju bugova.',
                'type': 'job',
                'company': 'Quality Assurance Pro',
                'location': 'Zagreb',
                'salary': '7.000 - 10.000 kn',
                'requirements': [
                    'Poznavanje testiranja softvera',
                    'Osnovno poznavanje programiranja',
                    'Pažljivost i analitičko razmišljanje',
                    'Komunikacijske vještine'
                ],
                'tags': ['qa', 'testing', 'quality-assurance', 'junior', 'zagreb'],
                'status': 'active',
                'created_by': employer_user.id
            },
            {
                'title': 'UI/UX Designer Praksa',
                'description': 'Pružamo priliku studentima dizajna da steknu praktično iskustvo u UI/UX dizajnu. Radit ćete na dizajnu web i mobilnih aplikacija koristeći Figma.',
                'type': 'internship',
                'company': 'Design Studio Zagreb',
                'location': 'Zagreb',
                'salary': 'Neplaćeno (praksa)',
                'requirements': [
                    'Poznavanje Figma ili Adobe XD',
                    'Osnovno poznavanje UI/UX principa',
                    'Portfolio s primjerima radova',
                    'Kreativnost i pažljivost'
                ],
                'tags': ['ui-ux', 'design', 'figma', 'internship', 'creative'],
                'status': 'active',
                'created_by': employer_user.id
            }
        ]
        
        for job_data in jobs_data:
            existing = db.session.query(JobModel).filter_by(
                title=job_data['title'],
                company=job_data['company']
            ).first()
            if not existing:
                job = JobModel(**job_data)
                db.session.add(job)
        
        db.session.commit()
        print("Database seeded successfully!")

def reset_database(app):
    """Reset database (drop and recreate)"""
    print("Dropping all tables...")
    with app.app_context():
        # Import models first to register them
        from src import models
        # Use the db instance that was initialized with the app
        db = app.extensions['sqlalchemy']
        db.drop_all()
    
    print("Creating new tables...")
    with app.app_context():
        from src import models
        # Use the db instance that was initialized with the app
        db = app.extensions['sqlalchemy']
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