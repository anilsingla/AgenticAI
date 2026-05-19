#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "Starting Docker deployment..."
docker compose -f deployment/docker/docker-compose.yml up --build -d

echo "Application is starting at http://localhost:8501"
