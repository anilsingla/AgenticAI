# Agentic AI Projects Collection

Welcome to the comprehensive collection of Agentic AI projects organized by topic and learning difficulty. These projects demonstrate practical implementations of agentic AI concepts covered in the learning guides.

---

## 📁 Project Organization

All projects are organized into 7 topic-wise categories, designed for progressive learning:

### **01_Framework_Basics**
Foundational agent implementations using different frameworks.
- **Agno Framework** - Basic agent patterns with Agno
- **CrewAI Basics** - Simple CrewAI agent examples

👉 [Explore Framework Basics →](01_Framework_Basics/README.md)

---

### **02_Multi_Agent_Systems**
Advanced multi-agent orchestration and coordination patterns.
- Learn orchestration patterns
- Hierarchical agent architectures
- Agent communication strategies

👉 [Explore Multi-Agent Systems →](02_Multi_Agent_Systems/README.md)

---

### **03_RAG_And_Knowledge**
Retrieval-Augmented Generation and knowledge integration.
- **LlamaIndex RAG** - RAG implementation with vector stores
- Vector embeddings and semantic search
- Knowledge base integration

👉 [Explore RAG Projects →](03_RAG_And_Knowledge/README.md)

---

### **04_Specialized_Agents**
Domain-specific agent implementations.
- **HR Agent** - Human Resources automation
- **DevOps Agent** - DevOps operations automation
- **MAF Framework** - Multi-agent framework examples

👉 [Explore Specialized Agents →](04_Specialized_Agents/README.md)

---

### **05_Observability_Monitoring**
Logging, monitoring, and observability for agents.
- **Langfuse Monitoring** - Agent tracing and monitoring
- **Langsmith Monitoring** - LangSmith integration

👉 [Explore Observability →](05_Observability_Monitoring/README.md)

---

### **06_Integration_Tools**
Integration with external tools and platforms.
- **MCP Demo** - Model Context Protocol integration
- **N8N Workflow** - Workflow automation integration

👉 [Explore Integration Tools →](06_Integration_Tools/README.md)

---

### **07_Real_World_Projects**
Complete, production-grade implementations.
- **Agno Project** - Full Agno-based application
- **Capstone Project** - Comprehensive capstone implementation

👉 [Explore Real-World Projects →](07_Real_World_Projects/README.md)

---

## 🎯 Learning Paths

### Path 1: Complete Beginner (2-4 weeks)
```
01_Framework_Basics
  ↓
02_Multi_Agent_Systems (Concepts)
  ↓
03_RAG_And_Knowledge (Concepts)
  ↓
04_Specialized_Agents (Pick one)
  ↓
07_Real_World_Projects (Study)
```

### Path 2: Build & Learn (1-2 weeks)
```
01_Framework_Basics
  ↓
Pick ONE:
├─ HR Agent (04_Specialized_Agents)
├─ DevOps Agent (04_Specialized_Agents)
└─ LlamaIndex RAG (03_RAG_And_Knowledge)
  ↓
Add Monitoring: (05_Observability_Monitoring)
  ↓
Deploy & Integrate: (06_Integration_Tools)
```

### Path 3: Advanced (2-3 weeks)
```
All of 01_Framework_Basics
  ↓
02_Multi_Agent_Systems (Build custom)
  ↓
03_RAG_And_Knowledge (Custom RAG)
  ↓
07_Real_World_Projects (Analyze & build on)
  ↓
Integrate all: 05 + 06
```

---

## 📊 Project Statistics

| Category | Projects | Focus | Level |
|----------|----------|-------|-------|
| Framework Basics | 2 | Foundation | Beginner |
| Multi-Agent Systems | - | Coordination | Intermediate |
| RAG & Knowledge | 1 | Retrieval | Intermediate |
| Specialized Agents | 3 | Domain-specific | Intermediate |
| Observability | 2 | Monitoring | Advanced |
| Integration Tools | 2 | Integration | Advanced |
| Real-World | 2 | Production | Advanced |
| **Total** | **12+** | **Complete ecosystem** | **Beginner → Expert** |

---

## 🚀 Deployment & Run Matrix

Use this section as the single reference for how to run each app, where Docker lives, and current cloud script readiness.

