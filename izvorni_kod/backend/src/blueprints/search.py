from flask import Blueprint, request, jsonify

search_bp = Blueprint('search', __name__, url_prefix='/api')

# Mock data for associations (in production, this would come from a database)
ASSOCIATIONS_DATA = [
    {
        'id': 1,
        'slug': 'aiesec-fer',
        'name': 'AIESEC FER',
        'faculty': 'FER',
        'type': 'international',
        'logoText': 'AIESEC',
        'logoBg': '#1e70bf',
        'shortDescription': 'Međunarodna studentska organizacija za razvoj mladih lidera',
        'description': 'AIESEC je najveća studentska organizacija na svijetu koja pruža prilike za međunarodnu razmjenu i razvoj vještina.',
        'tags': ['leadership', 'international', 'exchange', 'networking'],
        'links': {
            'website': 'https://aiesec.hr',
            'facebook': 'https://facebook.com/aiesecfer',
            'instagram': 'https://instagram.com/aiesecfer'
        }
    },
    {
        'id': 2,
        'slug': 'best-fer',
        'name': 'BEST Zagreb',
        'faculty': 'FER',
        'type': 'academic',
        'logoText': 'BEST',
        'logoBg': '#ff6b35',
        'shortDescription': 'Studentska organizacija za tehničke studente',
        'description': 'BEST pruža prilike za razvoj tehničkih vještina kroz razne projekte i događaje.',
        'tags': ['technical', 'engineering', 'workshops', 'competitions'],
        'links': {
            'website': 'https://best.hr',
            'facebook': 'https://facebook.com/bestzagreb'
        }
    },
    {
        'id': 3,
        'slug': 'efsa-fer',
        'name': 'EFSA FER',
        'faculty': 'FER',
        'type': 'academic',
        'logoText': 'EFSA',
        'logoBg': '#2d5016',
        'shortDescription': 'Europska federacija studentskih udruga',
        'description': 'EFSA promiče suradnju između studentskih organizacija diljem Europe.',
        'tags': ['european', 'academic', 'networking'],
        'links': {
            'website': 'https://efsa.hr'
        }
    },
    {
        'id': 4,
        'slug': 'ieee-student-branch',
        'name': 'IEEE Student Branch Zagreb',
        'faculty': 'FER',
        'type': 'professional',
        'logoText': 'IEEE',
        'logoBg': '#00629b',
        'shortDescription': 'Profesionalna organizacija za elektrotehničare i računarce',
        'description': 'IEEE Student Branch pruža prilike za profesionalni razvoj i networking u području elektrotehnike i računarstva.',
        'tags': ['professional', 'engineering', 'technology', 'networking'],
        'links': {
            'website': 'https://ieee.hr',
            'facebook': 'https://facebook.com/ieeezagreb'
        }
    },
    {
        'id': 5,
        'slug': 'hackathons-fer',
        'name': 'Hackathons FER',
        'faculty': 'FER',
        'type': 'technical',
        'logoText': 'HACK',
        'logoBg': '#1a1a1a',
        'shortDescription': 'Organizacija hackathona i programerskih natjecanja',
        'description': 'Organiziramo hackathone i programerska natjecanja za studente.',
        'tags': ['hackathon', 'programming', 'competition', 'coding'],
        'links': {
            'website': 'https://hackathons.fer.hr'
        }
    },
    {
        'id': 6,
        'slug': 'ffzg-studentski-savjet',
        'name': 'Studentski savjet FFZG',
        'faculty': 'FFZG',
        'type': 'academic',
        'logoText': 'SS FFZG',
        'logoBg': '#8b4513',
        'shortDescription': 'Studentska samouprava Filozofskog fakulteta',
        'description': 'Zastupamo interese studentata Filozofskog fakulteta.',
        'tags': ['student-government', 'academic', 'representation'],
        'links': {
            'website': 'https://ss.ffzg.hr'
        }
    },
    {
        'id': 7,
        'slug': 'pmf-studentski-klub',
        'name': 'Studentski klub PMF',
        'faculty': 'PMF',
        'type': 'academic',
        'logoText': 'SK PMF',
        'logoBg': '#006400',
        'shortDescription': 'Studentska organizacija Prirodoslovno-matematičkog fakulteta',
        'description': 'Organiziramo događaje i aktivnosti za studente PMF-a.',
        'tags': ['academic', 'science', 'mathematics', 'events'],
        'links': {
            'website': 'https://sk.pmf.hr'
        }
    }
]

