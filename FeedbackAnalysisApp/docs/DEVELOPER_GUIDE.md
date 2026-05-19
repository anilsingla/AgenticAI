# Developer Guide

This guide is for engineers maintaining or extending FeedbackAnalysisApp.

## 1) Architecture Overview

The system is a multi-agent pipeline with RAG-backed context and CSV outputs.

High-level flow:
1. CSV Reader ingests and normalizes records.
2. Classifier assigns category + confidence.
3. Bug Analyzer enriches bug items.
4. Feature Extractor enriches feature items.
5. Ticket Creator generates structured tickets + duplicate checks.
6. Quality Critic validates/revises ticket quality.
7. Pipeline saves ticket/log/metric outputs and DB snapshots.

## 2) Component Breakdown

### Agents

- agents/csv_reader.py
  - Reads input CSVs into unified feedback items.
  - Upserts raw feedback to Chroma feedback collection.

- agents/classifier.py
  - Categorizes each item.
  - Uses AutoGen/OpenAI when configured; otherwise deterministic fallback.

- agents/bug_analyzer.py
  - Extracts bug details (severity, component, steps, known bug match).
  - Uses product-doc RAG context.

- agents/feature_extractor.py
  - Extracts feature summary, impact, segment, roadmap alignment.

- agents/ticket_creator.py
  - Creates final ticket payload for actionable categories.
  - Performs duplicate detection using feedback + ticket embeddings.

- agents/quality_critic.py
  - Scores and optionally revises low-quality tickets.

- agents/pipeline.py
  - AutoGen-based orchestration wrapper.
  - Executes full stage sequence and writes outputs.
  - Computes classification accuracy vs expected labels.

- agents/heuristics.py
  - Deterministic fallback for classification/analysis/ticketing/review.
  - Ensures runnability without external model access.

- agents/llm.py
  - AutoGen model client setup and JSON response utilities.

### Configuration and Infra

- config/settings.py
  - .env configuration loader and typed constants.

- config/vectorstore.py
  - Chroma client/collection helpers and product doc loader/chunker.

- config/database.py
  - SQLAlchemy models (Ticket, ProcessingLog, Metric) and session helpers.

- config/logger.py
  - Structured CSV and console logging.

### UI (Streamlit)

- ui/app.py
  - Multipage entry and navigation.

- ui/pages/*
  - dashboard.py, run_pipeline.py, configuration.py,
    manual_override.py, analytics.py, processing_log.py, product_docs.py

### Data

- data/app_store_reviews.csv
- data/support_emails.csv
- data/expected_classifications.csv
- data/product_docs/*.md
- Outputs:
  - data/generated_tickets.csv
  - data/processing_log.csv
  - data/metrics.csv

### Logs and Reports

- logs/pipeline_flow.log
  - Human-readable flow logs for stage-level understanding.

- reports/latest_run_report.md
  - Friendly summary of the latest run.

- reports/latest_run_report.json
  - Structured summary for tooling/automation.

- reports/run_<run_id>.md and reports/run_<run_id>.json
  - Historical per-run reports.

## 3) Technology Stack

- Language: Python 3.14+
- Agent framework: AutoGen
  - autogen-agentchat
  - autogen-ext[openai]
- UI: Streamlit
- Data processing: pandas
- Vector store / RAG: ChromaDB
- Persistence: SQLite + SQLAlchemy
- Testing: pytest, pytest-cov, pytest-asyncio
- Deployment: Docker + docker-compose

## 4) Setup for Development

### Local setup

```powershell
cd FeedbackAnalysisApp
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional for model-backed mode:

```powershell
$env:OPENAI_API_KEY="your-key"
```

### Run pipeline only

```powershell
python -m agents.pipeline
```

### Run UI only

```powershell
streamlit run ui/app.py
```

### One-click demo

```powershell
.\deployment\windows-local\run_demo.ps1
```

## 5) Configuration Model

Managed in config/settings.py and .env.

Key variables:
- OPENAI_API_KEY
- LLM_MODEL_NAME
- CLASSIFICATION_CONFIDENCE_THRESHOLD
- CRITICAL_RATING_THRESHOLD
- HIGH_RATING_THRESHOLD
- MEDIUM_RATING_THRESHOLD
- INPUT/OUTPUT path variables

Notes:
- Missing OPENAI_API_KEY triggers deterministic fallback behavior.
- Configuration page writes to .env for next-run settings.

## 6) Accuracy and Evaluation

Accuracy source:
- data/expected_classifications.csv

Calculation implementation:
- agents/pipeline.py
- Weighted score:
  - Category match: 75%
  - Priority match: 25%

Result persistence:
- accuracy field in data/metrics.csv

## 7) Error Handling Strategy

- Agent-level try/except to continue processing when single items fail.
- Errors accumulated in pipeline state.
- Structured logs include agent name, action, details, confidence.
- Fallback mode avoids hard failure when model credentials are absent.

## 8) Extension Patterns

### Add a new category

1. Update category definitions in config/settings.py.
2. Extend classification logic in agents/classifier.py and agents/heuristics.py.
3. Reflect changes in UI filters and analytics visualizations.
4. Update expected_classifications.csv and tests.

### Add a new agent stage

1. Implement new stage function under agents/.
2. Insert stage call in agents/pipeline.py.
3. Add structured logging and output field mapping.
4. Extend tests for regression coverage.

### Improve duplicate detection

1. Tune vector query thresholding and features in agents/ticket_creator.py.
2. Add metadata filters in config/vectorstore.py.
3. Validate with synthetic near-duplicate fixtures.

## 9) Testing Strategy

Current tests include:
- tests/agents/test_heuristics.py
- tests/integration/test_pipeline_outputs.py

Recommended additions:
- Agent unit tests with fixture-driven expectations.
- Snapshot tests for ticket schema stability.
- UI smoke tests for Streamlit pages.
- Accuracy regression tests over controlled datasets.

## 10) Code Reading Order (Suggested)

For new contributors:
1. agents/state.py
2. agents/pipeline.py
3. agents/csv_reader.py
4. agents/classifier.py
5. agents/bug_analyzer.py and agents/feature_extractor.py
6. agents/ticket_creator.py
7. agents/quality_critic.py
8. ui/app.py + ui/pages/
9. config/*

## 11) Architecture Notes

- The architecture is intentionally modular: each agent owns one concern.
- Pipeline coordination is centralized, while business logic remains inside agents.
- The fallback layer supports deterministic execution, which helps CI and demos.
- RAG collections are split by purpose for cleaner retrieval behavior:
  - feedback_embeddings
  - ticket_embeddings
  - product_docs
