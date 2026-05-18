"""
BE-10: AutoGen orchestration
Coordinates the feedback agents, saves outputs, and computes run metrics.
"""

from __future__ import annotations

import csv
import json
import time
import uuid
from datetime import datetime, timezone

import pandas as pd
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.state import PipelineState
from agents.csv_reader import csv_reader_agent
from agents.classifier import classifier_agent
from agents.bug_analyzer import bug_analyzer_agent
from agents.feature_extractor import feature_extractor_agent
from agents.ticket_creator import ticket_creator_agent
from agents.quality_critic import quality_critic_agent
from config.settings import OUTPUT_TICKETS_PATH, OUTPUT_METRICS_PATH, PROJECT_ROOT
from config.logger import get_logger, log_stage_overview
from config.vectorstore import load_product_docs
from config.database import init_db, get_session, Ticket, Metric

logger = get_logger("pipeline")

TICKET_CSV_FIELDS = [
    "source_id", "source_type", "category", "priority", "title",
    "description", "technical_details", "component", "is_duplicate",
    "duplicate_of", "quality_score", "confidence",
]

REPORTS_DIR = PROJECT_ROOT / "reports"


def _stringify(value) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value) if value else ""


def _load_expected_classifications() -> pd.DataFrame:
    expected_path = PROJECT_ROOT / "data" / "expected_classifications.csv"
    if not expected_path.exists():
        return pd.DataFrame()
    return pd.read_csv(expected_path, dtype=str).fillna("")


def _calculate_accuracy(items: list[dict]) -> float:
    expected = _load_expected_classifications()
    if expected.empty:
        return 0.0

    actual = pd.DataFrame([
        {
            "source_id": item.get("source_id", ""),
            "source_type": item.get("source_type", ""),
            "category": item.get("category", ""),
            "priority": item.get("ticket", {}).get("priority", item.get("priority", "")),
        }
        for item in items
    ])
    if actual.empty:
        return 0.0

    merged = expected.merge(actual, on=["source_id", "source_type"], suffixes=("_expected", "_actual"))
    if merged.empty:
        return 0.0

    category_matches = merged["category_expected"] == merged["category_actual"]
    priority_matches = merged["priority_expected"] == merged["priority_actual"]
    score = ((category_matches.astype(float) * 0.75) + (priority_matches.astype(float) * 0.25)).mean()
    return round(float(score), 4)


