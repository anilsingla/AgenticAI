# CrewAI_Basics - Multi-Agent Workflows

Learn how to build multi-agent systems and workflows using CrewAI framework.

---

## 📚 What is This Project?

This project demonstrates CrewAI capabilities for building multi-agent systems with tasks, workflows, and coordination.

**Level:** Beginner → Intermediate  
**Time to complete:** 1-2 hours  
**Prerequisites:** Python 3.8+, OpenAI API key

---

## 🎯 What You'll Learn

- ✅ CrewAI framework basics
- ✅ Agent definition and roles
- ✅ Task creation and assignment
- ✅ Multi-agent coordination
- ✅ Sequential workflows
- ✅ Branching/conditional workflows
- ✅ Real-world workflow patterns

---

## 📂 Project Structure

```
CrewAI_Basics/
├─ basic_agent.py               # Single agent example
├─ multi_agent.py               # Multi-agent with linear workflow
├─ customer_care_flow.py        # Real workflow example
├─ flow_linear.py               # Sequential execution
├─ flow_branching.py            # Conditional branching
├─ prd_review.py                # Product review workflow
├─ PRD.md                        # Sample product requirements
├─ CUSTOMER_CARE_README.md      # Customer care workflow guide
├─ requirements.txt             # Python dependencies
├─ .env.example                 # Environment template
└─ README.md                    # This file
```

---

## 🚀 Quick Start

### Step 1: Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate       # Linux/Mac
# or
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Step 2: Run Examples

```bash
# Run single agent
python basic_agent.py

# Run multi-agent system
python multi_agent.py

# Run customer care workflow
python customer_care_flow.py

# Run linear workflow
python flow_linear.py

# Run branching workflow
python flow_branching.py

# Run product review
python prd_review.py
```

---

## 📖 Script Descriptions

### basic_agent.py

**What:** Single agent answering questions

**Contains:**
- Agent creation (role, goal, backstory)
- Task definition
- Execution

**To run:**
```bash
python basic_agent.py
```

**Expected output:**
```
Agent: Researcher
Working on task: Research AI...
[LLM response]
```

**Learn:**
- Basic agent structure
- Task creation
- Single-agent execution

---

### multi_agent.py

**What:** Multiple agents working together

**Contains:**
- 2+ agents with different roles
- Tasks for each agent
- Coordination

**To run:**
```bash
python multi_agent.py
```

**Expected output:**
```
Agent 1: Researches topic
Agent 2: Analyzes research
[Combined output]
```

**Learn:**
- Multi-agent coordination
- Task sequence
- Result aggregation

---

### customer_care_flow.py

**What:** Real-world customer support workflow

**Contains:**
- Customer inquiry processing
- Support agent routing
- Solution generation
- Quality assurance

**To run:**
```bash
python customer_care_flow.py
```

**Learn:**
- Real business workflows
- Multi-agent patterns
- Error handling

See [CUSTOMER_CARE_README.md](./CUSTOMER_CARE_README.md) for details.

---

### flow_linear.py

**What:** Sequential task execution

**Architecture:**
```
Task 1 → Task 2 → Task 3 → Result
```

**To run:**
```bash
python flow_linear.py
```

**Learn:**
- Sequential execution
- Task dependencies
- Step-by-step processing

---

### flow_branching.py

**What:** Conditional workflow with branching

**Architecture:**
```
    ├─ Path A
Input ─┤
    └─ Path B
```

**To run:**
```bash
python flow_branching.py
```

**Learn:**
- Conditional logic
- Branching paths
- Dynamic workflows

---

### prd_review.py

**What:** Product requirement document review workflow

**Contains:**
- Technical reviewer agent
- UX reviewer agent
- Business analyst agent
- Quality assurance

**To run:**
```bash
python prd_review.py
```

See [PRD.md](./PRD.md) for sample input.

**Learn:**
- Complex workflows
- Specialist agents
- Multi-perspective analysis

---

## 🔑 Key Concepts

### Agent Definition

```python
from crewai import Agent

agent = Agent(
    role="Data Analyst",
    goal="Analyze data and find insights",
    backstory="Expert data analyst with 10 years experience",
    verbose=True,
    allow_delegation=False
)
```

### Task Definition

```python
from crewai import Task

task = Task(
    description="Analyze sales data for Q4...",
    expected_output="Summary of key metrics",
    agent=analyst_agent
)
```

### Crew Orchestration

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    verbose=True
)

result = crew.kickoff()
```

---

## 🛠️ Common Tasks

### "How do I create an agent?"

```python
from crewai import Agent

my_agent = Agent(
    role="Your role",
    goal="Your goal",
    backstory="Your backstory"
)
```

### "How do I assign a task?"

```python
from crewai import Task

my_task = Task(
    description="What to do",
    agent=my_agent
)
```

### "How do I run multiple agents?"

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2]
)

result = crew.kickoff()
```

### "How do I handle branching?"

See `flow_branching.py` for conditional execution patterns.

---

## 💡 Workflow Patterns

### Pattern 1: Sequential Pipeline

Best for: Tasks that depend on previous results

```python
# Agent A processes input
# Agent B processes A's output
# Agent C processes B's output
```

### Pattern 2: Parallel Processing

Best for: Independent analysis from multiple angles

```python
# Agent A analyzes angle 1
# Agent B analyzes angle 2
# Aggregate results
```

### Pattern 3: Hierarchical

Best for: Different levels of review/approval

```python
# Specialist agents do detailed work
# Manager agent reviews and approves
# Director agent makes final decision
```

---

