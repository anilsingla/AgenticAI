# Agno_Framework - Basic Agent Implementation

Learn the fundamentals of agentic AI using the Agno framework.

---

## 📚 What is This Project?

This project demonstrates basic agent patterns using Agno, a simple and intuitive agent framework.

**Level:** Beginner  
**Time to complete:** 30-45 minutes  
**Prerequisites:** Python 3.8+, OpenAI API key

---

## 🎯 What You'll Learn

- ✅ What is an agent?
- ✅ How to initialize an agent
- ✅ How to run an agent
- ✅ How to manage agent state
- ✅ Basic agent patterns
- ✅ Agent output handling

---

## 📂 Project Structure

```
Agno_Framework/
├─ basic_agent.ipynb           # Simple agent example
├─ state_memory_agent.ipynb    # Agent with state management
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

### Step 2: Run Notebooks

```bash
# Start Jupyter
jupyter notebook

# Open basic_agent.ipynb in browser
```

---

## 📖 Notebooks Overview

### basic_agent.ipynb

**What:** Simple agent that answers questions

**Contains:**
1. Agent initialization
2. Running the agent
3. Getting responses
4. Basic configuration

**Time:** 15 minutes

**To run:**
```bash
jupyter notebook basic_agent.ipynb
# Execute cells in order
```

**Expected output:**
```
Agent initialized successfully
Running query: "What is machine learning?"
Response: [LLM response about machine learning]
```

---

### state_memory_agent.ipynb

**What:** Agent that remembers information across calls

**Contains:**
1. State management basics
2. Persisting information
3. Using history
4. Context awareness

**Time:** 20 minutes

**To run:**
```bash
jupyter notebook state_memory_agent.ipynb
# Execute cells in order
```

**Expected output:**
```
Agent with memory initialized
Query 1: "My name is John"
Response: "Hello John!"

Query 2: "What is my name?"
Response: "Your name is John"
```

---

## 🔑 Key Concepts

### What is an Agent?

An agent is an AI system that can:
- Understand instructions
- Decide what to do
- Take actions (call tools)
- Learn from results
- Improve over time

### Simple Agent Pattern

```python
from agno.agent import Agent

# Create agent
agent = Agent(
    name="Assistant",
    model="gpt-4o-mini",
    instructions="You are a helpful assistant"
)

# Run agent
response = agent.run("Your question here")

# Get result
print(response)
```

### State and Memory

```python
# Agent can remember information
agent.memory.add("fact", "John is interested in AI")

# Agent can access memory
info = agent.memory.get("fact")
```

---

## 🛠️ Common Tasks

### "How do I create an agent?"

```python
agent = Agent(
    name="MyAgent",
    model="gpt-4o-mini",          # LLM model
    instructions="Your role here" # Agent instructions
)
```

### "How do I run an agent?"

```python
response = agent.run("Your question")
print(response)
```

### "How do I add information to memory?"

```python
agent.memory.add("key", "value")
```

### "How do I retrieve from memory?"

```python
info = agent.memory.get("key")
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'agno'"

```bash
pip install agno
# or
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"

```bash
# Make sure .env file exists
cat .env
# Should show: OPENAI_API_KEY=sk-...

# If not set, edit .env with your key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### "Jupyter kernel not found"

```bash
pip install jupyter
python -m ipykernel install --user
```

### "Agent doesn't respond"

1. Check internet connection
2. Verify API key is valid
3. Check OpenAI account has credits
4. Review error message in notebook
5. Try a simpler query first

---

## 📚 Learning Path

1. **Read this README** (5 min)
2. **Run basic_agent.ipynb** (15 min)
   - Understand agent creation
   - See how it responds
3. **Modify basic_agent** (15 min)
   - Change the instructions
   - Try different questions
   - Observe how agent behaves
4. **Run state_memory_agent.ipynb** (20 min)
   - Understand state management
   - See how memory works
5. **Experiment** (15 min)
   - Create your own agent
   - Add custom instructions
   - Test memory features

---

## 💡 Experiments to Try

### Experiment 1: Change Agent Role

```python
# Make agent a teacher
agent = Agent(
    instructions="You are an expert teacher. Explain complex topics simply."
)

# Ask educational questions
agent.run("Explain quantum computing")
```

### Experiment 2: Use Memory

```python
# Store information
agent.memory.add("user_level", "beginner")
agent.memory.add("user_interest", "AI")

# Agent can use this information
agent.run("Recommend resources for learning")
```

### Experiment 3: Different Models

```python
# Try different models
agent_fast = Agent(model="gpt-4o-mini")      # Fast and cheap
agent_smart = Agent(model="gpt-4")           # More capable
```

---

## ✅ Completion Checklist

- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Configure .env with API key
- [ ] Run basic_agent.ipynb successfully
- [ ] Understand agent initialization
- [ ] Understand agent execution
- [ ] Modify agent instructions
- [ ] Try different questions
- [ ] Run state_memory_agent.ipynb successfully
- [ ] Understand state management
- [ ] Experiment with memory
- [ ] Create custom agent
- [ ] Ready to explore CrewAI!

---

## 🚀 Next Steps

After completing this project:

1. **Explore CrewAI** → Go to ../CrewAI_Basics/
2. **Learn Multi-Agent Systems** → Go to ../../02_Multi_Agent_Systems/
3. **Build Your Own** → Create your first agent-based application

---

## 📖 Additional Resources

- [Agno Documentation](https://docs.agno.dev/)
- [Parent Category Guide](../README.md)
- [Main Learning Resource](../../README.md)
- [Fundamentals Guide](../../01_Agentic_AI_Fundamentals.md)

---

## 💬 Tips for Success

1. **Start simple** - Try basic examples first
2. **Read code carefully** - Understand before running
3. **Run cells one by one** - Don't run all at once
4. **Modify and observe** - Change code and see what happens
5. **Experiment fearlessly** - You can't break anything
6. **Ask questions** - Use agent to clarify concepts
7. **Document learnings** - Write notes about what you learn

---

## 🤝 Getting Help

If you get stuck:

1. **Check the notebook** - Re-read the explanation
2. **Check troubleshooting** - See common issues above
3. **Review requirements.txt** - Make sure all packages installed
4. **Check .env file** - Verify API key is set
5. **Try simplified example** - Start with bare minimum
6. **Check error message** - Usually explains the problem

---

## ⏱️ Time Estimates

| Activity | Time |
|----------|------|
| Setup | 10 min |
| basic_agent.ipynb | 20 min |
| Experimentation | 15 min |
| state_memory_agent.ipynb | 20 min |
| Custom agent | 15 min |
| Total | ~80 min |

---

## 🎓 What Success Looks Like

When you've completed this project, you should be able to:

✅ Create an agent with specific instructions  
✅ Run an agent and get responses  
✅ Modify agent behavior via instructions  
✅ Use agent memory to store information  
✅ Understand agent lifecycle  
✅ Troubleshoot common issues  

---

**Ready to continue?** 👉 [Move to CrewAI Basics](../CrewAI_Basics/README.md)

Last Updated: May 18, 2026
