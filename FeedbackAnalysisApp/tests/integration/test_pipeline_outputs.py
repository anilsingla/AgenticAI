from pathlib import Path
import sys
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.pipeline import run_pipeline
from config.settings import OUTPUT_METRICS_PATH, OUTPUT_TICKETS_PATH, OUTPUT_LOG_PATH


def test_pipeline_generates_required_output_files(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = run_pipeline()

    assert result["processed_count"] == 50
    assert OUTPUT_TICKETS_PATH.exists()
    assert OUTPUT_METRICS_PATH.exists()
    assert OUTPUT_LOG_PATH.exists()

    with open(OUTPUT_TICKETS_PATH, newline="", encoding="utf-8") as handle:
        ticket_rows = list(csv.DictReader(handle))
    with open(OUTPUT_METRICS_PATH, newline="", encoding="utf-8") as handle:
        metric_rows = list(csv.DictReader(handle))
    with open(OUTPUT_LOG_PATH, newline="", encoding="utf-8") as handle:
        log_rows = list(csv.DictReader(handle))

    assert ticket_rows, "generated_tickets.csv should have at least one row"
    assert metric_rows, "metrics.csv should have at least one row"
    assert log_rows, "processing_log.csv should have at least one row"

    assert set(["source_id", "category", "priority", "title"]).issubset(ticket_rows[0].keys())
    assert {"run_id", "total_processed", "accuracy"}.issubset(metric_rows[0].keys())
    assert {"timestamp", "agent_name", "source_id", "action"}.issubset(log_rows[0].keys())
    assert float(metric_rows[-1]["accuracy"]) >= 0.80