## 📊 Comparison: Agno vs CrewAI

| Aspect | Agno | CrewAI |
|--------|------|--------|
| Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Agents | Individual | Teams |
| Task Management | Basic | Advanced |
| Workflows | Simple | Complex |
| Best for | Learning | Production |
| Community | Small | Large |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'crewai'"

```bash
pip install crewai
# or
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"

```bash
# Edit .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### "Agent doesn't execute tasks"

1. Check all agents are defined
2. Check all tasks have agents assigned
3. Verify task descriptions are clear
4. Check for circular dependencies

### "Slow execution"

- CrewAI is verbose by default
- Use `verbose=False` for faster output
- Parallel execution can speed up

---

## 🎓 Learning Path

1. **Understand CrewAI concepts** (10 min)
   - Read this README
   - Understand agent/task/crew structure

2. **Run basic_agent.py** (10 min)
   - See single agent in action
   - Understand output format

3. **Run multi_agent.py** (15 min)
   - See coordination
   - Understand task sequence

4. **Study flow examples** (20 min)
   - Run flow_linear.py
   - Run flow_branching.py
   - Understand differences

5. **Study real workflow** (15 min)
   - Run customer_care_flow.py
   - Read CUSTOMER_CARE_README.md
   - Understand business logic

6. **Run prd_review.py** (10 min)
   - See complex workflow
   - Understand specialist agents

7. **Experiment** (20 min)
   - Modify an example
   - Add your own task
   - Observe changes

---

## 💡 Experiments to Try

### Experiment 1: Add New Agent

```python
# Add a new agent to multi_agent.py
new_agent = Agent(
    role="Your role",
    goal="Your goal",
    backstory="Your backstory"
)

# Add its task
new_task = Task(
    description="What it should do",
    agent=new_agent
)

# Add to crew
crew = Crew(
    agents=[...existing agents..., new_agent],
    tasks=[...existing tasks..., new_task]
)
```

### Experiment 2: Change Workflow

```python
# Modify flow_linear.py to run tasks in different order
# Or make it parallel instead of sequential
```

### Experiment 3: Conditional Logic

```python
# Add conditions to flow_branching.py
# Create new branches based on conditions
```

---

## ✅ Completion Checklist

- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Configure .env
- [ ] Run basic_agent.py
- [ ] Run multi_agent.py
- [ ] Run customer_care_flow.py
- [ ] Run flow_linear.py
- [ ] Run flow_branching.py
- [ ] Run prd_review.py
- [ ] Understand each script
- [ ] Modify an example
- [ ] Create custom workflow
- [ ] Ready to move forward!

---

## 📖 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [CUSTOMER_CARE_README.md](./CUSTOMER_CARE_README.md)
- [Parent Category Guide](../README.md)
- [Main Learning Resource](../../README.md)

---

## 🚀 Next Steps

After completing this project:

1. **Learn Multi-Agent Systems** → ../../02_Multi_Agent_Systems/
2. **Add Knowledge (RAG)** → ../../03_RAG_And_Knowledge/
3. **Build Specialized Agents** → ../../04_Specialized_Agents/
4. **Compare Frameworks** → Back to ../README.md

---

## 💬 Tips for Success

1. **Start with basic_agent.py** - Simplest example
2. **Understand each script** before modifying
3. **Read output carefully** - Agents show their thinking
4. **Experiment with prompts** - Change agent instructions
5. **Try different workflows** - Run each example
6. **Combine concepts** - Mix patterns together
7. **Document changes** - Keep track of what you try

---

## ⏱️ Time Estimates

| Activity | Time |
|----------|------|
| Setup | 10 min |
| basic_agent.py | 10 min |
| multi_agent.py | 15 min |
| Flow examples | 20 min |
| customer_care_flow.py | 15 min |
| prd_review.py | 10 min |
| Experimentation | 20 min |
| Total | ~100 min |

---

## 🎓 What Success Looks Like

When you've completed this project, you should be able to:

✅ Create agents with specific roles  
✅ Define tasks for agents  
✅ Orchestrate multiple agents  
✅ Create sequential workflows  
✅ Create branching workflows  
✅ Understand workflow patterns  
✅ Build real business workflows  

---

**Ready to explore advanced topics?** 👉 [Move to Multi-Agent Systems](../../02_Multi_Agent_Systems/README.md)

Last Updated: May 18, 2026

---

## Prerequisites And Requirements

- Python 3.10+ recommended
- OpenAI API key (`OPENAI_API_KEY`)
- Optional: Serper API key for web search tools (`SERPER_API_KEY`)
- Basic understanding of agent/task workflow concepts

## Files Explained (Beginner View)

- `basic_agent.py`: Minimal single-agent CrewAI execution
- `multi_agent.py`: Multi-agent sequential orchestration (research -> analysis -> write)
- `multi_agent_hierarchical.py`: Hierarchical agent pattern with supervisor-like flow
- `customer_care_flow.py`: Practical customer-support style process
- `flow_linear.py`: Linear chain of tasks
- `flow_branching.py`: Conditional path routing based on input/state
- `prd_review.py`: Multi-role PRD review pipeline
- `PRD.md`: Input document used for review examples
- `CUSTOMER_CARE_README.md`: Project-specific scenario notes
- `requirements.txt`: Python dependencies

## API/Tool Cost Notes (Approx, verify before usage)

- OpenAI `gpt-4o-mini`: pay-per-token (low-cost for demos)
- Serper API (if used by `SerperDevTool`): external paid plan after free quota
- Website scraping tools: no direct API fee from CrewAI itself, but target sites may rate-limit
