# UNIZG Career Hub - Backend API

Complete backend framework with OAuth2 authentication, AAI@EduHr integration, Firebase Cloud Messaging, and Chatbot services.

## Project Structure

```
backend/
├── src/                    # Source code
│   ├── __init__.py
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models
│   ├── utils.py            # Utility functions
│   ├── oauth2_service.py   # OAuth2 authentication service
│   ├── firebase_service.py # Firebase Cloud Messaging service
│   ├── aai_service.py      # AAI@EduHr authentication service
│   ├── chatbot_service.py  # Chatbot framework
│   └── blueprints/         # Route blueprints
│       ├── __init__.py
│       ├── auth.py         # Authentication routes
│       ├── oauth.py        # OAuth2 routes
│       ├── aai.py          # AAI@EduHr routes
│       ├── notifications.py # Notification routes
│       └── chatbot.py      # Chatbot routes
├── tests/                  # Test files
│   └── __init__.py
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env                   # Environment variables (not committed)
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

### 3. Run the Application

```bash
python run.py
```

Or using the module:

```bash
python -m src.app
```

The API will be available at `http://localhost:5000`

## Docker

Build and run with Docker:

```bash
docker-compose build backend
docker-compose up backend
```

## Features

- **OAuth2 Authentication**: Support for Google OAuth2 and extensible for other providers
- **AAI@EduHr Integration**: Automatic faculty email detection and AAI@EduHr login
- **JWT Token-based Authentication**: Secure token-based authentication
- **Firebase Cloud Messaging**: Push notifications support
- **Chatbot Framework**: Integration with Smotra UNIZG and Career Development Office chatbots
- **RESTful API**: Clean, organized API structure using Flask blueprints
- **Modular Architecture**: Separated services, models, and routes

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password (auto-detects faculty emails)
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### OAuth2
- `GET /api/oauth/login/<provider>` - Initiate OAuth2 login
- `GET /api/oauth/callback/<provider>` - Handle OAuth2 callback

### AAI@EduHr
- `GET /api/aai/login` - Initiate AAI@EduHr login
- `GET /api/aai/callback` - Handle AAI@EduHr callback
- `POST /api/aai/logout` - Logout from AAI@EduHr

### Notifications
- `POST /api/notifications/register-token` - Register FCM token
- `GET /api/notifications` - Get user notifications
- `PUT /api/notifications/<id>/read` - Mark notification as read
- `POST /api/notifications/send` - Send notification (admin)

### Chatbot
- `POST /api/chatbot/send` - Send message to chatbot
- `GET /api/chatbot/providers` - Get available providers
- `GET /api/chatbot/history` - Get conversation history
- `POST /api/chatbot/career-office/query` - Query Career Development Office

## Development Notes

- Source code is organized in `src/` directory
- Tests should be placed in `tests/` directory
- All imports use relative imports within the `src` package
- Entry point is `run.py` for easier execution

## Production Considerations

1. Use a proper database (PostgreSQL, MySQL, etc.)
2. Set strong `SECRET_KEY` in environment variables
3. Enable HTTPS
4. Configure proper CORS origins
5. Set up proper logging
6. Use environment variables for all sensitive data
7. Implement rate limiting
8. Add input validation and sanitization
