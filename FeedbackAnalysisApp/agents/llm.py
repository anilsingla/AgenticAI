"""
Shared AutoGen/OpenAI helper utilities.
"""

from __future__ import annotations

import asyncio
import json
import re

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from config.settings import LLM_MODEL_NAME, OPENAI_API_KEY


def llm_is_configured() -> bool:
    return bool(OPENAI_API_KEY.strip())


def get_model_client(temperature: float = 0.0) -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
        model=LLM_MODEL_NAME,
        api_key=OPENAI_API_KEY,
        temperature=temperature,
    )


def run_json_agent(system_message: str, prompt: str, *, agent_name: str = "analysis_agent", temperature: float = 0.0) -> dict:
    """Run a single AutoGen assistant and parse its JSON response."""
    if not llm_is_configured():
        raise RuntimeError("OPENAI_API_KEY is not configured")

    async def _run() -> dict:
        model_client = get_model_client(temperature=temperature)
        try:
            agent = AssistantAgent(
                name=agent_name,
                model_client=model_client,
                system_message=system_message,
            )
            result = await agent.run(task=prompt)
            for message in reversed(result.messages):
                if isinstance(message, TextMessage) and message.source == agent_name:
                    return parse_llm_json(message.content)
            raise RuntimeError("AutoGen agent did not return a text response")
        finally:
            await model_client.close()

    return asyncio.run(_run())


def parse_llm_json(text: str) -> dict:
    """Extract and parse JSON from a model response, handling markdown code fences."""
    match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    return json.loads(text)
