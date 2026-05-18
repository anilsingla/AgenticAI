# SignalDesk Feedback Intelligence Hub

An AI-powered multi-agent system that automatically processes user feedback from app store reviews and support emails, classifies them, extracts actionable insights, and generates structured support tickets, all with RAG-enhanced context from product documentation.

## Features

- **Automated Feedback Classification** â€” Classifies feedback into Bug, Feature Request, Praise, Complaint, or Spam with confidence scores
- **RAG-Enhanced Bug Analysis** â€” Matches reported bugs against known issues using product documentation stored in ChromaDB
- **RAG-Enhanced Feature Extraction** â€” Cross-references feature requests with the product roadmap to identify already-planned features
- **Duplicate Detection** â€” Uses vector similarity search across feedback and ticket embeddings to flag duplicates
- **Quality Assurance** â€” Auto-reviews and revises low-quality tickets (score < 0.7)
- **Interactive Dashboard** â€” Real-time metrics, charts, and ticket management via Streamlit
- **Product Docs Upload** â€” Upload technical documentation to enrich RAG context for agents
- **Configurable Pipeline** â€” Adjust model, thresholds, and priority mappings from the UI

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| LLM Engine | OpenAI GPT-4o-mini | Feedback reasoning and extraction |
| Agent Framework | AutoGen | Multi-agent coordination and state flow |
| Knowledge Store | ChromaDB | Vector embeddings for RAG (feedback, tickets, product docs) |
| Data Layer | SQLite + SQLAlchemy | Persistent ticket and metrics storage |
| UI Layer | Streamlit | Real-time dashboard and operations interface |
| Deployment | Docker Compose | Container orchestration for reproducibility |
| Runtime | Python 3.14 | Core implementation language |

## Architecture

### System Overview

```mermaid
graph TB
    subgraph Input["Data Sources"]
        CSV1[App Store Reviews CSV]
        CSV2[Support Emails CSV]
        DOCS[Product Documentation]
    end

    subgraph RAG["ChromaDB Vector Store"]
        FC[feedback_embeddings]
        TC[ticket_embeddings]
        PDC[product_docs]
    end

    subgraph Pipeline["AutoGen Agent Pipeline"]
        A1[CSV Reader Agent]
        A2[Classifier Agent]
        A3[Bug Analyzer Agent]
        A4[Feature Extractor Agent]
        A5[Ticket Creator Agent]
        A6[Quality Critic Agent]
    end

    subgraph Storage["Persistent Storage"]
        DB[(SQLite DB)]
        OUT1[generated_tickets.csv]
        OUT2[metrics.csv]
        OUT3[processing_log.csv]
    end

    subgraph UI["Streamlit UI"]
        D[Dashboard]
        RP[Run Pipeline]
        MO[Manual Override]
        AN[Analytics]
        PL[Processing Log]
        CF[Configuration]
        PD[Product Docs Upload]
    end

    CSV1 & CSV2 --> A1
    DOCS --> PDC
    A1 -->|stores feedback| FC
    A1 --> A2
    A2 --> A3
    A2 --> A4
    A3 -.->|queries| PDC
    A4 -.->|queries| PDC
    A3 & A4 --> A5
    A5 -.->|queries & stores| TC
    A5 -.->|queries| FC
    A5 --> A6
    A6 --> Storage
    Storage --> UI
```

### Agent Pipeline Flow

```mermaid
flowchart LR
    START((Start)) --> CSVReader

    subgraph Ingestion
        CSVReader[CSV Reader\nAgent]
    end

    subgraph Classification
        Classifier[Classifier\nAgent]
    end

    subgraph Analysis
        BugAnalyzer[Bug Analyzer\nAgent]
        FeatureExtractor[Feature Extractor\nAgent]
    end

    subgraph TicketGen["Ticket Generation"]
        TicketCreator[Ticket Creator\nAgent]
        QualityCritic[Quality Critic\nAgent]
    end

    CSVReader --> Classifier
    Classifier --> BugAnalyzer
    BugAnalyzer --> FeatureExtractor
    FeatureExtractor --> TicketCreator
    TicketCreator --> QualityCritic
    QualityCritic --> SaveOutputs[Save Outputs]
    SaveOutputs --> DONE((End))

    style CSVReader fill:#4CAF50,color:#fff
    style Classifier fill:#2196F3,color:#fff
    style BugAnalyzer fill:#FF9800,color:#fff
    style FeatureExtractor fill:#FF9800,color:#fff
    style TicketCreator fill:#9C27B0,color:#fff
    style QualityCritic fill:#F44336,color:#fff
```

