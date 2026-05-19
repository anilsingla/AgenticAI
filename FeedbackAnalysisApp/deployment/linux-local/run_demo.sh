#!/usr/bin/env bash
set -euo pipefail

SKIP_PIPELINE=false
PORT=8501

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-pipeline)
      SKIP_PIPELINE=true
      shift
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: ./deployment/linux-local/run_demo.sh [--skip-pipeline] [--port <port>]"
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

if [[ -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
  PYTHON_EXE="$PROJECT_ROOT/.venv/bin/python"
else
  PYTHON_EXE="python3"
fi

echo "Project root: $PROJECT_ROOT"
echo "Using Python: $PYTHON_EXE"

if [[ "$SKIP_PIPELINE" != "true" ]]; then
  echo "Running pipeline..."
  "$PYTHON_EXE" -m agents.pipeline
  echo "Pipeline completed successfully."
fi

echo "Starting Streamlit on port $PORT ..."
"$PYTHON_EXE" -m streamlit run ui/app.py --server.port "$PORT"