# Mock data for faculties (in production, this would come from a database)
FACULTIES_DATA = [
    {
        'slug': 'fer',
        'name': 'Fakultet elektrotehnike i računarstva',
        'abbreviation': 'FER',
        'type': 'faculty',
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
        'abbreviation': 'FFZG',
        'type': 'faculty',
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
        'abbreviation': 'PMF',
        'type': 'faculty',
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
        'abbreviation': 'EFZG',
        'type': 'faculty',
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
        'abbreviation': 'FSB',
        'type': 'faculty',
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
        'abbreviation': 'GRAD',
        'type': 'faculty',
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
        'abbreviation': 'ARH',
        'type': 'faculty',
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
        'abbreviation': 'AGR',
        'type': 'faculty',
        'contacts': {
            'email': 'info@agr.hr',
            'phone': '+385 1 2393 777',
            'address': 'Svetošimunska cesta 25, 10000 Zagreb',
            'website': 'https://www.agr.unizg.hr'
        }
    }
]

def search_associations(query: str, faculty: str = None):
    """Search associations by query and optionally filter by faculty"""
    query_lower = query.lower()
    results = []
    
    for assoc in ASSOCIATIONS_DATA:
        # Filter by faculty if specified
        if faculty and assoc.get('faculty') != faculty:
            continue
        
        # Search in name, description, tags
        name_match = query_lower in assoc.get('name', '').lower()
        desc_match = query_lower in assoc.get('shortDescription', '').lower() or query_lower in assoc.get('description', '').lower()
        tags_match = any(query_lower in tag.lower() for tag in assoc.get('tags', []))
        
        if name_match or desc_match or tags_match:
            results.append(assoc)
    
    return results

def search_faculties(query: str, faculty: str = None):
    """Search faculties by query"""
    query_lower = query.lower()
    results = []
    
    for fac in FACULTIES_DATA:
        # Filter by faculty abbreviation if specified (for filtering by user's faculty)
        if faculty and fac.get('abbreviation') != faculty:
            continue
        
        # Search in name, abbreviation
        name_match = query_lower in fac.get('name', '').lower()
        abbrev_match = query_lower in fac.get('abbreviation', '').lower()
        address_match = query_lower in fac.get('contacts', {}).get('address', '').lower() if fac.get('contacts') else False
        
        if name_match or abbrev_match or address_match:
            results.append(fac)
    
    return results

@search_bp.route('/search', methods=['GET'])
def search_all():
    """Search both associations and faculties"""
    query = request.args.get('q', '').strip()
    faculty = request.args.get('faculty', '').strip() or None
    
    if not query:
        return jsonify({
            'success': True,
            'query': query,
            'results': {
                'associations': [],
                'faculties': []
            }
        }), 200
    
    associations = search_associations(query, faculty)
    faculties = search_faculties(query, faculty)
    
    return jsonify({
        'success': True,
        'query': query,
        'results': {
            'associations': associations,
            'faculties': faculties
        }
    }), 200

@search_bp.route('/associations', methods=['GET'])
def get_associations():
    """Get all associations, optionally filtered by faculty and search query"""
    faculty = request.args.get('faculty', '').strip() or None
    query = request.args.get('q', '').strip() or None
    
    results = ASSOCIATIONS_DATA
    
    # Filter by faculty
    if faculty:
        results = [a for a in results if a.get('faculty') == faculty]
    
    # Search by query
    if query:
        results = search_associations(query, faculty)
    
    return jsonify({
        'success': True,
        'count': len(results),
        'items': results
    }), 200

@search_bp.route('/associations/<slug>', methods=['GET'])
def get_association(slug):
    """Get a single association by slug"""
    association = next((a for a in ASSOCIATIONS_DATA if a.get('slug') == slug), None)
    
    if not association:
        return jsonify({
            'success': False,
            'message': 'Association not found'
        }), 404
    
    return jsonify({
        'success': True,
        'item': association
    }), 200

@search_bp.route('/faculties', methods=['GET'])
def get_faculties():
    """Get all faculties, optionally filtered by search query"""
    query = request.args.get('q', '').strip() or None
    
    if query:
        results = search_faculties(query)
    else:
        results = FACULTIES_DATA
    
    return jsonify({
        'success': True,
        'count': len(results),
        'items': results
    }), 200

@search_bp.route('/faculties/<slug>', methods=['GET'])
def get_faculty(slug):
    """Get a single faculty by slug"""
    faculty = next((f for f in FACULTIES_DATA if f.get('slug') == slug), None)
    
    if not faculty:
        return jsonify({
            'success': False,
            'message': 'Faculty not found'
        }), 404
    
    return jsonify({
        'success': True,
        'item': faculty
    }), 200

