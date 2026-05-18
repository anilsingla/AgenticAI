"""
BE-05: Feedback Classifier Agent
Classifies each feedback item into Bug / Feature Request / Praise /
Complaint / Spam with a confidence score using AutoGen/OpenAI.
Falls back to deterministic heuristics when the LLM is unavailable.
"""

from agents.heuristics import classify_feedback_item
from agents.llm import llm_is_configured, run_json_agent
from agents.state import PipelineState
from config.logger import get_logger, log_to_csv
from config.settings import CATEGORIES

logger = get_logger("classifier_agent")

CLASSIFIER_PROMPT = """You are a feedback classifier for a productivity app called SignalDesk.

Classify the following user feedback into exactly ONE of these categories:
{categories}

Also assign a confidence score between 0.0 and 1.0.

Respond ONLY with valid JSON:
{{"category": "<category>", "confidence": <float>}}

---
Source type: {source_type}
Platform: {platform}
Rating: {rating}
Subject: {subject}
Feedback text:
{text}
"""


def classifier_agent(state: PipelineState) -> dict:
    """Classify every feedback item in state."""
    items = state["feedback_items"]
    errors = list(state.get("errors", []))
    use_llm = llm_is_configured()
    logger.info(
        "[FLOW] Classifier started: %d items, mode=%s.",
        len(items),
        "AutoGen/OpenAI" if use_llm else "Deterministic fallback",
    )

    for item in items:
        try:
            if use_llm:
                prompt = CLASSIFIER_PROMPT.format(
                    categories=", ".join(CATEGORIES),
                    source_type=item["source_type"],
                    platform=item.get("platform", ""),
                    rating=item.get("rating", "N/A"),
                    subject=item.get("subject", ""),
                    text=item["text"],
                )
                result = run_json_agent(
                    "You are a careful feedback classifier. Return valid JSON only.",
                    prompt,
                    agent_name="classifier_agent",
                    temperature=0.0,
                )
            else:
                result = classify_feedback_item(item)

            category = result["category"]
            if category not in CATEGORIES:
                category = "Complaint"  # fallback

            item["category"] = category
            item["confidence"] = float(result["confidence"])

            log_to_csv(
                "classifier", item["source_id"], "classified",
                f"category={category}", item["confidence"],
            )
            logger.info("%s â†’ %s (%.2f)", item["source_id"], category, item["confidence"])

        except Exception as e:
            msg = f"Classification error for {item['source_id']}: {e}"
            logger.error(msg)
            errors.append(msg)
            item["category"] = "Complaint"
            item["confidence"] = 0.0

            logger.info("[FLOW] Classifier completed: %d items classified (%d errors).", len(items), len(errors))

    return {"feedback_items": items, "errors": errors}

