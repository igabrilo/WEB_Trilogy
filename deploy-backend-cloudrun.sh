#!/bin/bash

# Cloud Run deployment script for backend

set -e

echo "🚀 Deploying backend to Cloud Run..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed!"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No Google Cloud project set!"
    echo "Run: gcloud config set project your-project-id"
    exit 1
fi

echo "📦 Using Google Cloud project: $PROJECT_ID"

# Get region
read -p "Enter region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

# Build and push image
echo "🔨 Building Docker image..."
cd izvorni_kod/backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/unizg-career-hub-backend

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy unizg-career-hub-backend \
  --image gcr.io/$PROJECT_ID/unizg-career-hub-backend \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080

# Get service URL
SERVICE_URL=$(gcloud run services describe unizg-career-hub-backend --region $REGION --format="value(status.url)")

echo ""
echo "✅ Backend deployed successfully!"
echo "🌐 Backend URL: $SERVICE_URL"
echo ""
echo "📋 Next steps:"
echo "1. Set environment variables:"
echo "   gcloud run services update unizg-career-hub-backend --region $REGION \\"
echo "     --update-env-vars SECRET_KEY=your-secret-key \\"
echo "     --update-env-vars FLASK_ENV=production \\"
echo "     --update-env-vars FRONTEND_URL=https://$PROJECT_ID.web.app \\"
echo "     --update-env-vars CORS_ORIGINS=https://$PROJECT_ID.web.app"
echo ""
echo "2. Set DATABASE_URL:"
echo "   gcloud run services update unizg-career-hub-backend --region $REGION \\"
echo "     --update-env-vars DATABASE_URL=your-database-url"
echo ""
echo "3. Initialize database:"
echo "   gcloud run jobs create migrate-db \\"
echo "     --image gcr.io/$PROJECT_ID/unizg-career-hub-backend \\"
echo "     --region $REGION \\"
echo "     --set-env-vars DATABASE_URL=your-database-url \\"
echo "     --command python --args migrate.py,init"
echo ""
echo "   gcloud run jobs execute migrate-db --region $REGION"

