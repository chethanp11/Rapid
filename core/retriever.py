# ✅ retriever.py — RFI Category Matcher
# --------------------------------------
# Loads known RFI signal patterns and matches input text to the most likely category.

import csv
import os
from typing import List, Dict
from config.pyenv import get_path

# 📍 Path to RFI pattern file
PATTERN_FILE = os.path.join(get_path("RAPID_KNOWLEDGE_BASE_PATH"), "rfi_patterns.csv")

def load_rfi_patterns() -> List[Dict[str, any]]:
    """
    Load RFI patterns from the CSV file into a list of dictionaries.

    Returns:
        List[Dict[str, Any]]: Parsed pattern rules.
    """
    patterns = []
    with open(PATTERN_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            patterns.append({
                "rfi_id": row.get("rfi_id", "").strip(),
                "category": row.get("category", "").strip().lower(),
                "question": row.get("question", "").strip(),
                "trigger_signal": row.get("trigger_signal", "").lower(),
                "tags": row.get("tags", "").strip(),
                "confidence_weight": float(row.get("confidence_weight", 0.0) or 0.0)
            })
    return patterns

def match_rfi_to_category(rfi_text: str) -> str:
    """
    Match an incoming RFI to the best-fitting category using weighted keyword scoring.

    Args:
        rfi_text (str): RFI title or description.

    Returns:
        str: Best-matched category name (default: "evidence_gap").
    """
    rfi_text = rfi_text.lower()
    patterns = load_rfi_patterns()

    best_score = 0
    best_category = "evidence_gap"

    for pattern in patterns:
        signals = [token.strip() for token in pattern["trigger_signal"].split(",") if token.strip()]
        score = sum(signal in rfi_text for signal in signals)
        weighted_score = score * pattern["confidence_weight"]

        if weighted_score > best_score:
            best_score = weighted_score
            best_category = pattern["category"]

    return best_category