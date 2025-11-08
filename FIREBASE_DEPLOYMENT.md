# Firebase Deployment Guide

This guide explains how to deploy the UNIZG Career Hub application to Firebase.

## Architecture

- **Frontend**: Firebase Hosting (static files)
- **Backend**: Cloud Run (containerized Flask app) or Cloud Functions
- **Database**: Cloud SQL (PostgreSQL) or Firestore
- **Storage**: Firebase Storage (if needed)

## Prerequisites

- Firebase account
- Firebase CLI installed (`npm install -g firebase-tools`)
- Google Cloud account (linked to Firebase)
- Docker (for Cloud Run deployment)

## Quick Start

### 1. Install Firebase CLI

```bash
npm install -g firebase-tools
```

### 2. Login to Firebase

```bash
firebase login
```

### 3. Initialize Firebase Project

```bash
# Initialize Firebase in project root
firebase init

# Select:
# - Hosting: Configure files for Firebase Hosting
# - Functions: Set up Cloud Functions
# - (Optional) Firestore: Set up Firestore database
```

### 4. Set Firebase Project

```bash
# List available projects
firebase projects:list

# Set project
firebase use your-project-id

# Or edit .firebaserc directly
```

## Frontend Deployment (Firebase Hosting)

### 1. Build Frontend

```bash
cd izvorni_kod/frontend
npm install
npm run build
```

### 2. Deploy to Firebase Hosting

```bash
# From project root
firebase deploy --only hosting
```

### 3. Configure Environment Variables

Set `VITE_API_URL` in your build process or use Firebase Hosting environment variables:

```bash
# Build with environment variable
cd izvorni_kod/frontend
VITE_API_URL=https://your-backend-url.run.app/api npm run build
firebase deploy --only hosting
```

## Backend Deployment Options

### Option 1: Cloud Run (Recommended)

Cloud Run allows you to run containerized applications with automatic scaling.

#### 1. Build Docker Image

```bash
cd izvorni_kod/backend
gcloud builds submit --tag gcr.io/your-project-id/unizg-career-hub-backend
```

#### 2. Deploy to Cloud Run

```bash
gcloud run deploy unizg-career-hub-backend \
  --image gcr.io/your-project-id/unizg-career-hub-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=your-secret-key,FLASK_ENV=production \
  --add-cloudsql-instances=your-project-id:region:instance-name \
  --set-env-vars DATABASE_URL=postgresql://user:password@/dbname?host=/cloudsql/your-project-id:region:instance-name
```

#### 3. Set Environment Variables

```bash
gcloud run services update unizg-career-hub-backend \
  --update-env-vars FRONTEND_URL=https://your-project-id.web.app \
  --update-env-vars CORS_ORIGINS=https://your-project-id.web.app
```

### Option 2: Cloud Functions (Alternative)

For serverless backend deployment using Cloud Functions.

#### 1. Create Cloud Function

Create `functions/main.py`:

```python
from flask import Flask
from flask_cors import CORS
import os

# Import your Flask app
import sys
sys.path.insert(0, os.path.dirname(__file__))
from src.app import create_app

app = create_app()
CORS(app)

def api(request):
    """Cloud Function entry point"""
    with app.app_context():
        return app.full_dispatch_request()
```

#### 2. Deploy Function

```bash
firebase deploy --only functions
```

## Database Setup

### Option 1: Cloud SQL (PostgreSQL) - Recommended

#### 1. Create Cloud SQL Instance

```bash
gcloud sql instances create unizg-career-hub-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1
```

#### 2. Create Database

```bash
gcloud sql databases create unizg_career_hub \
  --instance=unizg-career-hub-db
```

#### 3. Create User

```bash
gcloud sql users create dbuser \
  --instance=unizg-career-hub-db \
  --password=your-secure-password
```

#### 4. Get Connection String

```bash
gcloud sql instances describe unizg-career-hub-db
```

### Option 2: Firestore (NoSQL)

If using Firestore instead of PostgreSQL:

1. Enable Firestore in Firebase Console
2. Update backend to use Firestore instead of SQLAlchemy
3. Configure Firestore in `firebase.json`

## Environment Variables

### Cloud Run Environment Variables

Set via `gcloud`:

```bash
gcloud run services update unizg-career-hub-backend \
  --update-env-vars SECRET_KEY=your-secret-key \
  --update-env-vars FLASK_ENV=production \
  --update-env-vars FRONTEND_URL=https://your-project-id.web.app \
  --update-env-vars CORS_ORIGINS=https://your-project-id.web.app \
  --update-env-vars DATABASE_URL=your-database-url \
  --update-env-vars OAUTH2_CLIENT_ID=your-client-id \
  --update-env-vars OAUTH2_CLIENT_SECRET=your-client-secret \
  --update-env-vars FIREBASE_CREDENTIALS_JSON='{"type":"service_account",...}' \
  --update-env-vars FIREBASE_PROJECT_ID=your-project-id
```

