# SignalDesk Product Demo Script (5-7 Minutes)

A guided walkthrough showcasing the agentic feedback operations platform in action.

## 0) Opening (30-45 sec)

Welcome to SignalDesk—an agentic feedback operations platform designed to handle high-volume user feedback at enterprise scale.

SignalDesk transforms feedback triage from a manual, slow process into an intelligent, automated pipeline. It reads app reviews and support emails, classifies them with high confidence, enriches them with product context, generates ready-to-act tickets, and maintains full auditability for compliance and learning.

## 1) Business Problem (45-60 sec)

When customer feedback comes in at scale—across app stores and support channels—manual triage breaks down:
- Critical bugs get lost in the noise while praise sits unread.
- Priority assignment varies widely across team members.
- There's no audit trail explaining why a ticket was created or closed.
- Engineers waste time parsing raw customer text instead of working with structured tickets.

SignalDesk solves this by automating the entire feedback-to-ticket workflow while keeping humans in control when it matters.

## 2) How It Works (60-75 sec)

SignalDesk uses a six-stage agentic pipeline:
1. **Ingestion** – Reads structured feedback from CSV files and normalizes into a unified schema.
2. **Classification** – Categorizes each item (bug, feature, praise, complaint, spam) with confidence scoring.
3. **Bug Enrichment** – For bugs, extracts device info, OS, reproduction steps, and matches against known issues.
4. **Feature Enrichment** – For feature requests, evaluates impact and cross-references planned features.
5. **Ticket Generation** – Creates standardized tickets and detects duplicates using vector similarity.
6. **Quality Review** – Scores ticket completeness and clarity; revises low-quality entries.

All data flows through ChromaDB for semantic search, SQLite for persistence, and the Streamlit UI for human oversight and intervention.

## 3) Live Demo Steps (3-4 min)

### Step A: Launch demo

Run:

```powershell
.\run_demo.ps1
```

Explain:
- It executes the pipeline on the mock dataset.
- Then starts Streamlit at http://localhost:8501.

### Step B: Run Pipeline page

Show:
- CSV inputs are loaded.
- Trigger pipeline and stage-by-stage progress.

Narration:
- The system classifies each item and routes it through bug/feature extraction as needed.

### Step C: Dashboard page

Show:
- Total processed count,
- Category breakdown,
- Generated tickets table.

Narration:
- Tickets are standardized with title, priority, details, confidence, and quality score.

### Step D: Analytics page

Show:
- Accuracy metric,
- Confidence distribution,
- Processing time and run history.

Narration:
- Accuracy is computed against expected_classifications.csv and saved to metrics.csv.

### Step E: Manual Override page

Show:
- Edit category/priority/title/description for a ticket.
- Save changes.

Narration:
- This supports human-in-the-loop control for edge cases.

### Step F: Processing Log page

Show:
- Filter by agent and source_id.

Narration:
- Full audit trail gives traceability from input feedback to final ticket decision.

## 4) Operational Outputs (45-60 sec)

Show the generated artifacts:
- `data/generated_tickets.csv` - Standardized tickets ready for your ticketing system
- `data/processing_log.csv` - Full decision audit trail for compliance and learning
- `data/metrics.csv` - Performance KPIs including classification accuracy and run timing

Key benefit:
- These outputs integrate with downstream systems and enable data-driven feedback analysis.

## 5) Key Differentiators (30-45 sec)

What makes SignalDesk unique:
- **Modular agents** - Each stage is independently testable and can be configured or extended
- **Product-aware reasoning** - Feeds product docs to agents for smarter, context-aware decisions
- **Human oversight** - Manual override page lets you correct edge cases and tune the system
- **Auditability** - Every decision is logged with reasoning for compliance and improvement
- **Offline mode** - Falls back to deterministic heuristics when API keys aren't available

This makes SignalDesk suitable for regulated industries and high-compliance environments.

## 6) Closing (20-30 sec)

SignalDesk significantly reduces manual feedback triage effort, improves consistency, and creates visibility across the entire feedback-to-action lifecycle.

This enables product teams to respond faster to critical issues, prioritize roadmap features based on user demand, and maintain a scalable feedback loop as your user base grows.

Get started with your feedback data, and SignalDesk will be processing tickets within minutes.

## Optional Q&A Prompts

If asked about offline behavior:
- SignalDesk includes a deterministic fallback mode that works without API keys, useful for development and testing.

If asked about scalability:
- The architecture uses AutoGen for orchestration and ChromaDB for efficient similarity search, supporting thousands of feedback items per run.

If asked about integration:
- Generated tickets are CSV-formatted and JSON-reportable, making it easy to import into Jira, Linear, or other ticketing systems.

