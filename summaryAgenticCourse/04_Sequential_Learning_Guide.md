# Sequential Learning Guide: Master Agentic AI

This guide provides a structured learning path to understand and implement agentic AI systems, from foundations to production.

---

## Learning Path Overview

```
Phase 1: Fundamentals (Week 1-2)
├─ Understand AI agents
├─ Learn agent frameworks
└─ Basic LLM concepts

Phase 2: Core Concepts (Week 3-4)
├─ Multi-agent systems
├─ RAG and knowledge retrieval
├─ State management
└─ Tool use and function calling

Phase 3: Hands-On Building (Week 5-8)
├─ Build first agent
├─ Build multi-agent system
├─ Add RAG context
└─ Create observability

Phase 4: Production Systems (Week 9-12)
├─ Error handling and resilience
├─ Performance optimization
├─ Deployment patterns
└─ Monitoring and scaling
```

---

## Phase 1: Fundamentals (Week 1-2)

### Week 1: Day 1-2 — Core Concepts

**Learning Objectives:**
- [ ] Understand what agentic AI is
- [ ] Learn the difference between chatbots and agents
- [ ] Understand the agent loop (sense → reason → act)

**Reading:**
1. [01_Agentic_AI_Fundamentals.md](01_Agentic_AI_Fundamentals.md) - Sections 1-3
   - What is Agentic AI?
   - Key Characteristics
   - Core Topics: Multi-Agent Systems

**Key Concepts to Understand:**
```
Agent Loop:
┌────────────────────────────┐
│ 1. Observe environment     │ (What's happening now?)
│ 2. Reason about action     │ (What should I do?)
│ 3. Execute action          │ (Do it)
│ 4. Get feedback            │ (Did it work?)
│ 5. Update state            │ (Remember for next time)
└────────────────────────────┘
```

**Exercise 1.1: Identify Agent Loops**
```
Task: Read these scenarios and identify the agent loop:

Scenario 1: "Email classifier agent"
  1. Observe: Read incoming email
  2. Reason: Classify into spam/important/later
  3. Act: Move to appropriate folder
  4. Feedback: User marks as correct/incorrect
  5. Update: Remember pattern for similar emails

Scenario 2: "Customer support chatbot"
  1. Observe: Customer message received
  2. Reason: Understand customer issue
  3. Act: Generate response (could call tools)
  4. Feedback: Did customer get solution?
  5. Update: Add to knowledge base

Practice: Describe the agent loop for your own use case
```

**Discussion:** What's the difference?
```
Chatbot: Responds to queries
Agent: Works toward goals autonomously

Chatbot: "What is the weather?"
        "It is sunny, 72°F"
        END

Agent: Goal: "Get me the best umbrella deal"
       1. Search web for umbrella deals
       2. Compare prices and reviews
       3. Check my budget
       4. Present top 3 options
       5. Help user decide
```

---

### Week 1: Day 3-4 — Agent Frameworks Overview

**Learning Objectives:**
- [ ] Understand different frameworks
- [ ] Know when to use each
- [ ] Set up your first framework

**Reading:**
1. [03_Alternative_Frameworks_And_Tools.md](03_Alternative_Frameworks_And_Tools.md) - Agent Frameworks section
   - AutoGen basics
   - LangChain basics
   - Pydantic AI basics

**Framework Comparison Chart:**
```
AutoGen:
  - Best for: Multi-agent orchestration
  - Learning curve: Low
  - Setup time: 5 minutes
  - Best for learning: ✅ YES

LangChain:
  - Best for: Complex workflows + integrations
  - Learning curve: High
  - Setup time: 15 minutes
  - Best for learning: ⚠️ Start with AutoGen first

Pydantic AI:
  - Best for: Type-safe outputs
  - Learning curve: Medium
  - Setup time: 5 minutes
  - Best for learning: ✅ YES (after AutoGen)
```

**Exercise 1.2: Set Up Your First Framework**

Option A: AutoGen (Recommended for learning)
```python
# Installation
pip install autogen-agentchat autogen-ext[openai]

# First agent
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIModelClient

# Create client
client = OpenAIModelClient(model="gpt-4o-mini")

# Create agent
agent = AssistantAgent(
    name="helper",
    model_client=client,
    system_message="You are a helpful assistant."
)

print("Framework installed successfully!")
```

Option B: Pydantic AI (Simple alternative)
```python
# Installation
pip install pydantic-ai openai

# First agent
from pydantic_ai import Agent

agent = Agent(model="openai:gpt-4o-mini")

result = agent.run_sync("What is 2+2?")
print(result.data)
```

**Exercise 1.3: Compare Frameworks with Code**
```
Write hello world in each framework and note:
1. Lines of code needed
2. Setup complexity
3. Learning curve feeling
4. Which feels more natural?
```

---

### Week 1: Day 5 — LLM Fundamentals

**Learning Objectives:**
- [ ] Understand how LLMs work at high level
- [ ] Know the difference between LLM providers
- [ ] Set up API keys for local development

**Reading:**
1. [03_Alternative_Frameworks_And_Tools.md](03_Alternative_Frameworks_And_Tools.md) - LLM Comparison section

**Key Concepts:**
```
Prompt:          Input text you give to LLM
                 "Classify this text: '...'"

Tokens:          Chunks of text/numbers
                 ~4 characters = 1 token
                 "Hello" = 1 token
                 "world" = 1 token

Temperature:     Creativity setting
                 0.0 = Deterministic (same output always)
                 1.0 = Creative (different outputs)
                 For classification: Use 0.0

Context Window:  Max tokens in conversation
                 GPT-4o-mini: 128K tokens
                 Claude: 200K tokens
                 More = more history/documents
```

