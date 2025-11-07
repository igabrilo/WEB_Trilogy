"""
Email Service for sending notifications
Uses Flask-Mail for SMTP email delivery
"""
from flask import Flask
from flask_mail import Mail, Message
import os

class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self, app=None):
        self.app = None
        self.mail = None
        self.initialized = False
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Flask app"""
        self.app = app
        
        # Configure Flask-Mail
        app.config['MAIL_SERVER'] = app.config.get('MAIL_SERVER', 'smtp.gmail.com')
        app.config['MAIL_PORT'] = app.config.get('MAIL_PORT', 587)
        app.config['MAIL_USE_TLS'] = app.config.get('MAIL_USE_TLS', True)
        app.config['MAIL_USE_SSL'] = app.config.get('MAIL_USE_SSL', False)
        app.config['MAIL_USERNAME'] = app.config.get('MAIL_USERNAME', '')
        app.config['MAIL_PASSWORD'] = app.config.get('MAIL_PASSWORD', '')
        app.config['MAIL_DEFAULT_SENDER'] = app.config.get('MAIL_DEFAULT_SENDER', '')
        
        # Initialize Flask-Mail if credentials are provided
        if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
            try:
                self.mail = Mail(app)
                self.initialized = True
                print("✅ Email service initialized successfully")
                print(f"   SMTP Server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
            except Exception as e:
                print(f"❌ Email service initialization error: {str(e)}")
                self.initialized = False
        else:
            print("⚠️  Email service not configured. MAIL_USERNAME and MAIL_PASSWORD required.")
            self.initialized = False
    
    def send_email(self, to, subject, body, html_body=None):
        """
        Send email to recipient
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        if not self.initialized or self.mail is None:
            return {
                'success': False,
                'message': 'Email service not initialized'
            }
        
        try:
            msg = Message(
                subject=subject,
                recipients=[to],
                body=body,
                html=html_body
            )
            
            self.mail.send(msg)
            return {
                'success': True,
                'message': f'Email sent successfully to {to}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to send email: {str(e)}'
            }
    
    def send_job_application_status_email(self, applicant_email, applicant_name, job_title, status, employer_name=None, employer_email=None):
        """
        Send email notification when job application status changes
        
        Args:
            applicant_email: Applicant's email address
            applicant_name: Applicant's name
            job_title: Job title
            status: Application status ('approved' or 'rejected')
            employer_name: Employer's name (optional)
            employer_email: Employer's email for replies (optional)
        """
        if status == 'approved':
            subject = f'Vaša prijava za posao "{job_title}" je odobrena'
            body = f"""Poštovani/na {applicant_name},

Zadovoljstvo nam je obavijestiti Vas da je Vaša prijava za posao "{job_title}" odobrena.

Čestitamo!

Uskoro će Vas kontaktirati poslodavac za daljnje korake."""
            
            html_body = f"""<html>
<head></head>
<body>
    <h2>Vaša prijava je odobrena!</h2>
    <p>Poštovani/na <strong>{applicant_name}</strong>,</p>
    <p>Zadovoljstvo nam je obavijestiti Vas da je Vaša prijava za posao <strong>"{job_title}"</strong> odobrena.</p>
    <p><strong>Čestitamo!</strong></p>
    <p>Uskoro će Vas kontaktirati poslodavac za daljnje korake.</p>
    {f'<p>Za dodatne informacije možete kontaktirati: {employer_email if employer_email else "poslodavca"}</p>' if employer_email else ''}
    <hr>
    <p><small>Ova poruka je automatski generirana. Molimo ne odgovarajte na ovu poruku.</small></p>
</body>
</html>"""
        
        elif status == 'rejected':
            subject = f'Odluka o prijavi za posao "{job_title}"'
            body = f"""Poštovani/na {applicant_name},

Nažalost, moramo Vas obavijestiti da Vaša prijava za posao "{job_title}" nije odobrena.

Hvala Vam na interesu i želimo Vam sreću u traženju drugih prilika.

S poštovanjem,
Tim za karijere"""
            
            html_body = f"""<html>
<head></head>
<body>
    <h2>Odluka o prijavi</h2>
    <p>Poštovani/na <strong>{applicant_name}</strong>,</p>
    <p>Nažalost, moramo Vas obavijestiti da Vaša prijava za posao <strong>"{job_title}"</strong> nije odobrena.</p>
    <p>Hvala Vam na interesu i želimo Vam sreću u traženju drugih prilika.</p>
    <hr>
    <p><small>Ova poruka je automatski generirana. Molimo ne odgovarajte na ovu poruku.</small></p>
</body>
</html>"""
        
        else:
            # For pending status or other statuses, don't send email
            return {
                'success': False,
                'message': f'Email not sent for status: {status}'
            }
        
        return self.send_email(
            to=applicant_email,
            subject=subject,
            body=body,
            html_body=html_body
        )

