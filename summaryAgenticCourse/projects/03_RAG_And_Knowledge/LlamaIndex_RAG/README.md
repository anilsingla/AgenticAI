# LlamaIndex Demos

## New User Start Here`r`n`r`n1. Open `deployment/README.md` for the environment-specific run commands.`r`n2. For local execution, use one of:`r`n   - Windows: `./deployment/windows-local/run_demo.ps1``r`n   - Linux/macOS: `./deployment/linux-local/run_demo.sh``r`n3. Review project conventions in `docs/CODING_STANDARDS.md`.`r`n4. Check outputs after running:`r`n   - Logs: `logs/``r`n   - Reports: `reports/``r`n

Three small demos showing the core agent patterns in LlamaIndex:

| Demo | File | What it shows |
|---|---|---|
| Basic agent | `basic_agent.py` | Single `FunctionAgent` with two function tools |
| Multi-agent | `multi_agent.py` | `AgentWorkflow` with handoff between Researcher and Writer |
| Agent with RAG | `rag_agent.py` | `FunctionAgent` with a `QueryEngineTool` over a local vector index |

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Uses `OPENAI_API_KEY` from the repo-root `.env` (loaded via `load_dotenv("../.env")`).

## Run

```bash
python basic_agent.py     # tool-using single agent
python multi_agent.py     # researcher → writer handoff
python rag_agent.py       # answers questions using docs in ./data
```

The RAG demo builds a vector index from `data/*.txt` on first run and persists it under `./storage/`. Delete that folder to rebuild from scratch (e.g. after editing the docs).

## Notes

- All agents are async — use `asyncio.run(main())` to invoke
- `FunctionAgent` is the OpenAI-style tool-calling agent; switch to `ReActAgent` if you want explicit reasoning traces
- In the multi-agent demo, `can_handoff_to=[...]` controls who each agent can pass control to; the orchestrator (`AgentWorkflow`) handles the routing
- The RAG demo uses `text-embedding-3-small` for embeddings; change in `Settings.embed_model` to swap models

## Prerequisites And Requirements

- Python 3.10+ recommended
- OpenAI API key in `.env`
- Basic understanding of RAG terms: embeddings, chunks, retriever, index
- Sufficient local disk for persisted vector index (`./storage`)

## Files Explained (Beginner View)

- `basic_agent.py`: Single tool-calling agent with two simple tools
- `multi_agent.py`: Multi-agent handoff flow using `AgentWorkflow`
- `rag_agent.py`: Builds/loads vector index, exposes retrieval as a tool, then answers with grounded context
- `data/`: Source documents used to build the RAG index
- `storage/`: Persisted index data (auto-created on first RAG run)
- `requirements.txt`: Required dependencies

## API/Tool Cost Notes (Approx, verify before usage)

- OpenAI `gpt-4o-mini`: pay-per-token for generation
- OpenAI `text-embedding-3-small`: pay-per-token for embeddings during indexing/querying
- Local vector storage (`storage/`): no managed DB fee in this demo