**Exercise 1.4: Calculate API Costs**
```
SignalDesk example:
- 50 items to classify
- Input: ~30 tokens/item = 1,500 tokens
- Output: ~10 tokens/item = 500 tokens
- Total: 2,000 tokens

Cost (GPT-4o-mini):
- Input: $0.05 per 1M = $0.000075
- Output: $0.15 per 1M = $0.000075
- Total: $0.00015 per run

For 100 runs/month:
- Cost: $0.015/month (basically free!)

Calculate for your use case:
- How many items?
- How many tokens?
- What's your monthly cost?
```

**Setup Exercise 1.5: Create Your First API Key**

```python
# 1. Create OpenAI account: openai.com
# 2. Create API key: https://platform.openai.com/api-keys
# 3. Save to environment

# Create .env file
OPENAI_API_KEY=sk-...your-key...

# In Python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {api_key[:10]}...")
```

---

### Week 2: Day 1-2 — First Working Agent

**Learning Objectives:**
- [ ] Build your first working agent
- [ ] Understand prompt engineering
- [ ] Get comfortable with API calls

**Project: Email Classifier Agent**

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIModelClient

# Create client with API key
client = OpenAIModelClient(model="gpt-4o-mini")

# Define the classifier agent
classifier = AssistantAgent(
    name="email_classifier",
    model_client=client,
    system_message="""You are an email classifier. 
Your job is to classify incoming emails into one category:
- URGENT: Requires immediate attention (payment issues, outage, etc.)
- SUPPORT: Support requests (bugs, features, how-to)
- FEEDBACK: Product feedback (improvements, suggestions)
- SPAM: Irrelevant or promotional content

Respond with ONLY the category name, nothing else.
"""
)

# Test emails
test_emails = [
    "Our site is down! We need immediate help!",
    "Can you add dark mode to your app?",
    "Buy cheap followers here!",
    "The login button doesn't work on mobile"
]

# Classify each
for email in test_emails:
    response = classifier.run_sync(email)
    print(f"Email: {email[:40]}...")
    print(f"Classification: {response.data}\n")
```

**What's Happening:**
```
1. System message sets agent role/expectations
2. Agent receives email text
3. LLM (GPT-4o-mini) processes email with system message
4. LLM returns classification
5. We get the result back
```

**Exercise 1.6: Experiment with Prompts**

Try different system messages and see how output changes:

```python
# Prompt 1: Simple
"Classify email as URGENT, SUPPORT, FEEDBACK, or SPAM"

# Prompt 2: With examples
"""Classify emails:
Examples:
- "Server is down!" → URGENT
- "Add dark mode?" → SUPPORT
- "Buy followers" → SPAM
- "Great product!" → FEEDBACK
Now classify: ..."""

# Prompt 3: With scoring
"""Classify and score confidence 0-100:
[URGENT|SUPPORT|FEEDBACK|SPAM] confidence:XX%
Reason: ..."""

# Question: Which prompt gives best results?
# Try 10 emails and compare!
```

---

### Week 2: Day 3-4 — Function Calling (Tool Use)

**Learning Objectives:**
- [ ] Understand function calling
- [ ] Implement tools for agents
- [ ] See agents call functions

**Concept: Agent Autonomy with Tools**

```
Simple Agent (current):
  Input → LLM → Output
  (Agent can only talk, not act)

Agent with Tools:
  Input → LLM (sees available tools) 
       → Decides which tool to call
       → Call tool
       → Get result
       → LLM processes result
       → Output
  (Agent can take action!)
```

**Project: Customer Support Agent with Tools**

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIModelClient
import json

client = OpenAIModelClient(model="gpt-4o-mini")

# Define tools
tools = {
    "check_order_status": {
        "description": "Check the status of a customer order",
        "parameters": {
            "order_id": "Customer order ID"
        }
    },
    "process_refund": {
        "description": "Process a refund for an order",
        "parameters": {
            "order_id": "Order ID to refund",
            "reason": "Reason for refund"
        }
    }
}

# Mock database
orders = {
    "ORD-123": {"status": "shipped", "amount": 50},
    "ORD-456": {"status": "delivered", "amount": 75}
}

def check_order_status(order_id):
    if order_id in orders:
        return json.dumps(orders[order_id])
    return json.dumps({"error": "Order not found"})

def process_refund(order_id, reason):
    if order_id in orders:
        orders[order_id]["status"] = "refunded"
        return json.dumps({"success": True, "message": f"Refunded {order_id}"})
    return json.dumps({"error": "Order not found"})

# Test interaction
customer_question = "Hi, I want a refund for order ORD-123 because it arrived damaged"
print(f"Customer: {customer_question}")

# Agent sees tools and decides to use them
# (This is simplified; actual implementation varies by framework)
# Agent would:
# 1. See the question
# 2. Decide to check order status first
# 3. Call check_order_status("ORD-123")
# 4. See order details
# 5. Call process_refund("ORD-123", "Arrived damaged")
# 6. Inform customer "Refund processed!"
```

**Exercise 1.7: Design Your Own Tools**

