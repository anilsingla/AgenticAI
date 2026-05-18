# Quick Reference Guide: Agentic AI

Your go-to cheat sheet for concepts, code patterns, and best practices.

---

## 🎯 Core Concepts at a Glance

### What is an Agent?
```
Chatbot: Question → LLM → Answer
Agent:   Goal → Loop(Observe → Reason → Act → Update) → Success
```

### The Agent Loop
```python
while not goal_achieved:
    state = observe_environment()     # What's happening now?
    action = reason(state)             # What should I do?
    result = execute_action(action)    # Do it
    goal_achieved = evaluate(result)   # Did it work?
    state = update_state(result)       # Remember
```

### Key Difference: Autonomy
```
Chatbot: Responds to user queries
Agent: Works toward goals independently

Example:
  Chatbot: "How do I book a flight?"
           "Go to airline website..."
  
  Agent: Goal: "Get me the cheapest flight tomorrow"
         1. Search multiple airlines
         2. Compare prices
         3. Check my preferences
         4. Present options
         5. Help user book
```

---

## 🛠️ Framework Quick Comparison

| Framework | Best For | Setup | Curve | Code Size |
|-----------|----------|-------|-------|-----------|
| **AutoGen** | Multi-agent | 5 min | Low | 50 lines |
| **LangChain** | Complex workflows | 15 min | High | 100 lines |
| **Pydantic AI** | Type-safe outputs | 5 min | Low | 30 lines |
| **Claude SDK** | Claude models | 2 min | Low | 20 lines |

### Choose:
- **Learning?** → AutoGen or Pydantic AI
- **Production?** → LangChain or AutoGen
- **Speed matters?** → Claude SDK or Pydantic AI
- **Complex workflows?** → LangChain

---

## 📝 Common Code Patterns

### Pattern 1: Simple Agent
```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIModelClient

client = OpenAIModelClient(model="gpt-4o-mini")
agent = AssistantAgent(name="helper", model_client=client)
result = agent.run_sync("Do something...")
print(result.data)
```

### Pattern 2: Multi-Agent Pipeline
```python
# Create agents
agent1 = AssistantAgent(name="classifier", model_client=client, ...)
agent2 = AssistantAgent(name="analyzer", model_client=client, ...)

# Execute in sequence
result1 = agent1.run_sync(input_text)
result2 = agent2.run_sync(result1.data)
final = result2.data
```

### Pattern 3: RAG Context
```python
from chromadb import Client
collection = client.get_or_create_collection("docs")
collection.add(ids=["doc1"], documents=["Your knowledge..."])

# Query for context
results = collection.query(query_texts=[user_query], n_results=3)
context = "\n".join(results["documents"][0])

# Enrich agent with context
prompt = f"Context: {context}\nQuestion: {user_query}"
result = agent.run_sync(prompt)
```

### Pattern 4: Error Handling with Fallback
```python
def process_with_fallback(data):
    try:
        # Primary: Use LLM
        return use_llm(data)
    except Exception as e:
        print(f"LLM failed: {e}, using fallback")
        # Fallback: Use heuristics
        return use_heuristics(data)
```

### Pattern 5: Retry with Backoff
```python
import time

def retry_with_backoff(func, max_retries=3, backoff=2):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = backoff ** attempt
            time.sleep(wait)
```

### Pattern 6: Structured Logging
```python
import csv
from datetime import datetime

def log_decision(agent, source_id, action, confidence):
    with open("log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            agent, source_id, action, confidence
        ])
```

### Pattern 7: State Management
```python
class AgentState:
    def __init__(self, input_data):
        self.original = input_data
        self.classification = None
        self.analysis = None
        self.output = None

state = AgentState(data)
state.classification = classify(state.original)
state.analysis = analyze(state.classification)
state.output = generate(state.analysis)
```

### Pattern 8: Batch Processing
```python
def process_batch(items, batch_size=50):
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        for item in batch:
            results.append(process_item(item))
        time.sleep(5)  # Rate limit
    return results
```

---

## 📊 Performance Metrics

### Key Metrics
```
Accuracy:    % correct predictions
            = true_positives / total

Precision:   % positive predictions correct
            = true_positives / (true_positives + false_positives)

Recall:      % actual positives found
            = true_positives / (true_positives + false_negatives)

Latency:     Time per request (seconds)

Cost:        $ per request or per month

Throughput:  Items processed per minute
```

### Calculate Accuracy
```python
def calculate_accuracy(predictions, ground_truth):
    correct = sum(p == g for p, g in zip(predictions, ground_truth))
    return correct / len(predictions)

accuracy = calculate_accuracy(predicted, expected)
print(f"Accuracy: {accuracy*100:.1f}%")
```

### SignalDesk Benchmark
```
Processing:  50 items in 90 seconds = 33 items/min
Cost:        ~$0.0002/run (GPT-4o-mini)
Accuracy:    87% on ground truth
Quality:     94.4% average ticket quality
Confidence:  90.48% average model confidence
```

---

## 🚀 Deployment Quick Start

