# 04_Specialized_Agents

Domain-specific agent implementations for real-world applications.

---

## 📚 Overview

This category demonstrates specialized agents built for specific domains:
- **HR Agent** - Human Resources automation
- **DevOps Agent** - Operations automation
- **MAF Framework** - Multi-agent framework patterns

**Level:** Intermediate → Advanced  
**Prerequisites:** 01_Framework_Basics, 02_Multi_Agent_Systems

---

## 🎯 What You'll Learn

- ✅ Domain-specific agent design
- ✅ Tool integration
- ✅ Database interaction
- ✅ Complex workflows
- ✅ Real business logic
- ✅ Production patterns

---

## 📂 Projects in This Category

### 1. HR_Agent
**What:** Complete HR automation system  
**Why:** Real-world business application  
**Level:** Intermediate  
**Time:** 2-3 hours

**Contains:**
- `agent.py` - HR agent implementation
- `app.py` - Application interface
- `tools.py` - HR-specific tools
- `db_setup.py` - Database initialization
- `hr_database.db` - Sample data
- `policies/` - Company policies (knowledge base)
- `chroma_db/` - Vector storage for RAG
- `README.md` - Project-specific guide

**Features:**
- Employee management
- Policy lookup (RAG)
- Onboarding workflows
- HR queries
- Document processing

**Learn:**
- Tool creation and use
- Database operations
- RAG for policies
- Multi-step workflows

---

### 2. DevOps_Agent
**What:** DevOps operations automation  
**Why:** Infrastructure and deployment tasks  
**Level:** Intermediate → Advanced  
**Time:** 2-3 hours

**Contains:**
- Infrastructure automation
- Deployment management
- Monitoring integration
- Incident response
- Log analysis
- System diagnostics

**Features:**
- Server health checks
- Deployment assistance
- Log parsing
- Incident escalation
- Troubleshooting workflows

**Learn:**
- Complex tool integration
- System automation
- Error handling
- Operational workflows

---

### 3. MAF_Framework
**What:** Multi-Agent Framework examples  
**Why:** Framework patterns and best practices  
**Level:** Advanced  
**Time:** 1-2 hours

**Contains:**
- Framework architecture
- Agent patterns
- Coordination examples
- Best practices

**Learn:**
- Framework design
- Scalability patterns
- Architecture decisions

---

## 🚀 Quick Start

### Setup HR_Agent

```bash
cd HR_Agent

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python db_setup.py

# Configure environment
cp .env.example .env
# Add OPENAI_API_KEY
```

### Run HR_Agent

```bash
# Interactive app
python app.py

# Or use agent directly
python agent.py
```

### Setup DevOps_Agent

```bash
cd ../DevOps_Agent

# Same setup as HR_Agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## 🔑 Key Concepts

### Domain-Specific Tools

HR Agent tools example:
```python
# Tool 1: Look up employee
def search_employee(name):
    # Query database
    return employee_info

# Tool 2: Check policy
def get_policy(policy_name):
    # RAG query
    return policy_text

# Tool 3: Process request
def process_request(request_type, data):
    # Complex logic
    return result
```

### Workflow Integration

```python
# Step 1: Agent receives request
request = "Tell me about vacation policy"

# Step 2: Agent selects tool
tool = "get_policy"

# Step 3: Agent uses tool
result = get_policy("vacation")

# Step 4: Agent generates response
response = generate_response(result)
```

### Database Interaction

```python
# Connect to HR database
db = connect_to_database()

# Query employees
employees = db.query("SELECT * FROM employees")

# Update records
db.update("employees", {"status": "active"})
```

---

## 💼 HR_Agent Deep Dive

### Features

| Feature | Description | Tools Used |
|---------|-------------|-----------|
| Employee Lookup | Find employee info | SQL + Vector DB |
| Policy Search | Find HR policies | RAG |
| Onboarding | New employee workflow | Multi-step |
| Offboarding | Employee exit process | Multi-step |
| Leave Management | Vacation/sick leave | Database |
| Benefits Info | Employee benefits | Vector DB |

### Architecture

```
User Request
    ↓
HR Agent
├─ SQL Database (employee data)
├─ Vector DB (policies via RAG)
└─ Tool Router
    ├─ Employee Tools
    ├─ Policy Tools
    └─ Request Tools
```

### Example Usage

```python
agent.run("What are the vacation policies?")
# Uses: RAG lookup in policies/

agent.run("Who is the manager of John Doe?")
# Uses: SQL query to database

agent.run("Start onboarding for new employee")
# Uses: Multi-step workflow
```

---

## 💡 Design Patterns

### Pattern 1: Database + RAG
```
Query: "Policy for X"
├─ Check database for X
├─ If not found, RAG search
└─ Return best match
```

### Pattern 2: Multi-Step Workflow
```
Onboarding:
├─ Create employee record
├─ Send welcome email
├─ Schedule training
└─ Generate access tokens
```

### Pattern 3: Tool Selection
```
Agent decides:
├─ Is it a policy question? → Use RAG
├─ Is it employee data? → Use SQL
├─ Is it a workflow? → Use multi-step
```

---

## 🎓 Exercises

### Exercise 1: Extend HR_Agent
1. Add new tool (e.g., salary lookup)
2. Integrate with database
3. Test end-to-end

### Exercise 2: Create New Workflow
1. Design workflow (e.g., performance review)
2. Implement steps
3. Test integration

### Exercise 3: Improve Knowledge Base
1. Add more policies to RAG
2. Test retrieval quality
3. Optimize embeddings

### Exercise 4: Build DevOps Agent
1. Study DevOps_Agent code
2. Understand tool integration
3. Extend with new capabilities

---

## 📊 When to Specialize?

When building an agent, ask:
- ✅ Is it domain-specific? → Specialize
- ✅ Does it need tools? → Add tools
- ✅ Does it access databases? → Integrate DB
- ✅ Does it need knowledge? → Add RAG
- ✅ Is it a workflow? → Design workflow

---

## 🔗 Related Projects

- **Foundation:** 01_Framework_Basics + 03_RAG_And_Knowledge
- **Monitor:** 05_Observability_Monitoring
- **Deploy:** 07_Real_World_Projects
- **Similar Pattern:** HR_Agent and Capstone_Project

---

## 🛠️ Common Tasks

### "How do I add a new tool?"

```python
def my_new_tool(input_param):
    """Tool description"""
    # Do something
    return result

# Register with agent
agent.add_tool(my_new_tool)
```

### "How do I connect to database?"

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM table")
results = cursor.fetchall()
```

### "How do I use RAG in my agent?"

See HR_Agent policies/ folder and chroma_db/

---

## ✅ Completion Checklist

- [ ] Set up HR_Agent
- [ ] Run HR_Agent app
- [ ] Understand HR tools
- [ ] Query HR database
- [ ] Test policy RAG
- [ ] Understand workflow
- [ ] Study DevOps_Agent
- [ ] Understand tool integration
- [ ] Study MAF_Framework
- [ ] Complete Exercise 1
- [ ] Complete Exercise 2
- [ ] Ready to add monitoring!

---

## 🚀 Next Steps

After mastering specialized agents:
1. **Add Monitoring** → 05_Observability_Monitoring
2. **Integrate Tools** → 06_Integration_Tools
3. **Build Project** → 07_Real_World_Projects

---

**Ready to add observability?** 👉 [05_Observability_Monitoring](../05_Observability_Monitoring/README.md)

Last Updated: May 18, 2026
