#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "")" && pwd)"
PROJECT_ROOT="$(cd "/../.." && pwd)"
cd ""
docker compose -f deployment/docker/docker-compose.yml up --build -d
