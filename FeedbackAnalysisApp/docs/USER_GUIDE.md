# User Guide

This guide explains how to deploy, run, use, and interpret outputs for the Intelligent User Feedback Analysis and Action System.

## 1) What This Application Does

The app automates user-feedback triage by:
- Reading app reviews and support emails from CSV files.
- Classifying feedback into Bug, Feature Request, Praise, Complaint, or Spam.
- Extracting bug/feature insights.
- Generating prioritized support tickets.
- Logging processing history and run metrics.

## 2) Quick Start (Recommended)

From FeedbackAnalysisApp folder:

```powershell
.\run_demo.ps1
```

What this does:
1. Runs pipeline once on current input CSV files.
2. Starts Streamlit UI.
3. Opens the app at http://localhost:8501

## 3) Deployment Options

### Option A: Local Deployment

1. Open terminal in FeedbackAnalysisApp.
2. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Optional (for model-backed mode):

```powershell
$env:OPENAI_API_KEY="your-key"
```

5. Run UI:

```powershell
streamlit run ui/app.py
```

### Option B: Docker Deployment

```powershell
docker compose up --build -d
```

Open:
- http://localhost:8501

## 4) How to Use the UI

### A) Run Pipeline page

- Upload one or both files:
  - app_store_reviews.csv
  - support_emails.csv
- Click Run Analysis Pipeline.
- Wait for status messages to complete.

### B) Dashboard

- Shows total processed volume, category counts, confidence, and timing.
- Displays generated ticket table and ticket detail view.

### C) Manual Override

- Filter tickets by category/priority.
- Edit title, category, priority, description, technical details.
- Save all changes back to generated_tickets.csv.

### D) Analytics

- View run history from metrics.csv.
- Review category distribution, quality, confidence, duplicates.
- Check latest accuracy metric against expected labels.

### E) Processing Log

- View full processing events from processing_log.csv.
- Filter by agent and source ID.
- Download filtered log as CSV.

### F) Flow Explorer

- View `logs/pipeline_flow.log` directly in the app.
- Review latest markdown/json run reports.
- Browse historical run reports and download them.

### G) Configuration

- Change model, confidence threshold, and priority mappings.
- Save to .env for next run.

### H) Product Docs

- Upload product markdown docs for better bug/feature context retrieval.

## 5) How to Interpret Results

### New Learning Aids (Logs and Reports)

After each run, check:
- logs/pipeline_flow.log: stage-by-stage narrative logs for understanding agent flow.
- reports/latest_run_report.md: plain-English run summary.
- reports/latest_run_report.json: structured run summary for programmatic inspection.

### generated_tickets.csv

Each row is a generated ticket. Key fields:
- source_id, source_type: traceability to original feedback.
- category: one of the 5 classes.
- priority: Critical/High/Medium/Low.
- title, description: standardized action item.
- technical_details: extracted bug/feature detail JSON/text.
- is_duplicate, duplicate_of: duplicate detection signals.
- quality_score: ticket quality assessment.
- confidence: classifier confidence.

Interpretation tips:
- High confidence + high quality score usually indicates low manual effort.
- Low confidence or unusual category should be manually reviewed.
- Duplicate tickets should be merged or linked in project management tooling.

### processing_log.csv

Shows detailed per-agent activity:
- timestamp, agent_name, source_id, action, details, confidence

Interpretation tips:
- Use this file for auditability and debugging agent decisions.
- Repeated errors for the same source indicate malformed input or model issues.

### metrics.csv

Shows per-run summary:
- total_processed, category counts, avg_confidence, processing_time_seconds, accuracy

Interpretation tips:
- accuracy >= 0.80 indicates acceptable baseline match to expected labels.
- processing_time can be tracked to detect performance regressions.
- avg_confidence drift may indicate model/config changes affecting certainty.

## 6) Operating Modes

### Model-backed mode (OPENAI_API_KEY set)

- Uses AutoGen + OpenAI for agent reasoning.

### Fallback mode (no API key)

- Uses deterministic heuristics to keep pipeline runnable for demos/tests.
- Useful in restricted/offline environments.

## 7) Troubleshooting

### UI not loading

- Confirm Streamlit command and port availability.
- Try:

```powershell
streamlit run ui/app.py --server.port 8502
```

### Missing outputs

- Ensure at least one valid CSV input is present.
- Re-run from Run Pipeline page.

### Accuracy lower than expected

- Check input data quality.
- Tune thresholds in Configuration.
- Upload richer product docs in Product Docs page.

### Dependency errors

- Recreate venv and reinstall:

```powershell
pip install -r requirements.txt
```

## 8) Demo Flow (Presentation Ready)

1. Start with .\run_demo.ps1
2. Open Dashboard and show baseline metrics.
3. Go to Run Pipeline and execute with mock CSVs.
4. Show generated tickets and duplicate detection.
5. Show accuracy trend in Analytics.
6. Demonstrate Manual Override edits and save.
7. Show Processing Log for traceability.
