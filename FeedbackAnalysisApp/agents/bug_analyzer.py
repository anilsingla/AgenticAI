"""
BE-06: Bug Analysis Agent
For items classified as Bug: extracts technical details and uses RAG
to search product documentation for known bugs and architecture context.
Uses AutoGen/OpenAI when configured and deterministic fallback otherwise.
"""

from agents.heuristics import analyze_bug_item
from agents.llm import llm_is_configured, run_json_agent
from agents.state import PipelineState
from config.logger import get_logger, log_to_csv
from config.vectorstore import get_product_docs_collection, query_similar

logger = get_logger("bug_analyzer_agent")

BUG_ANALYSIS_PROMPT = """You are a senior QA engineer analysing a bug report for SignalDesk, a productivity app.

## Product Context (from internal documentation)
{product_context}

## Bug Report
Source: {source_type} | Platform: {platform} | Rating: {rating} | App Version: {app_version}
Subject: {subject}
Text:
{text}

---
Extract structured bug details. If information is not available, use "unknown".
Respond ONLY with valid JSON:
{{
  "steps_to_reproduce": "<numbered steps or 'not provided'>",
  "device": "<device model>",
  "os": "<OS and version>",
  "app_version": "<version>",
  "severity": "<Critical|High|Medium|Low>",
  "component": "<affected component e.g. Authentication, Sync, Dashboard, Notifications, Search, Attachments, Settings>",
  "known_bug_match": "<BUG-ID if matches a known bug, else 'none'>",
  "root_cause_hint": "<possible root cause based on product docs, or 'unknown'>"
}}
"""


def bug_analyzer_agent(state: PipelineState) -> dict:
    """Analyse Bug items using product docs RAG."""
    items = state["feedback_items"]
    errors = list(state.get("errors", []))
    product_docs_col = get_product_docs_collection()
    use_llm = llm_is_configured()
    bug_count = sum(1 for item in items if item.get("category") == "Bug")
    logger.info(
        "[FLOW] Bug Analyzer started: %d bug items, mode=%s.",
        bug_count,
        "AutoGen/OpenAI" if use_llm else "Deterministic fallback",
    )

    for item in items:
        if item.get("category") != "Bug":
            continue

        try:
            # RAG: retrieve relevant product documentation
            rag_results = query_similar(product_docs_col, item["text"], n_results=3)
            product_context = "\n---\n".join(rag_results["documents"][0]) if rag_results["documents"][0] else "No product documentation available."

            if use_llm:
                prompt = BUG_ANALYSIS_PROMPT.format(
                    product_context=product_context,
                    source_type=item["source_type"],
                    platform=item.get("platform", ""),
                    rating=item.get("rating", "N/A"),
                    app_version=item.get("app_version", ""),
                    subject=item.get("subject", ""),
                    text=item["text"],
                )
                bug_details = run_json_agent(
                    "You are a senior QA engineer. Return valid JSON only.",
                    prompt,
                    agent_name="bug_analyzer_agent",
                    temperature=0.0,
                )
            else:
                bug_details = analyze_bug_item(item, product_context)
            item["bug_details"] = bug_details

            # Use severity from LLM analysis as priority
            severity = bug_details.get("severity", "Medium")
            item["priority"] = severity

            log_to_csv(
                "bug_analyzer", item["source_id"], "analyzed",
                f"severity={severity}, component={bug_details.get('component', '?')}, known_bug={bug_details.get('known_bug_match', 'none')}",
                item.get("confidence", 0.0),
            )
            logger.info(
                "%s â†’ severity=%s, component=%s, known_bug=%s",
                item["source_id"], severity,
                bug_details.get("component", "?"),
                bug_details.get("known_bug_match", "none"),
            )

        except Exception as e:
            msg = f"Bug analysis error for {item['source_id']}: {e}"
            logger.error(msg)
            errors.append(msg)
            item["bug_details"] = {}
            item["priority"] = "Medium"

            logger.info("[FLOW] Bug Analyzer completed: %d bug items processed (%d errors).", bug_count, len(errors))

    return {"feedback_items": items, "errors": errors}

