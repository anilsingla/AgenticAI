"""
Central configuration module.
Loads settings from .env and exposes them as typed constants.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - fallback for minimal runtimes
    def load_dotenv(*_args, **_kwargs):
        return False

# Project root is one level up from config/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


# --- OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")

# --- Database ---
SQLITE_DB_PATH = PROJECT_ROOT / os.getenv("SQLITE_DB_PATH", "data/feedback_system.db")

# --- ChromaDB ---
CHROMA_PERSIST_DIR = PROJECT_ROOT / os.getenv("CHROMA_PERSIST_DIR", "data/chroma_db")
CHROMA_COLLECTION_FEEDBACK = os.getenv("CHROMA_COLLECTION_FEEDBACK", "feedback_embeddings")
CHROMA_COLLECTION_TICKETS = os.getenv("CHROMA_COLLECTION_TICKETS", "ticket_embeddings")
CHROMA_COLLECTION_PRODUCT_DOCS = os.getenv("CHROMA_COLLECTION_PRODUCT_DOCS", "product_docs")

# --- Product Documentation ---
PRODUCT_DOCS_DIR = PROJECT_ROOT / os.getenv("PRODUCT_DOCS_DIR", "data/product_docs")

# --- Classification ---
CLASSIFICATION_CONFIDENCE_THRESHOLD = float(
    os.getenv("CLASSIFICATION_CONFIDENCE_THRESHOLD", "0.7")
)
CATEGORIES = ["Bug", "Feature Request", "Praise", "Complaint", "Spam"]
PRIORITIES = ["Critical", "High", "Medium", "Low"]

CRITICAL_RATING_THRESHOLD = int(os.getenv("CRITICAL_RATING_THRESHOLD", "1"))
HIGH_RATING_THRESHOLD = int(os.getenv("HIGH_RATING_THRESHOLD", "2"))
MEDIUM_RATING_THRESHOLD = int(os.getenv("MEDIUM_RATING_THRESHOLD", "3"))

# --- File paths ---
INPUT_REVIEWS_PATH = PROJECT_ROOT / os.getenv("INPUT_REVIEWS_PATH", "data/app_store_reviews.csv")
INPUT_EMAILS_PATH = PROJECT_ROOT / os.getenv("INPUT_EMAILS_PATH", "data/support_emails.csv")
OUTPUT_TICKETS_PATH = PROJECT_ROOT / os.getenv("OUTPUT_TICKETS_PATH", "data/generated_tickets.csv")
OUTPUT_LOG_PATH = PROJECT_ROOT / os.getenv("OUTPUT_LOG_PATH", "data/processing_log.csv")
OUTPUT_METRICS_PATH = PROJECT_ROOT / os.getenv("OUTPUT_METRICS_PATH", "data/metrics.csv")

# --- Human-readable run logs and reports ---
LOGS_DIR = PROJECT_ROOT / os.getenv("LOGS_DIR", "logs")
REPORTS_DIR = PROJECT_ROOT / os.getenv("REPORTS_DIR", "reports")
FLOW_LOG_PATH = LOGS_DIR / os.getenv("FLOW_LOG_FILE", "pipeline_flow.log")
