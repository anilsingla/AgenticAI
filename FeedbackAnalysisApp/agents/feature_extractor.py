"""
BE-07: Feature Extractor Agent
For Feature Request items: extracts feature details and uses RAG to
check product roadmap and existing features for context.
Uses AutoGen/OpenAI when configured and deterministic fallback otherwise.
"""

from agents.heuristics import extract_feature_request
from agents.llm import llm_is_configured, run_json_agent
from agents.state import PipelineState
from config.logger import get_logger, log_to_csv
from config.vectorstore import get_product_docs_collection, query_similar

logger = get_logger("feature_extractor_agent")

FEATURE_PROMPT = """You are a product analyst evaluating a feature request for SignalDesk, a productivity app.

## Product Context (from internal documentation - features, roadmap, known limitations)
{product_context}

## Feature Request
Source: {source_type} | Platform: {platform} | Rating: {rating}
Subject: {subject}
Text:
{text}

---
Extract structured feature request details.
Respond ONLY with valid JSON:
{{
  "feature_summary": "<one-line summary of the requested feature>",
  "user_benefit": "<how this helps the user>",
  "impact_score": <1-10 integer, 10 = highest impact>,
  "user_segment": "<who benefits: all_users | power_users | teams | accessibility>",
  "already_planned": "<true if on roadmap, false otherwise>",
  "planned_version": "<version from roadmap if planned, else 'none'>",
  "existing_workaround": "<workaround if any, else 'none'>",
  "priority_suggestion": "<Critical|High|Medium|Low>"
}}
"""


def feature_extractor_agent(state: PipelineState) -> dict:
    """Analyse Feature Request items using product docs RAG."""
    items = state["feedback_items"]
    errors = list(state.get("errors", []))
    product_docs_col = get_product_docs_collection()
    use_llm = llm_is_configured()
    feature_count = sum(1 for item in items if item.get("category") == "Feature Request")
    logger.info(
        "[FLOW] Feature Extractor started: %d feature items, mode=%s.",
        feature_count,
        "AutoGen/OpenAI" if use_llm else "Deterministic fallback",
    )

    for item in items:
        if item.get("category") != "Feature Request":
            continue

        try:
            # RAG: retrieve relevant product docs (features, roadmap)
            query = f"{item.get('subject', '')} {item['text']}"
            rag_results = query_similar(product_docs_col, query, n_results=3)
            product_context = "\n---\n".join(rag_results["documents"][0]) if rag_results["documents"][0] else "No product documentation available."

            if use_llm:
                prompt = FEATURE_PROMPT.format(
                    product_context=product_context,
                    source_type=item["source_type"],
                    platform=item.get("platform", ""),
                    rating=item.get("rating", "N/A"),
                    subject=item.get("subject", ""),
                    text=item["text"],
                )
                feature_details = run_json_agent(
                    "You are a product analyst. Return valid JSON only.",
                    prompt,
                    agent_name="feature_extractor_agent",
                    temperature=0.0,
                )
            else:
                feature_details = extract_feature_request(item, product_context)
            item["feature_details"] = feature_details
            item["priority"] = feature_details.get("priority_suggestion", "Medium")

            log_to_csv(
                "feature_extractor", item["source_id"], "analyzed",
                f"feature={feature_details.get('feature_summary', '?')}, impact={feature_details.get('impact_score', '?')}, planned={feature_details.get('already_planned', '?')}",
                item.get("confidence", 0.0),
            )
            logger.info(
                "%s â†’ %s (impact=%s, planned=%s)",
                item["source_id"],
                feature_details.get("feature_summary", "?"),
                feature_details.get("impact_score", "?"),
                feature_details.get("already_planned", "?"),
            )

        except Exception as e:
            msg = f"Feature extraction error for {item['source_id']}: {e}"
            logger.error(msg)
            errors.append(msg)
            item["feature_details"] = {}
            item["priority"] = "Medium"

    logger.info(
        "[FLOW] Feature Extractor completed: %d feature items processed (%d errors).",
        feature_count,
        len(errors),
    )

    return {"feedback_items": items, "errors": errors}