### RAG Architecture

```mermaid
graph LR
    subgraph Collections["ChromaDB Collections"]
        C1["feedback_embeddings\n(reviews + emails)"]
        C2["ticket_embeddings\n(generated tickets)"]
        C3["product_docs\n(technical docs)"]
    end

    subgraph Agents
        CSVReader[CSV Reader] -->|upsert| C1
        BugAnalyzer[Bug Analyzer] -->|query| C3
        FeatureExtractor[Feature Extractor] -->|query| C3
        TicketCreator[Ticket Creator] -->|query| C1
        TicketCreator -->|query + upsert| C2
    end

    subgraph DocUpload["Product Docs Upload (UI)"]
        Upload[Upload .md files] -->|chunk by ## headings| C3
    end
```

### Data Flow

```mermaid
flowchart TD
    subgraph Input
        R[app_store_reviews.csv\n30 rows]
        E[support_emails.csv\n20 rows]
    end

    subgraph Processing
        R & E --> PARSE[Parse & Normalize\ninto FeedbackItems]
        PARSE --> CLASS{Classify}
        CLASS -->|Bug| BUG[Bug Analysis\n+ RAG Lookup]
        CLASS -->|Feature Request| FEAT[Feature Extraction\n+ Roadmap Check]
        CLASS -->|Praise / Complaint / Spam| SKIP[Skip Analysis]
        BUG & FEAT & SKIP --> TICKET[Create Tickets\n+ Duplicate Detection]
        TICKET --> QA[Quality Review\n& Auto-Revision]
    end

    subgraph Output
        QA --> CSV[generated_tickets.csv]
        QA --> DB[(SQLite: tickets + metrics)]
        QA --> LOG[processing_log.csv]
        QA --> MET[metrics.csv]
    end
```

## Project Structure

```
FeedbackAnalysisApp/
â”œâ”€â”€ agents/                    # AutoGen-backed agent modules
â”‚   â”œâ”€â”€ bug_analyzer.py        # Bug analysis with product docs RAG
â”‚   â”œâ”€â”€ classifier.py          # Feedback classification (5 categories)
â”‚   â”œâ”€â”€ csv_reader.py          # CSV ingestion + RAG storage
â”‚   â”œâ”€â”€ feature_extractor.py   # Feature extraction with roadmap RAG
â”‚   â”œâ”€â”€ heuristics.py          # Deterministic fallback logic for offline/demo runs
â”‚   â”œâ”€â”€ llm.py                 # Shared AutoGen/OpenAI helper + JSON parsing
â”‚   â”œâ”€â”€ pipeline.py            # AutoGen orchestration + output saving
â”‚   â”œâ”€â”€ quality_critic.py      # Ticket quality review + auto-revision
â”‚   â”œâ”€â”€ state.py               # PipelineState & FeedbackItem TypedDicts
â”‚   â””â”€â”€ ticket_creator.py      # Ticket creation + duplicate detection
â”œâ”€â”€ config/                    # Configuration & infrastructure
â”‚   â”œâ”€â”€ database.py            # SQLAlchemy models (Ticket, Metric, ProcessingLog)
â”‚   â”œâ”€â”€ logger.py              # Structured logging to CSV + console
â”‚   â”œâ”€â”€ settings.py            # Central config from .env
â”‚   â””â”€â”€ vectorstore.py         # ChromaDB setup (3 collections) + helpers
â”œâ”€â”€ data/                      # Input data & outputs
â”‚   â”œâ”€â”€ app_store_reviews.csv  # Mock app reviews (30 rows)
â”‚   â”œâ”€â”€ support_emails.csv     # Mock support emails (20 rows)
â”‚   â”œâ”€â”€ expected_classifications.csv  # Ground truth labels
â”‚   â””â”€â”€ product_docs/          # Technical docs for RAG
â”‚       â”œâ”€â”€ architecture.md
â”‚       â”œâ”€â”€ features.md
â”‚       â”œâ”€â”€ known_bugs.md
â”‚       â””â”€â”€ roadmap.md
â”œâ”€â”€ ui/                        # Streamlit frontend
â”‚   â”œâ”€â”€ app.py                 # Main app with sidebar navigation
â”‚   â””â”€â”€ pages/
â”‚       â”œâ”€â”€ dashboard.py       # Overview metrics & ticket table
â”‚       â”œâ”€â”€ run_pipeline.py    # CSV upload & pipeline execution
â”‚       â”œâ”€â”€ configuration.py   # Settings panel (model, thresholds)
â”‚       â”œâ”€â”€ manual_override.py # Inline ticket editing
â”‚       â”œâ”€â”€ analytics.py       # Charts & statistics
â”‚       â”œâ”€â”€ processing_log.py  # Filterable log viewer
â”‚       â””â”€â”€ product_docs.py    # Upload & manage RAG documents
â”œâ”€â”€ tests/                     # Test suite (pytest)
â”œâ”€â”€ logs/                      # Human-readable runtime flow logs
â”‚   â””â”€â”€ pipeline_flow.log
â”œâ”€â”€ reports/                   # Per-run summary reports for beginners
â”‚   â”œâ”€â”€ latest_run_report.md
â”‚   â””â”€â”€ latest_run_report.json
â”œâ”€â”€ Dockerfile
â”œâ”€â”€ docker-compose.yml
â”œâ”€â”€ requirements.txt
â””â”€â”€ .env                       # Environment configuration
```

