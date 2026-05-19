# SignalDesk Demo Runbook

This guide shows exactly how to run and present a complete SignalDesk demo, including prerequisites, setup choices, live walkthrough flow, and where to find generated artifacts.

## Audience

- Product demos
- Stakeholder walkthroughs
- Technical validation sessions

## Prerequisites

### Required

- Windows PowerShell terminal
- Python virtual environment with dependencies installed (`.venv` recommended)
- Streamlit dependencies from `requirements.txt`

### Optional (for model-backed behavior)

- OpenAI API key in `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
```

If no API key is present, the app still works in deterministic fallback mode for demo/testing flows.

## Fastest Demo Path (Recommended)

From the `FeedbackAnalysisApp` folder, run:

```powershell
.\deployment\windows-local\run_demo.ps1
```

What this does:

1. Runs the full agent pipeline.
2. Starts the Streamlit app.
3. Opens the UI at `http://localhost:8501`.

### Useful script options

```powershell
# Start UI only (skip pipeline run)
.\deployment\windows-local\run_demo.ps1 -SkipPipeline

# Use a custom UI port
.\deployment\windows-local\run_demo.ps1 -Port 8502
```

## Alternative Run Paths

### Local manual run

```powershell
cd FeedbackAnalysisApp
.\.venv\Scripts\Activate.ps1
python -m agents.pipeline
python -m streamlit run ui/app.py --server.port 8501
```

### Docker run

```powershell
cd FeedbackAnalysisApp
docker compose -f deployment/docker/docker-compose.yml up --build -d
```

Then open: `http://localhost:8501`

## Demo Flow (5-7 Minutes)

Use this sequence for a clean and convincing walkthrough.

### 1) Launch and orient

- Start with `./deployment/windows-local/run_demo.ps1` (or show it already running).
- Explain that feedback is processed end-to-end by multi-agent orchestration.

### 2) Run Pipeline page

- Show data ingestion and run trigger.
- Explain category routing (Bug/Feature/Praise/Complaint/Spam).

### 3) Dashboard page

- Show total processed count and category mix.
- Open generated tickets table and highlight standardized output format.

### 4) Analytics page

- Show confidence distribution and run KPIs.
- Mention that classification accuracy is measured against expected labels.

### 5) Manual Override page

- Edit a ticket field (priority/title/category).
- Save to demonstrate human-in-the-loop controls.

### 6) Processing Log page

- Filter by agent and/or source id.
- Show audit trail from raw input to final decision.

## Artifacts to Show During Demo

After a run, show these generated outputs:

- `data/generated_tickets.csv` - Ticket-ready structured output
- `data/processing_log.csv` - Full decision/audit history
- `data/metrics.csv` - Accuracy, timing, and summary KPIs
- `reports/latest_run_report.md` - Human-readable run summary
- `reports/latest_run_report.json` - Machine-readable run summary
- `logs/pipeline_flow.log` - Stage-by-stage runtime narration

Supporting persisted stores:

- `data/feedback_system.db` - SQLite persistence (tickets/metrics/logs)
- `data/chroma_db/` - Chroma vector collections for RAG and deduplication

## Demo Readiness Checklist

- `.venv` is active and dependencies are installed.
- Input CSV files are present in `data/`.
- `deployment/windows-local/run_demo.ps1` executes without errors.
- Streamlit UI is reachable at the selected port.
- Artifacts are regenerated after running pipeline.

## Common Troubleshooting

### Port already in use

Run on another port:

```powershell
.\deployment\windows-local\run_demo.ps1 -Port 8502
```

### Pipeline fails before UI starts

- Re-run with `-SkipPipeline` to bring up UI first.
- Then run pipeline manually to isolate errors:

```powershell
python -m agents.pipeline
```

### No API key available

- Continue in fallback mode for deterministic demo behavior.
- Mention this explicitly during the walkthrough.

## Suggested Talk Track (Short)

"SignalDesk ingests feedback, classifies it, enriches bugs and features with product context, generates standardized tickets, checks duplicates, and quality-reviews the result. We keep full traceability through logs and reports, while still allowing manual overrides for edge cases."
