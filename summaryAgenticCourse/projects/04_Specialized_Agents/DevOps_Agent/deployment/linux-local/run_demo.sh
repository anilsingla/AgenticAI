#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "")" && pwd)"
PROJECT_ROOT="$(cd "/../.." && pwd)"
cd ""

PYTHON_EXE="python3"
if [[ -x ".venv/bin/python" ]]; then
  PYTHON_EXE=".venv/bin/python"
fi

ENTRY=""
if [[ -z "" ]]; then
  for c in "ui/app.py" "app.py" "agent.py" "basic_agent.py"; do
    if [[ -f "" ]]; then ENTRY=""; break; fi
  done
fi

if [[ -z "" ]]; then
  echo "No runnable entry file found. Pass an entry path as first argument."
  exit 1
fi

if [[ "" == "ui/app.py" ]]; then
  "" -m streamlit run ""
else
  "" ""
fi
