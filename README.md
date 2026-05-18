# AgenticAI

Multi-agent feedback processing platform built with AutoGen for enterprise feedback operations.

- `FeedbackAnalysisApp/` - SignalDesk: Agentic Feedback Operations Platform

## Overview

**SignalDesk** is a production-grade multi-agent AI system that processes app reviews and support emails at scale. It classifies feedback, extracts actionable insights, generates structured tickets, and provides real-time operations oversight through an interactive dashboard.

## Quick Start (Local)

1. Go to the project folder:

```powershell
cd FeedbackAnalysisApp
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Set required environment variable:

```powershell
$env:OPENAI_API_KEY="your-openai-key"
```

5. Run the Streamlit app:

```powershell
streamlit run ui/app.py
```

## Quick Start (Docker)

From `FeedbackAnalysisApp/`:

```powershell
docker compose up --build -d
```

Then open: `http://localhost:8501`

## Notes

- Main project docs are in `FeedbackAnalysisApp/README.md`.
- Input/output sample files are under `FeedbackAnalysisApp/data/`.
- Agent and pipeline code is under `FeedbackAnalysisApp/agents/`.