### Docker (Local)
```dockerfile
FROM python:3.14
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
docker build -t myapp:latest .
docker run -p 8000:8000 myapp:latest
```

### Docker Compose (Multi-container)
```yaml
version: '3.8'
services:
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=app_db
```

### Streamlit
```python
import streamlit as st

st.title("My Agentic App")
st.write("Hello world!")

if st.button("Process"):
    result = my_agent.run_sync(input_text)
    st.write(result)
```

### Environment Variables
```bash
# Create .env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
LOG_LEVEL=INFO

# Load in Python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

---

## 💰 Cost Optimization

### LLM API Costs (per 1M tokens)
```
GPT-4o-mini:       $0.05 input, $0.15 output
GPT-4 Turbo:       $0.01 input, $0.03 output (cheaper!)
Claude 3.5 Sonnet: $3.00 input, $15.00 output
Llama 2 (self):    ~$0.00 (compute cost)
```

### Cost Calculator
```python
def estimate_cost(items, tokens_per_item=50, cost_per_m=0.05):
    total_tokens = items * tokens_per_item
    cost = (total_tokens / 1_000_000) * cost_per_m
    return cost

# 1000 items, 50 tokens each, GPT-4o-mini input
cost = estimate_cost(1000, 50, 0.05)
print(f"Estimated cost: ${cost:.4f}")  # $0.0025
```

### Cost Reduction Strategies
```
1. Cache responses (Redis, LRU)
2. Use cheaper model (gpt-4o-mini vs gpt-4)
3. Fallback to heuristics
4. Batch process (fewer API calls)
5. Use local model (Llama) for some tasks
```

---

## 🔍 Observability Checklist

### What to Log
- [ ] Input and output for every agent
- [ ] Decision reasoning
- [ ] Confidence scores
- [ ] Errors and exceptions
- [ ] Performance (latency)
- [ ] API costs

### Logging Template
```python
def log_agent_action(agent_name, input_data, output_data, confidence, duration):
    log_record = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "input": input_data[:100],  # First 100 chars
        "output": output_data[:100],
        "confidence": confidence,
        "duration_ms": duration * 1000
    }
    logger.info(json.dumps(log_record))
```

### Query Logs
```python
import pandas as pd

# Load structured logs
logs = pd.read_csv("agent_log.csv")

# Analyze
print(logs.groupby("agent")["confidence"].mean())
print(logs["duration_ms"].describe())
print(logs[logs["confidence"] < 0.5])  # Low confidence
```

---

## 🛡️ Error Handling Patterns

### Try-Catch Template
```python
try:
    result = agent.run_sync(input_text)
    return result.data
except TimeoutError:
    logger.warning("Request timed out, using fallback")
    return fallback_result()
except RateLimitError:
    logger.warning("Rate limited, waiting 60s")
    time.sleep(60)
    return agent.run_sync(input_text)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return None
```

### Health Check
```python
def health_check():
    checks = {}
    
    # Check LLM API
    try:
        agent.run_sync("test")
        checks["llm"] = "OK"
    except:
        checks["llm"] = "DOWN"
    
    # Check database
    try:
        db.query("SELECT 1")
        checks["db"] = "OK"
    except:
        checks["db"] = "DOWN"
    
    return all(v == "OK" for v in checks.values())
```

---

## 📈 Scaling Checklist

### Development to Production
```
Development:
  ├─ SQLite (OK for now)
  ├─ ChromaDB (OK for now)
  ├─ Single process
  └─ Manual deployment

Production:
  ├─ PostgreSQL (scalable)
  ├─ Pinecone or Milvus (managed)
  ├─ Multiple workers
  ├─ Load balancer
  ├─ Auto-scaling
  ├─ Monitoring
  └─ Automated deployment
```

### Horizontal Scaling
```
Before: 1 server, 1 worker
  50 requests/sec → Overload

After: Load balancer
  ├─ Server 1 (10 workers)
  ├─ Server 2 (10 workers)
  └─ Server 3 (10 workers)
  500 requests/sec → Smooth
```

---

## 🧪 Testing Quick Reference

### Unit Test Template
```python
import unittest

class TestAgent(unittest.TestCase):
    def test_classification(self):
        result = agent.run_sync("App crashes")
        self.assertEqual(result.data, "Bug")
    
    def test_error_handling(self):
        with self.assertRaises(ValueError):
            agent.run_sync(None)

if __name__ == "__main__":
    unittest.main()
```

### Load Testing
```python
import concurrent.futures
import time

def load_test(agent, items, num_workers=10):
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(num_workers) as executor:
        futures = [executor.submit(agent.run_sync, item) for item in items]
        results = [f.result() for f in futures]
    
    elapsed = time.time() - start
    throughput = len(items) / elapsed
    
    print(f"Processed {len(items)} items in {elapsed:.1f}s")
    print(f"Throughput: {throughput:.0f} items/sec")
