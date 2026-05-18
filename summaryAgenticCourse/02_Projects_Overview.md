# Projects Overview: Agentic AI Implementations

## Overview

This document details all projects built using Agentic AI principles, their architecture, technology stack, and the rationale behind each technology choice.

---

## Project 1: SignalDesk - Feedback Intelligence Hub

### Project Description

**Objective:** Automate feedback analysis from app store reviews and support emails, generate structured support tickets, with full observability and manual override capability.

**Complexity Level:** Intermediate (6-agent pipeline with RAG)

**Use Case:** SaaS/Mobile app support teams

**Key Problem Solved:**
- Manual ticket creation is slow and error-prone
- Categorizing feedback at scale is labor-intensive
- Technical details are often missed or misclassified
- Duplicate tickets waste developer time
- No visibility into what feedback looks like at scale

---

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Data Sources                           │
├──────────────────┬──────────────────┬──────────────────────┤
│ App Store        │ Support Emails   │ Product Docs         │
│ Reviews CSV      │ CSV              │ (for RAG context)    │
└──────────────────┴──────────────────┴──────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   ChromaDB Vector Store                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ feedback_    │  │ ticket_      │  │ product_     │     │
│  │ embeddings   │  │ embeddings   │  │ docs         │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  AutoGen Agent Pipeline                     │
├───────┬───────┬───────┬───────┬───────┬──────────┤
│ CSV   │Classi-│ Bug   │Feature│Ticket│Quality   │
│Reader │fier  │Analyzer│Extract│Create│Critic    │
└───────┴───────┴───────┴───────┴───────┴──────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Outputs & Storage                          │
├──────────────────┬──────────────────┬──────────────────────┤
│ generated_       │ processing_      │ metrics.csv          │
│ tickets.csv      │ log.csv          │ (run KPIs)           │
└──────────────────┴──────────────────┴──────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Streamlit UI                               │
│  Dashboard | Run Pipeline | Manual Override | Analytics    │
│  Processing Log | Configuration | Product Docs | Flow View │
└─────────────────────────────────────────────────────────────┘
```

---

### Technology Stack Breakdown

#### 1. **LLM Engine: OpenAI GPT-4o-mini**

**Choice:** OpenAI GPT-4o-mini

**Why:**
- **Speed** - Mini variant optimized for low latency (~1-2s per classification)
- **Cost** - Significantly cheaper than GPT-4 Turbo
- **Accuracy** - Still capable of complex reasoning and NLP tasks
- **Maturity** - Proven API, good documentation
- **Balance** - Fast enough for real-time, smart enough for accuracy

**Alternative Considered:** Claude 3.5 Sonnet
- Pros: Better reasoning, longer context
- Cons: More expensive, slower for simple classification

**Trade-off Decision:** Chose mini for cost optimization since classification is repetitive and doesn't need advanced reasoning

---

#### 2. **Agent Framework: AutoGen**

**Choice:** Microsoft AutoGen (autogen-agentchat)

**Why:**
- **Multi-agent Orchestration** - Built-in support for sequential and parallel agent coordination
- **State Management** - Clean JSON-based state passing between agents
- **Flexibility** - Works with any LLM provider
- **Fallback Support** - Built-in capability to fall back to heuristics
- **Scalability** - Handles 6-agent pipeline smoothly

**Architecture Pattern:**
```python
AutoGenPipelineCoordinator
├─ CSV Reader Agent
├─ Classifier Agent
├─ Bug Analyzer Agent
├─ Feature Extractor Agent
├─ Ticket Creator Agent
└─ Quality Critic Agent
```

**Alternative Considered:** LangChain
- Pros: Larger ecosystem, more integrations
- Cons: Overkill for this use case, more overhead

**Trade-off Decision:** AutoGen is simpler and more focused on agent orchestration

---

#### 3. **Knowledge Store: ChromaDB**

**Choice:** ChromaDB for vector embeddings

**Why:**
- **Lightweight** - No server required, in-memory by default
- **Python-First** - Direct Python API, no network overhead
- **Development Speed** - Instant setup for prototyping
- **RAG Implementation** - Purpose-built for semantic search
- **Similarity Matching** - Perfect for duplicate detection (vector similarity)

**Collections:**
1. **feedback_embeddings** - All input feedback for deduplication
2. **ticket_embeddings** - Generated tickets for duplicate detection
3. **product_docs** - Product documentation for RAG context

**How RAG Works:**
```
User Input → Embed → Vector Search in ChromaDB 
         → Retrieve similar docs → Add to LLM context 
         → Generate response with context
