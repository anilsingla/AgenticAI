# Agno_Project - Multi-Agent Finance And Support Demo

This project demonstrates practical Agno usage with single-agent memory, multi-agent teamwork, and a refund-support bot workflow.

## Prerequisites And Requirements

- Python 3.10+
- API keys in `.env`:
  - `GOOGLE_API_KEY` (for Gemini models)
  - `TELEGRAM_BOT_TOKEN` (for refund bot in `refund_agent.py`)
- Internet access for market tools (`YFinanceTools`, `DuckDuckGoTools`)
- Basic understanding of agents, tools, and chat sessions

## Project Files Explained (Beginner View)

- `agent.py`:
  - Single Agno agent with stock market tool usage
  - Demonstrates session-specific memory using SQLite
- `agent_team.py`:
  - Two specialized agents (web + finance) combined in one team
  - Demonstrates collaborative answers from multiple agents
- `refund_agent.py`:
  - Telegram-integrated support workflow
  - Uses tool calls for order lookup + refund request routing
  - Adds human approval loop using Telegram inline buttons
- `memory.db`:
  - SQLite memory backend used by Agno sessions
- `Agno Basic.md`:
  - Supporting notes/documentation
- `requirements.txt`:
  - Python dependency list

## Setup

```bash
cd Agno_Project
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt
```

Create `.env` in this folder:

```env
GOOGLE_API_KEY=your-google-ai-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

## Run

```bash
# Single memory-aware finance agent
python agent.py

# Team-based web + finance response
python agent_team.py

# Telegram refund support bot (requires TELEGRAM_BOT_TOKEN)
python refund_agent.py
```

## API/Tool Cost Notes (Approx, verify before usage)

- Google Gemini (`gemini-2.5-pro`, `gemini-2.5-flash`): pay-per-token pricing based on model tier
- Yahoo Finance tool (`YFinanceTools`): generally no direct API subscription in this demo path
- DuckDuckGo search tool: no direct tool fee in this demo path (subject to provider behavior/limits)
- Telegram Bot API: typically free for bot messaging usage

## Beginner Notes

- Start with `agent.py` first to understand basic tool calling + memory.
- Then run `agent_team.py` to see specialization across agents.
- Run `refund_agent.py` last because it adds external platform integration (Telegram callbacks).
- If responses fail, first verify `.env` keys and internet connectivity.
