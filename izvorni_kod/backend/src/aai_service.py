"""
AAI@EduHr (Academic Authentication Infrastructure) Service
AAI@EduHr uses SAML 2.0 for authentication
"""
from flask import Flask, redirect, url_for, session, request
import urllib.parse

class AAIService:
    """AAI@EduHr Authentication Service"""
    
    def __init__(self, app=None):
        self.app = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize AAI service with Flask app"""
        self.app = app
        
        # AAI@EduHr configuration
        self.aai_entity_id = app.config.get('AAI_ENTITY_ID', 'https://aai.fer.hr/idp/shibboleth')
        self.aai_login_url = app.config.get('AAI_LOGIN_URL', 'https://aai.fer.hr/idp/profile/SAML2/Redirect/SSO')
        self.aai_logout_url = app.config.get('AAI_LOGOUT_URL', 'https://aai.fer.hr/idp/profile/Logout')
        self.aai_metadata_url = app.config.get('AAI_METADATA_URL', 'https://aai.fer.hr/idp/shibboleth')
        
        # Our service provider configuration
        self.sp_entity_id = app.config.get('SP_ENTITY_ID', '')
        self.sp_acs_url = app.config.get('SP_ACS_URL', '')  # Assertion Consumer Service URL
        self.sp_sls_url = app.config.get('SP_SLS_URL', '')  # Single Logout Service URL
    
    def get_login_url(self, redirect_after_login=None):
        """
        Generate AAI@EduHr login URL
        
        Args:
            redirect_after_login (str): URL to redirect to after successful login
            
        Returns:
            str: AAI@EduHr login URL
        """
        # Store redirect URL in session
        if redirect_after_login:
            session['aai_redirect_after_login'] = redirect_after_login
        
        # Build AAI login URL with SAML 2.0 parameters
        # For now, we'll use a simple redirect approach
        # In production, you'd use proper SAML 2.0 AuthnRequest
        
        # Use provided callback URL or default from config
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
    
    def handle_callback(self):
        """
        Handle AAI@EduHr callback after authentication
        
        In a real implementation, this would:
        1. Parse SAML Response
        2. Verify SAML signature
        3. Extract user attributes (email, name, etc.)
        4. Return user information
        
        For now, this is a placeholder that expects email in query params
        In production, implement proper SAML 2.0 response parsing
        
        Returns:
            dict: User information from AAI, or None if invalid
        """
        # In production, parse SAML Response from POST data
        # For development/testing, we can accept email from query params
        email = request.args.get('email') or request.form.get('email')
        
        if not email:
            return None
        
        # Extract user attributes
        # In real SAML, these come from SAML attributes:
        # - eppn (eduPersonPrincipalName) -> email
        # - cn (Common Name) -> full name
        # - givenName -> first name
        # - sn (Surname) -> last name
        
        # For now, parse email to extract name parts
        name_parts = email.split('@')[0].split('.')
        first_name = name_parts[0].capitalize() if name_parts else ''
        last_name = name_parts[1].capitalize() if len(name_parts) > 1 else ''
        
        return {
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'provider': 'aai',
            'provider_id': email,  # Use email as provider ID for AAI
            'role': 'student'  # Default role, can be determined from email domain
        }
    
    def get_logout_url(self, redirect_after_logout=None):
        """
        Generate AAI@EduHr logout URL
        
        Args:
            redirect_after_logout (str): URL to redirect to after logout
            
        Returns:
            str: AAI@EduHr logout URL
        """
        params = {}
        if redirect_after_logout:
            params['return'] = redirect_after_logout
        
        query_string = urllib.parse.urlencode(params)
        logout_url = f"{self.aai_logout_url}?{query_string}"
        
        return logout_url