```

---

## 🎓 Common Mistakes & Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| No error handling | System crashes on edge case | Add try/catch everywhere |
| No logging | Can't debug when things fail | Log everything (decisions, errors) |
| No ground truth | Can't measure accuracy | Create test dataset |
| Expensive model | High API costs | Use gpt-4o-mini instead of gpt-4 |
| Hardcoded API keys | Security risk | Use environment variables |
| No fallback | System fails if API down | Always have heuristics fallback |
| Single agent | Low accuracy | Break into multi-agent pipeline |
| No caching | Redundant API calls | Cache or memoize |

---

## 📚 Decision Trees

### Choose LLM Model
```
Is cost critical?
  Yes → GPT-4o-mini
  No → Need best quality?
       Yes → Claude 3.5 Sonnet
       No → GPT-4o-mini (usually enough)

Is privacy critical?
  Yes → Self-hosted (Llama)
  No → Use cloud (OpenAI/Anthropic)
```

### Choose Framework
```
Need multi-agent orchestration?
  Yes → AutoGen
  No → Simple task?
       Yes → Pydantic AI or Claude SDK
       No → Complex workflow?
            Yes → LangChain
            No → Pydantic AI
```

### Choose Vector Database
```
Data volume?
  < 100K items → ChromaDB
  100K-10M → Pinecone
  > 10M → Milvus

Self-hosted preference?
  Yes → Milvus
  No → Need managed?
       Yes → Pinecone
       No → ChromaDB
```

---

## 🔗 Common Integration Patterns

### Pattern: Email to Ticket
```python
# 1. Read email
email_text = read_email()

# 2. Classify
category = classifier.run_sync(email_text)

# 3. Extract details (if bug)
if category == "Bug":
    details = bug_analyzer.run_sync(email_text)
else:
    details = {}

# 4. Create ticket
ticket = ticket_creator.run_sync(
    f"{email_text}\n{details}"
)

# 5. Save
save_to_database(ticket)

# 6. Send confirmation
send_email(ticket["customer_email"], ticket)
```

### Pattern: RAG Q&A
```python
question = "What's the fix for issue X?"

# 1. Search knowledge base
relevant_docs = kb.search(question, top_k=3)

# 2. Enrich context
context = "\n".join(relevant_docs)

# 3. Generate answer
answer = agent.run_sync(
    f"Context: {context}\nQuestion: {question}"
)

# 4. Return
return answer.data
```

---

## 📞 Support & Debugging

### Debug Checklist
```
Problem: Agent returns wrong output
  1. Check system message (is role clear?)
  2. Check input (is it reasonable?)
  3. Add logging (what's happening?)
  4. Test with simpler input
  5. Try different LLM model
  6. Check temperature (should be 0 for classification)

Problem: API timeout
  1. Check network
  2. Check API key
  3. Try with simpler input
  4. Use exponential backoff retry

Problem: High costs
  1. Check token count
  2. Use cheaper model
  3. Implement caching
  4. Use batch processing
```

### Common Error Messages

```
"API key invalid"
  → Check OPENAI_API_KEY environment variable
  
"Rate limit exceeded"
  → Implement exponential backoff
  → Batch process
  → Upgrade plan
  
"Connection refused"
  → Check database connection
  → Check ChromaDB server

"Out of memory"
  → Process in batches
  → Use generator instead of list
  → Increase RAM or use Kubernetes
```

---

## 🎯 Production Readiness Checklist

```
Code Quality:
  [ ] Linting passes (black, flake8)
  [ ] Type hints everywhere
  [ ] Tests passing (> 80% coverage)
  [ ] Error handling comprehensive
  [ ] Logging everywhere

Operations:
  [ ] Environment variables configured
  [ ] Database backups automated
  [ ] Monitoring active
  [ ] Alerting configured
  [ ] Incident playbook written

Deployment:
  [ ] Docker image working
  [ ] Health check endpoint
  [ ] Graceful shutdown
  [ ] Zero-downtime deployment
  [ ] Rollback procedure

Documentation:
  [ ] API documented
  [ ] Architecture documented
  [ ] Deployment guide written
  [ ] Troubleshooting guide written
  [ ] Team trained
```

---

## 💡 Pro Tips

1. **Start with heuristics** - Implement rule-based logic first, add LLM later
2. **Log everything** - Future you will thank current you
3. **Use ground truth** - Create test dataset early
4. **Think in batches** - Process data efficiently
5. **Cache aggressively** - Don't repeat API calls
6. **Test at scale** - Use realistic data volume
7. **Monitor costs** - Track every API call
8. **Build fallbacks** - Never depend on single path
9. **Iterate fast** - Ship small improvements continuously
10. **Learn from production** - Real data teaches best

---

## 🚀 Next Steps

1. **Pick a framework** - Use decision tree above
2. **Build hello world** - Follow simple agent pattern
3. **Add logging** - Use logging template
4. **Add error handling** - Use try-catch template
5. **Add fallback** - Implement heuristics
6. **Test and measure** - Check accuracy
7. **Scale gradually** - Monitor and optimize
8. **Deploy to production** - Follow checklist

---

**Keep this guide handy for quick reference!** 📌

Last updated: May 18, 2026
