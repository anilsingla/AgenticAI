# 06_Integration_Tools

Connect agents with external tools, APIs, and platforms.

---

## 📚 Overview

Integration tools enable agents to work with external systems:
- **MCP (Model Context Protocol)** - Protocol for agent-tool communication
- **N8N** - No-code workflow automation platform

**Level:** Advanced  
**Prerequisites:** All previous sections

---

## 🎯 What You'll Learn

- ✅ MCP protocol basics
- ✅ Tool integration patterns
- ✅ API integration
- ✅ Workflow automation
- ✅ No-code vs code solutions
- ✅ Integration best practices

---

## 📂 Projects in This Category

### 1. MCP_Demo
**What:** Model Context Protocol demonstration  
**Why:** Standard protocol for agent-tool communication  
**Level:** Advanced  
**Time:** 1-2 hours

**Features:**
- MCP server implementation
- Tool definition
- Protocol communication
- Client-server architecture

**Learn:**
- MCP specification
- Building MCP servers
- Integrating tools
- Protocol patterns

---

### 2. N8N_Workflow
**What:** No-code workflow automation  
**Why:** Visual workflow builder for agents  
**Level:** Advanced  
**Time:** 1-2 hours

**Features:**
- Workflow design
- Integration nodes
- Conditional logic
- Error handling
- Scheduling

**Learn:**
- N8N basics
- Workflow patterns
- Integration nodes
- Automation design

---

## 🚀 Quick Start

### Setup MCP_Demo

```bash
cd MCP_Demo

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Setup N8N_Workflow

```bash
cd ../N8N_Workflow

# Using Docker (recommended)
docker-compose up

# Or local installation
npm install -g n8n
n8n
```

---

## 🔑 Key Concepts

### MCP Architecture

```
LLM Agent
    ↓
MCP Client
    ↓ (MCP Protocol)
MCP Server
    ├─ Tool 1
    ├─ Tool 2
    └─ Tool 3
```

### Integration Patterns

```
Pattern 1: Direct Tool Call
Agent → Tool → Result

Pattern 2: Via Integration Platform
Agent → Platform → Multiple Tools → Result

Pattern 3: Workflow Automation
Trigger → Workflow → Steps → Agents → Output
```

---

## 🛠️ MCP Basics

### Define a Tool in MCP

```python
# server.py
from mcp.server import Server

server = Server("my-tool-server")

@server.tool()
def search_database(query: str) -> str:
    """Search the database"""
    # Implementation
    return results

# Client uses via MCP protocol
```

### Register MCP Server

```python
# Agent configuration
agent.register_mcp_server(
    "https://localhost:3000",
    tools=["search_database", "update_record"]
)
```

---

## 🎯 N8N Basics

### Workflow Components

```
Trigger (When to start)
    ↓
Input Processing
    ↓
Decision (If/else)
    ↓
Tool Integration
    ↓
Agent Call
    ↓
Output Processing
    ↓
Result
```

### Integration Nodes Available

- **LLM Nodes:** GPT-4, Claude, etc.
- **API Nodes:** REST, GraphQL
- **Database Nodes:** SQL, NoSQL
- **Chat Nodes:** Slack, Teams, Discord
- **File Nodes:** S3, Google Drive, local
- **Custom Nodes:** JavaScript/Python

---

## 💡 MCP vs N8N

| Aspect | MCP | N8N |
|--------|-----|-----|
| Use case | Direct tool integration | Workflow automation |
| Requires code | ✅ Yes | ❌ No (mostly) |
| Flexibility | ✅✅✅ | ✅✅ |
| Ease of use | ⚠️ Medium | ✅✅ Easy |
| Best for | Developers | Business users |
| Scalability | ✅✅ | ✅✅✅ |
| Cost | Low | Low-Medium |

---

## 🔗 Integration Examples

### Example 1: Agent + MCP Tool

```python
# Agent needs to search database
# MCP server provides search_database tool
# Agent can call: agent.run("Search for John")
# Automatically uses search_database via MCP
```

### Example 2: N8N Workflow

```
When webhook received
    ↓
Parse JSON
    ↓
Call Agent (via HTTP)
    ↓
If agent says urgent
    ├─ Send Slack message
    └─ Create ticket
Else
    └─ Save to database
```

### Example 3: Combined

```
N8N Webhook
    ↓
N8N calls Agent API
    ↓
Agent uses MCP tools
    ↓
Agent returns result
    ↓
N8N sends to Slack
```

---

## 🛠️ Common Tasks

### "How do I add a tool to agent?"

Via MCP:
```python
# Define tool in MCP server
@server.tool()
def my_tool(input):
    return result

# Agent automatically gets access
```

Via N8N:
```
Drag tool node → Connect → Configure
```

### "How do I call external API?"

Via MCP:
```python
@server.tool()
def call_api(endpoint):
    response = requests.get(f"https://api.example.com/{endpoint}")
    return response.json()
```

Via N8N:
```
Drag "HTTP Request" node → Configure URL → Done
```

### "How do I add error handling?"

Via MCP:
```python
@server.tool()
def my_tool(input):
    try:
        # Call external service
        return result
    except Exception as e:
        return {"error": str(e)}
```

Via N8N:
```
Add "Error Handling" node after tool
→ Configure fallback path
```

---

## 🚀 Integration Patterns

### Pattern 1: Real-time Integration
```
Agent Request → Tool → Immediate Result
```
Use when: Need immediate response

### Pattern 2: Async Integration
```
Agent Request → Job Queue → Process → Notify
```
Use when: Long-running tasks

### Pattern 3: Scheduled Integration
```
Schedule → Check Conditions → Execute Actions
```
Use when: Periodic tasks

---

## 📊 When to Use Each

| Situation | Use |
|-----------|-----|
| Custom tool for agent | MCP |
| Visual workflow design | N8N |
| No-code solution needed | N8N |
| Direct API integration | Either |
| Complex business logic | MCP |
| Rapid prototyping | N8N |
| Production deployment | MCP |
| Team without coding | N8N |

---

## 🎓 Exercises

### Exercise 1: Build MCP Server
1. Define simple tool
2. Create MCP server
3. Register with agent
4. Test tool usage

### Exercise 2: Create N8N Workflow
1. Design workflow
2. Add trigger
3. Add tool nodes
4. Test end-to-end

### Exercise 3: Integration
1. Build MCP server with 2 tools
2. Create N8N workflow using those tools
3. Test integration

### Exercise 4: Real Integration
1. Choose external service (API)
2. Integrate via MCP or N8N
3. Test with agent
4. Document integration

---

## 📚 Reference

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [N8N Documentation](https://docs.n8n.io/)
- [Tool Building Guide](../../05_Quick_Reference.md) - Tool Integration section

---

## ✅ Completion Checklist

- [ ] Understand MCP protocol
- [ ] Set up MCP_Demo
- [ ] Build simple MCP tool
- [ ] Set up N8N
- [ ] Create simple workflow
- [ ] Integrate agent with tool
- [ ] Compare MCP vs N8N
- [ ] Complete Exercise 1
- [ ] Complete Exercise 2
- [ ] Complete Exercise 3
- [ ] Ready for real-world projects!

---

## 🚀 Next Steps

After mastering integrations:
1. **Build Project** → 07_Real_World_Projects
2. **Deploy** → Production deployment
3. **Scale** → Multi-agent orchestration

---

**Ready to build complete systems?** 👉 [07_Real_World_Projects](../07_Real_World_Projects/README.md)

Last Updated: May 18, 2026
