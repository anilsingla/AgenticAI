# 05_Observability_Monitoring

Monitor, trace, and observe agent behavior in production systems.

---

## 📚 Overview

Observability tools help understand what agents are doing:
- **Langfuse** - Comprehensive agent tracing
- **Langsmith** - LangChain monitoring

**Level:** Advanced  
**Prerequisites:** 01_Framework_Basics through 04_Specialized_Agents

---

## 🎯 What You'll Learn

- ✅ Agent tracing and logging
- ✅ Performance monitoring
- ✅ Cost tracking
- ✅ Debugging agents
- ✅ Production insights
- ✅ User behavior analysis

---

## 📂 Projects in This Category

### 1. Langfuse_Monitoring
**What:** Comprehensive agent observability platform  
**Why:** Best-in-class tracing for LLM applications  
**Level:** Advanced  
**Time:** 1-2 hours

**Features:**
- Agent trace logging
- LLM call tracking
- Latency measurement
- Cost calculation
- User session tracking
- Debug UI

**Learn:**
- Setting up Langfuse
- Integrating with agents
- Analyzing traces
- Performance optimization

---

### 2. Langsmith_Monitoring
**What:** LangChain native monitoring  
**Why:** Built-in monitoring for LangChain agents  
**Level:** Advanced  
**Time:** 1-2 hours

**Features:**
- LangChain tracing
- Chain visualization
- Performance metrics
- Debugging tools
- Production monitoring

**Learn:**
- Langsmith setup
- LangChain integration
- Debugging chains
- Production patterns

---

## 🚀 Quick Start

### Setup Langfuse_Monitoring

```bash
cd Langfuse_Monitoring

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add:
# OPENAI_API_KEY=...
# LANGFUSE_PUBLIC_KEY=...
# LANGFUSE_SECRET_KEY=...
# LANGFUSE_HOST=...
```

### Setup Langsmith_Monitoring

```bash
cd ../Langsmith_Monitoring

# Same setup as Langfuse
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## 🔑 Key Concepts

### What is Observability?

```
Monitoring:  Track metrics (latency, cost, errors)
Logging:     Record events and data
Tracing:     Follow requests through system
Debugging:   Understand why something happened
```

### Tracing Flow

```
Agent starts
    ↓ [Log: Agent invoked]
Tool call 1
    ↓ [Log: Tool executed]
LLM call
    ↓ [Log: LLM response received]
Processing
    ↓ [Log: Output generated]
Agent completes
    ↓ [Log: Agent finished, time: 5.2s, cost: $0.05]
```

### Key Metrics

| Metric | Why Important | Threshold |
|--------|---------------|-----------|
| Latency | User experience | < 2 seconds |
| Cost | Budget | < $0.10 per request |
| Error Rate | Reliability | < 1% |
| Token Usage | Efficiency | Baseline |

---

## 🛠️ Common Tasks

### 1. Add Tracing to Agent

**Langfuse:**
```python
from langfuse.decorators import observe

@observe()
def my_agent(input):
    # Agent logic
    return result

# Trace recorded automatically!
```

**Langsmith:**
```python
from langsmith import traceable

@traceable()
def my_agent(input):
    # Agent logic
    return result
```

### 2. Log Events

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Log event
langfuse.log_event({
    "name": "agent_started",
    "input": user_input,
    "timestamp": datetime.now()
})
```

### 3. Track Performance

```python
# Automatic with tracing decorator
# Metrics captured:
# - Latency
# - Token count
# - Cost
# - Success/error
```

### 4. Debug Issues

1. Access trace dashboard
2. Find failed trace
3. Examine step-by-step execution
4. Identify problematic step
5. Fix and redeploy

---

## 📊 Observability Platform Comparison

| Feature | Langfuse | Langsmith |
|---------|----------|-----------|
| Cost tracking | ✅ | ✅ |
| Trace visualization | ✅✅ | ✅ |
| LangChain native | ⚠️ | ✅✅ |
| LLM agnostic | ✅✅ | ⚠️ |
| UI quality | ✅✅✅ | ✅✅ |
| Pricing | Per request | Subscription |
| Setup complexity | Medium | Easy |

---

## 🎯 Why Observability Matters

### In Development
- Debug issues quickly
- Understand agent behavior
- Optimize prompts
- Track cost during iteration

### In Production
- Monitor performance
- Track user behavior
- Debug customer issues
- Optimize costs
- Ensure reliability

---

## 📈 Metrics to Track

### Performance Metrics
```
Latency:     Time to complete request
Throughput:  Requests per second
Error Rate:  % of failed requests
Success Rate: % of successful requests
```

### Cost Metrics
```
Per Request: $X per API call
Total Cost:  $X per day/month
Token Usage: Tokens per request
LLM Cost:    LLM cost percentage
```

### Quality Metrics
```
Accuracy:      % correct outputs
User Feedback: User ratings
Failure Rate:  % of failed requests
Revision Rate: % needing revision
```

---

## 🎓 Exercises

### Exercise 1: Add Tracing
1. Take an existing agent
2. Add Langfuse/Langsmith integration
3. Run the agent
4. View traces in dashboard

### Exercise 2: Analyze Traces
1. Run agent 10 times
2. Analyze trace dashboard
3. Calculate average latency
4. Calculate average cost

### Exercise 3: Debugging
1. Create a failing agent
2. Add tracing
3. Run and see failure trace
4. Debug using trace information

### Exercise 4: Performance Optimization
1. Baseline agent metrics
2. Optimize LLM calls
3. Re-measure metrics
4. Compare before/after

---

## 🔗 Production Monitoring Setup

```
Production Agent
    ↓
Tracing/Logging
    ↓
Observability Platform (Langfuse/Langsmith)
    ↓
Dashboard & Alerts
    ↓
Ops Team
```

---

## 📚 Reference

- [Langfuse Documentation](https://langfuse.com/docs)
- [Langsmith Documentation](https://docs.smith.langchain.com/)
- [01_Agentic_AI_Fundamentals](../../01_Agentic_AI_Fundamentals.md) - Section 8 (Observability)

---

## ✅ Completion Checklist

- [ ] Set up Langfuse_Monitoring
- [ ] Understand tracing concept
- [ ] Add tracing to agent
- [ ] View traces in dashboard
- [ ] Set up Langsmith_Monitoring
- [ ] Compare the platforms
- [ ] Complete Exercise 1
- [ ] Complete Exercise 2
- [ ] Complete Exercise 3
- [ ] Complete Exercise 4
- [ ] Ready to integrate tools!

---

## 🚀 Next Steps

After mastering observability:
1. **Integrate Tools** → 06_Integration_Tools
2. **Build Project** → 07_Real_World_Projects
3. **Deploy Production** → Production deployment patterns

---

**Ready to integrate with external tools?** 👉 [06_Integration_Tools](../06_Integration_Tools/README.md)

Last Updated: May 18, 2026
