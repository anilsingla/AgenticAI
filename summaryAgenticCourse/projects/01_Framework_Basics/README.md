# 01_Framework_Basics

Learn agentic AI fundamentals with simple, clear examples using different frameworks.

---

## 📚 Overview

This category contains foundational agent implementations using different frameworks. Perfect for:
- **Beginners** - Start here to understand basic agent patterns
- **Framework explorers** - Compare different frameworks
- **Learners** - Build understanding step by step

---

## 🎯 Projects in This Category

### 1. Agno_Framework
**What:** Basic agent implementations using the Agno framework
**Why:** Agno provides simple, intuitive agent building blocks
**Level:** Beginner
**Time:** 30-45 minutes

**Contains:**
- `basic_agent.ipynb` - Simple agent example
- `state_memory_agent.ipynb` - Agent with state management

**Learn:** Core agent concepts and lifecycle

---

### 2. CrewAI_Basics
**What:** CrewAI framework examples with multiple agents and workflows
**Why:** CrewAI provides excellent multi-agent patterns and orchestration
**Level:** Beginner → Intermediate
**Time:** 1-2 hours

**Contains:**
- `basic_agent.py` - Single agent example
- `multi_agent.py` - Multiple agents working together
- `customer_care_flow.py` - Real workflow example
- `flow_linear.py` & `flow_branching.py` - Different execution patterns
- `prd_review.py` - Complex workflow example

**Learn:** Agent coordination, workflows, task assignment

---

## 🚀 Quick Start

### Setup (Any Project)

```bash
# 1. Navigate to project folder
cd Agno_Framework
# or
cd CrewAI_Basics

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
# or
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Run Projects

**For Jupyter Notebooks (Agno):**
```bash
cd Agno_Framework
jupyter notebook
# Open basic_agent.ipynb or state_memory_agent.ipynb in browser
```

**For Python Scripts (CrewAI):**
```bash
cd CrewAI_Basics
python basic_agent.py
python multi_agent.py
python customer_care_flow.py
```

---

## 📖 Learning Path

### Recommended Order

1. **Start with Agno (30 min)**
   - Open `basic_agent.ipynb`
   - Read through the notebook
   - Run each cell
   - Understand the flow

2. **Explore State Management (20 min)**
   - Open `state_memory_agent.ipynb`
   - See how agents remember information
   - Understand the difference

3. **Try CrewAI Basic Agent (20 min)**
   - Run `basic_agent.py`
   - See output
   - Modify the prompt and rerun

4. **Study CrewAI Multi-Agent (30 min)**
   - Read `multi_agent.py`
   - Understand agent coordination
   - Try running it

5. **Explore Workflows (40 min)**
   - Run `linear_flow.py` - sequential tasks
   - Run `branching_flow.py` - conditional logic
   - Understand flow control

6. **Real Example (30 min)**
   - Study `customer_care_flow.py`
   - See a realistic workflow
   - Understand how everything fits together

---

## 🔑 Key Concepts Covered

### In Agno Framework
- ✅ What is an agent?
- ✅ Agent initialization and configuration
- ✅ Running an agent
- ✅ Getting agent output
- ✅ State and memory management
- ✅ Agent lifecycle

### In CrewAI Framework
- ✅ Agent definition (role, goal, backstory)
- ✅ Task creation and assignment
- ✅ Agent coordination
- ✅ Linear workflows
- ✅ Branching/conditional execution
- ✅ Real-world workflow patterns

---

## 🛠️ Common Tasks

### "How do I create an agent?"

**Agno:**
```python
from agno.agent import Agent

agent = Agent(
    name="Helper",
    model="gpt-4o-mini",
    instructions="You are a helpful assistant"
)

response = agent.run("Hello!")
print(response)
```

**CrewAI:**
```python
from crewai import Agent, Task

agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert data analyst"
)