```
For your use case, what tools do agents need?

Example for SignalDesk:
- search_product_docs() → RAG queries
- lookup_known_bugs() → Bug database
- check_roadmap() → Feature database
- send_notification() → Notify team
- save_ticket() → Store in database

Exercise: List 5 tools your agents would need:
1. ...
2. ...
3. ...
4. ...
5. ...

For each, define:
- What does it do?
- What are the inputs?
- What does it return?
```

---

### Week 2: Day 5 — Test & Evaluate

**Learning Objectives:**
- [ ] Measure agent performance
- [ ] Compare outputs
- [ ] Understand accuracy metrics

**Exercise 1.8: Build a Simple Test Suite**

```python
# Test your classifier from Exercise 1.6

test_cases = [
    ("Our server is down!", "URGENT"),
    ("Can you add dark mode?", "SUPPORT"),
    ("Buy followers here", "SPAM"),
    ("Love your product!", "FEEDBACK"),
    # Add 10 more...
]

correct = 0
for email, expected_category in test_cases:
    result = classifier.run_sync(email)
    actual_category = result.data.strip().upper()
    
    is_correct = actual_category == expected_category
    correct += is_correct
    
    print(f"Email: {email[:30]}...")
    print(f"Expected: {expected_category}, Got: {actual_category}, {'✅' if is_correct else '❌'}")

accuracy = correct / len(test_cases)
print(f"\nAccuracy: {accuracy*100:.1f}%")
```

**Metrics to Calculate:**
```
Accuracy:  % correct predictions
           = correct / total

Precision: % of predicted positives that are correct
           = true_positives / (true_positives + false_positives)

Recall:    % of actual positives found
           = true_positives / (true_positives + false_negatives)

F1-Score:  Harmonic mean of precision and recall
           Better when you want balance
```

---

## Phase 2: Core Concepts (Week 3-4)

### Week 3: Multi-Agent Systems

**Learning Objectives:**
- [ ] Understand orchestration patterns
- [ ] Build your first multi-agent system
- [ ] Learn state passing between agents

**Reading:**
1. [01_Agentic_AI_Fundamentals.md](01_Agentic_AI_Fundamentals.md) - Section 4 (Multi-Agent Systems)
2. [02_Projects_Overview.md](02_Projects_Overview.md) - Architecture section

**Orchestration Patterns:**

Pattern 1: Sequential (Used in SignalDesk)
```
Email Input
   ↓
Agent 1: Classifier
   (Decides: Bug or Feature or Spam)
   ↓
Agent 2: Bug Analyzer
   (Only runs if Bug)
   ↓
Agent 3: Ticket Creator
   (Takes analysis, creates ticket)
   ↓
Ticket Output
```

Pattern 2: Parallel
```
         ┌→ Agent 1 ┐
Input ──┤          ├→ Aggregator → Output
         └→ Agent 2 ┘
```

Pattern 3: Hierarchical
```
Supervisor Agent
├→ Bug Specialist
├→ Feature Specialist
└→ Spam Filter
```

**Project: Build a Multi-Agent Feedback Processor**

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIModelClient

client = OpenAIModelClient(model="gpt-4o-mini")

# Step 1: Classifier Agent
classifier_agent = AssistantAgent(
    name="classifier",
    model_client=client,
    system_message="""Classify feedback into ONE:
- Bug: Software errors
- Feature: Feature requests
- Praise: Positive feedback
- Complaint: Service issues
- Spam: Irrelevant

Output: ONLY the category"""
)

# Step 2: Bug Analyzer Agent  
bug_analyzer = AssistantAgent(
    name="bug_analyzer",
    model_client=client,
    system_message="""Analyze the bug:
1. Severity (Critical/High/Medium/Low)
2. Component affected
3. Steps to reproduce
Output in JSON format"""
)

# Step 3: Feature Analyzer Agent
feature_analyzer = AssistantAgent(
    name="feature_analyzer",
    model_client=client,
    system_message="""Analyze the feature request:
1. Impact (1-10 scale)
2. User segment (all_users/power_users/teams)
3. Complexity estimate
Output in JSON format"""
)

# Step 4: Ticket Creator Agent
ticket_creator = AssistantAgent(
    name="ticket_creator",
    model_client=client,
    system_message="""Create a support ticket:
Title: Clear, action-oriented
Description: Full details
Priority: Based on analysis
Output in structured format"""
)

# Orchestration function
def process_feedback(feedback_text):
    print(f"\n📝 Processing: {feedback_text[:50]}...")
    
    # Step 1: Classify
    classification = classifier_agent.run_sync(feedback_text)
    category = classification.data.strip()
    print(f"1️⃣  Classified as: {category}")
    
    # Step 2: Route to appropriate analyzer
    if category == "Bug":
        analysis = bug_analyzer.run_sync(feedback_text)
        print(f"2️⃣  Bug Analysis: {analysis.data[:100]}...")
    elif category == "Feature":
        analysis = feature_analyzer.run_sync(feedback_text)
        print(f"2️⃣  Feature Analysis: {analysis.data[:100]}...")
    else:
        analysis = f"No detailed analysis for {category}"
        print(f"2️⃣  {analysis}")
    
    # Step 3: Create ticket
    ticket_input = f"Feedback: {feedback_text}\nAnalysis: {analysis.data if hasattr(analysis, 'data') else analysis}"
    ticket = ticket_creator.run_sync(ticket_input)
    print(f"3️⃣  Ticket Created: {ticket.data[:100]}...")
    
    return ticket.data

