"""
Chatbot Service Framework
Supports integration with various chatbot providers and external services
"""
from flask import Flask, session
import requests
import json
from typing import Dict, Optional, List
from abc import ABC, abstractmethod

class ChatbotProvider(ABC):
    """Abstract base class for chatbot providers"""
    
    @abstractmethod
    def send_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Send a message to the chatbot and get response"""
        pass
    
    @abstractmethod
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        pass

class SmotraUnizgChatbot(ChatbotProvider):
    """Integration with Smotra UNIZG chatbot"""
    
    def __init__(self, api_key: str, base_url: str = "https://smotra.unizg.hr"):
        self.api_key = api_key
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/chatbot"  # Adjust based on actual API
    
    def send_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Send message to Smotra chatbot"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'message': message,
                'context': context or {}
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'response': response.json(),
                    'provider': 'smotra_unizg'
                }
            else:
                return {
                    'success': False,
                    'error': f'API returned status {response.status_code}',
                    'provider': 'smotra_unizg'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'smotra_unizg'
            }
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_endpoint}/history/{session_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching conversation history: {str(e)}")
            return []

class CareerDevelopmentOfficeChatbot(ChatbotProvider):
    """Integration with Ured za razvoj karijera chatbot"""
    
    def __init__(self, api_key: str, base_url: str = "https://www.unizg.hr"):
        self.api_key = api_key
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/o-sveucilistu/sveucilisna-tijela-i-sluzbe/rektorat/ured-za-razvoj-karijera/api/chatbot"
    
    def send_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Send message to Career Development Office chatbot"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'X-API-Key': self.api_key
            }
            
            payload = {
                'message': message,
                'context': context or {},
                'source': 'career_hub'
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'response': response.json(),
                    'provider': 'career_development_office'
                }
            else:
                return {
                    'success': False,
                    'error': f'API returned status {response.status_code}',
                    'provider': 'career_development_office'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'career_development_office'
            }
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_endpoint}/history/{session_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching conversation history: {str(e)}")
            return []

class OpenAIChatbot(ChatbotProvider):
    """Generic OpenAI-compatible chatbot provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or "https://api.openai.com/v1"
    
    def send_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Send message using OpenAI-compatible API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            messages = context.get('messages', []) if context else []
            messages.append({'role': 'user', 'content': message})
            
            payload = {
                'model': self.model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 500
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'response': {
                        'message': data['choices'][0]['message']['content'],
                        'model': data['model'],
                        'usage': data.get('usage', {})
                    },
                    'provider': 'openai'
                }
            else:
                return {
                    'success': False,
                    'error': f'API returned status {response.status_code}',
                    'provider': 'openai'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'openai'
            }
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """OpenAI doesn't store history, return empty"""
        return []

class ChatbotService:
    """Main chatbot service that manages multiple providers"""
    
    def __init__(self, app=None):
        self.app = None
        self.providers: Dict[str, ChatbotProvider] = {}
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize chatbot service with Flask app"""
        self.app = app
        
        # Initialize Smotra UNIZG chatbot if API key is configured
        smotra_api_key = app.config.get('SMOTRA_CHATBOT_API_KEY')
        if smotra_api_key:
            self.providers['smotra'] = SmotraUnizgChatbot(
                api_key=smotra_api_key,
                base_url=app.config.get('SMOTRA_BASE_URL', 'https://smotra.unizg.hr')
            )
        
        # Initialize Career Development Office chatbot if API key is configured
        career_api_key = app.config.get('CAREER_OFFICE_CHATBOT_API_KEY')
        if career_api_key:
            self.providers['career_office'] = CareerDevelopmentOfficeChatbot(
                api_key=career_api_key,
                base_url=app.config.get('CAREER_OFFICE_BASE_URL', 'https://www.unizg.hr')
            )
        
        # Initialize OpenAI-compatible chatbot if API key is configured
        openai_api_key = app.config.get('OPENAI_API_KEY')
        if openai_api_key:
            openai_base_url = app.config.get('OPENAI_BASE_URL')
            self.providers['openai'] = OpenAIChatbot(
                api_key=openai_api_key,
                model=app.config.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
                base_url=openai_base_url if openai_base_url else None
            )
    
    def get_provider(self, provider_name: str) -> Optional[ChatbotProvider]:
        """Get a chatbot provider by name"""
        return self.providers.get(provider_name)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available chatbot provider names"""
        return list(self.providers.keys())
    
    def send_message(self, message: str, provider_name: str = 'smotra', 
                    context: Optional[Dict] = None, session_id: Optional[str] = None) -> Dict:
        """
        Send a message to the specified chatbot provider
        
        Args:
            message: User message
            provider_name: Name of the provider ('smotra', 'career_office', 'openai')
            context: Additional context for the conversation
            session_id: Session ID for conversation tracking
            
        Returns:
            Dict with response from chatbot
        """
        provider = self.get_provider(provider_name)
        
        if not provider:
            return {
                'success': False,
                'error': f'Provider "{provider_name}" not configured or not found',
                'available_providers': list(self.providers.keys())
            }
        
        # Add session_id to context if provided
        if context is None:
            context = {}
        
        if session_id:
            context['session_id'] = session_id
        
        return provider.send_message(message, context)
    
    def register_provider(self, name: str, provider: ChatbotProvider):
        """Register a custom chatbot provider"""
        self.providers[name] = provider

