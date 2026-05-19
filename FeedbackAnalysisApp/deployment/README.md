# Deployment Scripts Index

This folder contains all deployment and teardown scripts, grouped by target environment.

## Folder Layout

- `windows-local/` - Local run scripts for Windows (PowerShell)
- `linux-local/` - Local run scripts for Linux/macOS (Bash)
- `docker/` - Docker Compose deployment scripts and container definitions
- `azure/` - Azure deployment and teardown scripts
- `aws/` - AWS deployment and teardown templates

## Quick Commands

Run these from the `FeedbackAnalysisApp` project root.

### Windows local

```powershell
.\deployment\windows-local\run_demo.ps1
```

Options:

```powershell
.\deployment\windows-local\run_demo.ps1 -SkipPipeline
.\deployment\windows-local\run_demo.ps1 -Port 8502
```

### Linux local

```bash
./deployment/linux-local/run_demo.sh
```

Options:

```bash
./deployment/linux-local/run_demo.sh --skip-pipeline
./deployment/linux-local/run_demo.sh --port 8502
```

### Docker

```bash
./deployment/docker/deploy.sh
```

Stop:

```bash
./deployment/docker/terminate.sh
```

Direct compose command:

```bash
docker compose -f deployment/docker/docker-compose.yml up --build -d
```

### Azure

```bash
./deployment/azure/deploy.sh
```

Teardown:

```bash
./deployment/azure/terminate.sh
```

### AWS

```bash
./deployment/aws/deploy.sh
```

Teardown template:

```bash
./deployment/aws/terminate.sh
```

## Notes

- Azure scripts are functional and create/delete cloud resources.
- AWS scripts are templates and require environment-specific values before production use.
- Docker files are intentionally centralized in `deployment/docker/`.
