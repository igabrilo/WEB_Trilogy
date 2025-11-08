#!/bin/bash

# Firebase deployment script for UNIZG Career Hub

set -e

echo "🚀 Starting Firebase deployment..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI is not installed!"
    echo "Install it with: npm install -g firebase-tools"
    exit 1
fi

# Check if logged in to Firebase
if ! firebase projects:list &> /dev/null; then
    echo "❌ Not logged in to Firebase!"
    echo "Run: firebase login"
    exit 1
fi

# Get project ID
PROJECT_ID=$(firebase use 2>/dev/null | grep -oP '(?<=\()[^)]+' || echo "")

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No Firebase project selected!"
    echo "Run: firebase use your-project-id"
    exit 1
fi

echo "📦 Using Firebase project: $PROJECT_ID"

# Build frontend
echo "🔨 Building frontend..."
cd izvorni_kod/frontend
npm install

# Get backend URL
read -p "Enter backend URL (e.g., https://unizg-career-hub-backend-xxx.run.app): " BACKEND_URL
if [ -z "$BACKEND_URL" ]; then
    echo "⚠️  No backend URL provided. Using default."
    BACKEND_URL="https://your-backend-url.run.app"
fi

VITE_API_URL="${BACKEND_URL}/api" npm run build
cd ../..

# Deploy frontend
echo "🚀 Deploying frontend to Firebase Hosting..."
firebase deploy --only hosting

echo ""
echo "✅ Frontend deployed successfully!"
echo ""
echo "🌐 Frontend URL: https://$PROJECT_ID.web.app"
echo ""
echo "📋 Next steps:"
echo "1. Deploy backend to Cloud Run (see FIREBASE_DEPLOYMENT.md)"
echo "2. Update CORS_ORIGINS in Cloud Run with frontend URL"
echo "3. Initialize database: gcloud run jobs execute migrate-db"

