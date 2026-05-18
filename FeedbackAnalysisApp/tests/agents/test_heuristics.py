from agents.heuristics import classify_feedback_item, analyze_bug_item, extract_feature_request


def test_classifier_labels_core_examples():
    bug = classify_feedback_item({"text": "App crashes on startup after the latest update and I lost all my tasks."})
    feature = classify_feedback_item({"text": "Please add dark mode support for night use."})
    praise = classify_feedback_item({"text": "Amazing app, works perfectly for my daily workflow!", "rating": 5})
    spam = classify_feedback_item({"text": "Buy now http://spam.example promo code free followers"})

    assert bug["category"] == "Bug"
    assert feature["category"] == "Feature Request"
    assert praise["category"] == "Praise"
    assert spam["category"] == "Spam"


def test_bug_and_feature_extractors_return_required_fields():
    bug_details = analyze_bug_item({
        "subject": "Login Issue",
        "text": "Cannot login after update on Pixel 7 Android 14 app 3.2.1.",
        "app_version": "3.2.1",
    })
    feature_details = extract_feature_request({
        "subject": "Feature Request: Dark Mode",
        "text": "Would love dark mode support for late-night work.",
    }, "Roadmap includes dark mode planned for version 8.0")

    assert bug_details["component"] == "Authentication"
    assert bug_details["severity"] in {"Critical", "High", "Medium", "Low"}
    assert feature_details["feature_summary"] == "Add dark mode support"
    assert feature_details["planned_version"] == "8.0"
