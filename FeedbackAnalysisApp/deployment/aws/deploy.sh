#!/usr/bin/env bash
#
# deploy.sh - AWS deployment template for SignalDesk.
#
# Usage:
#   ./deployment/aws/deploy.sh
#
# Prerequisites:
#   - AWS CLI v2 configured (aws configure)
#   - Docker installed and running
#   - Existing ECS cluster and VPC networking setup
#   - .env at project root with OPENAI_API_KEY
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

AWS_REGION="${AWS_REGION:-us-east-1}"
ECR_REPO="${ECR_REPO:-signaldesk-feedback}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "============================================"
echo "  AWS deployment template"
echo "============================================"
echo "Region: $AWS_REGION"
echo "ECR repository: $ECR_REPO"
echo ""

if [[ ! -f .env ]]; then
  echo "ERROR: .env file is required at project root."
  exit 1
fi

echo "Step 1: Build image"
docker build -f deployment/docker/Dockerfile -t "$ECR_REPO:$IMAGE_TAG" .

echo "Step 2: Push to ECR (requires repo and auth setup)"
echo "  aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin <account>.dkr.ecr.$AWS_REGION.amazonaws.com"
echo "  docker tag $ECR_REPO:$IMAGE_TAG <account>.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG"
echo "  docker push <account>.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG"

echo "Step 3: Deploy image on ECS/Fargate"
echo "  Update ECS task definition image URI and deploy service update."
echo ""
echo "This script is a safe template. Fill account- and environment-specific values before production use."
