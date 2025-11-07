"""
AAI@EduHr (Academic Authentication Infrastructure) Service
Supports multiple authentication protocols:
- SAML 2.0 (recommended)
- OpenID Connect (OIDC)
- CAS (Central Authentication Service)
"""
from flask import Flask, redirect, url_for, session, request
import urllib.parse
import os
import base64
from datetime import datetime

try:
    from onelogin.saml2.auth import OneLogin_Saml2_Auth
    from onelogin.saml2.utils import OneLogin_Saml2_Utils
    SAML_AVAILABLE = True
except ImportError:
    SAML_AVAILABLE = False
    # Create dummy classes for type checking when SAML is not available
    OneLogin_Saml2_Auth = None  # type: ignore
    OneLogin_Saml2_Utils = None  # type: ignore
    print("Warning: python3-saml not installed. SAML 2.0 authentication will not be available.")

try:
    from cas import CASClient
    CAS_AVAILABLE = True
except ImportError:
    CAS_AVAILABLE = False
    print("Warning: python-cas not installed. CAS authentication will not be available.")
    CASClient = None


class AAIService:
    """AAI@EduHr Authentication Service supporting SAML 2.0, OIDC, and CAS"""
    
    def __init__(self, app=None):
        self.app = None
        self.saml_auth = None
        self.cas_client = None
        self.protocol = 'SAML'  # Default protocol: SAML, OIDC, or CAS
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize AAI service with Flask app"""
        self.app = app
        
        # Determine which protocol to use (default: SAML)
        self.protocol = app.config.get('AAI_PROTOCOL', 'SAML').upper()
        
        # AAI@EduHr configuration
        self.aai_entity_id = app.config.get('AAI_ENTITY_ID', 'https://aai.fer.hr/idp/shibboleth')
        self.aai_login_url = app.config.get('AAI_LOGIN_URL', 'https://aai.fer.hr/idp/profile/SAML2/Redirect/SSO')
        self.aai_logout_url = app.config.get('AAI_LOGOUT_URL', 'https://aai.fer.hr/idp/profile/Logout')
        self.aai_metadata_url = app.config.get('AAI_METADATA_URL', 'https://aai.fer.hr/idp/shibboleth')
        
        # Service Provider (SP) Configuration for AAI
        self.sp_entity_id = app.config.get('SP_ENTITY_ID', '')
        self.sp_acs_url = app.config.get('SP_ACS_URL', '')  # Assertion Consumer Service URL
        self.sp_sls_url = app.config.get('SP_SLS_URL', '')  # Single Logout Service URL
        
        # Initialize SAML 2.0 if available
        if SAML_AVAILABLE and self.protocol == 'SAML':
            self._init_saml()
        
        # Initialize CAS if available and configured
        if CAS_AVAILABLE and self.protocol == 'CAS':
            self._init_cas()
        
        # OIDC configuration (uses Authlib from oauth2_service)
        self.oidc_available = app.config.get('AAI_OIDC_CLIENT_ID', '') != ''
        if self.protocol == 'OIDC' and not self.oidc_available:
            print("Warning: OIDC protocol selected but AAI_OIDC_CLIENT_ID not configured")
    
    def _init_saml(self):
        """Initialize SAML 2.0 authentication"""
        if not SAML_AVAILABLE:
            return
        
        if self.app is None:
            print("Warning: Cannot initialize SAML: Flask app not initialized")
            return
        
        try:
            # Prepare SAML request dictionary
            sp_x509_cert = self.app.config.get('SP_X509_CERT', '')
            sp_private_key = self.app.config.get('SP_PRIVATE_KEY', '')
            idp_x509_cert = self.app.config.get('IDP_X509_CERT', '')
            
            saml_settings = {
                'sp': {
                    'entityId': self.sp_entity_id or self.app.config.get('SP_ENTITY_ID', ''),
                    'assertionConsumerService': {
                        'url': self.sp_acs_url or self.app.config.get('SP_ACS_URL', ''),
                        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'
                    },
                    'singleLogoutService': {
                        'url': self.sp_sls_url or self.app.config.get('SP_SLS_URL', ''),
                        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                    },
                    'NameIDFormat': 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient',
                    'x509cert': sp_x509_cert.replace('\\n', '\n') if sp_x509_cert else '',
                    'privateKey': sp_private_key.replace('\\n', '\n') if sp_private_key else '',
                },
                'idp': {
                    'entityId': self.aai_entity_id,
                    'singleSignOnService': {
                        'url': self.aai_login_url,
                        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                    },
                    'singleLogoutService': {
                        'url': self.aai_logout_url,
                        'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                    },
                    'x509cert': idp_x509_cert.replace('\\n', '\n') if idp_x509_cert else '',
                },
                'security': {
                    'authnRequestsSigned': False,
                    'wantAssertionsSigned': True,
                    'wantMessagesSigned': False,
                    'wantAssertionsEncrypted': False,
                    'wantNameIdEncrypted': False,
                    'requestedAuthnContext': [
                        'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport'
                    ],
                }
            }
            
            # Initialize SAML auth (will be used in request context)
            self.saml_settings = saml_settings
        except Exception as e:
            print(f"Warning: Failed to initialize SAML: {str(e)}")
            self.saml_settings = None
    
    def _init_cas(self):
        """Initialize CAS authentication"""
        if not CAS_AVAILABLE or CASClient is None:
            return
        
        if self.app is None:
            print("Warning: Cannot initialize CAS: Flask app not initialized")
            return
        
        try:
            cas_server_url = self.app.config.get('AAI_CAS_SERVER_URL', 'https://aai.fer.hr/cas')
            service_url = self.app.config.get('SP_CAS_SERVICE_URL', self.sp_acs_url)
            version = self.app.config.get('AAI_CAS_VERSION', '2')
            
            # CASClient constructor may vary by library version
            # Try different parameter combinations
            try:
                self.cas_client = CASClient(
                    version=int(version),
                    server_url=cas_server_url,
                    service_url=service_url
                )
            except TypeError:
                # Try alternative constructor signature
                self.cas_client = CASClient(
                    server_url=cas_server_url,
                    service_url=service_url,
                    version=int(version)
                )
        except Exception as e:
            print(f"Warning: Failed to initialize CAS: {str(e)}")
            self.cas_client = None
    
    def get_login_url(self, redirect_after_login=None, protocol=None):
        """
        Generate AAI@EduHr login URL based on configured protocol
        
        Args:
            redirect_after_login (str): URL to redirect to after successful login
            protocol (str): Override protocol (SAML, OIDC, CAS). If None, uses configured protocol
            
        Returns:
            str: AAI@EduHr login URL
        """
        # Store redirect URL in session
        if redirect_after_login:
            session['aai_redirect_after_login'] = redirect_after_login
        
        protocol = protocol or self.protocol
        
        if protocol == 'SAML' and SAML_AVAILABLE:
            return self._get_saml_login_url(redirect_after_login)
        elif protocol == 'OIDC' and self.oidc_available:
            return self._get_oidc_login_url(redirect_after_login)
        elif protocol == 'CAS' and CAS_AVAILABLE and self.cas_client:
            return self._get_cas_login_url(redirect_after_login)
        else:
            # Fallback to simple redirect approach
            return self._get_simple_login_url(redirect_after_login)
    
    def _get_saml_login_url(self, redirect_after_login=None):
        """Generate SAML 2.0 AuthnRequest login URL"""
        if not SAML_AVAILABLE or not self.saml_settings or OneLogin_Saml2_Auth is None:
            return self._get_simple_login_url(redirect_after_login)
        
        try:
            # Prepare request data
            req = self._prepare_saml_request()
            
            # Create SAML auth instance
            auth = OneLogin_Saml2_Auth(req, self.saml_settings)
            
            # Generate login URL with SAML AuthnRequest
            login_url = auth.login(return_to=redirect_after_login)
            
            return login_url
        except Exception as e:
            print(f"Error generating SAML login URL: {str(e)}")
            # Fallback to simple redirect
            return self._get_simple_login_url(redirect_after_login)
    
    def _get_oidc_login_url(self, redirect_after_login=None):
        """Generate OpenID Connect login URL"""
        if self.app is None:
            raise RuntimeError("Flask app not initialized")
        
        # OIDC implementation would use Authlib
        # For now, return a placeholder that would use OIDC discovery
        oidc_discovery_url = self.app.config.get('AAI_OIDC_DISCOVERY_URL', 'https://aai.fer.hr/.well-known/openid-configuration')
        oidc_client_id = self.app.config.get('AAI_OIDC_CLIENT_ID', '')
        callback_url = redirect_after_login or self.sp_acs_url
        
        params = {
            'client_id': oidc_client_id,
            'response_type': 'code',
            'scope': 'openid email profile',
            'redirect_uri': callback_url,
            'state': session.get('aai_state', '')
        }
        
        query_string = urllib.parse.urlencode(params)
        login_url = f"{self.aai_login_url}?{query_string}"
        
        return login_url
    
    def _get_cas_login_url(self, redirect_after_login=None):
        """Generate CAS login URL"""
        if not self.cas_client:
            return self._get_simple_login_url(redirect_after_login)
        
        if self.app is None:
            raise RuntimeError("Flask app not initialized")
        
        try:
            service_url = redirect_after_login or self.app.config.get('SP_CAS_SERVICE_URL', self.sp_acs_url)
            login_url = self.cas_client.get_login_url()
            return login_url
        except Exception as e:
            print(f"Error generating CAS login URL: {str(e)}")
            return self._get_simple_login_url(redirect_after_login)
    
    def _get_simple_login_url(self, redirect_after_login=None):
        """Fallback: Generate simple redirect login URL"""
        callback_url = redirect_after_login or self.sp_acs_url
        
        params = {
            'entityID': self.aai_entity_id,
        }
        
        if callback_url:
            params['target'] = callback_url
        
        if self.sp_entity_id:
            params['sp'] = self.sp_entity_id
        
        query_string = urllib.parse.urlencode(params)
        login_url = f"{self.aai_login_url}?{query_string}"
        
        return login_url
    
    def _prepare_saml_request(self):
        """Prepare request dictionary for SAML authentication"""
        return {
            'https': 'on' if request.is_secure else 'off',
            'http_host': request.host,
            'server_port': request.environ.get('SERVER_PORT', ''),
            'script_name': request.path,
            'get_data': dict(request.args),
            'post_data': dict(request.form),
            'query_string': request.query_string.decode('utf-8') if request.query_string else '',
        }
    
    def handle_callback(self, protocol=None):
        """
        Handle AAI@EduHr callback after authentication
        
        Args:
            protocol (str): Protocol used (SAML, OIDC, CAS). If None, uses configured protocol
            
        Returns:
            dict: User information from AAI, or None if invalid
        """
        protocol = protocol or self.protocol
        
        if protocol == 'SAML' and SAML_AVAILABLE:
            return self._handle_saml_callback()
        elif protocol == 'OIDC' and self.oidc_available:
            return self._handle_oidc_callback()
        elif protocol == 'CAS' and CAS_AVAILABLE and self.cas_client:
            return self._handle_cas_callback()
        else:
            # Fallback to simple callback handling
            return self._handle_simple_callback()
    
    def _handle_saml_callback(self):
        """Handle SAML 2.0 Response"""
        if not SAML_AVAILABLE or not self.saml_settings or OneLogin_Saml2_Auth is None:
            return self._handle_simple_callback()
        
        try:
            # Prepare request data
            req = self._prepare_saml_request()
            
            # Create SAML auth instance
            auth = OneLogin_Saml2_Auth(req, self.saml_settings)
            
            # Process SAML Response
            auth.process_response()
            
            # Check for errors
            errors = auth.get_errors()
            if errors:
                print(f"SAML authentication errors: {errors}")
                return None
            
            if not auth.is_authenticated():
                print("SAML authentication failed: User not authenticated")
                return None
            
            # Extract user attributes from SAML assertion
            attributes = auth.get_attributes()
            
            # Map SAML attributes to user info
            # Common SAML attributes in AAI@EduHr:
            # - eppn (eduPersonPrincipalName) -> email
            # - cn (Common Name) -> full name
            # - givenName -> first name
            # - sn (Surname) -> last name
            # - mail -> email (alternative)
            # - displayName -> display name
            
            email = None
            if attributes.get('eppn'):
                email = attributes['eppn'][0] if isinstance(attributes['eppn'], list) else attributes['eppn']
            elif attributes.get('mail'):
                email = attributes['mail'][0] if isinstance(attributes['mail'], list) else attributes['mail']
            
            if not email:
                # Try to get email from name ID
                name_id = auth.get_nameid()
                if name_id and '@' in name_id:
                    email = name_id
            
            if not email:
                print("SAML authentication failed: No email found in attributes")
                return None
            
            # Extract name information
            first_name = ''
            last_name = ''
            
            if attributes.get('givenName'):
                first_name = attributes['givenName'][0] if isinstance(attributes['givenName'], list) else attributes['givenName']
            
            if attributes.get('sn'):
                last_name = attributes['sn'][0] if isinstance(attributes['sn'], list) else attributes['sn']
            
            # If no first/last name, try to parse from cn (Common Name)
            if not first_name and not last_name and attributes.get('cn'):
                cn = attributes['cn'][0] if isinstance(attributes['cn'], list) else attributes['cn']
                name_parts = cn.split(' ', 1)
                first_name = name_parts[0] if len(name_parts) > 0 else ''
                last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # If still no name, parse from email
            if not first_name and not last_name:
                name_parts = email.split('@')[0].split('.')
                first_name = name_parts[0].capitalize() if name_parts else ''
                last_name = name_parts[1].capitalize() if len(name_parts) > 1 else ''
            
            return {
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'provider': 'aai',
                'provider_id': auth.get_nameid() or email,
                'role': 'student',  # Default role, can be determined from email domain
                'attributes': attributes  # Include all attributes for further processing
            }
            
        except Exception as e:
            print(f"Error processing SAML callback: {str(e)}")
            return None
    
    def _handle_oidc_callback(self):
        """Handle OpenID Connect callback"""
        # OIDC implementation would use Authlib to exchange code for tokens
        # and then get user info from userinfo endpoint
        # For now, return None (would need OAuth2Service integration)
        code = request.args.get('code')
        if not code:
            return None
        
        # In a full implementation, this would:
        # 1. Exchange authorization code for access token
        # 2. Use access token to get user info from userinfo endpoint
        # 3. Return user information
        
        return None
    
    def _handle_cas_callback(self):
        """Handle CAS callback"""
        if not self.cas_client:
            return self._handle_simple_callback()
        
        if self.app is None:
            raise RuntimeError("Flask app not initialized")
        
        try:
            ticket = request.args.get('ticket')
            if not ticket:
                return None
            
            # verify_ticket only takes ticket as parameter (service_url is set in CASClient init)
            result = self.cas_client.verify_ticket(ticket)
            # CASClient returns different formats based on version
            # Handle tuple return (username, attributes, pgtiou) or just username
            if isinstance(result, tuple):
                username, attributes, pgtiou = result
            else:
                username = result
                attributes = {}
                pgtiou = None
            
            if not username:
                return None
            
            # Ensure attributes is a dictionary
            if not isinstance(attributes, dict):
                attributes = {}
            
            # CAS typically returns username, which is often the email
            email = username if '@' in username else f"{username}@fer.hr"
            
            # Extract name from attributes if available
            first_name = attributes.get('givenName', [''])[0] if attributes.get('givenName') else ''
            last_name = attributes.get('sn', [''])[0] if attributes.get('sn') else ''
            
            if not first_name and not last_name:
                name_parts = email.split('@')[0].split('.')
                first_name = name_parts[0].capitalize() if name_parts else ''
                last_name = name_parts[1].capitalize() if len(name_parts) > 1 else ''
            
            return {
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'provider': 'aai',
                'provider_id': username,
                'role': 'student',
                'attributes': attributes
            }
            
        except Exception as e:
            print(f"Error processing CAS callback: {str(e)}")
            return None
    
    def _handle_simple_callback(self):
        """
        Fallback: Handle simple callback (development/testing only)
        Expects email in query params or form data
        """
        email = request.args.get('email') or request.form.get('email')
        
        if not email:
            return None
        
        # Parse email to extract name parts
        name_parts = email.split('@')[0].split('.')
        first_name = name_parts[0].capitalize() if name_parts else ''
        last_name = name_parts[1].capitalize() if len(name_parts) > 1 else ''
        
        return {
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'provider': 'aai',
            'provider_id': email,
            'role': 'student'
        }
    
    def get_logout_url(self, redirect_after_logout=None, protocol=None, name_id=None, session_index=None):
        """
        Generate AAI@EduHr logout URL
        
        Args:
            redirect_after_logout (str): URL to redirect to after logout
            protocol (str): Protocol used (SAML, OIDC, CAS)
            name_id (str): SAML NameID for SLO
            session_index (str): SAML SessionIndex for SLO
            
        Returns:
            str: AAI@EduHr logout URL
        """
        protocol = protocol or self.protocol
        
        if protocol == 'SAML' and SAML_AVAILABLE and name_id:
            return self._get_saml_logout_url(redirect_after_logout, name_id, session_index)
        elif protocol == 'OIDC' and self.oidc_available:
            return self._get_oidc_logout_url(redirect_after_logout)
        elif protocol == 'CAS' and CAS_AVAILABLE and self.cas_client:
            return self._get_cas_logout_url(redirect_after_logout)
        else:
            return self._get_simple_logout_url(redirect_after_logout)
    
    def _get_saml_logout_url(self, redirect_after_logout=None, name_id=None, session_index=None):
        """Generate SAML 2.0 Single Logout URL"""
        if not SAML_AVAILABLE or not self.saml_settings or OneLogin_Saml2_Auth is None:
            return self._get_simple_logout_url(redirect_after_logout)
        
        try:
            req = self._prepare_saml_request()
            auth = OneLogin_Saml2_Auth(req, self.saml_settings)
            
            logout_url = auth.logout(
                name_id=name_id,
                session_index=session_index,
                return_to=redirect_after_logout
            )
            
            return logout_url
        except Exception as e:
            print(f"Error generating SAML logout URL: {str(e)}")
            return self._get_simple_logout_url(redirect_after_logout)
    
    def _get_oidc_logout_url(self, redirect_after_logout=None):
        """Generate OpenID Connect logout URL"""
        if self.app is None:
            raise RuntimeError("Flask app not initialized")
        
        oidc_end_session_url = self.app.config.get('AAI_OIDC_END_SESSION_URL', 'https://aai.fer.hr/oidc/end_session')
        params = {}
        if redirect_after_logout:
            params['post_logout_redirect_uri'] = redirect_after_logout
        query_string = urllib.parse.urlencode(params)
        return f"{oidc_end_session_url}?{query_string}" if query_string else oidc_end_session_url
    
    def _get_cas_logout_url(self, redirect_after_logout=None):
        """Generate CAS logout URL"""
        if not self.cas_client:
            return self._get_simple_logout_url(redirect_after_logout)
        return self.cas_client.get_logout_url(redirect_after_logout)
    
    def _get_simple_logout_url(self, redirect_after_logout=None):
        """Fallback: Generate simple logout URL"""
        params = {}
        if redirect_after_logout:
            params['return'] = redirect_after_logout
        query_string = urllib.parse.urlencode(params)
        logout_url = f"{self.aai_logout_url}?{query_string}"
        return logout_url