task = Task(
    description="Analyze this data: ...",
    agent=agent
)
```

### "How do I run agents in sequence?"

See `customer_care_flow.py` in CrewAI_Basics for a complete example.

### "How do I add tools to agents?"

Check the advanced projects in `04_Specialized_Agents` for tool use examples.

---

## 📊 Framework Comparison

| Feature | Agno | CrewAI |
|---------|------|--------|
| Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Learning curve | Gentle | Moderate |
| Multi-agent | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Documentation | Good | Excellent |
| Community | Growing | Very active |
| Best for | Learning | Production |

---

## 🔗 Project Structure

```
01_Framework_Basics/
├─ Agno_Framework/
│  ├─ basic_agent.ipynb
│  ├─ state_memory_agent.ipynb
│  ├─ requirements.txt
│  ├─ .env.example
│  └─ README.md
│
└─ CrewAI_Basics/
   ├─ basic_agent.py
   ├─ multi_agent.py
   ├─ customer_care_flow.py
   ├─ flow_linear.py
   ├─ flow_branching.py
   ├─ prd_review.py
   ├─ requirements.txt
   ├─ .env.example
   ├─ PRD.md
   ├─ CUSTOMER_CARE_README.md
   └─ README.md
```

---

## 📚 What You'll Learn

### After Agno_Framework
- [x] Understand agent basics
- [x] Know how to initialize agents
- [x] Understand state management
- [x] Can run simple agents

### After CrewAI_Basics
- [x] Understand agent roles and goals
- [x] Can create multi-agent systems
- [x] Understand workflows
- [x] Know when to use sequential vs branching
- [x] Can build realistic workflows

---

## 🎓 Next Steps

After completing these basic projects:

1. **Explore Multi-Agent Systems** (02_Multi_Agent_Systems)
   - Learn advanced orchestration
   - Hierarchical agents
   - Complex coordination

2. **Add RAG** (03_RAG_And_Knowledge)
   - Connect to knowledge bases
   - Improve agent reasoning

3. **Specialize** (04_Specialized_Agents)
   - Build domain-specific agents
   - Implement real workflows

4. **Add Monitoring** (05_Observability_Monitoring)
   - Track agent behavior
   - Debug issues

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
```bash
# Create .env file with:
OPENAI_API_KEY=sk-your-key-here
```

### "Jupyter kernel not found"
```bash
pip install jupyter
python -m ipykernel install --user
```

### "Agent doesn't respond"
- Check API key is set
- Verify internet connection
- Check API quota on OpenAI dashboard

---

## 💡 Tips for Best Learning

1. **Read before running** - Understand code first
2. **Run each example** - Observe the output
3. **Modify the code** - Change prompts and settings
4. **Experiment** - Try different inputs
5. **Compare frameworks** - Understand pros/cons
6. **Move forward** - Don't get stuck, move to next topic

---

## 📖 Additional Resources

- [Agno Documentation](https://docs.agno.dev/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [01_Agentic_AI_Fundamentals.md](../../01_Agentic_AI_Fundamentals.md)
- [04_Sequential_Learning_Guide.md](../../04_Sequential_Learning_Guide.md) Phase 1

---

## ✅ Checklist for Completion

- [ ] Set up Agno_Framework
- [ ] Run basic_agent.ipynb
- [ ] Modify Agno agent and see change
- [ ] Understand state_memory_agent.ipynb
- [ ] Set up CrewAI_Basics
- [ ] Run basic_agent.py
- [ ] Run multi_agent.py
- [ ] Run customer_care_flow.py
- [ ] Understand workflow patterns
- [ ] Compare the two frameworks
- [ ] Ready for next level!

---

## 🚀 You're Ready When...

✅ You understand what an agent is  
✅ You can run agents  
✅ You understand how agents are configured  
✅ You can create multi-agent workflows  
✅ You understand different framework choices  

👉 **Next:** Move to [02_Multi_Agent_Systems](../02_Multi_Agent_Systems/README.md) or pick a specialized agent from [04_Specialized_Agents](../04_Specialized_Agents/README.md)

---

**Happy learning!** 🎓

Last Updated: May 18, 2026
