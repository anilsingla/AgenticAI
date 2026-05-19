#!/usr/bin/env bash
#
# terminate.sh - AWS deployment termination template for SignalDesk.
#
# Usage:
#   ./deployment/aws/terminate.sh
#
set -euo pipefail

echo "============================================"
echo "  AWS termination template"
echo "============================================"
echo ""
echo "Typical cleanup steps:"
echo "1) Scale ECS service to 0 tasks"
echo "2) Delete ECS service/task definition (if desired)"
echo "3) Optionally delete ECR images/repository"
echo "4) Optionally delete load balancer/network resources"
echo ""
echo "No destructive action is executed automatically in this template."
