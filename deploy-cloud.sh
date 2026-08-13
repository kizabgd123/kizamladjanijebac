#!/usr/bin/env bash
set -e

echo "🚀 Starting Google Cloud Run Deployment for Nexus Multi-Agent RAG Studio..."

# Verify gcloud authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🛑 Error: No active gcloud account found. Please run 'gcloud auth login' first."
    exit 1
fi

ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n 1)
echo "✅ Authenticated Account: ${ACTIVE_ACCOUNT}"

PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")
if [ -z "$PROJECT_ID" ]; then
    echo "⚠️ No default project set. Attempting auto-detection..."
    PROJECT_ID=$(gcloud projects list --format="value(projectId)" | head -n 1 || echo "")
fi

if [ -z "$PROJECT_ID" ]; then
    echo "🛑 Error: GCP Project ID not specified. Please set a project: gcloud config set project <PROJECT_ID>"
    exit 1
fi

echo "📦 GCP Project ID: ${PROJECT_ID}"

REGION=${REGION:-"us-central1"}
SERVICE_NAME=${SERVICE_NAME:-"nexus-multiagent-rag-studio"}

echo "⚡ Deploying service '${SERVICE_NAME}' to region '${REGION}' on Cloud Run..."

gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --project "${PROJECT_ID}" \
    --region "${REGION}" \
    --allow-unauthenticated \
    --port 5000 \
    --memory 1Gi \
    --cpu 1

echo "✅ Google Cloud Run deployment command complete!"
