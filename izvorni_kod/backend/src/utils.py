"""
Utility functions for the application
"""
import re

# List of recognized faculty/university email domains
FACULTY_DOMAINS = [
    'fer.hr',           # Fakultet elektrotehnike i računarstva
    'unizg.hr',         # Sveučilište u Zagrebu
    'ffzg.hr',          # Filozofski fakultet
    'efzg.hr',          # Ekonomski fakultet
    'pmf.hr',           # Prirodoslovno-matematički fakultet
    'agr.hr',           # Agronomski fakultet
    'fzg.unizg.hr',     # Farmaceutsko-biokemijski fakultet
    'vet.hr',           # Veterinarski fakultet
    'grad.hr',          # Građevinski fakultet
    'arhitekt.hr',      # Arhitektonski fakultet
    'fizika.hr',        # Fizički fakultet
    'kemija.pmf.hr',    # Kemijski fakultet
    'geof.pmf.hr',      # Geofizički fakultet
    'geol.pmf.hr',      # Geološki fakultet
    'matf.hr',          # Matematički fakultet
    'fpz.hr',           # Fakultet prometnih znanosti
    'fsb.hr',           # Fakultet strojarstva i brodogradnje
    'fsreb.hr',         # Fakultet šumarstva i drvne tehnologije
    'rgn.hr',           # Rudarsko-geološko-naftni fakultet
    'ktk.hr',           # Kineziološki fakultet
    'pfst.hr',          # Prehrambeno-biotehnološki fakultet
    'ttf.hr',           # Tekstilno-tehnološki fakultet
    'uni-osijek.hr',    # Sveučilište Josipa Jurja Strossmayera
    'unist.hr',         # Sveučilište u Splitu
    'uniri.hr',         # Sveučilište u Rijeci
    'unidu.hr',         # Sveučilište u Dubrovniku
    'unizd.hr',         # Sveučilište u Zadru
    'unipu.hr',         # Sveučilište Jurja Dobrile u Puli
]

def is_faculty_email(email):
    """
    Check if an email belongs to a faculty/university domain
    
    Args:
        email (str): Email address to check
        
    Returns:
        bool: True if email is from a faculty domain, False otherwise
    """
    if not email or '@' not in email:
        return False
    
    domain = email.lower().split('@')[1]
    
    # Check exact match or subdomain match
    for faculty_domain in FACULTY_DOMAINS:
        if domain == faculty_domain or domain.endswith('.' + faculty_domain):
            return True
    
    return False

def extract_domain(email):
    """
    Extract domain from email address
    
    Args:
        email (str): Email address
        
    Returns:
        str: Domain part of email, or None if invalid
    """
    if not email or '@' not in email:
        return None
    
    return email.lower().split('@')[1]

def validate_email_format(email):
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

