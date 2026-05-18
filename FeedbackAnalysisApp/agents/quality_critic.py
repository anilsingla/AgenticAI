"""
BE-09: Quality Critic Agent
Reviews generated tickets for completeness and accuracy.
Flags or rewrites low-quality tickets.
"""

import json

from agents.heuristics import review_ticket
from agents.llm import llm_is_configured, run_json_agent
from agents.state import PipelineState
from config.logger import get_logger, log_to_csv

logger = get_logger("quality_critic_agent")

QUALITY_PROMPT = """You are a QA reviewer checking the quality of generated support tickets for SignalDesk.

## Original Feedback
Source ID: {source_id}
Category: {category}
Text: {text}

## Generated Ticket
{ticket_json}

---
Review this ticket for:
1. Title clarity and actionability
2. Description completeness (does it capture the user's issue/request?)
3. Priority correctness
4. Technical details (for bugs: are device, OS, steps included?)
5. Is the category correct?

Respond ONLY with valid JSON:
{{
  "quality_score": <0.0-1.0, where 1.0 is perfect>,
  "issues": ["<issue1>", "<issue2>"],
  "revised_title": "<improved title if score < 0.7, else same title>",
  "revised_description": "<improved description if score < 0.7, else same description>",
  "needs_review": <true if score < 0.7>
}}
"""


def quality_critic_agent(state: PipelineState) -> dict:
    """Review all generated tickets for quality."""
    items = state["feedback_items"]
    errors = list(state.get("errors", []))
    use_llm = llm_is_configured()
    ticket_count = sum(1 for item in items if item.get("ticket", {}).get("title"))
    logger.info(
        "[FLOW] Quality Critic started: %d tickets, mode=%s.",
        ticket_count,
        "AutoGen/OpenAI" if use_llm else "Deterministic fallback",
    )

    for item in items:
        ticket = item.get("ticket")
        if not ticket or not ticket.get("title"):
            continue

        try:
            prompt = QUALITY_PROMPT.format(
                source_id=item["source_id"],
                category=item.get("category", ""),
                text=item["text"],
                ticket_json=json.dumps(ticket, indent=2),
            )
            if use_llm:
                review = run_json_agent(
                    "You are a QA reviewer checking ticket quality. Return valid JSON only.",
                    prompt,
                    agent_name="quality_critic_agent",
                    temperature=0.0,
                )
            else:
                review = review_ticket(item)

            item["quality_score"] = float(review.get("quality_score", 0.0))
            item["quality_notes"] = "; ".join(review.get("issues", []))

            # Apply revisions if quality is low
            if review.get("needs_review", False):
                if review.get("revised_title"):
                    ticket["title"] = review["revised_title"]
                if review.get("revised_description"):
                    ticket["description"] = review["revised_description"]
                item["ticket"] = ticket

            log_to_csv(
                "quality_critic", item["source_id"], "reviewed",
                f"score={item['quality_score']:.2f}, needs_review={review.get('needs_review', False)}",
                item["quality_score"],
            )
            logger.info(
                "%s â†’ quality=%.2f %s",
                item["source_id"], item["quality_score"],
                "(REVISED)" if review.get("needs_review") else "(OK)",
            )

        except Exception as e:
            msg = f"Quality review error for {item['source_id']}: {e}"
            logger.error(msg)
            errors.append(msg)
            item["quality_score"] = 0.0
            item["quality_notes"] = f"Review failed: {e}"

            logger.info("[FLOW] Quality Critic completed: %d tickets reviewed (%d errors).", ticket_count, len(errors))

    return {"feedback_items": items, "errors": errors}