# Test
feedbacks = [
    "App crashes when I try to open settings",
    "Please add dark mode support",
    "Great app, love the new features!"
]

for feedback in feedbacks:
    ticket = process_feedback(feedback)
```

**Exercise 2.1: Visualize Agent Flow**

Create a diagram of your multi-agent system:
```
Your System:
  Input
   ↓
  [Agent names here]
   ↓
  Output
```

**Exercise 2.2: Implement State Passing**

```python
# Multi-agent systems need to pass context

class FeedbackState:
    def __init__(self, text):
        self.original_text = text
        self.category = None
        self.analysis = None
        self.ticket = None

# Create and update state through pipeline
state = FeedbackState("App crashes when...")
state.category = "Bug"  # Classifier sets this
state.analysis = {"severity": "Critical"}  # Analyzer sets this
state.ticket = {"title": "App crash on settings"}  # Creator sets this

# Each agent sees the current state and adds to it
```

---

### Week 3: RAG and Knowledge Retrieval

**Learning Objectives:**
- [ ] Understand RAG (Retrieval-Augmented Generation)
- [ ] Implement RAG in your agents
- [ ] See how agents become smarter with context

**Reading:**
1. [01_Agentic_AI_Fundamentals.md](01_Agentic_AI_Fundamentals.md) - Section 5 (RAG)
2. [03_Alternative_Frameworks_And_Tools.md](03_Alternative_Frameworks_And_Tools.md) - Vector Databases

**RAG Concept:**
```
Without RAG:
  Bug Report: "Settings crashes" 
  → LLM: "Probably a memory issue"
  → Not specific, generic answer

With RAG:
  Bug Report: "Settings crashes"
  → Search knowledge base: Find similar bugs
  → Find: "BUG-101: Settings crash on Android 14"
  → LLM: "This is BUG-101, known to Android 14..."
  → Specific, actionable answer
```

**Project: Add Knowledge Base to Bug Analyzer**

```python
from chromadb import Client
from chromadb.utils import embedding_functions

# Initialize ChromaDB
client = Client()
collection = client.get_or_create_collection(
    name="product_docs",
    embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        api_key="your-api-key",
        model_name="text-embedding-3-small"
    )
)

# Add known bugs to knowledge base
known_bugs = [
    {
        "id": "BUG-101",
        "description": "Settings page crashes on Android 14 with app version 3.2.1",
        "fix": "Update to version 3.2.2"
    },
    {
        "id": "BUG-102", 
        "description": "Login fails after password reset",
        "fix": "Clear app cache and reinstall"
    },
    # Add more...
]

# Store in database
for bug in known_bugs:
    collection.add(
        ids=[bug["id"]],
        documents=[bug["description"]],
        metadatas=[{"fix": bug["fix"]}]
    )

# When analyzing a bug, query the knowledge base
def analyze_bug_with_rag(bug_report):
    # Search knowledge base
    results = collection.query(
        query_texts=[bug_report],
        n_results=3  # Get top 3 similar bugs
    )
    
    # Use results to enrich agent reasoning
    context = ""
    if results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            fix = results["metadatas"][0][i].get("fix", "")
            context += f"\nPossible match: {doc}\nFix: {fix}"
    
    # Feed to agent
    enriched_prompt = f"""Analyze this bug with context:
Bug Report: {bug_report}

Similar known issues:
{context}

Determine:
1. Is this a known bug?
2. If yes, what's the fix?
3. If no, what's the likely cause?"""
    
    return enriched_prompt

# Test
bug_report = "App crashes when opening settings on Android device"
enriched = analyze_bug_with_rag(bug_report)
print(enriched)
```

**Exercise 2.3: Build a Knowledge Base**

```
For your domain, create a knowledge base:

1. Identify knowledge areas
   - Common bugs
   - Product features
   - Processes
   - FAQs

2. Create documents
   [Bug-001]
   Title: "Login issues after reset"
   Solution: "Clear cache, reinstall app"
   
   [Feature-001]
   Name: "Dark mode"
   Status: "Planned for v4.0"
   ETA: "Q3 2024"

3. Add to vector database
4. Query it with real questions
5. Check relevance
```

**Exercise 2.4: Evaluate RAG Quality**

```python
# Test if RAG improves accuracy

# Test Case 1: Without RAG
bug = "App crashes when opening settings"
answer_without_rag = bug_analyzer.run_sync(bug)
print(f"Without RAG: {answer_without_rag}")

# Test Case 2: With RAG
enriched = analyze_bug_with_rag(bug)
answer_with_rag = bug_analyzer.run_sync(enriched)
print(f"With RAG: {answer_with_rag}")

# Question: Is the answer more specific with RAG?
# Did it match known issues better?
# Is the suggested fix more actionable?
```

---

### Week 4: State Management and Persistence

**Learning Objectives:**
- [ ] Understand agent state
- [ ] Implement state persistence
- [ ] Query historical states

**Reading:**
1. [01_Agentic_AI_Fundamentals.md](01_Agentic_AI_Fundamentals.md) - Section 5 (State Management)

**State Types:**

```
Agent State:
├─ Input State: What was given
├─ Working Memory: Info during processing
├─ Decision State: What was decided
├─ Output State: What was produced

Persistence:
├─ In-Memory: Fast, but lost on restart
├─ Files: CSV/JSON, portable, limited querying
├─ Database: Queryable, reliable, scalable
```

**Project: Persistent Ticket Storage**

```python
import sqlite3
from datetime import datetime