## Learning-Friendly Observability

To understand flow quickly after each run:

- Read `logs/pipeline_flow.log` for stage-by-stage runtime narration.
- Read `reports/latest_run_report.md` for a plain-English run summary.
- Read `reports/latest_run_report.json` for machine-readable run details.
- Open the **Flow Explorer** page in Streamlit to view logs/reports in-app.

## Quick Start

## Guides

- Requirements traceability: `docs/REQUIREMENTS_TRACEABILITY.md`
- User guide (deploy, run, interpret results): `docs/USER_GUIDE.md`
- Developer guide (architecture, components, setup, stack): `docs/DEVELOPER_GUIDE.md`
- Demo presentation script (5-7 min talk track): `docs/DEMO_PRESENTATION_SCRIPT.md`

## One-Click Demo

From the `FeedbackAnalysisApp/` folder:

```powershell
.\run_demo.ps1
```

Options:

```powershell
# Skip pipeline and only start UI
.\run_demo.ps1 -SkipPipeline

# Run on a custom port
.\run_demo.ps1 -Port 8502
```

### Prerequisites

- Docker & Docker Compose
- OpenAI API key for model-backed runs

If no API key is configured, the application still runs using deterministic fallback logic for demo and testing flows.

### Run with Docker

```bash
# Set your OpenAI API key in .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Build and start
docker compose up --build -d

# Open in browser
open http://localhost:8501
```

### Run Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=sk-your-key-here

# Run the Streamlit app
streamlit run ui/app.py
```

## Usage

1. **Run Pipeline** â€” Upload CSV files or use the included mock data, then click "Run Analysis Pipeline"
2. **Dashboard** â€” View processed feedback metrics, category/priority charts, and generated tickets
3. **Manual Override** â€” Edit ticket fields (title, category, priority, description) inline
4. **Analytics** â€” Explore quality scores, confidence distributions, and processing trends
5. **Product Docs** â€” Upload technical documentation (.md files) to improve RAG context
6. **Configuration** â€” Adjust model, confidence thresholds, and priority mappings

## Agent Details

| Agent | Role | RAG Usage |
|---|---|---|
| **CSV Reader** | Parses reviews + emails into unified schema | Stores all feedback in `feedback_embeddings` |
| **Classifier** | Categorizes into Bug / Feature / Praise / Complaint / Spam | â€” |
| **Bug Analyzer** | Extracts severity, component, steps to reproduce | Queries `product_docs` for known bugs & root causes |
| **Feature Extractor** | Extracts impact score, user segment, planned status | Queries `product_docs` for roadmap & existing features |
| **Ticket Creator** | Generates structured tickets with duplicate detection | Queries `feedback_embeddings` + `ticket_embeddings` |
| **Quality Critic** | Scores ticket quality (0-1), auto-revises if < 0.7 | â€” |

## Configuration

Key settings in `.env`:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | â€” | OpenAI API key (required) |
| `LLM_MODEL_NAME` | `gpt-4o-mini` | Model for all agents |
| `CLASSIFICATION_CONFIDENCE_THRESHOLD` | `0.7` | Min confidence for auto-classification |
| `CRITICAL_RATING_THRESHOLD` | `1` | Rating threshold for Critical priority |
| `HIGH_RATING_THRESHOLD` | `2` | Rating threshold for High priority |
| `MEDIUM_RATING_THRESHOLD` | `3` | Rating threshold for Medium priority |

