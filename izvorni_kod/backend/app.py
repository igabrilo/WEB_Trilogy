from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Secret key for JWT (in production, use environment variable)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# In-memory database (replace with real database in production)
users_db = []
user_id_counter = 1

# Demo in-memory data for student associations
associations_db = [
    {
        "id": 1,
        "slug": "eestec-fer",
        "name": "EESTEC LC Zagreb",
        "faculty": "FER",
        "type": "student_association",
        "logoText": "EESTEC",
        "logoBg": "#e11d48",
        "shortDescription": "Europsko udruženje studenata elektrotehnike – lokalni komitet Zagreb.",
        "description": "EESTEC LC Zagreb okuplja studente FER-a zainteresirane za inženjerstvo, radionice i međunarodnu suradnju.",
        "tags": ["FER", "elektrotehnika", "workshop", "networking"],
        "links": {
            "website": "https://eestec.hr",
            "instagram": "https://instagram.com/eestec_zagreb"
        }
    },
    {
        "id": 2,
        "slug": "best-zagreb",
        "name": "BEST Zagreb",
        "faculty": "FER",
        "type": "student_association",
        "logoText": "BEST",
        "logoBg": "#f59e0b",
        "shortDescription": "Board of European Students of Technology – lokalna grupa Zagreb.",
        "description": "BEST Zagreb organizira tečajeve, inženjerska natjecanja i događaje za studente tehničkih fakulteta.",
        "tags": ["FER", "tehnologija", "natjecanja", "tečajevi"],
        "links": {
            "website": "https://best.hr",
            "instagram": "https://instagram.com/bestzagreb"
        }
    },
    {
        "id": 3,
        "slug": "kset",
        "name": "KSET",
        "faculty": "FER",
        "type": "student_association",
        "logoText": "KSET",
        "logoBg": "#1d4ed8",
        "shortDescription": "Klub studenata elektrotehnike – kulturni i tehnički događaji.",
        "description": "KSET je studentski klub FER-a poznat po koncertima, tech radionicama i druženjima.",
        "tags": ["FER", "kultura", "koncerti", "radionice"],
        "links": {
            "website": "https://www.kset.org/"
        }
    },
    {
        "id": 4,
        "slug": "ieee-sb-zagreb",
        "name": "IEEE Student Branch Zagreb",
        "faculty": "FER",
        "type": "student_association",
        "logoText": "IEEE",
        "logoBg": "#0ea5e9",
        "shortDescription": "IEEE studentska sekcija – predavanja, natjecanja i umrežavanje.",
        "description": "IEEE SB Zagreb okuplja studente zainteresirane za elektroniku, računarstvo i STEM projekte.",
        "tags": ["FER", "IEEE", "STEM", "natjecanja"],
        "links": {
            "website": "https://ieee.fer.hr/"
        }
    },
]