# Create database
db = sqlite3.connect("tickets.db")
cursor = db.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    source_id TEXT,
    category TEXT,
    priority TEXT,
    title TEXT,
    description TEXT,
    quality_score REAL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
""")

# Save ticket
def save_ticket(ticket_data):
    cursor.execute("""
    INSERT INTO tickets 
    (source_id, category, priority, title, description, quality_score, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_data["source_id"],
        ticket_data["category"],
        ticket_data["priority"],
        ticket_data["title"],
        ticket_data["description"],
        ticket_data["quality_score"],
        datetime.now(),
        datetime.now()
    ))
    db.commit()
    return cursor.lastrowid

# Query tickets
def get_tickets_by_priority(priority):
    cursor.execute(
        "SELECT * FROM tickets WHERE priority = ? ORDER BY created_at DESC",
        (priority,)
    )
    return cursor.fetchall()

def get_statistics():
    cursor.execute("""
    SELECT 
        category, 
        COUNT(*) as count,
        AVG(quality_score) as avg_quality
    FROM tickets
    GROUP BY category
    """)
    return cursor.fetchall()

# Test
sample_ticket = {
    "source_id": "R001",
    "category": "Bug",
    "priority": "High",
    "title": "Settings crash on Android 14",
    "description": "App crashes when opening settings...",
    "quality_score": 0.95
}

ticket_id = save_ticket(sample_ticket)
print(f"Saved ticket: {ticket_id}")

high_priority = get_tickets_by_priority("High")
print(f"High priority tickets: {len(high_priority)}")

stats = get_statistics()
print(f"Statistics: {stats}")
```

**Exercise 2.5: Design Your Data Schema**

```
What data does your system need to store?

