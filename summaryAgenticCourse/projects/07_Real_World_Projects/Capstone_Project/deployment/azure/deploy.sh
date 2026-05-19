#!/usr/bin/env bash
#
# deploy.sh â€” Deploy the Capstone Project to Azure Container Instances (cheapest option)
#
# Usage:  ./deployment/azure/deploy.sh
#
# Prerequisites:
#   - Azure CLI installed and logged in (az login)
#   - Docker running locally
#   - .env file with OPENAI_API_KEY set
#
set -euo pipefail

# â”€â”€ Configuration â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
RESOURCE_GROUP="rg-capstone-feedback"
LOCATION="eastus"
ACR_NAME="cpstonefeedbackacr"       # must be globally unique, lowercase, no dashes
CONTAINER_NAME="capstone-feedback"
IMAGE_NAME="capstone-feedback-app"
IMAGE_TAG="latest"
CPU=1
MEMORY=1.5                           # GB â€” minimum for ChromaDB + Streamlit
PORT=8501

# â”€â”€ Load .env for secrets â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERROR: .env file not found at $ENV_FILE"
    exit 1
fi

# Read OPENAI_API_KEY from .env
OPENAI_API_KEY=$(grep -E '^OPENAI_API_KEY=' "$ENV_FILE" | cut -d'=' -f2-)
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "ERROR: OPENAI_API_KEY not set in .env"
    exit 1
fi

echo "============================================"
echo "  Deploying Capstone Project to Azure ACI"
echo "============================================"
echo ""

# â”€â”€ Step 1: Create Resource Group â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo "[1/6] Creating resource group: $RESOURCE_GROUP ..."
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --output none

# â”€â”€ Step 2: Create Azure Container Registry (Basic = cheapest) â”€â”€â”€â”€â”€
echo "[2/6] Creating Azure Container Registry: $ACR_NAME (Basic tier) ..."
az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ACR_NAME" \
    --sku Basic \
    --admin-enabled true \
    --output none

# Get ACR credentials
ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --query "loginServer" -o tsv)
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

# â”€â”€ Step 3: Build & push Docker image â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo "[3/6] Building Docker image (linux/amd64 for Azure) ..."
cd "$PROJECT_ROOT"
docker build --platform linux/amd64 -f deployment/docker/Dockerfile -t "$IMAGE_NAME:$IMAGE_TAG" .

echo "[4/6] Pushing image to ACR ($ACR_LOGIN_SERVER) ..."
docker tag "$IMAGE_NAME:$IMAGE_TAG" "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"
az acr login --name "$ACR_NAME" --output none
docker push "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"

# â”€â”€ Step 5: Deploy to Azure Container Instances â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo "[5/6] Deploying container instance: $CONTAINER_NAME ..."

# Collect all non-secret env vars from .env (exclude OPENAI_API_KEY)
ENV_VARS=""
while IFS= read -r line; do
    line=$(echo "$line" | xargs)  # trim whitespace
    [[ -z "$line" || "$line" == \#* ]] && continue
    key=$(echo "$line" | cut -d'=' -f1)
    [[ "$key" == "OPENAI_API_KEY" ]] && continue
    ENV_VARS="$ENV_VARS $line"
done < "$ENV_FILE"

az container create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$CONTAINER_NAME" \
    --image "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG" \
    --registry-login-server "$ACR_LOGIN_SERVER" \
    --registry-username "$ACR_USERNAME" \
    --registry-password "$ACR_PASSWORD" \
    --cpu "$CPU" \
    --memory "$MEMORY" \
    --ports "$PORT" \
    --ip-address Public \
    --os-type Linux \
    --secure-environment-variables "OPENAI_API_KEY=$OPENAI_API_KEY" \
    --environment-variables $ENV_VARS \
    --output none

# â”€â”€ Step 6: Get public IP â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo "[6/6] Getting deployment info ..."
PUBLIC_IP=$(az container show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$CONTAINER_NAME" \
    --query "ipAddress.ip" -o tsv)

STATE=$(az container show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$CONTAINER_NAME" \
    --query "instanceView.state" -o tsv)

echo ""
echo "============================================"
echo "  Deployment Complete!"
echo "============================================"
echo ""
echo "  Status:   $STATE"
echo "  URL:      http://$PUBLIC_IP:$PORT"
echo ""
echo "  Resource Group:  $RESOURCE_GROUP"
echo "  Container:       $CONTAINER_NAME"
echo "  Registry:        $ACR_LOGIN_SERVER"
echo ""
echo "  To view logs:    az container logs -g $RESOURCE_GROUP -n $CONTAINER_NAME"
echo "  To terminate:    ./deployment/azure/terminate.sh"
echo "============================================"