```

**Example Use:**
```
Bug: "Settings page crashes"
→ Search product_docs for "Settings crash"
→ Find: "Known issue BUG-101: Settings crash on Android 14"
→ Include in bug_analyzer context
→ Agent marks as known_bug_match
```

**Alternative Considered:** Pinecone
- Pros: Cloud-based, higher scale
- Cons: Monthly cost, network latency, overkill for development

**Trade-off Decision:** ChromaDB for development/learning, Pinecone for production scale

---

#### 4. **Data Persistence: SQLite + SQLAlchemy**

**Choice:** SQLite for database + SQLAlchemy ORM

**Why:**
- **Serverless** - No separate database server needed
- **Zero Configuration** - File-based database
- **Development Speed** - Instant setup
- **SQLAlchemy** - Type-safe, clean ORM abstraction
- **Production Ready** - SQLite handles moderate load

**Schema:**
```python
class Ticket(Base):
    id: int (primary key)
    source_id: str
    category: str
    priority: str
    title: str
    description: str
    quality_score: float
    is_duplicate: bool

class ProcessingLog(Base):
    timestamp: datetime
    agent_name: str
    action: str
    confidence: float

class Metric(Base):
    run_id: str
    total_processed: int
    accuracy: float
    processing_time: float
```

**Alternative Considered:** PostgreSQL
- Pros: Better for production scale (100+ concurrent users)
- Cons: Setup overhead, unnecessary for this project scale

**Trade-off Decision:** SQLite for development, PostgreSQL for enterprise deployment

---

#### 5. **UI Framework: Streamlit**

**Choice:** Streamlit for dashboard and operations interface

**Why:**
- **Python-First** - Write UI in pure Python, no HTML/CSS needed
- **Fast Prototyping** - Go from idea to interactive dashboard in hours
- **Learning-Friendly** - Perfect for educational projects
- **Real-Time Updates** - Hot reload on code changes
- **Built-In Widgets** - Buttons, forms, charts with minimal code
- **8-Page Multipage App** - Native support for multi-page dashboards

**Pages Implemented:**
```
Dashboard         → Overview metrics and real-time stats
Run Pipeline      → Trigger execution, see progress
Flow Explorer     → View logs and run reports
Manual Override   → Edit tickets and save changes
Analytics         → Charts and trends
Processing Log    → Audit trail, searchable
Configuration     → Adjust parameters
Product Docs      → Upload/manage docs
```

**Why Not:**
- React/Vue: Overkill for this scope, requires frontend engineer
- Flask/Django: More boilerplate, slower development

**Trade-off Decision:** Streamlit for 70% of MVP, could switch to React for mature product

---

#### 6. **Logging and Observability: Dual-Channel Logging**

**Choice:** File logging + CSV structured logging

**Why:**
- **Learning-Friendly** - Plain-English flow logs at [STAGE] level
- **Audit Trail** - CSV format for analysis and compliance
- **Machine-Readable** - processing_log.csv enables data analysis
- **Debuggable** - Timestamp and agent-level detail
- **Storage** - Can be queried and visualized later

**Dual Channels:**
```
1. pipeline_flow.log (Human-readable)
   [2026-05-18 20:29:25] [STAGE] CSV Reader
   [2026-05-18 20:29:25] [FLOW] Loading reviews and emails
   [2026-05-18 20:29:30] [FLOW] Stored 50 items in RAG

2. processing_log.csv (Machine-readable)
   timestamp,agent_name,source_id,action,details,confidence
   2026-05-18 20:29:30,CSV Reader,R001,LOAD,Loaded review from Google Play,1.0
   2026-05-18 20:29:35,Classifier,R001,CLASSIFY,Category: Bug,0.95