Common fields:
├─ ID (unique identifier)
├─ Source (where did it come from?)
├─ Type (what category/type?)
├─ Status (what state is it in?)
├─ Timestamp (when did it happen?)
├─ Metadata (additional context)
└─ User (who's involved?)

For your system, define:
1. What entities exist?
2. What fields each entity?
3. What relationships?
4. What queries do you need?
```

---

## Phase 3: Hands-On Building (Week 5-8)

### Week 5: Build SignalDesk Yourself

**Learning Objectives:**
- [ ] Understand the complete system
- [ ] Build a simplified version
- [ ] Learn deployment

**Project Overview:**

SignalDesk processes feedback through 6 agents:
```
1. CSV Reader → Load feedback
2. Classifier → Determine category
3. Bug Analyzer → Extract bug details
4. Feature Extractor → Analyze feature impact
5. Ticket Creator → Generate ticket + detect duplicates
6. Quality Critic → Score and revise tickets
```

**Exercise 3.1: Simplified SignalDesk (Mini Version)**

```python
"""
Mini-SignalDesk: 3-agent version (simplified from 6-agent)
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIModelClient
import csv

client = OpenAIModelClient(model="gpt-4o-mini")

# Agent 1: Classifier
classifier = AssistantAgent(
    name="classifier",
    model_client=client,
    system_message="Classify feedback as: Bug, Feature, Praise, Complaint, Spam. Output ONE WORD only."
)

# Agent 2: Analyzer (for bugs and features)
analyzer = AssistantAgent(
    name="analyzer",
    model_client=client,
    system_message="Extract key details and impact. Format as JSON."
)

# Agent 3: Ticket Creator
ticket_creator = AssistantAgent(
    name="ticket_creator",
    model_client=client,
    system_message="Create a support ticket with title, description, priority. Format as JSON."
)

# Pipeline
def process_feedback_item(feedback):
    # Step 1: Classify
    classification = classifier.run_sync(feedback["text"])
    category = classification.data.strip()
    
    # Step 2: Analyze
    analysis = analyzer.run_sync(f"{category}: {feedback['text']}")
    
    # Step 3: Create ticket (only for actionable categories)
    if category in ["Bug", "Feature"]:
        ticket_data = f"Category: {category}\nFeedback: {feedback['text']}\nAnalysis: {analysis.data}"
        ticket = ticket_creator.run_sync(ticket_data)
    else:
        ticket = f"No ticket needed for {category}"
    
    return {
        "source_id": feedback["id"],
        "category": category,
        "analysis": analysis.data[:100],
        "ticket": str(ticket.data)[:100]
    }

# Load CSV
feedbacks = []
with open("feedback.csv") as f:
    reader = csv.DictReader(f)
    feedbacks = list(reader)

# Process all
results = []
for feedback in feedbacks[:5]:  # Process first 5 for testing
    print(f"\nProcessing: {feedback['text'][:50]}...")
    result = process_feedback_item(feedback)
    results.append(result)
    print(f"  Category: {result['category']}")

# Save results
with open("output_tickets.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["source_id", "category", "analysis", "ticket"])
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Processed {len(results)} items")
print(f"💾 Saved to output_tickets.csv")
```

**Exercise 3.2: Add Logging**

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("SignalDesk")

# Add to pipeline
def process_feedback_item_with_logging(feedback):
    logger.info(f"Starting processing of {feedback['id']}")
    
    # Step 1
    classification = classifier.run_sync(feedback["text"])
    category = classification.data.strip()
    logger.info(f"Classified {feedback['id']} as {category}")
    
    # Step 2
    analysis = analyzer.run_sync(f"{category}: {feedback['text']}")
    logger.info(f"Analyzed {feedback['id']}")
    
    # Step 3
    if category in ["Bug", "Feature"]:
        ticket_data = f"Category: {category}\nFeedback: {feedback['text']}\nAnalysis: {analysis.data}"
        ticket = ticket_creator.run_sync(ticket_data)
        logger.info(f"Created ticket for {feedback['id']}")
    else:
        ticket = f"No ticket needed"
        logger.info(f"Skipped ticket creation for {feedback['id']} ({category})")
    
    logger.info(f"Completed processing of {feedback['id']}")
    
    return {
        "source_id": feedback["id"],
        "category": category,
        "ticket": str(ticket.data)[:100]
    }
```

**Exercise 3.3: Add Error Handling**

```python
def process_feedback_item_robust(feedback):
    try:
        logger.info(f"Processing {feedback['id']}")
        
        # Try to classify
        try:
            classification = classifier.run_sync(feedback["text"])
            category = classification.data.strip()
        except Exception as e:
            logger.error(f"Classification failed for {feedback['id']}: {e}")
            category = "Unknown"
        
        # Try to analyze
        try:
            analysis = analyzer.run_sync(f"{category}: {feedback['text']}")
        except Exception as e:
            logger.error(f"Analysis failed for {feedback['id']}: {e}")
            analysis = {"data": "Analysis failed"}
        
        # Create ticket if applicable
        try:
            if category in ["Bug", "Feature"]:
                ticket = ticket_creator.run_sync(f"...")
            else:
                ticket = None
        except Exception as e:
            logger.error(f"Ticket creation failed for {feedback['id']}: {e}")
            ticket = None
        
        return {
            "source_id": feedback["id"],
            "category": category,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Fatal error processing {feedback['id']}: {e}")
        return {
            "source_id": feedback["id"],
            "category": "Error",
            "status": "failed",
            "error": str(e)
        }
```

---

### Week 6-7: Advanced Observability

**Learning Objectives:**
- [ ] Implement structured logging
- [ ] Create dashboards
- [ ] Monitor system health

**Exercise 3.4: Structured Logging to CSV**

```python
import csv
from datetime import datetime

def log_decision(agent_name, source_id, action, details, confidence=0.0):
    """Log agent decisions to CSV for analysis"""
    with open("processing_log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            agent_name,
            source_id,
            action,
            details,
            confidence
        ])

# Use in pipeline
def process_with_decision_logging(feedback):
    source_id = feedback["id"]
    
    # Classify and log
    classification = classifier.run_sync(feedback["text"])
    category = classification.data.strip()
    log_decision("Classifier", source_id, "CLASSIFY", f"Category: {category}", confidence=0.95)
    
    # Analyze and log
    analysis = analyzer.run_sync(f"{category}: {feedback['text']}")
    log_decision("Analyzer", source_id, "ANALYZE", f"Extracted details", confidence=0.90)
    
    # Create ticket and log
    if category in ["Bug", "Feature"]:
        ticket = ticket_creator.run_sync(f"...")
        log_decision("TicketCreator", source_id, "CREATE", f"Created ticket", confidence=0.92)
    
    return {"source_id": source_id, "category": category}

# Now you can query logs
def get_agent_stats():
    with open("processing_log.csv") as f:
        reader = csv.DictReader(f)
        logs = list(reader)
    
    # Analyze
    total = len(logs)
    by_agent = {}
    for log in logs:
        agent = log["agent_name"]
        by_agent[agent] = by_agent.get(agent, 0) + 1
    
    print(f"Total decisions logged: {total}")
    print(f"By agent: {by_agent}")
```

**Exercise 3.5: Build Observability Dashboard**

```python
# Using Streamlit (from Week 5 of Phase 2)
import streamlit as st
import pandas as pd

st.title("SignalDesk Observability Dashboard")

# Load logs
@st.cache_data
def load_logs():
    return pd.read_csv("processing_log.csv")

logs = load_logs()

# Show stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Processed", len(logs))
col2.metric("Avg Confidence", f"{logs['confidence'].mean():.2%}")
col3.metric("Unique Agents", logs['agent_name'].nunique())

# Show logs
st.subheader("Recent Decisions")
st.dataframe(logs.tail(20))

# Show charts
st.subheader("Agent Activity")
agent_counts = logs['agent_name'].value_counts()
st.bar_chart(agent_counts)

# Filter by action
st.subheader("Filter by Action")
action = st.selectbox("Select action:", logs['action'].unique())
filtered = logs[logs['action'] == action]
st.write(f"Found {len(filtered)} records")
st.dataframe(filtered)
```

---

### Week 8: Deployment and Testing

**Learning Objectives:**
- [ ] Test your system
- [ ] Deploy to production
- [ ] Monitor in production

**Exercise 3.6: Create Test Suite**

```python
import unittest

class TestSignalDesk(unittest.TestCase):
    
    def test_classification_accuracy(self):
        """Test classifier accuracy against ground truth"""
        test_cases = [
            ("App crashes", "Bug"),
            ("Add dark mode", "Feature"),
            ("Buy followers", "Spam"),
        ]
        
        for text, expected in test_cases:
            result = classifier.run_sync(text)
            self.assertEqual(result.data.strip(), expected)
    
    def test_pipeline_completes(self):
        """Test that pipeline runs without errors"""
        feedback = {"id": "TEST-1", "text": "App crashes when..."}
        result = process_feedback_item(feedback)
        self.assertIsNotNone(result["category"])
        self.assertIsNotNone(result["ticket"])
    
    def test_output_format(self):
        """Test that outputs are in correct format"""
        feedback = {"id": "TEST-1", "text": "Test"}
        result = process_feedback_item(feedback)
        
        required_fields = ["source_id", "category", "ticket"]
        for field in required_fields:
            self.assertIn(field, result)

if __name__ == "__main__":
    unittest.main()
```

**Exercise 3.7: Docker Deployment**

```dockerfile
# Dockerfile
FROM python:3.14

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Run app
CMD ["streamlit", "run", "ui/app.py"]
```

```bash
# Build image
docker build -t signaldesk:latest .

# Run locally
docker run -p 8501:8501 signaldesk:latest

# Push to registry
docker tag signaldesk:latest myregistry/signaldesk:latest
docker push myregistry/signaldesk:latest
```

---

## Phase 4: Production Systems (Week 9-12)

### Week 9: Error Handling and Resilience

**Learning Objectives:**
- [ ] Implement comprehensive error handling
- [ ] Build fallback mechanisms
- [ ] Ensure uptime

**Reading:**
1. [01_Agentic_AI_Fundamentals.md](01_Agentic_AI_Fundamentals.md) - Section 7 (Fallback and Resilience)

**Exercise 4.1: Heuristics Fallback**

```python
def classify_with_fallback(text):
    """
    Primary: Use LLM
    Fallback: Use heuristics if API fails
    """
    try:
        # Try LLM path
        result = classifier.run_sync(text)
        return result.data.strip(), "LLM"
    except Exception as e:
        print(f"LLM failed: {e}, using heuristics")
        
        # Fallback to heuristics
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["crash", "bug", "error", "fail"]):
            return "Bug", "Heuristic"
        elif any(word in text_lower for word in ["add", "feature", "please", "would like"]):
            return "Feature", "Heuristic"
        elif any(word in text_lower for word in ["love", "great", "awesome", "excellent"]):
            return "Praise", "Heuristic"
        elif any(word in text_lower for word in ["poor", "terrible", "bad", "waste"]):
            return "Complaint", "Heuristic"
        else:
            return "Unknown", "Heuristic"

# Test
feedbacks = [
    "App crashes on startup",
    "Can you add dark mode?",
    "Love the new design!",
]

for text in feedbacks:
    category, method = classify_with_fallback(text)
    print(f"{text[:30]}... → {category} ({method})")
```

**Exercise 4.2: Retry Logic**

```python
import time

def call_with_retry(func, max_retries=3, backoff_factor=2):
    """Call function with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Give up
            
            wait_time = backoff_factor ** attempt
            print(f"Attempt {attempt+1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)

# Use it
def call_classifier():
    return classifier.run_sync("Some feedback text")

try:
    result = call_with_retry(call_classifier)
    print(f"Success: {result}")
except Exception as e:
    print(f"Failed after retries: {e}")
```

---

### Week 10: Performance Optimization

**Learning Objectives:**
- [ ] Profile system performance
- [ ] Identify bottlenecks
- [ ] Optimize for speed and cost

**Exercise 4.2: Performance Profiling**

```python
import time
import cProfile
import pstats

def profile_pipeline():
    """Profile the entire pipeline"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run pipeline
    for feedback in feedbacks[:10]:
        process_feedback_item(feedback)
    
    profiler.disable()
    
    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(10)  # Top 10 functions

profile_pipeline()
```

**Exercise 4.3: Caching for Cost Optimization**

```python
from functools import lru_cache

# Cache LLM responses
@lru_cache(maxsize=1000)
def classify_cached(text):
    """Cache classification results"""
    return classifier.run_sync(text)

# Usage: Second call with same text returns cached result instantly
result1 = classify_cached("App crashes")  # API call
result2 = classify_cached("App crashes")  # Cached, instant

# For larger systems: Use Redis
# import redis
# redis_client = redis.Redis()
# 
# def classify_with_redis(text):
#     cached = redis_client.get(f"classify:{text}")
#     if cached:
#         return cached.decode()
#     result = classifier.run_sync(text)
#     redis_client.setex(f"classify:{text}", 86400, result)  # 1 day
#     return result
```

**Exercise 4.4: Batch Processing**

```python
def process_batch(feedbacks, batch_size=50):
    """Process in batches to optimize API calls"""
    results = []
    
    for i in range(0, len(feedbacks), batch_size):
        batch = feedbacks[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} ({len(batch)} items)...")
        
        batch_results = []
        for feedback in batch:
            result = process_feedback_item(feedback)
            batch_results.append(result)
        
        results.extend(batch_results)
        
        # Time between batches to avoid rate limits
        if i + batch_size < len(feedbacks):
            time.sleep(5)
    
    return results

# Much faster than processing one-by-one
all_results = process_batch(feedbacks, batch_size=50)
```

---

### Week 11: Monitoring and Alerting

**Learning Objectives:**
- [ ] Monitor system metrics
- [ ] Set up alerts
- [ ] Create incident response procedures

**Exercise 4.5: Health Checks**

```python
def health_check():
    """Verify system is operational"""
    checks = {}
    
    # Check 1: Can we connect to LLM API?
    try:
        result = classifier.run_sync("test")
        checks["llm_api"] = "OK"
    except Exception as e:
        checks["llm_api"] = f"FAIL: {e}"
    
    # Check 2: Can we access database?
    try:
        db = sqlite3.connect("tickets.db")
        db.execute("SELECT 1")
        db.close()
        checks["database"] = "OK"
    except Exception as e:
        checks["database"] = f"FAIL: {e}"
    
    # Check 3: Can we access knowledge base?
    try:
        # Try a query
        results = collection.query(query_texts=["test"], n_results=1)
        checks["vectordb"] = "OK"
    except Exception as e:
        checks["vectordb"] = f"FAIL: {e}"
    
    # Overall status
    all_ok = all("OK" in v for v in checks.values())
    status = "HEALTHY" if all_ok else "DEGRADED"
    
    return {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "checks": checks
    }

# Expose as endpoint
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def get_health():
    return jsonify(health_check())

if __name__ == "__main__":
    app.run(debug=False)
```

**Exercise 4.6: Alerting**

```python
import smtplib

def send_alert(subject, message):
    """Send alert email"""
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    msg = MIMEMultipart()
    msg["From"] = "alerts@signaldesk.com"
    msg["To"] = "team@company.com"
    msg["Subject"] = subject
    
    msg.attach(MIMEText(message, "plain"))
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("alerts@signaldesk.com", "password")
    server.send_message(msg)
    server.quit()

def monitor_system():
    """Continuous monitoring"""
    health = health_check()
    
    if health["status"] == "DEGRADED":
        send_alert(
            "SignalDesk Health Alert",
            f"System degraded: {health['checks']}"
        )
    
    # Check accuracy
    recent_accuracy = get_recent_accuracy()
    if recent_accuracy < 0.80:
        send_alert(
            "SignalDesk Accuracy Alert",
            f"Accuracy dropped to {recent_accuracy*100:.1f}%"
        )

# Run monitoring in background
import threading

def start_monitoring():
    """Start background monitoring thread"""
    while True:
        monitor_system()
        time.sleep(300)  # Check every 5 minutes

thread = threading.Thread(target=start_monitoring, daemon=True)
thread.start()
```

---

### Week 12: Scaling and Production Readiness

**Learning Objectives:**
- [ ] Scale to production load
- [ ] Multi-region deployment
- [ ] Disaster recovery

**Production Checklist:**

```
Infrastructure:
- [ ] Use PostgreSQL (not SQLite)
- [ ] Use Pinecone (not ChromaDB)
- [ ] Use managed Kubernetes
- [ ] Enable auto-scaling
- [ ] Set up load balancing

Security:
- [ ] API keys in secrets manager
- [ ] HTTPS everywhere
- [ ] Authentication for API
- [ ] Encryption in transit and at rest
- [ ] VPC/Network isolation

Operations:
- [ ] Centralized logging (ELK, Splunk)
- [ ] APM (Datadog, New Relic)
- [ ] Incident response procedures
- [ ] On-call rotation
- [ ] Runbooks for common issues

Data:
- [ ] Daily backups
- [ ] Backup validation (restore test)
- [ ] Data retention policies
- [ ] Audit logging
- [ ] Compliance (GDPR, etc.)

Testing:
- [ ] Unit tests > 80% coverage
- [ ] Integration tests
- [ ] Load testing
- [ ] Chaos engineering
- [ ] Disaster recovery drills
```

---

## Summary: Complete Learning Path

### By Week Completion:

**Week 2:** You understand agents, can build simple classifiers, and know the frameworks

**Week 4:** You understand multi-agent systems, RAG, state management, and orchestration

**Week 8:** You've built a working system (simplified SignalDesk) with logging, testing, and deployment

**Week 12:** You know how to take a system to production with scaling, monitoring, and reliability

### Next Steps After Course:

1. **Build your own project** using the patterns learned
2. **Join communities** (LangChain, AutoGen Discord servers)
3. **Read papers** on agent systems, RAG, LLMs
4. **Contribute to open source** (AutoGen, ChromaDB, LangChain)
5. **Stay updated** on new frameworks and techniques

### Recommended Reading:

- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- "AutoGen: Enabling Next-Gen LLM Applications"
- OpenAI, Anthropic, and Mistral documentation

### Key Takeaways:

1. **Start simple** - Heuristics before LLMs
2. **Measure everything** - You can't optimize what you don't measure
3. **Fallback is essential** - Never depend on single point of failure
4. **Observability is investment** - Pay upfront to understand later
5. **Ship early** - Perfect is enemy of good
6. **Learn from production** - Real data teaches fastest

---

## Appendix: Quick Reference

### Setting Up Your First Project

```bash
# 1. Create project
mkdir my-agentic-project
cd my-agentic-project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install core packages
pip install autogen-agentchat autogen-ext[openai] chromadb pydantic streamlit

# 4. Set API key
echo "OPENAI_API_KEY=sk-..." > .env

# 5. First script
cat > agent.py << 'EOF'
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIModelClient

client = OpenAIModelClient(model="gpt-4o-mini")
agent = AssistantAgent(name="helper", model_client=client)
result = agent.run_sync("What is 2+2?")
print(result.data)
EOF

# 6. Run
python agent.py
```

### Common Commands Reference

```bash
# Training
python -m pip install --upgrade autogen-agentchat

# Testing
python -m pytest tests/

# Formatting
python -m black .

# Type checking
python -m mypy agents/

# Profiling
python -m cProfile -s cumulative script.py | head -20

# Docker
docker build -t app:latest .
docker run -p 8501:8501 app:latest
```

---

**Good luck on your Agentic AI journey!** 🚀
