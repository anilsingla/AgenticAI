#!/usr/bin/env bash
set -euo pipefail
echo "AWS deployment template for Langfuse_Monitoring"
echo "Build image, push to ECR, and deploy to ECS/Fargate in this script."