```

---

#### 7. **Deployment: Docker + Docker Compose**

**Choice:** Docker containerization

**Why:**
- **Reproducibility** - Same environment everywhere (dev, test, prod)
- **Dependency Management** - All Python packages isolated
- **Easy Scaling** - Spin up multiple instances
- **Cloud Ready** - Can deploy to any cloud
- **Docker Compose** - Multi-container orchestration locally

**Compose Services:**
```yaml
services:
  app:
    build: .
    ports: ["8501:8501"]  # Streamlit
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    env_file: .env
```

---

#### 8. **Fallback Mechanism: Deterministic Heuristics**

**Choice:** Rule-based fallback in agents/heuristics.py

**Why:**
- **Reliability** - System works without API key
- **Cost Control** - Skip expensive LLM calls for obvious cases
- **Speed** - Heuristics much faster than API calls
- **Testing** - Predictable behavior for unit tests
- **Resilience** - Graceful degradation if OpenAI is down

**Example:**
```python
# Primary path: Use LLM
if api_key_available:
    category = use_llm_to_classify(feedback)
else:
    # Fallback: Use heuristics
    if "crash" in feedback.lower():
        category = "Bug"
    elif "please add" in feedback.lower():
        category = "Feature Request"
    else:
        category = "Other"
```

---

### Input Data Format

#### app_store_reviews.csv
```
review_id,platform,rating,review_text,user_name,date,app_version
R001,Google Play,1,"App crashes...",Mike T.,2026-03-01,3.2.1
```
**Rationale:**
- review_id: Unique tracking
- platform: Different contexts (Play vs App Store)
- rating: User satisfaction indicator
- review_text: Main feedback content
- user_name: Traceability
- date: Temporal analysis
- app_version: Bug tracking relevance

#### support_emails.csv
```
email_id,subject,body,sender_email,timestamp,priority
E001,App Crash Report,...,email@company.com,2026-03-01 09:15:00,High
```
**Rationale:**
- email_id: Unique tracking
- subject: Title extraction
- body: Detailed information
- sender_email: Contact for follow-up
- timestamp: Priority ordering
- priority: User perception of urgency

#### expected_classifications.csv
```
source_id,source_type,category,priority,technical_details,suggested_title
R001,app_review,Bug,Critical,"Device: Pixel 7...",App Crash...
```
**Rationale:**
- Ground truth for accuracy measurement
- Allows comparative evaluation
- Validates model training/tuning

---

### Output Data Format

#### generated_tickets.csv
```
source_id, category, priority, title, description, technical_details,
is_duplicate, duplicate_of, quality_score, confidence
```
**Rationale:**
- Full traceability back to source
- Actionable fields (priority, title, description)
- Quality metrics for QA
- Duplicate management
- Confidence for filtering/review

#### processing_log.csv
```
timestamp, agent_name, source_id, action, details, confidence
```
**Rationale:**
- Complete audit trail
- Debugging capability
- Pattern analysis
- Learning from decisions
- Compliance/accountability

#### metrics.csv
```
run_id, total_processed, accuracy, avg_confidence, processing_time,
bugs_count, features_count, praise_count, complaints_count, spam_count
```
**Rationale:**
- Performance tracking
- Trend analysis
- Cost estimation
- SLA validation

---

### Agent Responsibilities

| Agent | Input | Output | Tech Used | Why |
|-------|-------|--------|-----------|-----|
| CSV Reader | CSV files | Normalized feedback items | Pandas | Standard data library |
| Classifier | Feedback text | Category + confidence | AutoGen + GPT-4o-mini | NLP classification |
| Bug Analyzer | Bug category items | Severity, component, known_bug | RAG + GPT-4o-mini | Technical extraction |
| Feature Extractor | Feature category items | Impact score, roadmap status | RAG + GPT-4o-mini | Strategic analysis |
| Ticket Creator | Enriched items | Structured tickets | ChromaDB + SQLAlchemy | Dedup + storage |
| Quality Critic | Generated tickets | Quality score + revisions | GPT-4o-mini | Meta-analysis |

---

### Key Design Decisions

#### 1. **Why Sequential Pipeline Over Parallel?**
- Categorization must happen first (determines downstream agents)
- Bug/Feature data enriches ticket creation
- Quality review is final stage
- Sequential is simpler to debug

#### 2. **Why RAG for Bug/Feature Analysis?**
- Provides domain context (product docs)
- Reduces hallucinations
- Improves accuracy
- Examples: matching bugs to known issues, checking roadmap

#### 3. **Why Duplicate Detection?**
- Prevents wasted developer time
- Vector similarity captures semantic meaning
- Users describe same issue differently
- Example: "Settings crash" vs "Account tab freezes" = same bug

#### 4. **Why Quality Scoring?**
- Automatic QA before human review
- Identifies weak outputs for revision
- Trains team on quality standards
- Threshold-based automation (score < 0.7 → revise)

#### 5. **Why Manual Override?**
- Agents aren't perfect
- Domain experts can correct
- Builds feedback loop for improvement
- Addresses edge cases

---

### Performance Characteristics

**Latest Run (50 items):**
- Processing Time: ~90 seconds
- Classification Accuracy: 87%
- Average Confidence: 0.9048
- Unique Tickets Generated: 42
- Duplicates Detected: 8 (16%)
- Average Quality Score: 0.944

**Scalability:**
- Current: 50 items in 90 seconds = ~33 items/minute
- Estimated: Could handle 500-1000 items/run with parallel batch processing
- Bottleneck: LLM API rate limits (not code)

---

### Trade-offs Made

| Choice | Alternative | Why We Chose This | Cost |
|--------|-------------|-------------------|------|
| OpenAI GPT-4o-mini | Local LLaMA model | Speed + accuracy needed | $0.05/1K input tokens |
| AutoGen | Building custom orchestrator | Time to market | 0 (open source) |
| ChromaDB | DIY with numpy | Zero setup | 0 (open source) |
| SQLite | PostgreSQL | Development speed | 0 (open source) |
| Streamlit | React + Flask | Prototype speed | 0 (open source) |
| Docker | No containerization | Production consistency | 0 (open source) |

---

### Production Considerations

If scaling SignalDesk to production:
1. **Database** → Migrate SQLite to PostgreSQL
2. **Vector Store** → Migrate ChromaDB to Pinecone (managed, scalable)
3. **LLM** → Consider batching to reduce costs
4. **UI** → Build custom React app for branding
5. **Deployment** → Kubernetes for auto-scaling
6. **Monitoring** → Add Datadog/New Relic for observability
7. **Cache** → Add Redis for result caching

---

## Project Template

**For building your own agentic system, use this template:**

```
Your Project
├─ Data Layer
│  ├─ Input: CSV/API/Database
│  └─ Storage: SQLite/PostgreSQL
├─ Knowledge Layer
│  ├─ Vector Store: ChromaDB/Pinecone
│  └─ Embeddings: OpenAI/HuggingFace
├─ Agent Layer
│  ├─ Orchestrator: AutoGen/LangChain
│  ├─ Agents: Specialized workers
│  └─ Fallback: Heuristics engine
├─ Output Layer
│  ├─ CSV logs
│  ├─ Database records
│  └─ API webhooks
└─ UI Layer
   ├─ Dashboard: Streamlit/React
   └─ Monitoring: Logs + charts
```

---

## Lessons Learned

1. **Start Simple** - Begin with heuristics, add LLM later
2. **Logging is Critical** - Invest early in observability
3. **Ground Truth Matters** - Can't measure accuracy without expected_classifications.csv
4. **Fallback First** - Always have a non-LLM path
5. **Iterative Refinement** - Quality scoring + manual override creates feedback loop
6. **Multi-Agent > Single Agent** - Specialized agents outperform generalist
7. **RAG Boosts Accuracy** - Domain context significantly improves results
8. **Testing at Scale** - Test with realistic data volume (50+ items)