# Faculties/Academies dataset (subset; extend as needed)
faculties_db = [
    # Fakulteti
    {"slug": "agronomski", "name": "Agronomski fakultet", "abbreviation": "AGR", "type": "faculty", "contacts": {"website": "https://www.agr.hr", "email": "dekanat@agr.hr", "phone": "+385 1 239 37 77", "address": "Svetošimunska 25, 10000 Zagreb"}},
    {"slug": "arhitektonski", "name": "Arhitektonski fakultet", "abbreviation": "AF", "type": "faculty", "contacts": {"website": "https://www.arhitekt.hr", "email": "dekan@arhitekt.hr", "phone": "+385 1 463 92 22", "address": "Fra Andrije Kačića Miošića 26, 10000 Zagreb"}},
    {"slug": "erf", "name": "Edukacijsko-rehabilitacijski fakultet", "abbreviation": "ERF", "type": "faculty", "contacts": {"website": "https://www.erf.hr", "email": "dekan@erf.hr", "phone": "+385 1 245 75 00", "address": "Borongajska cesta 83f, 10000 Zagreb"}},
    {"slug": "efzg", "name": "Ekonomski fakultet", "abbreviation": "EFZG", "type": "faculty", "contacts": {"website": "https://www.efzg.hr", "email": "dean@efzg.hr", "phone": "+385 1 238 33 33", "address": "Kennedyjev trg 6, 10000 Zagreb"}},
    {"slug": "fer", "name": "Fakultet elektrotehnike i računarstva", "abbreviation": "FER", "type": "faculty", "contacts": {"website": "https://www.fer.hr", "email": "dekanat@fer.hr", "phone": "+385 1 612 99 99", "address": "Unska 3, 10000 Zagreb"}},
    {"slug": "ffrz", "name": "Fakultet filozofije i religijskih znanosti", "abbreviation": "FFRZ", "type": "faculty", "contacts": {"website": "https://www.ffrz.hr", "email": "dekan@ffrz.unizg.hr", "phone": "+385 1 2354 222", "address": "Jordanovac 110, 10000 Zagreb"}},
    {"slug": "hrstud", "name": "Fakultet hrvatskih studija", "abbreviation": "FHS", "type": "faculty", "contacts": {"website": "https://www.hrstud.hr", "email": "dekanov.ured@hrstud.hr", "phone": "+385 1 2457 600", "address": "Borongajska cesta 83d, 10000 Zagreb"}},
    {"slug": "fkit", "name": "Fakultet kemijskog inženjerstva i tehnologije", "abbreviation": "FKIT", "type": "faculty", "contacts": {"website": "https://www.fkit.hr", "email": "office@fkit.hr", "phone": "+385 1 459 72 81", "address": "Marulićev trg 19, 10000 Zagreb"}},
    {"slug": "foi", "name": "Fakultet organizacije i informatike", "abbreviation": "FOI", "type": "faculty", "contacts": {"website": "https://www.foi.unizg.hr", "email": "ured-dekana@foi.hr", "phone": "+385 42 390 800", "address": "Pavlinska 2, 42000 Varaždin"}},
    {"slug": "fpzg", "name": "Fakultet političkih znanosti", "abbreviation": "FPZG", "type": "faculty", "contacts": {"website": "https://www.fpzg.hr", "email": "dekanat@fpzg.hr", "phone": "+385 1 464 20 00", "address": "Lepušićeva 6, 10000 Zagreb"}},
    {"slug": "fpz", "name": "Fakultet prometnih znanosti", "abbreviation": "FPZ", "type": "faculty", "contacts": {"website": "https://www.fpz.unizg.hr", "email": "dekan@fpz.hr", "phone": "+385 1 238 02 22", "address": "Vukelićeva 4, 10000 Zagreb"}},
    {"slug": "fsb", "name": "Fakultet strojarstva i brodogradnje", "abbreviation": "FSB", "type": "faculty", "contacts": {"website": "https://www.fsb.unizg.hr", "email": "fsb@fsb.hr", "phone": "+385 1 616 82 22", "address": "Ivana Lučića 5, 10000 Zagreb"}},
    {"slug": "sumarski", "name": "Fakultet šumarstva i drvne tehnologije", "abbreviation": "ŠFDT", "type": "faculty", "contacts": {"website": "https://www.sumfak.hr", "email": "jmargaletic@sumfak.unizg.hr", "phone": "+385 1 235 25 55", "address": "Svetošimunska 25, 10000 Zagreb"}},
    {"slug": "fbf", "name": "Farmaceutsko-biokemijski fakultet", "abbreviation": "FBF", "type": "faculty", "contacts": {"website": "https://www.pharma.hr", "email": "dekanat@pharma.hr", "phone": "+385 1 481 82 88", "address": "Ante Kovačića 1, 10000 Zagreb"}},
    {"slug": "ffzg", "name": "Filozofski fakultet", "abbreviation": "FFZG", "type": "faculty", "contacts": {"website": "https://www.ffzg.unizg.hr", "email": "dekan@ffzg.hr", "phone": "+385 1 40 92 017", "address": "Ivana Lučića 3, 10000 Zagreb"}},
    {"slug": "geodetski", "name": "Geodetski fakultet", "abbreviation": "GEOF", "type": "faculty", "contacts": {"website": "https://www.geof.hr", "email": "dekan@geof.hr", "phone": "+385 1 463 92 22", "address": "Kačićeva 26, 10000 Zagreb"}},
    {"slug": "gfv", "name": "Geotehnički fakultet", "abbreviation": "GFV", "type": "faculty", "contacts": {"website": "https://www.gfv.unizg.hr", "email": "ured.dekana@gfv.hr", "phone": "+385 42 408 900", "address": "Hallerova aleja 7, 42000 Varaždin"}},
    {"slug": "gradjevinski", "name": "Građevinski fakultet", "abbreviation": "GF", "type": "faculty", "contacts": {"website": "https://www.grad.hr", "email": "ured_dekana@grad.hr", "phone": "+385 1 463 92 22", "address": "Fra Andrije Kačića Miošića 26, 10000 Zagreb"}},
    {"slug": "graficki", "name": "Grafički fakultet", "abbreviation": "GRF", "type": "faculty", "contacts": {"website": "https://www.grf.hr", "email": "dekan@grf.hr", "phone": "+385 1 237 10 80", "address": "Getaldićeva 2, 10000 Zagreb"}},
    {"slug": "kbf", "name": "Katolički bogoslovni fakultet", "abbreviation": "KBF", "type": "faculty", "contacts": {"website": "https://www.kbf.hr", "email": "ured@kbf.hr", "phone": "+385 1 489 04 00", "address": "Vlaška 38, 10000 Zagreb"}},
    {"slug": "kif", "name": "Kineziološki fakultet", "abbreviation": "KIF", "type": "faculty", "contacts": {"website": "https://www.kif.hr", "email": "dekanat@kif.hr", "phone": "+385 1 365 86 66", "address": "Horvaćanski zavoj 15, 10000 Zagreb"}},
    {"slug": "mef", "name": "Medicinski fakultet", "abbreviation": "MEF", "type": "faculty", "contacts": {"website": "https://www.mef.unizg.hr", "email": "mf@mef.hr", "phone": "+385 1 456 67 77", "address": "Šalata 3b, 10000 Zagreb"}},
    {"slug": "metalurski", "name": "Metalurški fakultet", "abbreviation": "SIMET", "type": "faculty", "contacts": {"website": "https://www.simet.hr", "email": "dekanat@simet.hr", "phone": "+385 44 533 380", "address": "Aleja narodnih heroja 3, 44000 Sisak"}},
    {"slug": "pravni", "name": "Pravni fakultet", "abbreviation": "PRAVO", "type": "faculty", "contacts": {"website": "https://www.pravo.unizg.hr", "email": "dekanat@pravo.hr", "phone": "+385 1 456 43 27", "address": "Trg Republike Hrvatske 14, 10000 Zagreb"}},
    {"slug": "pbf", "name": "Prehrambeno-biotehnološki fakultet", "abbreviation": "PBF", "type": "faculty", "contacts": {"website": "https://www.pbf.hr", "email": "dekan@pbf.hr", "phone": "+385 1 460 50 00", "address": "Pierottijeva 6, 10000 Zagreb"}},
    {"slug": "pmf", "name": "Prirodoslovno-matematički fakultet", "abbreviation": "PMF", "type": "faculty", "contacts": {"website": "https://www.pmf.hr", "email": "dekanat@dekanat.pmf.hr", "phone": "+385 1 460 60 00", "address": "Horvatovac 102a, 10000 Zagreb"}},
    {"slug": "rgn", "name": "Rudarsko-geološko-naftni fakultet", "abbreviation": "RGNF", "type": "faculty", "contacts": {"website": "https://www.rgn.hr", "email": "dekanat@rgn.hr", "phone": "+385 1 553 57 00", "address": "Pierottijeva 6, 10000 Zagreb"}},
    {"slug": "sfzg", "name": "Stomatološki fakultet", "abbreviation": "SFZG", "type": "faculty", "contacts": {"website": "https://www.sfzg.hr", "email": "dekanat@sfzg.hr", "phone": "+385 1 480 21 11", "address": "Gundulićeva 5, 10000 Zagreb"}},
    {"slug": "ttf", "name": "Tekstilno-tehnološki fakultet", "abbreviation": "TTF", "type": "faculty", "contacts": {"website": "https://www.ttf.unizg.hr", "email": "fakultet@ttf.hr", "phone": "+385 1 371 25 00", "address": "Prilaz baruna Filipovića 28a, 10000 Zagreb"}},
    {"slug": "ufzg", "name": "Učiteljski fakultet", "abbreviation": "UFZG", "type": "faculty", "contacts": {"website": "https://www.ufzg.unizg.hr", "email": "dekanat@ufzg.hr", "phone": "+385 1 632 73 00", "address": "Savska cesta 77, 10000 Zagreb"}},
    {"slug": "vef", "name": "Veterinarski fakultet", "abbreviation": "VEF", "type": "faculty", "contacts": {"website": "https://www.vef.hr", "email": "dekan@vef.hr", "phone": "+385 1 239 01 11", "address": "Heinzelova 55, 10000 Zagreb"}},

    # Akademije
    {"slug": "adu", "name": "Akademija dramske umjetnosti", "abbreviation": "ADU", "type": "academy", "contacts": {"website": "https://www.adu.hr", "email": "dekanat@adu.hr", "phone": "+385 1 482 85 06", "address": "Trg Republike Hrvatske 5, 10000 Zagreb"}},
    {"slug": "alu", "name": "Akademija likovnih umjetnosti", "abbreviation": "ALU", "type": "academy", "contacts": {"website": "https://www.alu.hr", "email": "alu@alu.hr", "phone": "+385 1 377 73 00", "address": "Ilica 85, 10000 Zagreb"}},
    {"slug": "muza", "name": "Muzička akademija", "abbreviation": "MUZA", "type": "academy", "contacts": {"website": "https://www.muza.hr", "email": "muza@muza.hr", "phone": "+385 1 482 01 00", "address": "Trg Republike Hrvatske 12, 10000 Zagreb"}},
]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = next((u for u in users_db if u['id'] == data['user_id']), None)
        except:
            return jsonify({'success': False, 'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/")
def home():
    return jsonify({"message": "Hello, Flask API!"})

@app.route("/api/auth/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'firstName', 'lastName']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Field {field} is required'
                }), 400
        
        # Check if user already exists
        if any(user['email'] == data['email'] for user in users_db):
            return jsonify({
                'success': False,
                'message': 'User with this email already exists'
            }), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Create new user
        global user_id_counter
        new_user = {
            'id': user_id_counter,
            'email': data['email'],
            'password': generate_password_hash(data['password']),
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'role': data.get('role', 'student'),
            'faculty': data.get('faculty'),
            'interests': data.get('interests', []),
            'created_at': datetime.datetime.now().isoformat()
        }
        users_db.append(new_user)
        user_id_counter += 1
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': new_user['id'],
            'email': new_user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Return user data (without password)
        user_response = {
            'id': new_user['id'],
            'email': new_user['email'],
            'firstName': new_user['firstName'],
            'lastName': new_user['lastName'],
            'role': new_user['role'],
            'faculty': new_user.get('faculty'),
            'interests': new_user.get('interests', [])
        }
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user_response,
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@app.route("/api/auth/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user = next((u for u in users_db if u['email'] == data['email']), None)
        
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Return user data (without password)
        user_response = {
            'id': user['id'],
            'email': user['email'],
            'firstName': user['firstName'],
            'lastName': user['lastName'],
            'role': user['role'],
            'faculty': user.get('faculty'),
            'interests': user.get('interests', [])
        }
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_response,
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@app.route("/api/auth/me", methods=['GET'])
@token_required
def get_current_user(current_user):
    user_response = {
        'id': current_user['id'],
        'email': current_user['email'],
        'firstName': current_user['firstName'],
        'lastName': current_user['lastName'],
        'role': current_user['role'],
        'faculty': current_user.get('faculty'),
        'interests': current_user.get('interests', [])
    }
    return jsonify(user_response), 200


@app.route("/api/faculties", methods=['GET'])
def list_faculties():
    q = request.args.get('q', '').strip().lower()
    items = faculties_db
    if q:
        def match(f):
            text = ' '.join([
                f.get('name', ''),
                f.get('abbreviation', ''),
                (f.get('contacts', {}) or {}).get('address', '') or ''
            ]).lower()
            return q in text
        items = [f for f in items if match(f)]
    return jsonify({'success': True, 'count': len(items), 'items': items}), 200


@app.route("/api/faculties/<slug>", methods=['GET'])
def get_faculty(slug: str):
    item = next((f for f in faculties_db if f['slug'] == slug), None)
    if not item:
        return jsonify({'success': False, 'message': 'Faculty not found'}), 404
    return jsonify({'success': True, 'item': item}), 200


@app.route("/api/associations", methods=['GET'])
def list_associations():
    """List associations with optional filters: faculty, q (search)."""
    faculty = request.args.get('faculty')
    q = request.args.get('q', '').strip().lower()

    results = associations_db
    if faculty:
        results = [a for a in results if a.get('faculty', '').lower() == faculty.lower()]
    if q:
        def match(a):
            text = ' '.join([
                a.get('name', ''),
                a.get('shortDescription', ''),
                a.get('description', ''),
                ' '.join(a.get('tags', []))
            ]).lower()
            return q in text
        results = [a for a in results if match(a)]

    return jsonify({
        'success': True,
        'count': len(results),
        'items': results
    }), 200


@app.route("/api/associations/<slug>", methods=['GET'])
def get_association(slug: str):
    assoc = next((a for a in associations_db if a['slug'] == slug), None)
    if not assoc:
        return jsonify({'success': False, 'message': 'Association not found'}), 404
    return jsonify({'success': True, 'item': assoc}), 200


@app.route("/api/search", methods=['GET'])
def search_all():
    """Simple search across available entities (currently associations only)."""
    q = request.args.get('q', '').strip().lower()
    faculty = request.args.get('faculty')

    assoc_results = associations_db
    if faculty:
        assoc_results = [a for a in assoc_results if a.get('faculty', '').lower() == faculty.lower()]
    if q:
        def match(a):
            text = ' '.join([
                a.get('name', ''),
                a.get('shortDescription', ''),
                a.get('description', ''),
                ' '.join(a.get('tags', []))
            ]).lower()
            return q in text
        assoc_results = [a for a in assoc_results if match(a)]

    faculty_results = faculties_db
    if q:
        def fmatch(f):
            contacts = (f.get('contacts', {}) or {})
            text = ' '.join([
                f.get('name', ''),
                f.get('abbreviation', ''),
                contacts.get('address', '') or '',
                contacts.get('website', '') or '',
                contacts.get('email', '') or '',
                contacts.get('phone', '') or ''
            ]).lower()
            return q in text
        faculty_results = [f for f in faculty_results if fmatch(f)]

    return jsonify({
        'success': True,
        'query': q,
        'results': {
            'associations': assoc_results,
            'faculties': faculty_results,
        }
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