| App | Recommended Local Run | Docker Command | Cloud Readiness |
|---|---|---|---|
| 01_Framework_Basics/Agno_Framework | `jupyter notebook` (notebook-first) or `./deployment/windows-local/run_demo.ps1 -Entry basic_agent.ipynb` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 01_Framework_Basics/CrewAI_Basics | `python basic_agent.py` or `./deployment/windows-local/run_demo.ps1 -Entry basic_agent.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 03_RAG_And_Knowledge/LlamaIndex_RAG | `python basic_agent.py` or `./deployment/windows-local/run_demo.ps1 -Entry basic_agent.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 04_Specialized_Agents/DevOps_Agent | `python -c "from agent import run_agent; run_agent()"` | `docker compose -f deployment/docker/docker-compose.yml up -d` | Azure: template, AWS: template |
| 04_Specialized_Agents/HR_Agent | `python app.py` or `./deployment/windows-local/run_demo.ps1 -Entry app.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 04_Specialized_Agents/MAF_Framework | `python basic_agent.py` or `./deployment/windows-local/run_demo.ps1 -Entry basic_agent.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 05_Observability_Monitoring/Langfuse_Monitoring | `python resume_review_agent.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 05_Observability_Monitoring/Langsmith_Monitoring | `python resume_review_agent.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 06_Integration_Tools/MCP_Demo | `python agent.py` (or `python app.py` for DateTime MCP) | `docker build -f deployment/docker/Dockerfile -t jokes-mcp .` | Azure: template script + manual README flow, AWS: template |
| 06_Integration_Tools/N8N_Workflow | Import JSON workflows into n8n UI | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 07_Real_World_Projects/Agno_Project | `python agent.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: template, AWS: template |
| 07_Real_World_Projects/Capstone_Project | `streamlit run ui/app.py` or `./deployment/windows-local/run_demo.ps1 -Entry ui/app.py` | `docker compose -f deployment/docker/docker-compose.yml up --build -d` | Azure: functional scripts, AWS: template |

### Notes

- All apps now include the same deployment scaffold under `deployment/` with `linux-local`, `windows-local`, `docker`, `azure`, and `aws` folders.
- Azure and AWS scripts are templates for most apps. Capstone Project has a functional Azure deploy/terminate pair.
- Standardized coding/log/report support files now exist in each app root: `docs/CODING_STANDARDS.md`, `logs/.gitkeep`, `reports/.gitkeep`.

---

## 🚀 Quick Start Guide

### For First-Time Users

1. **Start with Framework Basics**
   ```bash
   cd 01_Framework_Basics
   cd Agno_Framework
   cat README.md
   ```

2. **Follow the setup instructions** in each project's README

3. **Run your first agent**
   ```bash
   python basic_agent.py
   # or
   jupyter notebook basic_agent.ipynb
   ```

4. **Experiment and modify** the code

5. **Move to next project** and build on knowledge

### Prerequisites

```
Python 3.8+
pip package manager
Virtual environment (recommended)
OpenAI API key (for LLM-based projects)
```

### Universal Setup Steps

For ANY project in this collection:

```bash
# 1. Navigate to project
cd [project-folder]

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run project
python app.py
# OR
jupyter notebook *.ipynb
```

---

## 📚 Documentation Structure

Each project folder contains:

- **README.md** - Project overview, setup, and usage
- **requirements.txt** - Python dependencies
- **.env.example** - Environment variable template
- **Source code** - Implementation files (.py or .ipynb)
- **Data** - Sample data or configurations
- **docs** - Additional documentation

---

## 🔗 Connecting to Main Learning Resource

These projects complement the main learning materials:

| Project | Covers Concept From |
|---------|-------------------|
| Agno_Framework | [01_Fundamentals](../01_Agentic_AI_Fundamentals.md) Section 1-2 |
| CrewAI_Basics | [01_Fundamentals](../01_Agentic_AI_Fundamentals.md) Section 2 |
| LlamaIndex_RAG | [01_Fundamentals](../01_Agentic_AI_Fundamentals.md) Section 5 |
| HR_Agent | [02_Projects](../02_Projects_Overview.md) Similar pattern |
| Langfuse/Langsmith | [01_Fundamentals](../01_Agentic_AI_Fundamentals.md) Section 8 |
| All Projects | [04_Learning_Guide](../04_Sequential_Learning_Guide.md) Phase 3 |

---

## 💡 Project Selection Guide

**Don't know where to start?** Answer these questions:

### 1. What's your experience level?
- **Beginner** → Start with 01_Framework_Basics
- **Intermediate** → Try 02 or 03
- **Advanced** → Jump to 04, 05, 06, 07

### 2. What interests you most?
- **Understanding concepts** → 01_Framework_Basics
- **Building multi-agent** → 02_Multi_Agent_Systems
- **Knowledge retrieval** → 03_RAG_And_Knowledge
- **Specific domain** → 04_Specialized_Agents
- **Monitoring systems** → 05_Observability_Monitoring
- **Integrations** → 06_Integration_Tools
- **Production systems** → 07_Real_World_Projects

### 3. How much time do you have?
- **1 day** → Pick ONE project from 01_Framework_Basics
- **1 week** → Complete 01_Framework_Basics + ONE from 04
- **2 weeks** → 01 + 02 (concepts) + 03 or 04 (build)
- **1 month** → Do all 01-04, study 05-07
- **Ongoing** → Work through all in order

---

## 📖 How to Use These Projects

### For Learning
1. Read the README thoroughly
2. Understand the architecture
3. Study the code
4. Run it and observe
5. Modify and experiment
6. Build your own version

### For Reference
1. Search for specific patterns
2. Copy relevant code sections
3. Adapt to your use case
4. Document your changes

### For Building
1. Use as a starting template
2. Extend with your features
3. Add your own agents
4. Deploy and monitor
5. Share improvements

---

## 🛠️ Common Tasks

### Run a project
```bash
cd [project-folder]
python app.py  # or main.py, agent.py
```

### Run notebooks
```bash
cd [project-folder]
jupyter notebook
# Open the .ipynb file in browser
```

### Install all dependencies for a project
```bash
cd [project-folder]
pip install -r requirements.txt
```

### Check what's needed
```bash
# In the project folder
cat README.md          # Read instructions
cat requirements.txt   # See dependencies
ls                     # List files
```

---

## 🔍 Finding Specific Implementations

### "I want to learn [X]"

| Looking for | Found in |
|------------|----------|
| Basic agent | Agno_Framework/basic_agent.ipynb |
| CrewAI example | CrewAI_Basics/ |
| Multi-agent system | Check 02_Multi_Agent_Systems |
| RAG implementation | LlamaIndex_RAG/ |
| HR automation | HR_Agent/ |
| DevOps automation | DevOps_Agent/ |
| Agent monitoring | Langfuse_Monitoring or Langsmith_Monitoring |
| MCP integration | MCP_Demo/ |
| Full project | Agno_Project/ or Capstone_Project/ |

---

## 🐛 Troubleshooting

### "ImportError: No module named..."
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not set"
```bash
# Create .env file (copy from .env.example)
# Add your API key
# In Python: load_dotenv()
```

### "Jupyter notebook won't start"
```bash
pip install jupyter
jupyter notebook
```

### "Port already in use"
```bash
# Find and use different port
streamlit run app.py --server.port 8502
```

### For project-specific issues
👉 Check the README in that project folder

---

## 📈 Recommended Study Order

### Recommended sequence for complete mastery:

```
Week 1:  Framework Basics (Agno)
Week 2:  Framework Basics (CrewAI)
Week 3:  Multi-Agent Systems (Theory)
Week 4:  RAG & Knowledge (LlamaIndex)
Week 5:  Specialized Agents (Pick HR or DevOps)
Week 6:  Observability (Langfuse)
Week 7:  Integration (MCP + N8N)
Week 8:  Real-World (Study + Build)
Week 9:  Build your own project!
```

---

## 🤝 Contributing

Found an issue or improvement?
1. Check the project's README
2. See if it's documented
3. Try the troubleshooting section
4. Read the code comments
5. Experiment locally

---

## 📞 Support & Resources

### Within This Collection
- Each project has its own README
- Check the parent category README
- Review requirements.txt for dependencies

### Main Resources
- [01_Agentic_AI_Fundamentals.md](../01_Agentic_AI_Fundamentals.md)
- [02_Projects_Overview.md](../02_Projects_Overview.md)
- [03_Alternative_Frameworks_And_Tools.md](../03_Alternative_Frameworks_And_Tools.md)
- [04_Sequential_Learning_Guide.md](../04_Sequential_Learning_Guide.md)
- [05_Quick_Reference.md](../05_Quick_Reference.md)

---

## ✅ Completion Checklist

Track your progress through the projects:

### Framework Basics
- [ ] Set up Agno_Framework
- [ ] Run basic_agent.ipynb
- [ ] Understand the code
- [ ] Modify and experiment
- [ ] Set up CrewAI_Basics
- [ ] Run CrewAI examples
- [ ] Compare frameworks

### RAG & Knowledge
- [ ] Set up LlamaIndex_RAG
- [ ] Understand RAG concept
- [ ] Run example queries
- [ ] Experiment with embeddings

### Specialized Agents
- [ ] Set up one agent (HR, DevOps, or MAF)
- [ ] Understand domain logic
- [ ] Trace through execution
- [ ] Build on it

### Production-Ready
- [ ] Add monitoring (Langfuse/Langsmith)
- [ ] Integrate with tools (MCP/N8N)
- [ ] Study real-world projects
- [ ] Build your own!

---

## 🎓 Next Steps After Completing These Projects

1. **Combine concepts** - Mix patterns from different projects
2. **Build your own** - Create an agent for your domain
3. **Deploy** - Put it in production
4. **Monitor** - Add observability
5. **Share** - Document and share your work
6. **Contribute** - Share improvements back

---

## 📄 License & Attribution

These projects are part of the comprehensive Agentic AI learning resource. See individual project READMEs for specific licenses and attributions.

---

**Happy Learning! 🚀**

Start with [01_Framework_Basics](01_Framework_Basics/README.md) if you're new to agentic AI.

Last Updated: May 18, 2026
