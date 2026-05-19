#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "Stopping Docker deployment..."
docker compose -f deployment/docker/docker-compose.yml down

echo "Docker deployment stopped."
