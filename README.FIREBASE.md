# Quick Firebase Deployment

## Prerequisites

- Firebase account
- Google Cloud account
- Firebase CLI: `npm install -g firebase-tools`
- Google Cloud SDK: Install from https://cloud.google.com/sdk

## Quick Start

### 1. Setup Firebase

```bash
# Login to Firebase
firebase login

# Initialize Firebase
firebase init

# Select:
# - Hosting
# - (Optional) Functions
# - (Optional) Firestore
```

### 2. Deploy Frontend

```bash
# Option 1: Use deployment script
./deploy-firebase.sh

# Option 2: Manual deployment
cd izvorni_kod/frontend
npm install
VITE_API_URL=https://your-backend-url.run.app/api npm run build
cd ../..
firebase deploy --only hosting
```

### 3. Deploy Backend (Cloud Run)

```bash
# Option 1: Use deployment script
./deploy-backend-cloudrun.sh

# Option 2: Manual deployment
cd izvorni_kod/backend
gcloud builds submit --tag gcr.io/your-project-id/unizg-career-hub-backend
gcloud run deploy unizg-career-hub-backend \
  --image gcr.io/your-project-id/unizg-career-hub-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 4. Set Environment Variables

```bash
gcloud run services update unizg-career-hub-backend \
  --update-env-vars SECRET_KEY=your-secret-key \
  --update-env-vars FLASK_ENV=production \
  --update-env-vars FRONTEND_URL=https://your-project-id.web.app \
  --update-env-vars CORS_ORIGINS=https://your-project-id.web.app \
  --update-env-vars DATABASE_URL=your-database-url
```

### 5. Initialize Database

```bash
# Create Cloud SQL instance first, then:
gcloud run jobs create migrate-db \
  --image gcr.io/your-project-id/unizg-career-hub-backend \
  --region us-central1 \
  --set-env-vars DATABASE_URL=your-database-url \
  --command python \
  --args migrate.py,init

gcloud run jobs execute migrate-db --region us-central1
```

## URLs

- Frontend: `https://your-project-id.web.app`
- Backend: `https://unizg-career-hub-backend-xxx.run.app`
- API: `https://unizg-career-hub-backend-xxx.run.app/api`

## Full Documentation

See [FIREBASE_DEPLOYMENT.md](FIREBASE_DEPLOYMENT.md) for detailed instructions.