### Firebase Hosting Environment Variables

Build-time variables (set during build):

```bash
cd izvorni_kod/frontend
VITE_API_URL=https://your-backend-url.run.app/api npm run build
```

## Deployment Steps

### 1. Initial Setup

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize project
firebase init

# Set project
firebase use your-project-id
```

### 2. Build Frontend

```bash
cd izvorni_kod/frontend
npm install
VITE_API_URL=https://your-backend-url.run.app/api npm run build
```

### 3. Deploy Frontend

```bash
firebase deploy --only hosting
```

### 4. Deploy Backend (Cloud Run)

```bash
# Build and deploy
cd izvorni_kod/backend
gcloud builds submit --tag gcr.io/your-project-id/unizg-career-hub-backend

gcloud run deploy unizg-career-hub-backend \
  --image gcr.io/your-project-id/unizg-career-hub-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 5. Initialize Database

```bash
# Connect to Cloud Run service and run migrations
gcloud run services update unizg-career-hub-backend \
  --update-env-vars DATABASE_URL=your-database-url

# Run migrations (via Cloud Run execution)
gcloud run jobs create migrate-db \
  --image gcr.io/your-project-id/unizg-career-hub-backend \
  --region us-central1 \
  --set-env-vars DATABASE_URL=your-database-url \
  --command python \
  --args migrate.py,init

gcloud run jobs execute migrate-db --region us-central1
```

## Custom Domain

### 1. Add Custom Domain to Firebase Hosting

```bash
firebase hosting:channel:deploy production --only hosting
```

Or in Firebase Console:
1. Go to Hosting
2. Add custom domain
3. Follow verification steps

### 2. Add Custom Domain to Cloud Run

```bash
gcloud run domain-mappings create \
  --service unizg-career-hub-backend \
  --domain api.yourdomain.com \
  --region us-central1
```

## Monitoring and Logs

### View Logs

```bash
# Firebase Hosting logs (in Firebase Console)
firebase hosting:channel:list

# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Real-time logs
gcloud logging tail "resource.type=cloud_run_revision"
```

### Monitor Performance

- Firebase Console: Hosting → Usage
- Cloud Run Console: Services → Metrics

## Security

### 1. Firebase Security Rules

Create `firestore.rules` and `storage.rules` if using Firestore/Storage.

### 2. Cloud Run Security

- Use IAM for authentication
- Set up VPC connector for private resources
- Use Cloud Armor for DDoS protection

### 3. Environment Variables

- Never commit secrets to git
- Use Secret Manager for sensitive data
- Rotate secrets regularly

## Scaling

### Cloud Run Auto-scaling

Cloud Run automatically scales based on traffic:
- Min instances: 0 (scale to zero when idle)
- Max instances: Set based on needs
- Concurrency: 80 requests per instance (default)

### Firebase Hosting

- Automatically scales globally via CDN
- No configuration needed

## Cost Optimization

### Cloud Run

- Scale to zero when idle (saves costs)
- Use appropriate instance sizes
- Monitor usage in Cloud Console

### Firebase Hosting

- Free tier: 10 GB storage, 360 MB/day transfer
- Paid: Pay for additional usage

### Cloud SQL

- Use appropriate instance size
- Consider serverless option for variable workloads
- Enable automated backups

## Troubleshooting

### Frontend not loading

```bash
# Check hosting deployment
firebase hosting:channel:list

# View hosting logs
firebase hosting:channel:open
```

### Backend not responding

```bash
# Check Cloud Run status
gcloud run services describe unizg-career-hub-backend

# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit 100

# Check environment variables
gcloud run services describe unizg-career-hub-backend --format="value(spec.template.spec.containers[0].env)"
```

### Database connection issues

```bash
# Check Cloud SQL instance
gcloud sql instances describe unizg-career-hub-db

# Test connection
gcloud sql connect unizg-career-hub-db --user=dbuser
```

## Useful Commands

```bash
# Deploy frontend
firebase deploy --only hosting

# Deploy backend
gcloud run deploy unizg-career-hub-backend --image gcr.io/your-project-id/unizg-career-hub-backend

# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Update environment variables
gcloud run services update unizg-career-hub-backend --update-env-vars KEY=value

# Scale service
gcloud run services update unizg-career-hub-backend --min-instances=1 --max-instances=10
```

## Additional Resources

- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Firebase CLI Reference](https://firebase.google.com/docs/cli)

