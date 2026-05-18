# 03_RAG_And_Knowledge

Retrieval-Augmented Generation (RAG) - Enhance agents with external knowledge and context.

---

## 📚 Overview

RAG enables agents to access and reason about external knowledge sources:
- Vector databases and embeddings
- Semantic search
- Document retrieval
- Knowledge base integration
- Context-aware agents

**Level:** Intermediate  
**Prerequisites:** 01_Framework_Basics

---

## 🎯 What You'll Learn

- ✅ How RAG works
- ✅ Vector embeddings
- ✅ Semantic search
- ✅ ChromaDB integration
- ✅ Document chunking
- ✅ Knowledge base design
- ✅ Retrieval strategies

---

## 🏗️ RAG Architecture

```
User Question
    ↓
[Embeddings] (Convert to vector)
    ↓
Vector DB Search (Find similar documents)
    ↓
Retrieve Top-K Documents
    ↓
Augment Prompt (Add context)
    ↓
LLM with Context
    ↓
Better Answer!
```

---

## 📂 Projects in This Category

### LlamaIndex_RAG
**What:** Complete RAG implementation with LlamaIndex  
**Why:** LlamaIndex is the industry standard for RAG  
**Level:** Intermediate  
**Time:** 2-3 hours

**Contains:**
- `basic_agent.py` - Simple RAG setup
- `multi_agent.py` - Multi-agent with RAG
- `rag_agent.py` - Advanced RAG patterns
- Vector storage setup
- Sample data

**Learn:**
- Vector embeddings
- Semantic search
- Document indexing
- RAG best practices

---

## 🚀 Quick Start

### Setup LlamaIndex_RAG

```bash
cd LlamaIndex_RAG

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
# or
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment
cp .env.example .env
# Add OPENAI_API_KEY
```

### Run Examples

```bash
# Basic RAG
python basic_agent.py

# Multi-agent with RAG
python multi_agent.py

# Advanced RAG
python rag_agent.py
```

---

## 🔑 Key Concepts

### Vector Embeddings
Convert text to high-dimensional vectors:
```python
from openai import OpenAI

client = OpenAI()
embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
).data[0].embedding
```

### Semantic Search
Find similar documents:
```python
# Query vector is compared with document vectors
similarity = cosine_similarity(query_embedding, doc_embedding)

# Higher similarity = more relevant
if similarity > 0.8:
    return document
```

### Document Chunking
Split large documents intelligently:
```python
# Large document → many chunks
# Each chunk processed separately
chunks = [doc[i:i+chunk_size] for i in range(0, len(doc), chunk_size)]
```

---

## 🛠️ Common RAG Tasks

### 1. Create Vector Index
```python
from llama_index.core import VectorStoreIndex, Document

documents = [Document(text="..."), ...]
index = VectorStoreIndex.from_documents(documents)
```

### 2. Search Knowledge Base
```python
query_engine = index.as_query_engine()
response = query_engine.query("Your question here")
print(response)
```

### 3. Add to Existing Index
```python
# Load existing index
index = load_index_from_storage(storage_context)

# Add new documents
index.insert(Document(text="New content"))
```

### 4. Hybrid Search
```python
# Combine semantic + keyword search
# Better recall, more relevant results
```

---

## 📊 When to Use RAG

| Situation | Use RAG? |
|-----------|----------|
| Need domain expertise | ✅ Yes |
| Large knowledge base | ✅ Yes |
| Factual accuracy important | ✅ Yes |
| Context-aware responses | ✅ Yes |
| Simple Q&A | ⚠️ Maybe |
| General knowledge only | ❌ No |

---

## 🔗 Integration with Agents

### Without RAG
```
Question → LLM → General answer
           (Limited knowledge)
```

### With RAG
```
Question → Search knowledge base 
        → Augment prompt with context
        → LLM → Specific, accurate answer
```

---

## 📚 RAG Best Practices

1. **Good Document Chunking**
   - Not too small (lose context)
   - Not too large (retrieve irrelevant info)
   - Typically 256-512 tokens

2. **Quality Embeddings**
   - Use latest models (text-embedding-3-small)
   - Consistent model for all documents
   - Re-embed when updating

3. **Relevance Ranking**
   - Retrieve top-K results
   - Re-rank for relevance
   - Filter by similarity threshold

4. **Metadata Tagging**
   - Tag documents with source
   - Include timestamps
   - Add category information

---

## 💡 RAG vs Fine-Tuning

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| Speed | Fast | Slower |
| Cost | Low | High |
| Update knowledge | Easy | Expensive |
| Accuracy | Good | Best |
| Best for | Retrieval | Behavior change |

**Recommendation:** Start with RAG, add fine-tuning if needed

---

## 🎓 Exercises

### Exercise 1: Build Basic RAG
1. Load documents
2. Create vector index
3. Build query engine
4. Test with questions

### Exercise 2: Improve Retrieval
1. Experiment with chunk sizes
2. Try different similarity thresholds
3. Measure retrieval quality

### Exercise 3: Multi-Document Search
1. Create index with many documents
2. Query across all documents
3. Verify relevance

### Exercise 4: Integrate with Agent
1. Create agent
2. Add RAG retrieval as tool
3. Test end-to-end

---

## 📈 Measuring RAG Performance

```python
# Metric 1: Retrieval Quality
correct_docs / total_queries

# Metric 2: Answer Quality
(correct_answers / total_answers)

# Metric 3: Latency
time to retrieve + time to generate

# Metric 4: Cost
(retrieval_calls + generation_calls) * cost_per_call
```

---

## 🔗 Related Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Vector Database Comparison](../../03_Alternative_Frameworks_And_Tools.md) - Vector Databases section
- [01_Agentic_AI_Fundamentals](../../01_Agentic_AI_Fundamentals.md) - Section 5 (RAG)
- [HR_Agent](../04_Specialized_Agents/HR_Agent/) - RAG in practice

---

## ✅ Completion Checklist

- [ ] Set up LlamaIndex_RAG
- [ ] Run basic_agent.py
- [ ] Understand vector embeddings
- [ ] Understand semantic search
- [ ] Run multi_agent.py
- [ ] Run rag_agent.py
- [ ] Complete Exercise 1 (Basic RAG)
- [ ] Complete Exercise 2 (Improve Retrieval)
- [ ] Complete Exercise 3 (Multi-Document)
- [ ] Complete Exercise 4 (Agent Integration)
- [ ] Ready to specialize!

---

## 🚀 Next Steps

After mastering RAG:
1. **Specialized Agents** → 04_Specialized_Agents (HR Agent uses RAG)
2. **Add Monitoring** → 05_Observability_Monitoring
3. **Build Project** → 07_Real_World_Projects

---

**Ready to build specialized agents?** 👉 [04_Specialized_Agents](../04_Specialized_Agents/README.md)

Last Updated: May 18, 2026