def _save_outputs(state: PipelineState) -> dict:
    items = state["feedback_items"]
    run_id = state.get("run_id", "unknown")
    start_time = state.get("_start_time", time.time())

    OUTPUT_TICKETS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_TICKETS_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TICKET_CSV_FIELDS)
        writer.writeheader()
        for item in items:
            ticket = item.get("ticket", {})
            if not ticket.get("title"):
                continue
            writer.writerow({
                "source_id": item["source_id"],
                "source_type": item["source_type"],
                "category": item.get("category", ""),
                "priority": ticket.get("priority", item.get("priority", "")),
                "title": ticket.get("title", ""),
                "description": ticket.get("description", ""),
                "technical_details": _stringify(ticket.get("technical_details", "")),
                "component": _stringify(ticket.get("component", "")),
                "is_duplicate": ticket.get("is_duplicate", False),
                "duplicate_of": ticket.get("duplicate_of", ""),
                "quality_score": item.get("quality_score", ""),
                "confidence": item.get("confidence", ""),
            })

    session = get_session()
    try:
        session.query(Ticket).delete()
        for item in items:
            ticket = item.get("ticket", {})
            if not ticket.get("title"):
                continue
            session.add(Ticket(
                source_id=item["source_id"],
                source_type=item["source_type"],
                category=item.get("category", ""),
                priority=ticket.get("priority", item.get("priority", "")),
                title=ticket.get("title", ""),
                description=ticket.get("description", ""),
                technical_details=_stringify(ticket.get("technical_details", "")),
                confidence_score=item.get("confidence", 0.0),
                status="open",
            ))
        session.commit()
    finally:
        session.close()

    categories = [item.get("category", "") for item in items]
    confidences = [item.get("confidence", 0.0) for item in items if item.get("confidence") is not None]
    processing_time = time.time() - start_time
    accuracy = _calculate_accuracy(items)

    metrics = {
        "run_id": run_id,
        "total_processed": len(items),
        "bugs_count": categories.count("Bug"),
        "features_count": categories.count("Feature Request"),
        "praise_count": categories.count("Praise"),
        "complaints_count": categories.count("Complaint"),
        "spam_count": categories.count("Spam"),
        "avg_confidence": round(sum(confidences) / len(confidences), 4) if confidences else 0.0,
        "processing_time_seconds": round(processing_time, 2),
        "accuracy": accuracy,
    }

    OUTPUT_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(metrics.keys())
    write_mode = "a"
    write_header = not OUTPUT_METRICS_PATH.exists()
    if OUTPUT_METRICS_PATH.exists():
        with open(OUTPUT_METRICS_PATH, "r", newline="", encoding="utf-8") as handle:
            header_line = handle.readline().strip()
        existing_header = header_line.split(",") if header_line else []
        if existing_header != fieldnames:
            write_mode = "w"
            write_header = True

    with open(OUTPUT_METRICS_PATH, write_mode, newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(metrics)

    session = get_session()
    try:
        session.add(Metric(**metrics))
        session.commit()
    finally:
        session.close()

    logger.info(
        "Pipeline complete: %d items processed in %.1fs, accuracy=%.2f",
        metrics["total_processed"],
        processing_time,
        accuracy,
    )
    _write_run_reports(state, metrics)
    return {"processed_count": metrics["total_processed"], "accuracy": accuracy}


def _write_run_reports(state: PipelineState, metrics: dict) -> None:
    """Create beginner-friendly run reports in JSON and Markdown formats."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    run_id = metrics.get("run_id", "unknown")
    items = state.get("feedback_items", [])
    duplicates = sum(1 for item in items if item.get("ticket", {}).get("is_duplicate"))
    with_tickets = sum(1 for item in items if item.get("ticket", {}).get("title"))
    generated_at = datetime.now(timezone.utc).isoformat()

    report_payload = {
        "run_id": run_id,
        "generated_at": generated_at,
        "flow_summary": {
            "step_1": "CSV Reader loads app reviews and support emails.",
            "step_2": "Classifier assigns category and confidence.",
            "step_3": "Bug Analyzer enriches bug items with technical details.",
            "step_4": "Feature Extractor enriches feature request items.",
            "step_5": "Ticket Creator builds structured tickets and checks duplicates.",
            "step_6": "Quality Critic scores ticket quality and revises if needed.",
            "step_7": "Outputs are saved to CSV and SQLite with metrics.",
        },
        "metrics": metrics,
        "outputs": {
            "generated_tickets_csv": str(OUTPUT_TICKETS_PATH),
            "processing_log_csv": str(PROJECT_ROOT / "data" / "processing_log.csv"),
            "metrics_csv": str(OUTPUT_METRICS_PATH),
        },
        "counts": {
            "input_feedback_items": len(items),
            "tickets_with_title": with_tickets,
            "duplicate_tickets": duplicates,
        },
        "errors": state.get("errors", []),
    }

    json_path = REPORTS_DIR / f"run_{run_id}.json"
    latest_json_path = REPORTS_DIR / "latest_run_report.json"
    json_text = json.dumps(report_payload, indent=2)
    json_path.write_text(json_text, encoding="utf-8")
    latest_json_path.write_text(json_text, encoding="utf-8")

    md_lines = [
        f"# Run Report: {run_id}",
        "",
        f"Generated at (UTC): {generated_at}",
        "",
        "## Flow Summary",
        "1. CSV Reader loads app reviews and support emails.",
        "2. Classifier assigns category and confidence.",
        "3. Bug Analyzer extracts technical bug details.",
        "4. Feature Extractor derives feature impact/context.",
        "5. Ticket Creator generates structured tickets and duplicate links.",
        "6. Quality Critic reviews ticket quality.",
        "7. Save step writes ticket/log/metrics outputs.",
        "",
        "## Metrics",
        f"- Total processed: {metrics.get('total_processed', 0)}",
        f"- Accuracy: {metrics.get('accuracy', 0.0)}",
        f"- Avg confidence: {metrics.get('avg_confidence', 0.0)}",
        f"- Processing time (s): {metrics.get('processing_time_seconds', 0.0)}",
        f"- Bugs: {metrics.get('bugs_count', 0)}",
        f"- Feature Requests: {metrics.get('features_count', 0)}",
        f"- Praise: {metrics.get('praise_count', 0)}",
        f"- Complaints: {metrics.get('complaints_count', 0)}",
        f"- Spam: {metrics.get('spam_count', 0)}",
        "",
        "## Output Files",
        f"- {OUTPUT_TICKETS_PATH}",
        f"- {PROJECT_ROOT / 'data' / 'processing_log.csv'}",
        f"- {OUTPUT_METRICS_PATH}",
        "",
        "## Notes",
        f"- Ticket rows generated: {with_tickets}",
        f"- Duplicate tickets flagged: {duplicates}",
        f"- Error count: {len(state.get('errors', []))}",
    ]
    md_text = "\n".join(md_lines) + "\n"
    md_path = REPORTS_DIR / f"run_{run_id}.md"
    latest_md_path = REPORTS_DIR / "latest_run_report.md"
    md_path.write_text(md_text, encoding="utf-8")
    latest_md_path.write_text(md_text, encoding="utf-8")


class AutoGenPipelineCoordinator:
    """Thin orchestration wrapper that records AutoGen as the workflow framework."""

    def __init__(self) -> None:
        self.coordinator = None
        try:
            self.coordinator = AssistantAgent(
                name="pipeline_coordinator",
                model_client=OpenAIChatCompletionClient(model="gpt-4o-mini", api_key="placeholder"),
                system_message="Coordinate the execution order of the feedback processing agents.",
            )
        except Exception:
            self.coordinator = None

    def run(self, state: PipelineState) -> PipelineState:
        log_stage_overview(logger, "CSV Reader", "Load CSV files and normalize feedback into one schema.")
        state = {**state, **csv_reader_agent(state)}

        log_stage_overview(logger, "Classifier", "Classify each item into Bug/Feature/Praise/Complaint/Spam.")
        state = {**state, **classifier_agent(state)}

        log_stage_overview(logger, "Bug Analyzer", "Enrich only Bug items with technical details and severity.")
        state = {**state, **bug_analyzer_agent(state)}

        log_stage_overview(logger, "Feature Extractor", "Enrich only Feature Request items with impact/context.")
        state = {**state, **feature_extractor_agent(state)}

        log_stage_overview(logger, "Ticket Creator", "Generate structured tickets and detect duplicates.")
        state = {**state, **ticket_creator_agent(state)}

        log_stage_overview(logger, "Quality Critic", "Score ticket quality and revise low-quality entries.")
        state = {**state, **quality_critic_agent(state)}

        log_stage_overview(logger, "Save Outputs", "Write tickets, logs, metrics, and run reports.")
        state = {**state, **_save_outputs(state)}
        return state


def build_pipeline() -> AutoGenPipelineCoordinator:
    return AutoGenPipelineCoordinator()


def run_pipeline() -> dict:
    init_db()
    doc_count = load_product_docs()
    logger.info("Loaded %d product doc chunks into RAG", doc_count)

    pipeline = build_pipeline()
    run_id = str(uuid.uuid4())[:8]
    initial_state = PipelineState(
        feedback_items=[],
        current_index=0,
        processed_count=0,
        errors=[],
        run_id=run_id,
    )
    initial_state["_start_time"] = time.time()
    return pipeline.run(initial_state)


if __name__ == "__main__":
    run_pipeline()
