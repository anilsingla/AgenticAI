"""
Deterministic fallback logic used when the LLM is unavailable.
These helpers keep the app runnable for demos and tests.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Iterable

from config.settings import PRIORITIES

BUG_KEYWORDS = [
    "crash", "crashes", "crashing", "freeze", "frozen", "stuck", "bug",
    "not working", "doesn't work", "doesnt work", "can't", "cannot", "unable",
    "login", "log in", "authentication", "auth", "sync", "data loss", "lost",
    "logged out", "logout", "notification", "notifications", "search",
    "error", "failed", "failure", "slow load", "slow", "startup", "voiceover",
    "accessibility", "badge count", "attach", "attachment", "upload",
]
FEATURE_KEYWORDS = [
    "feature request", "please add", "would love", "i wish", "could you add",
    "missing functionality", "suggestion", "integration", "dark mode",
    "offline mode", "pdf export", "subtask", "subtasks", "sorting",
    "filtering", "templates", "template", "calendar", "slack", "siri",
    "export", "recurring", "improvement",
]
PRAISE_KEYWORDS = [
    "love", "amazing", "great", "awesome", "perfect", "works perfectly",
    "fantastic", "excellent", "best", "thank you", "helpful", "brilliant",
]
COMPLAINT_KEYWORDS = [
    "too expensive", "expensive", "poor customer service", "customer service",
    "support response", "response time", "no response", "frustrating", "disappointed",
    "bad service", "poor accessibility",
]
SPAM_KEYWORDS = [
    "buy now", "subscribe", "promo", "promotion", "discount", "click here",
    "visit my channel", "http://", "https://", "www.", "telegram", "crypto",
    "casino", "loan", "follow me", "free followers",
]
DEVICE_PATTERNS = [
    r"pixel\s?\d+",
    r"iphone\s?[\w\d\s\+]+",
    r"ipad\s?[\w\d\s]+",
    r"samsung galaxy\s?[\w\d\s]+",
    r"oneplus\s?\d+",
]
OS_PATTERNS = [
    r"android\s?\d+(?:\.\d+)?",
    r"ios\s?\d+(?:\.\d+)?",
    r"ipados\s?\d+(?:\.\d+)?",
]
APP_VERSION_PATTERN = r"(?:app|version|v)\s*[:]?\s*(\d+\.\d+\.\d+)"


def _text_blob(item: dict) -> str:
    return f"{item.get('subject', '')} {item.get('text', '')}".strip()


def _contains_any(text: str, phrases: Iterable[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def _extract_first(text: str, patterns: Iterable[str], default: str = "unknown") -> str:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return default


def _extract_version(text: str, item: dict) -> str:
    match = re.search(APP_VERSION_PATTERN, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return item.get("app_version", "unknown") or "unknown"


def infer_priority_from_text(item: dict, category: str) -> str:
    text = _text_blob(item).lower()
    rating = int(item.get("rating", 0) or 0)

    if category == "Bug":
        if any(keyword in text for keyword in ["startup", "crash", "data loss", "lost", "can't login", "cannot login", "authentication"]):
            return "Critical" if any(keyword in text for keyword in ["startup", "data loss", "lost", "crash"]) or rating <= 1 else "High"
        if any(keyword in text for keyword in ["sync", "notification", "search", "freeze", "dashboard", "attachment", "voiceover"]):
            return "High" if rating <= 2 else "Medium"
        return "Medium"

    if category == "Feature Request":
        if any(keyword in text for keyword in ["accessibility", "offline mode", "calendar", "dark mode", "slack"]):
            return "Medium"
        return "Low" if rating >= 4 else "Medium"

    if category == "Complaint":
        if any(keyword in text for keyword in ["no response", "2 weeks", "poor accessibility"]):
            return "High"
        return "Medium" if rating and rating <= 2 else "Low"

    return "Low"


def classify_feedback_item(item: dict) -> dict:
    text = _text_blob(item).lower()
    rating = int(item.get("rating", 0) or 0)

    if _contains_any(text, SPAM_KEYWORDS) or re.fullmatch(r"[a-z0-9]{2,6}(\s+[a-z0-9]{2,6})*", text) is not None:
        return {"category": "Spam", "confidence": 0.99}

    if any(keyword in text for keyword in ["data loss", "lost all", "logged me out", "crash", "authentication failed", "can't login", "cannot log"]):
        if "offline mode" not in text or any(keyword in text for keyword in ["gone", "lost", "urgent", "logged me out"]):
            return {"category": "Bug", "confidence": 0.94}

    if _contains_any(text, FEATURE_KEYWORDS):
        return {"category": "Feature Request", "confidence": 0.93}

    if _contains_any(text, BUG_KEYWORDS):
        if "too expensive" not in text and "customer service" not in text:
            return {"category": "Bug", "confidence": 0.91}

    if _contains_any(text, PRAISE_KEYWORDS) and rating >= 4:
        return {"category": "Praise", "confidence": 0.95}

    if _contains_any(text, COMPLAINT_KEYWORDS) or (rating and rating <= 2):
        if "voiceover" in text and any(token in text for token in ["button", "dropdown", "heading", "unlabelled"]):
            return {"category": "Bug", "confidence": 0.86}
        return {"category": "Complaint", "confidence": 0.82}

    if rating >= 4:
        return {"category": "Praise", "confidence": 0.72}

    return {"category": "Complaint", "confidence": 0.6}


def analyze_bug_item(item: dict, product_context: str = "") -> dict:
    text = _text_blob(item)
    lower = text.lower()

    component = "General"
    if "login" in lower or "authentication" in lower:
        component = "Authentication"
    elif "sync" in lower:
        component = "Sync"
    elif "settings" in lower:
        component = "Settings"
    elif "dashboard" in lower:
        component = "Dashboard"
    elif "notification" in lower or "badge" in lower:
        component = "Notifications"
    elif "search" in lower:
        component = "Search"
    elif "attach" in lower or "file" in lower:
        component = "Attachments"
    elif "voiceover" in lower or "accessibility" in lower:
        component = "Accessibility"
    elif "startup" in lower:
        component = "Startup"

    severity = infer_priority_from_text(item, "Bug")
    known_bug_match = "none"
    product_lower = product_context.lower()
    if "bug-" in product_lower:
        if component.lower() in product_lower or any(token in product_lower for token in ["settings", "sync", "search", "notification", "startup", "authentication"]):
            match = re.search(r"bug-\d+", product_lower)
            if match:
                known_bug_match = match.group(0).upper()

    steps = "not provided"
    if any(keyword in lower for keyword in ["when i", "after", "steps", "repro"]):
        steps = text.strip()
    elif "settings" in lower and "crash" in lower:
        steps = "1. Open the app. 2. Navigate to Settings. 3. Open the affected sub-page. 4. Observe the crash."
    elif "startup" in lower and "crash" in lower:
        steps = "1. Launch the app after updating. 2. Observe the startup crash before the home screen loads."
    elif "login" in lower:
        steps = "1. Open the login screen. 2. Enter credentials. 3. Submit the form. 4. Observe the authentication failure."

    return {
        "steps_to_reproduce": steps,
        "device": _extract_first(lower, DEVICE_PATTERNS),
        "os": _extract_first(lower, OS_PATTERNS),
        "app_version": _extract_version(lower, item),
        "severity": severity,
        "component": component,
        "known_bug_match": known_bug_match,
        "root_cause_hint": _guess_root_cause(component, lower, product_lower),
    }


def _guess_root_cause(component: str, lower: str, product_lower: str) -> str:
    if component == "Authentication":
        return "Recent auth token validation changes may be rejecting valid sessions."
    if component == "Sync":
        return "Background sync queue or conflict resolution may be failing."
    if component == "Dashboard":
        return "Dashboard query or rendering path may be regressing with larger datasets."
    if component == "Notifications":
        return "Notification registration or badge count refresh may be out of sync."
    if component == "Accessibility":
        return "UI components appear to be missing accessibility labels and semantic grouping."
    if "known bug" in product_lower:
        return "Potentially related to a documented known issue in the product docs."
    return "unknown"


def extract_feature_request(item: dict, product_context: str = "") -> dict:
    text = _text_blob(item)
    lower = text.lower()

    feature_summary = "Requested feature improvement"
    if "dark mode" in lower:
        feature_summary = "Add dark mode support"
    elif "calendar" in lower:
        feature_summary = "Add calendar integration"
    elif "offline mode" in lower:
        feature_summary = "Add offline mode"
    elif "slack" in lower:
        feature_summary = "Add Slack integration"
    elif "pdf export" in lower or "export" in lower:
        feature_summary = "Add PDF export"
    elif "subtask" in lower:
        feature_summary = "Add subtask support"
    elif "sorting" in lower or "filter" in lower:
        feature_summary = "Add advanced sorting and filtering"
    elif "template" in lower:
        feature_summary = "Add recurring task templates"
    elif "siri" in lower:
        feature_summary = "Add Siri shortcuts integration"

    user_segment = "all_users"
    if any(keyword in lower for keyword in ["team", "collaboration", "slack"]):
        user_segment = "teams"
    elif any(keyword in lower for keyword in ["accessibility", "voiceover"]):
        user_segment = "accessibility"
    elif any(keyword in lower for keyword in ["advanced", "sorting", "template", "export"]):
        user_segment = "power_users"

    impact_score = 6
    if any(keyword in lower for keyword in ["dark mode", "offline mode", "calendar", "subtask"]):
        impact_score = 7
    if any(keyword in lower for keyword in ["accessibility", "all users", "daily"]):
        impact_score = 8

    product_lower = product_context.lower()
    planned = any(token in product_lower for token in ["planned", "roadmap", "target", "q3", "q4"])
    planned_version = "none"
    version_match = re.search(r"\b\d+\.\d+(?:\.\d+)?\b", product_context)
    if planned and version_match:
        planned_version = version_match.group(0)

    return {
        "feature_summary": feature_summary,
        "user_benefit": _feature_benefit(feature_summary),
        "impact_score": impact_score,
        "user_segment": user_segment,
        "already_planned": str(planned).lower(),
        "planned_version": planned_version,
        "existing_workaround": "none",
        "priority_suggestion": infer_priority_from_text(item, "Feature Request"),
    }


def _feature_benefit(feature_summary: str) -> str:
    if "dark mode" in feature_summary.lower():
        return "Improves usability in low-light settings and reduces eye strain."
    if "calendar" in feature_summary.lower():
        return "Helps users manage tasks alongside existing schedules."
    if "offline mode" in feature_summary.lower():
        return "Allows uninterrupted productivity without connectivity."
    if "slack" in feature_summary.lower():
        return "Improves team coordination and task visibility."
    return "Improves user productivity and reduces workflow friction."


def issue_signature(item: dict) -> str:
    text = _text_blob(item).lower()
    if "dark mode" in text:
        return "feature_dark_mode"
    if "calendar" in text:
        return "feature_calendar"
    if "sync" in text:
        return "bug_sync"
    if "startup" in text and "crash" in text:
        return "bug_startup_crash"
    if "settings" in text and "crash" in text:
        return "bug_settings_crash"
    if "login" in text or "authentication" in text:
        return "bug_login"
    if "dashboard" in text and any(token in text for token in ["slow", "load"]):
        return "bug_dashboard_perf"
    if "notification" in text:
        return "bug_notifications"
    if "attach" in text or "file" in text:
        return "bug_attachments"
    if "search" in text:
        return "bug_search"
    if "badge" in text:
        return "bug_badge_count"
    if "voiceover" in text or "accessibility" in text:
        return "accessibility_voiceover"
    if "expensive" in text or "pricing" in text:
        return "complaint_pricing"
    if "customer service" in text or "response" in text:
        return "complaint_support"
    if "subtask" in text:
        return "feature_subtasks"
    if "sorting" in text or "filter" in text:
        return "feature_sorting"
    if "pdf export" in text or "export" in text:
        return "feature_pdf_export"
    tokens = re.findall(r"[a-z]{4,}", text)
    common = [token for token, _ in Counter(tokens).most_common(4)]
    return "_".join(common) if common else item.get("source_id", "unknown")


def build_ticket(item: dict, similar_ids: list[str] | None = None) -> dict:
    similar_ids = similar_ids or []
    category = item.get("category", "Complaint")
    priority = item.get("priority") or infer_priority_from_text(item, category)
    title = build_ticket_title(item)
    description = build_ticket_description(item)
    technical_details = build_technical_details(item)
    duplicate_of = similar_ids[0] if similar_ids else None

    return {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority if priority in PRIORITIES else "Medium",
        "technical_details": technical_details,
        "component": _ticket_component(item),
        "is_duplicate": bool(duplicate_of),
        "duplicate_of": duplicate_of,
    }


def build_ticket_title(item: dict) -> str:
    text = _text_blob(item).lower()
    category = item.get("category", "Complaint")

    if category == "Feature Request":
        if "dark mode" in text:
            return "Feature Request: Dark Mode Support"
        if "calendar" in text:
            return "Feature Request: Calendar Integration"
        if "offline mode" in text:
            return "Feature Request: Offline Mode"
        if "slack" in text:
            return "Feature Request: Slack Integration"
        if "pdf export" in text or "export" in text:
            return "Feature Request: PDF Export"
        if "subtask" in text:
            return "Feature Request: Subtask Support"
        if "sorting" in text or "filter" in text:
            return "Feature Request: Advanced Sorting Options"
        if "template" in text:
            return "Feature Request: Recurring Task Templates"
        return "Feature Request: Product Improvement"

    if category == "Complaint":
        if "expensive" in text or "pricing" in text:
            return "Complaint: Pricing Too Expensive"
        if "customer service" in text or "response" in text:
            return "Complaint: Poor Customer Support Response Time"
        if "accessibility" in text:
            return "Complaint: Accessibility Support Needs Improvement"
        return "Complaint: User Experience Issue"

    if "settings" in text and "crash" in text:
        return "App Crash on Settings Page"
    if "startup" in text and "crash" in text:
        return "App Crash on Startup After Update"
    if "login" in text or "authentication" in text:
        return "Login Authentication Failure After Update"
    if "sync" in text:
        return "Data Sync Broken Between Devices"
    if "dashboard" in text and any(token in text for token in ["slow", "load"]):
        return "Dashboard Performance Degradation"
    if "push" in text or "notification" in text:
        return "Push Notifications Completely Non-Functional"
    if "attach" in text or "file" in text:
        return "App Freeze or Crash on Large File Attachment"
    if "search" in text:
        return "Search Function Returning Incorrect Results"
    if "voiceover" in text or "accessibility" in text:
        return "Accessibility Issues - VoiceOver Support"
    if "badge" in text:
        return "Notification Badge Count Mismatch"
    return f"{category}: Feedback Review Needed"


def build_ticket_description(item: dict) -> str:
    base = item.get("text", "")
    category = item.get("category", "Complaint")
    source = item.get("source_type", "feedback")
    impact = "User-reported issue needs triage."
    if category == "Bug":
        impact = "This affects core app functionality and should be investigated by engineering."
    elif category == "Feature Request":
        impact = "This request should be evaluated for roadmap fit and user demand."
    elif category == "Complaint":
        impact = "This complaint should be reviewed for customer experience follow-up."
    return f"Source: {source}. Original feedback: {base} {impact}".strip()


def build_technical_details(item: dict) -> str:
    if item.get("bug_details"):
        return json.dumps(item["bug_details"])
    if item.get("feature_details"):
        return json.dumps(item["feature_details"])
    return item.get("technical_details", "N/A") or "N/A"


def _ticket_component(item: dict) -> str:
    if item.get("bug_details"):
        return item["bug_details"].get("component", "General")
    if item.get("feature_details"):
        return item["feature_details"].get("feature_summary", "Product")
    return "Customer Experience"


def review_ticket(item: dict) -> dict:
    ticket = item.get("ticket", {})
    score = 0.45
    issues = []

    if ticket.get("title"):
        score += 0.15
    else:
        issues.append("Missing ticket title")

    if ticket.get("description") and len(ticket["description"]) > 30:
        score += 0.15
    else:
        issues.append("Description is too short")

    if ticket.get("priority") in PRIORITIES:
        score += 0.1
    else:
        issues.append("Priority is missing or invalid")

    if item.get("category") == "Bug" and ticket.get("technical_details") not in ["", "N/A", None]:
        score += 0.1
    elif item.get("category") == "Bug":
        issues.append("Bug ticket is missing technical details")

    if ticket.get("category") == item.get("category"):
        score += 0.05
    else:
        issues.append("Ticket category does not match source classification")

    score = min(score, 0.98)
    needs_review = score < 0.7

    return {
        "quality_score": round(score, 2),
        "issues": issues,
        "revised_title": ticket.get("title") or build_ticket_title(item),
        "revised_description": ticket.get("description") or build_ticket_description(item),
        "needs_review": needs_review,
    }
