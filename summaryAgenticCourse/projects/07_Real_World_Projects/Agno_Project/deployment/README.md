# Deployment Index

This project uses a standardized deployment layout.

## Folders
- linux-local
- windows-local
- docker
- azure
- aws

## Quick Commands
- Windows local: .\\deployment\\windows-local\\run_demo.ps1
- Linux local: ./deployment/linux-local/run_demo.sh
- Docker up: docker compose -f deployment/docker/docker-compose.yml up --build -d
- Docker down: docker compose -f deployment/docker/docker-compose.yml down
- Azure deploy: ./deployment/azure/deploy.sh
- Azure terminate: ./deployment/azure/terminate.sh
- AWS deploy template: ./deployment/aws/deploy.sh
- AWS terminate template: ./deployment/aws/terminate.sh
